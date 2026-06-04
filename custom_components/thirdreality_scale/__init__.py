"""ThirdReality Smart Scale integration for Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr

from .const import (
    DOMAIN,
    CONF_PLATFORM,
    CONF_Z2M_TOPIC,
    CONF_ZHA_IEEE,
    CONF_FEATURES,
    FEATURE_COCKTAIL,
    FEATURE_CALORIE,
)

_LOGGER = logging.getLogger(__name__)

# Platforms registered by this integration
PLATFORMS = ["number", "text", "select", "button"]

BLUEPRINT_DIR = "thirdreality_scale"
BLUEPRINTS = {
    FEATURE_COCKTAIL: "cocktail_blueprint.yaml",
    FEATURE_CALORIE: "calorie_blueprint.yaml",
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ThirdReality Scale from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Step 1: Register device in device registry
    device_registry = dr.async_get(hass)
    device_name = _get_device_name(entry)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name=device_name,
        manufacturer="ThirdReality",
        model="Smart Scale",
    )

    # Step 2: Install blueprint files
    features = entry.data.get(CONF_FEATURES, [])
    await hass.async_add_executor_job(_install_blueprints, hass, features)

    # Step 3: Set up all platforms (number, text, select, button)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("ThirdReality Scale setup complete. Features: %s", features)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


def _get_device_name(entry: ConfigEntry) -> str:
    """Generate a friendly device name from config entry data."""
    data = entry.data
    topic = data.get(CONF_Z2M_TOPIC, "")
    ieee = data.get(CONF_ZHA_IEEE, "")
    identifier = topic or ieee or "Unknown"
    return f"ThirdReality Scale ({identifier})"


def _install_blueprints(hass: HomeAssistant, features: list[str]) -> None:
    """Copy blueprint YAML files to HA's blueprints directory."""
    source_dir = Path(__file__).parent / "blueprints"
    target_dir = Path(hass.config.path("blueprints", "automation", BLUEPRINT_DIR))
    target_dir.mkdir(parents=True, exist_ok=True)

    for feature, filename in BLUEPRINTS.items():
        if feature in features:
            source_file = source_dir / filename
            target_file = target_dir / filename
            if source_file.exists():
                shutil.copy2(source_file, target_file)
                _LOGGER.info("Installed blueprint: %s", filename)
