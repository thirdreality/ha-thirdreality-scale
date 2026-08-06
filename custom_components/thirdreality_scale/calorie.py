"""Calorie Tracker business logic for ThirdReality Smart Scale.

Handles:
- add_food: calculate calories, update meal log, tare scale, TTS announce
- finish_meal: add meal total to today's total, TTS summary, clear meal
- reset_today: clear all calorie data
"""
from __future__ import annotations

import logging
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
        """Finish the current meal: add to today's total, clear meal."""
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

        # Update today total
        await _set_number(hass, today_cal_eid, new_today_total)

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
        await _set_text(hass, status_eid, "🗑️ Reset! Today's calories cleared. Ready to start fresh.")

        await self._tts_speak("Calories reset. Today's count is back to zero. Ready to start fresh!")

    def _get_daily_target(self) -> float:
        """Get daily calorie target from entity."""
        eid = self._entity_id("daily_calorie_target")
        return _get_float(self._hass, eid) or 2000

    def _get_meal_warning(self) -> float:
        """Get meal calorie warning threshold from entity."""
        eid = self._entity_id("meal_calorie_warning")
        return _get_float(self._hass, eid) or 800

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
