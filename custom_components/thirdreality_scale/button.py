"""Button platform for ThirdReality Smart Scale."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
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
                entity_category=EntityCategory.CONFIG,
            ),
            ScaleButton(
                entry,
                key="undo_add",
                name="Undo Add",
                icon="mdi:undo",
                entity_category=EntityCategory.CONFIG,
            ),
            ScaleButton(
                entry,
                key="finish_meal",
                name="Finish Meal",
                icon="mdi:check-circle",
                entity_category=EntityCategory.CONFIG,
            ),
            ScaleButton(
                entry,
                key="reset_today",
                name="Reset Today",
                icon="mdi:delete-outline",
                entity_category=EntityCategory.CONFIG,
            ),
        ])

    if FEATURE_COCKTAIL in features:
        entities.extend([
            ScaleButton(
                entry,
                key="start_cocktail",
                name="Start Cocktail",
                icon="mdi:play-circle",
                entity_category=EntityCategory.CONFIG,
            ),
            ScaleButton(
                entry,
                key="done",
                name="Done",
                icon="mdi:check-bold",
                entity_category=EntityCategory.CONFIG,
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
        entity_category: EntityCategory | None = None,
    ) -> None:
        """Initialize the button entity."""
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
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

    async def async_press(self) -> None:
        """Handle the button press — dispatch to business logic."""
        entry_data = self.hass.data[DOMAIN].get(self._entry.entry_id, {})
        calorie_tracker = entry_data.get("calorie_tracker")
        cocktail_mixer = entry_data.get("cocktail_mixer")

        if self._key == "add_food" and calorie_tracker:
            await calorie_tracker.add_food()
        elif self._key == "undo_add" and calorie_tracker:
            await calorie_tracker.undo_add()
        elif self._key == "finish_meal" and calorie_tracker:
            await calorie_tracker.finish_meal()
        elif self._key == "reset_today" and calorie_tracker:
            await calorie_tracker.reset_today()
        elif self._key == "start_cocktail" and cocktail_mixer:
            await cocktail_mixer.start()
        elif self._key == "done" and cocktail_mixer:
            cocktail_mixer.signal_done()
        else:
            _LOGGER.debug("Button pressed but no handler: %s", self._key)
