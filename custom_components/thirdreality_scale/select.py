"""Select platform for ThirdReality Smart Scale."""
from __future__ import annotations

import json
import logging
from pathlib import Path

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN,
    CONF_FEATURES,
    FEATURE_CALORIE,
    FEATURE_COCKTAIL,
    DEFAULT_FOOD_DATABASE,
    DEFAULT_COCKTAIL_RECIPES,
)

_LOGGER = logging.getLogger(__name__)

# Storage keys
STORAGE_KEY_FOOD = f"{DOMAIN}_food_data"
STORAGE_KEY_COCKTAIL = f"{DOMAIN}_cocktail_data"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities for ThirdReality Scale."""
    features = entry.data.get(CONF_FEATURES, [])
    entities: list[SelectEntity] = []

    # Initialize data stores in hass.data
    hass.data.setdefault(DOMAIN, {})

    if FEATURE_CALORIE in features:
        # Load food database (name -> calories per 100g)
        food_data = await hass.async_add_executor_job(
            _load_data, hass, STORAGE_KEY_FOOD, DEFAULT_FOOD_DATABASE
        )
        hass.data[DOMAIN]["food_database"] = food_data
        food_options = list(food_data.keys())

        entities.append(
            ScaleSelect(
                hass,
                entry,
                key="food_preset",
                name="Food Preset",
                icon="mdi:food-apple",
                options=food_options,
                initial_option=food_options[0] if food_options else None,
                storage_key=STORAGE_KEY_FOOD,
            )
        )

    if FEATURE_COCKTAIL in features:
        # Load cocktail database (name -> ingredients string)
        cocktail_data = await hass.async_add_executor_job(
            _load_data, hass, STORAGE_KEY_COCKTAIL, DEFAULT_COCKTAIL_RECIPES
        )
        hass.data[DOMAIN]["cocktail_database"] = cocktail_data
        cocktail_options = list(cocktail_data.keys()) + ["custom"]

        entities.extend([
            ScaleSelect(
                hass,
                entry,
                key="select_cocktail",
                name="Select Cocktail",
                icon="mdi:glass-cocktail",
                options=cocktail_options,
                initial_option=cocktail_options[0] if cocktail_options else None,
                storage_key=STORAGE_KEY_COCKTAIL,
            ),
            ScaleSelect(
                hass,
                entry,
                key="cocktail_step",
                name="Cocktail Step",
                icon="mdi:progress-check",
                options=["idle", "mixing", "complete"],
                initial_option="idle",
                storage_key=None,
                entity_category=EntityCategory.DIAGNOSTIC,
            ),
        ])

    if entities:
        async_add_entities(entities)

    # ================================================================
    # Register services for managing food and cocktail data
    # ================================================================

    if FEATURE_CALORIE in features:

        async def handle_add_food(call: ServiceCall) -> None:
            """Add a food item with calories to the database and dropdown."""
            food_name = call.data.get("name", "").strip()
            calories = call.data.get("calories_per_100g", 0)
            if not food_name or calories <= 0:
                _LOGGER.warning("add_food requires 'name' and 'calories_per_100g' > 0")
                return

            # Update database
            food_data = hass.data[DOMAIN].get("food_database", {})
            food_data[food_name] = int(calories)
            hass.data[DOMAIN]["food_database"] = food_data

            # Save to storage
            await hass.async_add_executor_job(
                _save_data, hass, STORAGE_KEY_FOOD, food_data
            )

            # Update select entity options
            for entity in entities:
                if entity._key == "food_preset":
                    await entity.async_add_option(food_name)
                    break

            # Update the food_database text entity for blueprint compatibility
            await _update_food_database_text(hass, food_data)

            _LOGGER.info("Added food: %s (%d cal/100g)", food_name, calories)

        async def handle_remove_food(call: ServiceCall) -> None:
            """Remove a food item from the database and dropdown."""
            food_name = call.data.get("name", "").strip()
            if not food_name:
                return

            # Update database
            food_data = hass.data[DOMAIN].get("food_database", {})
            food_data.pop(food_name, None)
            hass.data[DOMAIN]["food_database"] = food_data

            # Save to storage
            await hass.async_add_executor_job(
                _save_data, hass, STORAGE_KEY_FOOD, food_data
            )

            # Update select entity options
            for entity in entities:
                if entity._key == "food_preset":
                    await entity.async_remove_option(food_name)
                    break

            # Update the food_database text entity
            await _update_food_database_text(hass, food_data)

            _LOGGER.info("Removed food: %s", food_name)

        hass.services.async_register(DOMAIN, "add_food", handle_add_food)
        hass.services.async_register(DOMAIN, "remove_food", handle_remove_food)

    if FEATURE_COCKTAIL in features:

        async def handle_add_cocktail(call: ServiceCall) -> None:
            """Add a cocktail with ingredients to the database and dropdown."""
            cocktail_name = call.data.get("name", "").strip()
            ingredients = call.data.get("ingredients", "").strip()
            if not cocktail_name or not ingredients:
                _LOGGER.warning(
                    "add_cocktail requires 'name' and 'ingredients' "
                    "(format: ingredient1:weight1,ingredient2:weight2)"
                )
                return

            # Update database
            cocktail_data = hass.data[DOMAIN].get("cocktail_database", {})
            cocktail_data[cocktail_name] = ingredients
            hass.data[DOMAIN]["cocktail_database"] = cocktail_data

            # Save to storage
            await hass.async_add_executor_job(
                _save_data, hass, STORAGE_KEY_COCKTAIL, cocktail_data
            )

            # Update select entity options
            for entity in entities:
                if entity._key == "select_cocktail":
                    await entity.async_add_option(cocktail_name)
                    break

            # Update the cocktail_recipes_db text entity
            await _update_cocktail_recipes_text(hass, cocktail_data)

            _LOGGER.info("Added cocktail: %s (%s)", cocktail_name, ingredients)

        async def handle_remove_cocktail(call: ServiceCall) -> None:
            """Remove a cocktail from the database and dropdown."""
            cocktail_name = call.data.get("name", "").strip()
            if not cocktail_name:
                return

            # Update database
            cocktail_data = hass.data[DOMAIN].get("cocktail_database", {})
            cocktail_data.pop(cocktail_name, None)
            hass.data[DOMAIN]["cocktail_database"] = cocktail_data

            # Save to storage
            await hass.async_add_executor_job(
                _save_data, hass, STORAGE_KEY_COCKTAIL, cocktail_data
            )

            # Update select entity options
            for entity in entities:
                if entity._key == "select_cocktail":
                    await entity.async_remove_option(cocktail_name)
                    break

            # Update the cocktail_recipes_db text entity
            await _update_cocktail_recipes_text(hass, cocktail_data)

            _LOGGER.info("Removed cocktail: %s", cocktail_name)

        hass.services.async_register(DOMAIN, "add_cocktail", handle_add_cocktail)
        hass.services.async_register(DOMAIN, "remove_cocktail", handle_remove_cocktail)




def _load_data(hass: HomeAssistant, storage_key: str, defaults: dict) -> dict:
    """Load user data from storage, or return defaults."""
    storage_path = Path(hass.config.path(".storage", storage_key))
    if storage_path.exists():
        try:
            with open(storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "data" in data:
                    return data["data"]
        except (json.JSONDecodeError, KeyError):
            pass
    return dict(defaults)


def _save_data(hass: HomeAssistant, storage_key: str, data: dict) -> None:
    """Save user data to storage."""
    storage_path = Path(hass.config.path(".storage", storage_key))
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    with open(storage_path, "w", encoding="utf-8") as f:
        json.dump({"data": data}, f, ensure_ascii=False, indent=2)


async def _update_food_database_text(hass: HomeAssistant, food_data: dict) -> None:
    """Update the food_database text entity with current data.

    Converts food_data dict to blueprint-compatible format: 'Apple:52,Banana:89,...'
    and writes it to the text.thirdreality_smart_scale_food_database entity.
    """
    db_string = ",".join(f"{name}:{cal}" for name, cal in food_data.items())
    # Find and update the food_database text entity
    entity_id = None
    for state in hass.states.async_all("text"):
        if "food_database" in state.entity_id and DOMAIN in state.entity_id:
            entity_id = state.entity_id
            break
    if entity_id:
        await hass.services.async_call(
            "text", "set_value",
            {"entity_id": entity_id, "value": db_string},
            blocking=True,
        )


async def _update_cocktail_recipes_text(hass: HomeAssistant, cocktail_data: dict) -> None:
    """Update the cocktail_recipes_db text entity with current data.

    Converts cocktail_data dict to format: 'name1=ing1:w1,ing2:w2|name2=...'
    and writes it to the text.thirdreality_smart_scale_cocktail_recipes_db entity.
    """
    db_string = "|".join(f"{name}={ingredients}" for name, ingredients in cocktail_data.items())
    # Find and update the cocktail_recipes_db text entity
    entity_id = None
    for state in hass.states.async_all("text"):
        if "cocktail_recipes_db" in state.entity_id and DOMAIN in state.entity_id:
            entity_id = state.entity_id
            break
    if entity_id:
        await hass.services.async_call(
            "text", "set_value",
            {"entity_id": entity_id, "value": db_string},
            blocking=True,
        )


class ScaleSelect(SelectEntity, RestoreEntity):
    """A select entity for ThirdReality Scale."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        key: str,
        name: str,
        icon: str,
        options: list[str],
        initial_option: str | None = None,
        storage_key: str | None = None,
        entity_category: EntityCategory | None = None,
    ) -> None:
        """Initialize the select entity."""
        self._hass_ref = hass
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_options = options
        self._attr_current_option = initial_option
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._initial_option = initial_option
        self._storage_key = storage_key
        if entity_category is not None:
            self._attr_entity_category = entity_category

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "ThirdReality Smart Scale",
            "manufacturer": "ThirdReality",
            "model": "Smart Scale",
        }

    async def async_added_to_hass(self) -> None:
        """Restore last state on startup."""
        await super().async_added_to_hass()
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.state in self._attr_options:
                self._attr_current_option = last_state.state
                return
        self._attr_current_option = self._initial_option

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self.async_write_ha_state()

    async def async_add_option(self, option: str) -> None:
        """Add a new option to the list."""
        if option not in self._attr_options:
            # Insert before "custom" if it exists, otherwise append
            if "custom" in self._attr_options:
                idx = self._attr_options.index("custom")
                self._attr_options = self._attr_options[:idx] + [option] + self._attr_options[idx:]
            else:
                self._attr_options = self._attr_options + [option]
            self.async_write_ha_state()
            _LOGGER.info("Added option '%s' to %s", option, self._key)

    async def async_remove_option(self, option: str) -> None:
        """Remove an option from the list."""
        if option in self._attr_options and option != "custom":
            self._attr_options = [o for o in self._attr_options if o != option]
            if self._attr_current_option == option:
                self._attr_current_option = self._attr_options[0] if self._attr_options else None
            self.async_write_ha_state()
            _LOGGER.info("Removed option '%s' from %s", option, self._key)
