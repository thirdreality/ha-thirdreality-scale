"""Cocktail Mixing Assistant business logic for ThirdReality Smart Scale.

State machine:
  idle → (Start pressed) → waiting_for_glass → (Done pressed) → mixing_step_N → ... → complete → idle

Each mixing step:
  1. Tare the scale
  2. Set target weight
  3. Update status display
  4. TTS announce current ingredient
  5. Wait for Done press OR weight reaches target
  6. Move to next step
"""
from __future__ import annotations

import asyncio
import logging
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN, DEFAULT_COCKTAIL_RECIPES

_LOGGER = logging.getLogger(__name__)

# Timeout for each step (seconds)
STEP_TIMEOUT = 600  # 10 minutes


class CocktailMixer:
    """Manages cocktail mixing state machine."""

    def __init__(self, hass: HomeAssistant, entry_id: str) -> None:
        """Initialize."""
        self._hass = hass
        self._entry_id = entry_id
        self._task: asyncio.Task | None = None
        self._done_event = asyncio.Event()
        self._unsub_done: callback | None = None
        self._unsub_weight: callback | None = None

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

    async def start(self) -> None:
        """Start the cocktail mixing process."""
        # Cancel any existing run
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except (asyncio.CancelledError, Exception):
                pass

        self._task = self._hass.async_create_task(self._run())

    def signal_done(self) -> None:
        """Signal that the Done button was pressed."""
        self._done_event.set()

    async def _run(self) -> None:
        """Main cocktail mixing coroutine."""
        hass = self._hass
        status_eid = self._entity_id("cocktail_status")
        recipe_list_eid = self._entity_id("cocktail_recipe_list")
        step_eid = self._entity_id("cocktail_step")
        recipe_select_eid = self._entity_id("select_cocktail")

        try:
            # Get selected recipe
            selected = _get_state(hass, recipe_select_eid)
            ingredients = self._get_recipe_ingredients(selected)

            if not ingredients:
                await _set_text(hass, status_eid, f"❌ Recipe '{selected}' not found.")
                return

            total_steps = len(ingredients)

            # Switch to mixing page
            await _select_option(hass, step_eid, "idle")
            await asyncio.sleep(0.2)
            await _select_option(hass, step_eid, "mixing")

            # Write full ingredient list
            recipe_display = " | ".join(
                f"{i+1}. {ing['name']} {ing['weight']}g"
                for i, ing in enumerate(ingredients)
            )
            await _set_text(hass, recipe_list_eid, recipe_display[:255])

            # Status: place glass
            await _set_text(
                hass, status_eid,
                f"🍸 {selected} | 📋 {total_steps} ingredients | 🥃 Place glass on scale | Press Done ✅ to start!"
            )

            # TTS: starting
            await self._tts_speak(
                f"Let's make a {selected}! There are {total_steps} steps. "
                "Please place your glass on the scale, then press the Done button to begin."
            )

            # Wait for Done (glass placed)
            if not await self._wait_for_done(timeout=STEP_TIMEOUT):
                await _set_text(hass, status_eid, "⏰ Timeout. Cancelled.")
                await _select_option(hass, step_eid, "idle")
                return

            # Start scale reporting
            await self._commands.start_report()
            await asyncio.sleep(1)

            # ============ INGREDIENT LOOP ============
            for step_idx, ing in enumerate(ingredients):
                step_num = step_idx + 1
                ing_name = ing["name"]
                ing_weight = ing["weight"]
                target_weight = ing_weight - 1  # slightly under for tolerance

                # Tare and wait for sensor to update
                await self._commands.tare()
                await asyncio.sleep(2)

                # Set target weight (scale beeps when target is reached)
                await self._commands.set_weight(ing_weight)

                # Update status
                await _set_text(
                    hass, status_eid,
                    f"🍸 {selected} | Step {step_num}/{total_steps} | 👉 Add: {ing_name} | 🎯 Target: {ing_weight}g"
                )

                # TTS: current step
                await self._tts_speak(
                    f"Step {step_num} of {total_steps}. Please add {ing_weight} grams of {ing_name}."
                )

                # Wait for Done OR weight reached
                reached = await self._wait_for_done_or_weight(
                    target_weight=target_weight, timeout=STEP_TIMEOUT
                )

                if not reached:
                    # Timeout
                    await self._commands.stop_report()
                    await _set_text(hass, status_eid, f"⏰ Timeout at step {step_num}.")
                    await _select_option(hass, step_eid, "idle")
                    return

                # Brief pause between steps
                await asyncio.sleep(2)

            # ============ DONE ============
            await self._commands.set_weight(0)  # Clear target weight — DO NOT stop_report, keep scale reporting for calorie mode

            # Switch to complete page
            await _select_option(hass, step_eid, "complete")
            await _set_text(
                hass, status_eid,
                f"🎉 {selected} — All {total_steps} ingredients done! Enjoy your cocktail! 🥂"
            )

            # TTS: complete
            await self._tts_speak(
                f"Congratulations! Your {selected} is ready. "
                f"All {total_steps} ingredients have been added. Enjoy your cocktail! Cheers!"
            )

            # Auto-return to idle
            await asyncio.sleep(5)
            await _select_option(hass, step_eid, "idle")
            await _set_text(hass, recipe_list_eid, "")

        except asyncio.CancelledError:
            _LOGGER.debug("Cocktail mixing cancelled")
            try:
                await self._commands.stop_report()
            except Exception:
                pass
        except Exception as err:
            _LOGGER.error("Cocktail mixing error: %s", err)
        finally:
            self._cleanup_listeners()

    def _get_recipe_ingredients(self, recipe_name: str) -> list[dict]:
        """Get ingredients for a recipe. Returns list of {name, weight}."""
        # Try custom recipe
        if recipe_name == "custom":
            custom_eid = self._entity_id("custom_recipe")
            raw = _get_state(self._hass, custom_eid)
            return _parse_ingredients(raw)

        # Try from cocktail_recipes_db text entity
        db_eid = self._entity_id("cocktail_recipes_db")
        db_raw = _get_state(self._hass, db_eid)
        if db_raw:
            for entry in db_raw.split("|"):
                parts = entry.split("=", 1)
                if len(parts) == 2 and parts[0].strip() == recipe_name:
                    return _parse_ingredients(parts[1].strip())

        # Try from in-memory database (stored at domain level by select.py)
        cocktail_db = self._hass.data[DOMAIN].get("cocktail_database", DEFAULT_COCKTAIL_RECIPES)
        if recipe_name in cocktail_db:
            return _parse_ingredients(cocktail_db[recipe_name])

        return []

    async def _wait_for_done(self, timeout: int) -> bool:
        """Wait for Done button press. Returns True if pressed, False on timeout."""
        self._done_event.clear()
        try:
            await asyncio.wait_for(self._done_event.wait(), timeout=timeout)
            return True
        except asyncio.TimeoutError:
            return False

    async def _wait_for_done_or_weight(self, target_weight: float, timeout: int) -> bool:
        """Wait for Done press OR weight reaching target. Returns True if either, False on timeout."""
        self._done_event.clear()
        weight_reached = asyncio.Event()

        weight_eid = self._entity_id("weight")

        @callback
        def _check_weight(event):
            new_state = event.data.get("new_state")
            if new_state is None or new_state.state in ("unknown", "unavailable"):
                return
            try:
                if float(new_state.state) >= target_weight:
                    weight_reached.set()
            except (ValueError, TypeError):
                pass

        # Subscribe to weight changes
        unsub = async_track_state_change_event(
            self._hass, [weight_eid], _check_weight
        )

        try:
            # Wait for either event (don't check current value to avoid stale readings after tare)
            done_task = self._hass.async_create_task(self._done_event.wait())
            weight_task = self._hass.async_create_task(weight_reached.wait())

            done_futures = {done_task, weight_task}
            try:
                finished, pending = await asyncio.wait(
                    done_futures, timeout=timeout, return_when=asyncio.FIRST_COMPLETED
                )
                for task in pending:
                    task.cancel()
                return len(finished) > 0
            except asyncio.CancelledError:
                for task in done_futures:
                    task.cancel()
                raise
        finally:
            unsub()

    def _cleanup_listeners(self) -> None:
        """Remove any active listeners."""
        if self._unsub_done:
            self._unsub_done()
            self._unsub_done = None
        if self._unsub_weight:
            self._unsub_weight()
            self._unsub_weight = None

    async def _tts_speak(self, message: str) -> None:
        """Speak a TTS message if configured."""
        data = self._data
        tts_speaker = data.get("tts_speaker", "")
        tts_engine = data.get("tts_engine", "")

        if not tts_speaker or not tts_engine:
            return

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

def _parse_ingredients(raw: str) -> list[dict]:
    """Parse 'name1:weight1,name2:weight2' into list of {name, weight}."""
    items = []
    if not raw or not raw.strip():
        return items
    for item in raw.split(","):
        parts = item.split(":")
        if len(parts) == 2:
            try:
                weight = int(parts[1].strip())
                if weight > 0:
                    items.append({"name": parts[0].strip(), "weight": weight})
            except ValueError:
                pass
    return items


def _get_state(hass: HomeAssistant, entity_id: str) -> str:
    """Get entity state as string."""
    if not entity_id:
        return ""
    state = hass.states.get(entity_id)
    if state is None or state.state in ("unknown", "unavailable"):
        return ""
    return state.state


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


async def _select_option(hass: HomeAssistant, entity_id: str, option: str) -> None:
    """Set a select entity option."""
    if not entity_id:
        return
    try:
        await hass.services.async_call(
            "select", "select_option",
            {"entity_id": entity_id, "option": option},
            blocking=True,
        )
    except Exception:
        pass
