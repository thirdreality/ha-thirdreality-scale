"""Number platform for ThirdReality Smart Scale."""
from __future__ import annotations

import logging

from homeassistant.components.number import (
    NumberEntity,
    NumberMode,
    RestoreNumber,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_FEATURES,
    FEATURE_CALORIE,
    DEFAULT_DAILY_TARGET,
    DEFAULT_MEAL_WARNING,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities for ThirdReality Scale."""
    features = entry.data.get(CONF_FEATURES, [])
    entities: list[NumberEntity] = []

    if FEATURE_CALORIE in features:
        entities.extend([
            ScaleNumber(
                entry,
                key="custom_cal_per_100g",
                name="Custom Cal per 100g",
                icon="mdi:fire",
                native_min_value=0,
                native_max_value=2000,
                native_step=1,
                initial_value=0,
                mode=NumberMode.BOX,
                unit=None,
                entity_category=EntityCategory.DIAGNOSTIC,
            ),
            ScaleNumber(
                entry,
                key="meal_calories",
                name="Meal Calories",
                icon="mdi:food",
                native_min_value=0,
                native_max_value=10000,
                native_step=1,
                initial_value=0,
                mode=NumberMode.BOX,
                unit="kcal",
                entity_category=EntityCategory.DIAGNOSTIC,
            ),
            ScaleNumber(
                entry,
                key="today_calories",
                name="Today Calories",
                icon="mdi:counter",
                native_min_value=0,
                native_max_value=20000,
                native_step=1,
                initial_value=0,
                mode=NumberMode.BOX,
                unit="kcal",
                entity_category=None,
            ),
            ScaleNumber(
                entry,
                key="daily_calorie_target",
                name="Daily Calorie Target",
                icon="mdi:target",
                native_min_value=500,
                native_max_value=5000,
                native_step=1,
                initial_value=DEFAULT_DAILY_TARGET,
                mode=NumberMode.BOX,
                unit="kcal",
                entity_category=EntityCategory.CONFIG,
            ),
            ScaleNumber(
                entry,
                key="meal_calorie_warning",
                name="Meal Calorie Warning",
                icon="mdi:alert",
                native_min_value=200,
                native_max_value=3000,
                native_step=1,
                initial_value=DEFAULT_MEAL_WARNING,
                mode=NumberMode.BOX,
                unit="kcal",
                entity_category=EntityCategory.CONFIG,
            ),
        ])

    if entities:
        async_add_entities(entities)


class ScaleNumber(RestoreNumber):
    """A number entity for ThirdReality Scale."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entry: ConfigEntry,
        key: str,
        name: str,
        icon: str,
        native_min_value: float,
        native_max_value: float,
        native_step: float,
        initial_value: float,
        mode: NumberMode,
        unit: str | None,
        entity_category: EntityCategory | None = None,
    ) -> None:
        """Initialize the number entity."""
        self._entry = entry
        self._key = key
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_min_value = native_min_value
        self._attr_native_max_value = native_max_value
        self._attr_native_step = native_step
        self._attr_native_value = initial_value
        self._attr_mode = mode
        self._attr_native_unit_of_measurement = unit
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_{key}"
        self._initial_value = initial_value
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
        if (last_number_data := await self.async_get_last_number_data()) is not None:
            if last_number_data.native_value is not None:
                self._attr_native_value = last_number_data.native_value
                return
        # If no restored state, use initial value
        self._attr_native_value = self._initial_value

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self._attr_native_value = value
        self.async_write_ha_state()
