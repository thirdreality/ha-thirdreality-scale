"""ThirdReality Smart Scale integration for Home Assistant."""
from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path

import yaml

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
    PLATFORM_Z2M,
)

_LOGGER = logging.getLogger(__name__)

# Platforms registered by this integration
PLATFORMS = ["number", "text", "select", "button"]

BLUEPRINT_DIR = "thirdreality_scale"
BLUEPRINTS = {
    FEATURE_COCKTAIL: "cocktail_blueprint.yaml",
    FEATURE_CALORIE: "calorie_blueprint.yaml",
}

DASHBOARDS = {
    FEATURE_CALORIE: {
        "url_path": "thirdreality-calories",
        "title": "Calories",
        "icon": "mdi:fire",
        "filename": "calorie_dashboard.yaml",
    },
    FEATURE_COCKTAIL: {
        "url_path": "thirdreality-cocktail",
        "title": "Cocktail",
        "icon": "mdi:glass-cocktail",
        "filename": "cocktail_dashboard.yaml",
    },
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

    # Step 4: Auto-install dashboards (delayed)
    hass.async_create_task(_install_dashboards(hass, entry, features))

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


def _get_weight_sensor_entity(entry: ConfigEntry) -> str:
    """Get the weight sensor entity ID based on platform config."""
    data = entry.data
    platform = data.get(CONF_PLATFORM, PLATFORM_Z2M)
    topic = data.get(CONF_Z2M_TOPIC, "")
    ieee = data.get(CONF_ZHA_IEEE, "")

    if platform == PLATFORM_Z2M and topic:
        return f"sensor.{topic}_weight"
    elif ieee:
        clean_ieee = ieee.replace(":", "_").replace("-", "_")
        return f"sensor.{clean_ieee}_weight"
    return "sensor.REPLACE_WITH_YOUR_SCALE_WEIGHT_SENSOR"


async def _install_dashboards(
    hass: HomeAssistant, entry: ConfigEntry, features: list[str]
) -> None:
    """Auto-install Lovelace dashboards using WebSocket API."""
    import asyncio
    # Wait for HA to fully start and lovelace to be ready
    await asyncio.sleep(10)

    try:
        weight_sensor = _get_weight_sensor_entity(entry)
        source_dir = Path(__file__).parent / "dashboards"

        for feature, dash_config in DASHBOARDS.items():
            if feature not in features:
                continue

            url_path = dash_config["url_path"]

            # Read and process dashboard YAML template
            source_file = source_dir / dash_config["filename"]
            if not source_file.exists():
                _LOGGER.warning("Dashboard file not found: %s", source_file)
                continue

            dashboard_config = await hass.async_add_executor_job(
                _read_and_process_dashboard, source_file, weight_sensor
            )

            if dashboard_config is None:
                continue

            # Check if dashboard already exists in lovelace
            lovelace_data = hass.data.get("lovelace")
            if lovelace_data is not None:
                dashboards = getattr(lovelace_data, "dashboards", {})
                if url_path in dashboards:
                    # Dashboard exists - save config to it
                    dashboard = dashboards[url_path]
                    if hasattr(dashboard, "async_save"):
                        await dashboard.async_save(dashboard_config)
                        _LOGGER.info("Updated existing dashboard: %s", url_path)
                        continue
                    else:
                        _LOGGER.debug("Dashboard %s exists but no async_save", url_path)
                        continue

            # Dashboard doesn't exist - create it via WebSocket API
            await _create_dashboard_via_ws(hass, url_path, dash_config, dashboard_config)

    except Exception as err:
        _LOGGER.warning("Dashboard auto-install failed (non-critical): %s", err)


async def _create_dashboard_via_ws(
    hass: HomeAssistant, url_path: str, dash_config: dict, dashboard_config: dict
) -> None:
    """Create a new dashboard using the lovelace WebSocket collection."""
    try:
        from homeassistant.components.lovelace import dashboard as lv_dashboard

        lovelace_data = hass.data.get("lovelace")
        if lovelace_data is None:
            _LOGGER.warning("Lovelace not loaded, cannot create dashboard")
            return

        # Use the dashboards collection to create a new dashboard
        dashboards_collection = getattr(lovelace_data, "dashboards_collection", None)
        if dashboards_collection is None:
            _LOGGER.warning("No dashboards_collection found in lovelace data")
            # Fallback: try to access via different attribute names
            for attr_name in dir(lovelace_data):
                obj = getattr(lovelace_data, attr_name, None)
                if obj and hasattr(obj, "async_create_item"):
                    dashboards_collection = obj
                    _LOGGER.debug("Found collection via attr: %s", attr_name)
                    break

        if dashboards_collection and hasattr(dashboards_collection, "async_create_item"):
            # Create the dashboard entry
            await dashboards_collection.async_create_item({
                "url_path": url_path,
                "title": dash_config["title"],
                "icon": dash_config["icon"],
                "show_in_sidebar": True,
                "require_admin": False,
                "mode": "storage",
            })
            _LOGGER.info("Created dashboard via collection: %s", url_path)

            # Wait for HA to register the new dashboard
            import asyncio
            await asyncio.sleep(2)

            # Now save the config to the newly created dashboard
            lovelace_data = hass.data.get("lovelace")
            dashboards = getattr(lovelace_data, "dashboards", {})
            if url_path in dashboards:
                dashboard = dashboards[url_path]
                if hasattr(dashboard, "async_save"):
                    await dashboard.async_save(dashboard_config)
                    _LOGGER.info("Saved config to new dashboard: %s", url_path)
            else:
                # Write config file directly as fallback
                storage_key = f"lovelace.{url_path}"
                storage_path = Path(hass.config.path(".storage", storage_key))
                storage_data = {
                    "version": 1,
                    "minor_version": 1,
                    "key": storage_key,
                    "data": {"config": dashboard_config},
                }
                await hass.async_add_executor_job(_write_json, storage_path, storage_data)
                _LOGGER.info("Wrote config file for dashboard: %s", url_path)
        else:
            _LOGGER.warning(
                "Cannot create dashboard %s: no suitable API found. "
                "Available lovelace attrs: %s",
                url_path,
                [a for a in dir(lovelace_data) if not a.startswith("_")],
            )

    except Exception as err:
        _LOGGER.warning("Failed to create dashboard %s: %s", url_path, err)


def _read_and_process_dashboard(source_file: Path, weight_sensor: str) -> dict | None:
    """Read dashboard YAML and replace placeholders."""
    try:
        content = source_file.read_text(encoding="utf-8")
        content = content.replace("WEIGHT_SENSOR_ENTITY", weight_sensor)
        return yaml.safe_load(content)
    except Exception as err:
        _LOGGER.warning("Failed to read dashboard %s: %s", source_file, err)
        return None


def _write_json(path: Path, data: dict) -> None:
    """Write JSON data to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
