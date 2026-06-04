"""Button platform for ThirdReality Smart Scale."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
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
    """Set up button entities for ThirdReality Scale."""
    features = entry.data.get(CONF_FEATURES, [])
    entities: list[ButtonEntity] = []

    if FEATURE_CALORIE in features:
        entities.extend([
            ScaleButton(
                entry,
                key="add_food",
                name="Add Food",
                icon="mdi:plus-circle",
            ),
            ScaleButton(
                entry,
                key="finish_meal",
                name="Finish Meal",
                icon="mdi:check-circle",
            ),
            ScaleButton(
                entry,
                key="reset_today",
                name="Reset Today",
                icon="mdi:delete-outline",
            ),
        ])

    if FEATURE_COCKTAIL in features:
        entities.extend([
            ScaleButton(
                entry,
                key="start_cocktail",
                name="Start Cocktail",
                icon="mdi:play-circle",
            ),
            ScaleButton(
                entry,
                key="done",
                name="Done",
                icon="mdi:check-bold",
            ),
        ])

    if entities:
        async_add_entities(entities)


class ScaleButton(ButtonEntity):
    """A button entity for ThirdReality Scale."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        key: str,
        name: str,
        icon: str,
    ) -> None:
        """Initialize the button entity."""
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "ThirdReality Smart Scale",
            "manufacturer": "ThirdReality",
            "model": "Smart Scale",
        }

    async def async_press(self) -> None:
        """Handle the button press.

        The actual logic is handled by blueprint automations that
        listen for state changes on these button entities.
        """
        _LOGGER.debug("Button pressed: %s", self._key)
