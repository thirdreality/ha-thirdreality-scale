"""ThirdReality Smart Scale integration for Home Assistant."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import (
    DOMAIN,
    CONF_FEATURES,
    CONF_PLATFORM,
    CONF_Z2M_TOPIC,
    CONF_TTS_SPEAKER,
    CONF_TTS_ENGINE,
    FEATURE_COCKTAIL,
    FEATURE_CALORIE,
    DEFAULT_DAILY_TARGET,
    DEFAULT_MEAL_WARNING,
    DEFAULT_FOOD_DATABASE,
    DEFAULT_COCKTAIL_RECIPES,
    DEFAULT_TTS_ENGINE,
)
from .helpers import setup_calorie_helpers, setup_cocktail_helpers

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ThirdReality Scale from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    features = entry.data.get(CONF_FEATURES, [])

    # 自动创建所有需要的 helper 实体
    if FEATURE_CALORIE in features:
        await setup_calorie_helpers(hass, entry)

    if FEATURE_COCKTAIL in features:
        await setup_cocktail_helpers(hass, entry)

    _LOGGER.info("ThirdReality Scale integration setup complete. Features: %s", features)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True
