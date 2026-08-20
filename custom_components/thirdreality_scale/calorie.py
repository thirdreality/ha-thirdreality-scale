"""Calorie Tracker business logic for ThirdReality Smart Scale.

Handles:
- add_food: calculate calories, update meal log, tare scale, TTS announce
- finish_meal: add meal total to today's total, TTS summary, clear meal, save history
- reset_today: clear all calorie data
- get_history: retrieve calorie history
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

from homeassistant.core import HomeAssistant

from .const import DOMAIN, DEFAULT_FOOD_DATABASE

_LOGGER = logging.getLogger(__name__)


class CalorieTracker:
    """Manages calorie tracking logic."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        """Initialize."""
        self._hass = hass
        self._entry_id = entry_id

    @property
    def _data(self) -> dict:
        """Get entry data from hass.data."""
        return self._hass.data[DOMAIN][self._entry_id]

    @property
    def _commands(self):
        """Get scale commands instance."""
        return self._data["commands"]

    def _entity_id(self, key: str) -> str:
        """Get entity_id for a given key."""
        return self._data["entities"].get(key, "")

    async def add_food(self) -> None:
        """Add current food on scale to the meal log."""
        hass = self._hass

        # Ensure scale is reporting and clear any leftover target weight from cocktail mode
        await self._commands.start_report()
        await self._commands.set_weight(0)

        # Read current state
        weight_sensor = self._entity_id("weight")
        food_select = self._entity_id("food_preset")
        custom_name_eid = self._entity_id("custom_food_name")
        custom_cal_eid = self._entity_id("custom_cal_per_100g")
        meal_cal_eid = self._entity_id("meal_calories")
        meal_log_eid = self._entity_id("meal_log")
        status_eid = self._entity_id("calorie_status")

        current_weight = _get_float(hass, weight_sensor)
        selected_food = _get_state(hass, food_select)
        custom_name = _get_state(hass, custom_name_eid).strip()
        custom_cal = _get_float(hass, custom_cal_eid)

        # Determine food name and cal/100g
        use_custom = len(custom_name) > 0 and custom_cal > 0
        if use_custom:
            food_name = custom_name
            cal_per_100g = custom_cal
        else:
            food_name = selected_food
            food_db = self._hass.data[DOMAIN].get("food_database", DEFAULT_FOOD_DATABASE)
            cal_per_100g = food_db.get(selected_food, 0)

        # Validate
        if cal_per_100g <= 0:
            await _set_text(hass, status_eid, "❌ Unknown food or no cal data. Select a preset or enter custom values.")
            return

        if current_weight <= 0:
            await _set_text(hass, status_eid, "❌ No weight. Place food on the scale first.")
            return

        # Calculate
        current_cal = round(current_weight * cal_per_100g / 100)
        current_meal_cal = _get_float(hass, meal_cal_eid)
        new_meal_total = round(current_meal_cal + current_cal)

        # Update meal calories
        await _set_number(hass, meal_cal_eid, new_meal_total)

        # Update meal log
        current_log = _get_state(hass, meal_log_eid)
        new_entry = f"{food_name} {round(current_weight)}g={current_cal}cal"
        if current_log and current_log not in ("Empty", "unknown", "unavailable", ""):
            new_log = f"{current_log} | {new_entry}"
        else:
            new_log = new_entry
        await _set_text(hass, meal_log_eid, new_log[:255])

        # Update status
        await _set_text(
            hass, status_eid,
            f"➕ Added: {food_name} {round(current_weight)}g = {current_cal} kcal | Meal: {new_meal_total} kcal"
        )

        # TTS announce
        await self._tts_speak(
            f"Added {food_name}, {round(current_weight)} grams, {current_cal} calories. "
            f"Meal total so far: {new_meal_total} calories."
            + (f" Heads up, {food_name} is {round(cal_per_100g)} calories per 100 grams. That's a high calorie food." if cal_per_100g >= 400 else "")
            + (f" Warning: This meal is already {new_meal_total} calories, exceeding your meal target." if new_meal_total > self._get_meal_warning() else "")
        )

        # Tare scale
        await self._commands.tare()

        # Clear custom inputs
        await _set_text(hass, custom_name_eid, "")
        await _set_number(hass, custom_cal_eid, 0)

    async def finish_meal(self) -> None:
        """Finish the current meal: add to today's total, clear meal, save history."""
        hass = self._hass
        meal_cal_eid = self._entity_id("meal_calories")
        today_cal_eid = self._entity_id("today_calories")
        meal_log_eid = self._entity_id("meal_log")
        status_eid = self._entity_id("calorie_status")

        current_meal_cal = _get_float(hass, meal_cal_eid)
        current_today_cal = _get_float(hass, today_cal_eid)
        new_today_total = round(current_today_cal + current_meal_cal)
        daily_target = self._get_daily_target()
        remaining = round(daily_target - new_today_total)

        # Get meal log before clearing
        meal_log_str = _get_state(hass, meal_log_eid)

        # Update today total
        await _set_number(hass, today_cal_eid, new_today_total)

        # Save to history
        if current_meal_cal > 0:
            await self._save_meal_history(current_meal_cal, meal_log_str)

        # Update status
        await _set_text(
            hass, status_eid,
            f"✅ Meal done! {round(current_meal_cal)} kcal added. Today's total: {new_today_total} kcal"
        )

        # TTS summary
        msg = f"Meal complete! This meal was {round(current_meal_cal)} calories. Today's total is now {new_today_total} calories. "
        if remaining > 0:
            msg += f"You have {remaining} calories remaining for today."
        else:
            msg += f"You have exceeded your daily target by {abs(remaining)} calories."
        await self._tts_speak(msg)

        # Clear meal
        await _set_number(hass, meal_cal_eid, 0)
        await _set_text(hass, meal_log_eid, "Empty")

        # Update history display entity
        await self._update_history_entity()

    async def reset_today(self) -> None:
        """Reset all calorie data for today."""
        hass = self._hass
        today_cal_eid = self._entity_id("today_calories")
        meal_cal_eid = self._entity_id("meal_calories")
        meal_log_eid = self._entity_id("meal_log")
        status_eid = self._entity_id("calorie_status")

        await _set_number(hass, today_cal_eid, 0)
        await _set_number(hass, meal_cal_eid, 0)
        await _set_text(hass, meal_log_eid, "Empty")
        await _set_text(hass, status_eid, "🔄 Counter cleared — past meals still saved in history.")

        await self._tts_speak("Calories reset. Today's count is back to zero. Ready to start fresh!")

    def _get_daily_target(self) -> float:
        """Get daily calorie target from entity."""
        eid = self._entity_id("daily_calorie_target")
        return _get_float(self._hass, eid) or 2000

    def _get_meal_warning(self) -> float:
        """Get meal calorie warning threshold from entity."""
        eid = self._entity_id("meal_calorie_warning")
        return _get_float(self._hass, eid) or 800

    # ============================================================
    # History
    # ============================================================

    def _history_file(self) -> Path:
        """Get the path to the history JSON file."""
        return Path(self._hass.config.config_dir) / ".storage" / "thirdreality_scale_calorie_history.json"

    def _load_history(self) -> list[dict]:
        """Load history from JSON file."""
        path = self._history_file()
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _save_history(self, history: list[dict]) -> None:
        """Save history to JSON file."""
        path = self._history_file()
        path.parent.mkdir(parents=True, exist_ok=True)
        # Keep only last 90 days of data (max ~500 entries)
        history = history[-500:]
        try:
            path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as err:
            _LOGGER.warning("Failed to save calorie history: %s", err)

    async def _save_meal_history(self, meal_calories: float, meal_log: str) -> None:
        """Save a finished meal to the history file."""
        now = datetime.now()
        entry = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "calories": round(meal_calories),
            "items": meal_log if meal_log and meal_log not in ("Empty", "") else "",
        }

        history = await self._hass.async_add_executor_job(self._load_history)
        history.append(entry)
        await self._hass.async_add_executor_job(self._save_history, history)

    async def _update_history_entity(self) -> None:
        """Update the history text entity with recent data for frontend display.

        Format: JSON string with last 7 days summary + today's meals.
        """
        hass = self._hass
        history_eid = self._entity_id("calorie_history")
        if not history_eid:
            return

        history = await hass.async_add_executor_job(self._load_history)
        if not history:
            await _set_text(hass, history_eid, "[]")
            return

        # Build daily summary for last 7 days
        today = datetime.now().strftime("%Y-%m-%d")
        daily_data: dict[str, dict] = {}
        for entry in history:
            date = entry.get("date", "")
            if not date:
                continue
            if date not in daily_data:
                daily_data[date] = {"date": date, "total": 0, "meals": []}
            daily_data[date]["total"] += entry.get("calories", 0)
            daily_data[date]["meals"].append({
                "time": entry.get("time", ""),
                "cal": entry.get("calories", 0),
                "items": entry.get("items", ""),
            })

        # Get last 7 days sorted
        sorted_days = sorted(daily_data.keys(), reverse=True)[:7]
        result = [daily_data[d] for d in sorted_days]

        # Truncate to fit in 255 chars — use compact format
        # Format: date:total:meal1_time=cal,meal2_time=cal|date:total:...
        compact_lines = []
        for day in result:
            meals_str = ",".join(
                f"{m['time']}={m['cal']}" for m in day["meals"]
            )
            compact_lines.append(f"{day['date']}:{day['total']}:{meals_str}")

        history_str = "|".join(compact_lines)
        # If too long, trim older days
        while len(history_str) > 255 and len(compact_lines) > 1:
            compact_lines.pop()
            history_str = "|".join(compact_lines)

        await _set_text(hass, history_eid, history_str[:255])

    async def get_history_json(self) -> str:
        """Get full history as JSON string (for API/frontend use)."""
        history = await self._hass.async_add_executor_job(self._load_history)
        # Build daily summary
        daily_data: dict[str, dict] = {}
        for entry in history:
            date = entry.get("date", "")
            if not date:
                continue
            if date not in daily_data:
                daily_data[date] = {"date": date, "total": 0, "meals": []}
            daily_data[date]["total"] += entry.get("calories", 0)
            daily_data[date]["meals"].append({
                "time": entry.get("time", ""),
                "cal": entry.get("calories", 0),
                "items": entry.get("items", ""),
            })
        sorted_days = sorted(daily_data.keys(), reverse=True)[:30]
        return json.dumps([daily_data[d] for d in sorted_days], ensure_ascii=False)

    async def _tts_speak(self, message: str) -> None:
        """Speak a TTS message if configured."""
        data = self._data
        tts_speaker = data.get("tts_speaker", "")
        tts_engine = data.get("tts_engine", "")

        if not tts_speaker or not tts_engine:
            return

        # Check speaker is available
        state = self._hass.states.get(tts_speaker)
        if state is None or state.state in ("unknown", "unavailable"):
            return

        try:
            await self._hass.services.async_call(
                "tts",
                "speak",
                {
                    "entity_id": tts_engine,
                    "media_player_entity_id": tts_speaker,
                    "message": message,
                },
                blocking=False,
            )
        except Exception as err:
            _LOGGER.debug("TTS failed: %s", err)


# ============================================================
# Utility functions
# ============================================================

def _get_state(hass: HomeAssistant, entity_id: str) -> str:
    """Get entity state as string."""
    if not entity_id:
        return ""
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        return ""
    return state.state


def _get_float(hass: HomeAssistant, entity_id: str) -> float:
    """Get entity state as float."""
    val = _get_state(hass, entity_id)
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


async def _set_text(hass: HomeAssistant, entity_id: str, value: str) -> None:
    """Set a text entity value."""
    if not entity_id:
        return
    try:
        await hass.services.async_call(
            "text", "set_value",
            {"entity_id": entity_id, "value": value},
            blocking=True,
        )
    except Exception:
        pass


async def _set_number(hass: HomeAssistant, entity_id: str, value: float) -> None:
    """Set a number entity value."""
    if not entity_id:
        return
    try:
        await hass.services.async_call(
            "number", "set_value",
            {"entity_id": entity_id, "value": value},
            blocking=True,
        )
    except Exception:
        pass
