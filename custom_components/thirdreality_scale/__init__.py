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

    # Step 4: Auto-install dashboards (delayed to ensure lovelace is ready)
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
    """Auto-install Lovelace dashboards using HA internal API."""
    import asyncio
    # Wait a bit for lovelace to fully initialize
    await asyncio.sleep(5)

    try:
        weight_sensor = _get_weight_sensor_entity(entry)
        source_dir = Path(__file__).parent / "dashboards"

        # Access lovelace data
        lovelace_data = hass.data.get("lovelace")
        if lovelace_data is None:
            _LOGGER.warning("Lovelace not available for dashboard install")
            return

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

            # Try to find existing dashboard and save config to it
            dashboards = getattr(lovelace_data, "dashboards", None)
            if dashboards and url_path in dashboards:
                dashboard = dashboards[url_path]
                # Use the dashboard's async_save method
                if hasattr(dashboard, "async_save"):
                    await dashboard.async_save(dashboard_config)
                    _LOGGER.info("Saved config to existing dashboard: %s", url_path)
                    continue

            # Dashboard doesn't exist yet - register it
            # First register in lovelace_dashboards storage
            await _register_dashboard_storage(hass, url_path, dash_config)

            # Write the dashboard config storage file
            storage_key = f"lovelace.{url_path}"
            storage_path = Path(hass.config.path(".storage", storage_key))
            storage_data = {
                "version": 1,
                "minor_version": 1,
                "key": storage_key,
                "data": {"config": dashboard_config},
            }
            await hass.async_add_executor_job(
                _write_json, storage_path, storage_data
            )

            _LOGGER.info(
                "Installed dashboard: %s (restart HA to see it)",
                dash_config["title"],
            )

    except Exception as err:
        _LOGGER.warning("Dashboard auto-install failed (non-critical): %s", err)


async def _register_dashboard_storage(
    hass: HomeAssistant, url_path: str, dash_config: dict
) -> None:
    """Register dashboard in the lovelace_dashboards storage file."""
    dashboards_storage_path = Path(hass.config.path(".storage", "lovelace_dashboards"))

    dashboards_data = await hass.async_add_executor_job(
        _read_json, dashboards_storage_path
    )

    if dashboards_data is None:
        dashboards_data = {
            "version": 1,
            "minor_version": 1,
            "key": "lovelace_dashboards",
            "data": {"items": []},
        }

    items = dashboards_data.get("data", {}).get("items", [])

    for item in items:
        if item.get("url_path") == url_path:
            return

    import uuid
    new_item = {
        "id": uuid.uuid4().hex[:12],
        "url_path": url_path,
        "title": dash_config["title"],
        "icon": dash_config["icon"],
        "show_in_sidebar": True,
        "require_admin": False,
        "mode": "storage",
    }
    items.append(new_item)
    dashboards_data["data"]["items"] = items

    await hass.async_add_executor_job(
        _write_json, dashboards_storage_path, dashboards_data
    )


def _read_and_process_dashboard(source_file: Path, weight_sensor: str) -> dict | None:
    """Read dashboard YAML and replace placeholders."""
    try:
        content = source_file.read_text(encoding="utf-8")
        content = content.replace("WEIGHT_SENSOR_ENTITY", weight_sensor)
        return yaml.safe_load(content)
    except Exception as err:
        _LOGGER.warning("Failed to read dashboard %s: %s", source_file, err)
        return None


def _read_json(path: Path) -> dict | None:
    """Read JSON file."""
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _write_json(path: Path, data: dict) -> None:
    """Write JSON data to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
