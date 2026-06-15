"""Text platform for ThirdReality Smart Scale."""
from __future__ import annotations

import logging

from homeassistant.components.text import TextEntity, RestoreText
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_FEATURES,
    FEATURE_CALORIE,
    FEATURE_COCKTAIL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up text entities for ThirdReality Scale."""
    features = entry.data.get(CONF_FEATURES, [])
    entities: list[TextEntity] = []

    if FEATURE_CALORIE in features:
        entities.extend([
            ScaleText(
                entry,
                key="custom_food_name",
                name="Custom Food Name",
                icon="mdi:food-apple-outline",
                initial_value="",
                max_length=100,
            ),
            ScaleText(
                entry,
                key="calorie_status",
                name="Calorie Status",
                icon="mdi:information-outline",
                initial_value="",
                max_length=255,
            ),
            ScaleText(
                entry,
                key="meal_log",
                name="Meal Log",
                icon="mdi:notebook-outline",
                initial_value="Empty",
                max_length=255,
            ),
        ])

    if FEATURE_COCKTAIL in features:
        # Build default cocktail recipes database string
        # Format: name1=ing1:w1,ing2:w2|name2=ing1:w1,ing2:w2
        from .const import DEFAULT_COCKTAIL_RECIPES
        default_cocktail_db_str = "|".join(
            f"{name}={ingredients}" for name, ingredients in DEFAULT_COCKTAIL_RECIPES.items()
        )
        entities.extend([
            ScaleText(
                entry,
                key="cocktail_status",
                name="Cocktail Status",
                icon="mdi:glass-cocktail",
                initial_value="",
                max_length=255,
            ),
            ScaleText(
                entry,
                key="cocktail_recipe_list",
                name="Cocktail Recipe List",
                icon="mdi:format-list-bulleted",
                initial_value="",
                max_length=255,
            ),
            ScaleText(
                entry,
                key="custom_recipe",
                name="Custom Recipe",
                icon="mdi:pencil-outline",
                initial_value="",
                max_length=255,
            ),
            ScaleText(
                entry,
                key="cocktail_recipes_db",
                name="Cocktail Recipes Database",
                icon="mdi:database-outline",
                initial_value=default_cocktail_db_str,
                max_length=255,
            ),
        ])

    if entities:
        async_add_entities(entities)


class ScaleText(RestoreText):
    """A text entity for ThirdReality Scale."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        key: str,
        name: str,
        icon: str,
        initial_value: str,
        max_length: int = 255,
    ) -> None:
        """Initialize the text entity."""
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_value = initial_value
        self._attr_native_max = max_length
        self._attr_native_min = 0
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._initial_value = initial_value

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
        if (last_text_data := await self.async_get_last_text_data()) is not None:
            if last_text_data.native_value is not None:
                self._attr_native_value = last_text_data.native_value
                return
        self._attr_native_value = self._initial_value

    async def async_set_value(self, value: str) -> None:
        """Set the text value."""
        self._attr_native_value = value
        self.async_write_ha_state()
