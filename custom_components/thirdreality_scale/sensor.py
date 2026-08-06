"""Sensor platform for ThirdReality Smart Scale.

Creates a weight sensor that mirrors the original Z2M/ZHA weight sensor,
providing a predictable entity_id for dashboards.
"""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfMass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN, CONF_FEATURES, FEATURE_COCKTAIL, FEATURE_CALORIE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities for ThirdReality Scale."""
    features = entry.data.get(CONF_FEATURES, [])

    # Only create weight sensor if any feature is enabled
    if FEATURE_CALORIE in features or FEATURE_COCKTAIL in features:
        # Get the source weight sensor entity_id from hass.data
        data = hass.data[DOMAIN][entry.entry_id]
        source_sensor = data.get("weight_sensor_entity", "")

        entity = ScaleWeightSensor(entry, source_sensor)
        async_add_entities([entity])


class ScaleWeightSensor(SensorEntity):
    """A weight sensor that mirrors the original Z2M/ZHA weight sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.WEIGHT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfMass.GRAMS

    def __init__(self, entry: ConfigEntry, source_entity_id: str) -> None:
        """Initialize the weight sensor."""
        self._entry = entry
        self._source_entity_id = source_entity_id
        self._attr_name = "Weight"
        self._attr_icon = "mdi:scale"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}_weight"
        self._attr_native_value = 0.0

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
        """Start tracking the source sensor when added to hass."""
        await super().async_added_to_hass()

        if not self._source_entity_id:
            _LOGGER.warning("No source weight sensor configured")
            return

        # Read current value
        state = self.hass.states.get(self._source_entity_id)
        if state and state.state not in ("unknown", "unavailable"):
            try:
                self._attr_native_value = float(state.state)
            except (ValueError, TypeError):
                pass

        # Track changes
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._source_entity_id],
                self._handle_source_change,
            )
        )

    @callback
    def _handle_source_change(self, event) -> None:
        """Handle state change of the source weight sensor."""
        new_state = event.data.get("new_state")
        if new_state is None or new_state.state in ("unknown", "unavailable"):
            return
        try:
            self._attr_native_value = float(new_state.state)
            self.async_write_ha_state()
        except (ValueError, TypeError):
            pass
