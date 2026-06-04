"""Select platform for ThirdReality Smart Scale."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select entities for ThirdReality Scale."""
    features = entry.data.get(CONF_FEATURES, [])
    entities: list[SelectEntity] = []

    if FEATURE_CALORIE in features:
        food_options = list(DEFAULT_FOOD_DATABASE.keys())
        entities.append(
            ScaleSelect(
                entry,
                key="food_preset",
                name="Food Preset",
                icon="mdi:food-apple",
                options=food_options,
                initial_option=food_options[0] if food_options else None,
            )
        )

    if FEATURE_COCKTAIL in features:
        cocktail_options = list(DEFAULT_COCKTAIL_RECIPES.keys()) + ["custom"]
        entities.extend([
            ScaleSelect(
                entry,
                key="select_cocktail",
                name="Select Cocktail",
                icon="mdi:glass-cocktail",
                options=cocktail_options,
                initial_option=cocktail_options[0] if cocktail_options else None,
            ),
            ScaleSelect(
                entry,
                key="cocktail_step",
                name="Cocktail Step",
                icon="mdi:progress-check",
                options=["idle", "mixing", "complete"],
                initial_option="idle",
            ),
        ])

    if entities:
        async_add_entities(entities)


class ScaleSelect(SelectEntity, RestoreEntity):
    """A select entity for ThirdReality Scale."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        key: str,
        name: str,
        icon: str,
        options: list[str],
        initial_option: str | None = None,
    ) -> None:
        """Initialize the select entity."""
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_options = options
        self._attr_current_option = initial_option
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._initial_option = initial_option

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
