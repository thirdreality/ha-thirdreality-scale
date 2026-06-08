"""ThirdReality Smart Scale integration for Home Assistant."""
from __future__ import annotations

import json
import logging
import shutil
from pathlib import Path

import yaml

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
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

    # Step 4: Auto-create automations based on blueprints
    await hass.async_add_executor_job(
        _install_automations, hass, entry, features
    )

    # Step 5: Auto-install dashboards
    # Write storage files immediately, then register after HA is fully started
    await hass.async_add_executor_job(
        _install_dashboards_storage, hass, entry, features
    )

    # Register dashboards in lovelace after HA is fully started
    async def _register_dashboards_when_ready(event=None):
        """Register dashboards after HA has fully started."""
        await _register_dashboards_in_lovelace(hass, entry, features)

    if hass.is_running:
        # HA already running (e.g., config entry added via UI after boot)
        hass.async_create_task(_register_dashboards_when_ready())
    else:
        # HA still starting up - wait for full start
        hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_STARTED, _register_dashboards_when_ready
        )

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


def _install_automations(
    hass: HomeAssistant, entry: ConfigEntry, features: list[str]
) -> None:
    """Auto-create automations based on installed blueprints.

    Appends blueprint-based automations to automations.yaml file,
    which is the standard HA automation configuration file.
    """
    from .const import CONF_TTS_SPEAKER, CONF_TTS_ENGINE, DEFAULT_TTS_ENGINE

    try:
        data = entry.data
        platform = data.get(CONF_PLATFORM, PLATFORM_Z2M)
        z2m_topic = data.get(CONF_Z2M_TOPIC, "")
        zha_ieee = data.get(CONF_ZHA_IEEE, "")
        tts_speaker = data.get(CONF_TTS_SPEAKER, "")
        tts_engine = data.get(CONF_TTS_ENGINE, DEFAULT_TTS_ENGINE)
        weight_sensor = _get_weight_sensor_entity(entry)

        # Entity ID prefix: based on how HA names entities from this integration
        prefix = "thirdreality_smart_scale"

        # Read existing automations.yaml
        automations_yaml_path = Path(hass.config.path("automations.yaml"))
        existing_automations = []

        if automations_yaml_path.exists():
            try:
                content = automations_yaml_path.read_text(encoding="utf-8")
                if content.strip():
                    loaded = yaml.safe_load(content)
                    if isinstance(loaded, list):
                        existing_automations = loaded
            except Exception as err:
                _LOGGER.warning("Failed to read automations.yaml: %s", err)

        # Check which automations already exist (by id or alias)
        existing_ids = {a.get("id") for a in existing_automations if isinstance(a, dict)}
        existing_aliases = {a.get("alias") for a in existing_automations if isinstance(a, dict)}
        new_automations = []

        # Calorie automation
        if FEATURE_CALORIE in features:
            auto_id = f"{DOMAIN}_calorie"
            calorie_alias = "🔥 Calorie Tracker (ThirdReality Scale)"
            if auto_id not in existing_ids and calorie_alias not in existing_aliases:
                calorie_automation = {
                    "id": auto_id,
                    "alias": "🔥 Calorie Tracker (ThirdReality Scale)",
                    "use_blueprint": {
                        "path": f"{BLUEPRINT_DIR}/calorie_blueprint.yaml",
                        "input": {
                            "platform_type": platform,
                            "z2m_device_topic": z2m_topic,
                            "zha_ieee_address": zha_ieee,
                            "tts_enable": bool(tts_speaker),
                            "tts_speaker": tts_speaker if tts_speaker else {},
                            "tts_engine": tts_engine,
                            "daily_calorie_target": 2000,
                            "meal_calorie_warning": 800,
                            "food_selector": f"select.{prefix}_food_preset",
                            "weight_sensor": weight_sensor,
                            "custom_food_name": f"text.{prefix}_custom_food_name",
                            "custom_cal_entity": f"number.{prefix}_custom_cal_per_100g",
                            "add_button": f"button.{prefix}_add_food",
                            "finish_meal_button": f"button.{prefix}_finish_meal",
                            "reset_today_button": f"button.{prefix}_reset_today",
                            "meal_cal_entity": f"number.{prefix}_meal_calories",
                            "today_cal_entity": f"number.{prefix}_today_calories",
                            "status_entity": f"text.{prefix}_calorie_status",
                            "meal_log_entity": f"text.{prefix}_meal_log",
                        },
                    },
                }
                new_automations.append(calorie_automation)
                _LOGGER.info("Adding calorie automation: %s", auto_id)

        # Cocktail automation
        if FEATURE_COCKTAIL in features:
            auto_id = f"{DOMAIN}_cocktail"
            cocktail_alias = "🍸 Cocktail Mixing Assistant (ThirdReality Scale)"
            if auto_id not in existing_ids and cocktail_alias not in existing_aliases:
                cocktail_automation = {
                    "id": auto_id,
                    "alias": "🍸 Cocktail Mixing Assistant (ThirdReality Scale)",
                    "use_blueprint": {
                        "path": f"{BLUEPRINT_DIR}/cocktail_blueprint.yaml",
                        "input": {
                            "platform_type": platform,
                            "z2m_device_topic": z2m_topic,
                            "zha_ieee_address": zha_ieee,
                            "tts_enable": bool(tts_speaker),
                            "tts_speaker": tts_speaker if tts_speaker else {},
                            "tts_engine": tts_engine,
                            "recipe_selector": f"select.{prefix}_select_cocktail",
                            "trigger_entity": f"button.{prefix}_start_cocktail",
                            "confirm_entity": f"button.{prefix}_done",
                            "scale_weight_sensor": weight_sensor,
                            "status_entity": f"text.{prefix}_cocktail_status",
                            "recipe_list_entity": f"text.{prefix}_cocktail_recipe_list",
                            "step_entity": f"select.{prefix}_cocktail_step",
                            "custom_recipe_entity": f"text.{prefix}_custom_recipe",
                        },
                    },
                }
                new_automations.append(cocktail_automation)
                _LOGGER.info("Adding cocktail automation: %s", auto_id)

        # Write updated automations.yaml if we added any
        if new_automations:
            all_automations = existing_automations + new_automations
            yaml_content = yaml.dump(
                all_automations,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )
            automations_yaml_path.write_text(yaml_content, encoding="utf-8")
            _LOGGER.info(
                "Installed %d automation(s) to automations.yaml",
                len(new_automations),
            )
        else:
            _LOGGER.debug("No new automations to install (already exist)")

    except Exception as err:
        _LOGGER.warning(
            "Automation auto-install failed (non-critical): %s", err
        )


def _install_dashboards_storage(
    hass: HomeAssistant, entry: ConfigEntry, features: list[str]
) -> None:
    """Write dashboard storage files directly to .storage directory.

    This is the most reliable method - it writes the dashboard registry
    and config files that HA reads on startup. Works across all HA versions.
    """
    try:
        weight_sensor = _get_weight_sensor_entity(entry)
        source_dir = Path(__file__).parent / "dashboards"
        storage_dir = Path(hass.config.path(".storage"))
        storage_dir.mkdir(parents=True, exist_ok=True)

        # Read existing lovelace_dashboards registry
        dashboards_registry_path = storage_dir / "lovelace_dashboards"
        existing_dashboards = {}
        if dashboards_registry_path.exists():
            try:
                with open(dashboards_registry_path, "r", encoding="utf-8") as f:
                    registry_data = json.load(f)
                    items = registry_data.get("data", {}).get("items", [])
                    for item in items:
                        existing_dashboards[item.get("url_path")] = item
            except (json.JSONDecodeError, KeyError) as err:
                _LOGGER.warning("Failed to read dashboard registry: %s", err)

        new_items_added = False

        for feature, dash_config in DASHBOARDS.items():
            if feature not in features:
                continue

            url_path = dash_config["url_path"]

            # Skip if dashboard already registered
            if url_path in existing_dashboards:
                _LOGGER.debug("Dashboard already registered: %s", url_path)
            else:
                # Add to registry
                existing_dashboards[url_path] = {
                    "icon": dash_config["icon"],
                    "id": url_path,
                    "mode": "storage",
                    "require_admin": False,
                    "show_in_sidebar": True,
                    "title": dash_config["title"],
                    "url_path": url_path,
                }
                new_items_added = True
                _LOGGER.info("Adding dashboard to registry: %s", url_path)

            # Write dashboard config storage file
            source_file = source_dir / dash_config["filename"]
            if not source_file.exists():
                _LOGGER.warning("Dashboard source file not found: %s", source_file)
                continue

            dashboard_config = _read_and_process_dashboard(source_file, weight_sensor)
            if dashboard_config is None:
                continue

            # Write the lovelace config for this dashboard
            config_storage_key = f"lovelace.{url_path}"
            config_storage_path = storage_dir / config_storage_key
            config_storage_data = {
                "version": 1,
                "minor_version": 1,
                "key": config_storage_key,
                "data": {"config": dashboard_config},
            }
            _write_json(config_storage_path, config_storage_data)
            _LOGGER.info("Wrote dashboard config: %s", config_storage_key)

        # Write updated registry if we added new items
        if new_items_added:
            registry_data = {
                "version": 1,
                "minor_version": 1,
                "key": "lovelace_dashboards",
                "data": {
                    "items": list(existing_dashboards.values())
                },
            }
            _write_json(dashboards_registry_path, registry_data)
            _LOGGER.info("Updated lovelace_dashboards registry")

    except Exception as err:
        _LOGGER.warning(
            "Dashboard storage install failed (non-critical): %s", err
        )


async def _register_dashboards_in_lovelace(
    hass: HomeAssistant, entry: ConfigEntry, features: list[str]
) -> None:
    """Register dashboards in the running lovelace system.

    This handles the case where HA is already running (e.g., integration
    added via UI). The storage files are already written, so we just need
    to notify lovelace to pick them up.
    """
    import asyncio

    try:
        # Small delay to ensure lovelace component is fully loaded
        await asyncio.sleep(3)

        lovelace_data = hass.data.get("lovelace")
        if lovelace_data is None:
            _LOGGER.debug(
                "Lovelace data not available. Dashboards will appear after restart."
            )
            return

        for feature, dash_config in DASHBOARDS.items():
            if feature not in features:
                continue

            url_path = dash_config["url_path"]

            # Check if already registered in running system
            dashboards = getattr(lovelace_data, "dashboards", {})
            if url_path in dashboards:
                _LOGGER.debug("Dashboard already active: %s", url_path)
                continue

            # Try to create via collection API (works on HA 2024.x+)
            created = False
            # Try different attribute names for the collection
            for attr_name in ("dashboards_collection", "_dashboards_collection"):
                collection = getattr(lovelace_data, attr_name, None)
                if collection and hasattr(collection, "async_create_item"):
                    try:
                        await collection.async_create_item({
                            "url_path": url_path,
                            "title": dash_config["title"],
                            "icon": dash_config["icon"],
                            "show_in_sidebar": True,
                            "require_admin": False,
                            "mode": "storage",
                        })
                        created = True
                        _LOGGER.info(
                            "Registered dashboard in lovelace: %s", url_path
                        )
                        break
                    except Exception as err:
                        _LOGGER.debug(
                            "Collection API failed for %s: %s", url_path, err
                        )

            if not created:
                _LOGGER.info(
                    "Dashboard %s written to storage. "
                    "It will appear after Home Assistant restart.",
                    url_path,
                )

    except Exception as err:
        _LOGGER.debug(
            "Live dashboard registration skipped: %s. "
            "Dashboards will appear after restart.",
            err,
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


def _write_json(path: Path, data: dict) -> None:
    """Write JSON data to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
