"""ThirdReality Smart Scale integration for Home Assistant."""
from __future__ import annotations

import logging
import json
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import async_track_time_change

from .const import (
    DOMAIN,
    CONF_PLATFORM,
    CONF_Z2M_TOPIC,
    CONF_ZHA_IEEE,
    CONF_FEATURES,
    CONF_TTS_SPEAKER,
    CONF_TTS_ENGINE,
    DEFAULT_TTS_ENGINE,
    FEATURE_COCKTAIL,
    FEATURE_CALORIE,
    PLATFORM_Z2M,
)
from .scale_commands import ScaleCommands
from .calorie import CalorieTracker
from .cocktail import CocktailMixer

from homeassistant.components import websocket_api
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

# Platforms registered by this integration
PLATFORMS = ["sensor", "number", "text", "select", "button"]

# Frontend panel
PANEL_TITLE = "Smart Scale"
PANEL_ICON = "mdi:scale"
PANEL_FRONTEND_PATH = "thirdreality-scale"

_MANIFEST = json.loads((Path(__file__).parent / "manifest.json").read_text(encoding="utf-8"))
INTEGRATION_VERSION = _MANIFEST["version"]
PANEL_URL = f"/thirdreality_scale_panel_{INTEGRATION_VERSION}"


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the ThirdReality Scale component."""
    hass.data.setdefault(DOMAIN, {})

    # Register WebSocket API for frontend to fetch calorie history
    websocket_api.async_register_command(hass, ws_get_calorie_history)

    return True


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/get_calorie_history",
    }
)
@websocket_api.async_response
async def ws_get_calorie_history(hass, connection, msg):
    """Handle get calorie history WebSocket command."""
    # Find the first calorie tracker instance
    for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
        tracker = entry_data.get("calorie_tracker") if isinstance(entry_data, dict) else None
        if tracker:
            history_json = await tracker.get_history_json()
            connection.send_result(msg["id"], {"history": json.loads(history_json)})
            return

    connection.send_result(msg["id"], {"history": []})


async def _async_register_panel(hass: HomeAssistant) -> None:
    """Register the frontend panel in the sidebar (same approach as Alarmo)."""
    # Skip if already registered
    if hass.data.get("frontend_panels", {}).get(PANEL_FRONTEND_PATH):
        return

    from homeassistant.components.http import StaticPathConfig
    from homeassistant.components import panel_custom

    # Path to the actual JS file (not directory!)
    panel_file = str(Path(__file__).parent / "frontend" / "dist" / "thirdreality-scale-panel.js")

    panel_url = PANEL_URL

    try:
        # Register static path for the JS file
        await hass.http.async_register_static_paths(
            [StaticPathConfig(panel_url, panel_file, cache_headers=False)]
        )
    except Exception:
        # Already registered
        pass

    try:
        # Register the custom panel in the sidebar
        await panel_custom.async_register_panel(
            hass,
            webcomponent_name="thirdreality-scale-panel",
            frontend_url_path=PANEL_FRONTEND_PATH,
            module_url=panel_url,
            sidebar_title=PANEL_TITLE,
            sidebar_icon=PANEL_ICON,
            require_admin=False,
            config={},
        )
    except Exception:
        # Panel already registered
        pass


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ThirdReality Scale from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Register the frontend panel (only once)
    await _async_register_panel(hass)

    data = entry.data
    platform = data.get(CONF_PLATFORM, PLATFORM_Z2M)
    z2m_topic = data.get(CONF_Z2M_TOPIC, "")
    zha_ieee = data.get(CONF_ZHA_IEEE, "")
    features = data.get(CONF_FEATURES, [])
    tts_speaker = data.get(CONF_TTS_SPEAKER, "")
    tts_engine = data.get(CONF_TTS_ENGINE, DEFAULT_TTS_ENGINE)

    # Determine weight sensor entity_id
    weight_sensor = _get_weight_sensor_entity(hass, platform, z2m_topic, zha_ieee)

    # Entity ID prefix (how HA names entities from this integration)
    prefix = "thirdreality_smart_scale"

    # Build entity lookup map for business logic modules
    entities = {
        "weight": weight_sensor,
        # Calorie entities
        "food_preset": f"select.{prefix}_food_preset",
        "custom_food_name": f"text.{prefix}_custom_food_name",
        "custom_cal_per_100g": f"number.{prefix}_custom_cal_per_100g",
        "meal_calories": f"number.{prefix}_meal_calories",
        "today_calories": f"number.{prefix}_today_calories",
        "daily_calorie_target": f"number.{prefix}_daily_calorie_target",
        "meal_calorie_warning": f"number.{prefix}_meal_calorie_warning",
        "calorie_status": f"text.{prefix}_calorie_status",
        "meal_log": f"text.{prefix}_meal_log",
        "calorie_history": f"text.{prefix}_calorie_history",
        # Cocktail entities
        "select_cocktail": f"select.{prefix}_select_cocktail",
        "cocktail_step": f"select.{prefix}_cocktail_step",
        "cocktail_status": f"text.{prefix}_cocktail_status",
        "cocktail_recipe_list": f"text.{prefix}_cocktail_recipe_list",
        "cocktail_recipes_db": f"text.{prefix}_cocktail_recipes_db",
        "custom_recipe": f"text.{prefix}_custom_recipe",
    }

    # Store entry data for other modules to access
    entry_data = {
        "config": data,
        "platform": platform,
        "z2m_topic": z2m_topic,
        "zha_ieee": zha_ieee,
        "tts_speaker": tts_speaker,
        "tts_engine": tts_engine,
        "weight_sensor_entity": weight_sensor,
        "entities": entities,
    }

    # Create scale commands instance
    commands = ScaleCommands(hass, platform, z2m_topic, zha_ieee)
    entry_data["commands"] = commands

    # Create business logic instances
    if FEATURE_CALORIE in features:
        calorie_tracker = CalorieTracker(hass, entry.entry_id)
        entry_data["calorie_tracker"] = calorie_tracker

    if FEATURE_COCKTAIL in features:
        cocktail_mixer = CocktailMixer(hass, entry.entry_id)
        entry_data["cocktail_mixer"] = cocktail_mixer

    hass.data[DOMAIN][entry.entry_id] = entry_data

    # Register device
    device_registry = dr.async_get(hass)
    device_name = _get_device_name(platform, z2m_topic, zha_ieee)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name=device_name,
        manufacturer="ThirdReality",
        model="Smart Scale",
    )

    # Set up all platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Auto start weight reporting after HA is fully started
    async def _start_reporting(event=None):
        """Start scale weight reporting so dashboard shows real-time weight."""
        try:
            await commands.start_report()
            _LOGGER.debug("Scale weight reporting started")
        except Exception as err:
            _LOGGER.debug("Failed to start reporting: %s", err)

    if hass.is_running:
        hass.async_create_task(_start_reporting())
    else:
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, _start_reporting)

    # Daily auto-reset at midnight (clear today's calories for a fresh start)
    if FEATURE_CALORIE in features:
        async def _daily_reset(now):
            """Reset today's calories at midnight."""
            _LOGGER.debug("Midnight auto-reset: clearing today's calories")
            tracker = entry_data.get("calorie_tracker")
            if tracker:
                await tracker.reset_today()

        unsub_midnight = async_track_time_change(hass, _daily_reset, hour=0, minute=0, second=0)
        entry_data["unsub_midnight"] = unsub_midnight

    _LOGGER.info("ThirdReality Scale setup complete. Features: %s", features)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Cancel midnight reset timer
    entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
    unsub_midnight = entry_data.get("unsub_midnight")
    if unsub_midnight:
        unsub_midnight()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

        # Remove panel if no more entries
        remaining = [
            eid for eid in hass.data[DOMAIN]
            if eid != "food_database" and eid != "cocktail_database"
        ]
        if not remaining:
            try:
                from homeassistant.components.frontend import async_remove_panel
                async_remove_panel(hass, PANEL_FRONTEND_PATH)
            except Exception:
                pass

    return unload_ok


def _get_device_name(platform: str, z2m_topic: str, zha_ieee: str) -> str:
    """Generate a friendly device name."""
    identifier = z2m_topic or zha_ieee or "Unknown"
    return f"ThirdReality Scale ({identifier})"


def _get_weight_sensor_entity(
    hass: HomeAssistant, platform: str, z2m_topic: str, zha_ieee: str
) -> str:
    """Determine the weight sensor entity_id.

    For Z2M: entity ID is sensor.{topic}_weight
    For ZHA: search entity registry for the weight sensor on the device.
    """
    if platform == PLATFORM_Z2M and z2m_topic:
        return f"sensor.{z2m_topic}_weight"

    if zha_ieee:
        found = _find_zha_weight_sensor(hass, zha_ieee)
        if found:
            return found
        # Fallback: guess
        clean_ieee = zha_ieee.replace(":", "").replace("-", "").lower()
        if not clean_ieee.startswith("0x"):
            clean_ieee = f"0x{clean_ieee}"
        return f"sensor.{clean_ieee}_weight"

    return ""


def _find_zha_weight_sensor(hass: HomeAssistant, ieee: str) -> str | None:
    """Find the weight sensor entity for a ZHA device by IEEE address."""
    try:
        dev_reg = dr.async_get(hass)
        ent_reg = er.async_get(hass)

        # Normalize IEEE
        normalized = ieee.replace(":", "").replace("-", "").lower()
        if normalized.startswith("0x"):
            normalized = normalized[2:]

        # Find ZHA device
        target_device_id = None
        for device in dev_reg.devices.values():
            for domain, ident in device.identifiers:
                if domain != "zha":
                    continue
                norm_ident = ident.replace(":", "").replace("-", "").lower()
                if norm_ident.startswith("0x"):
                    norm_ident = norm_ident[2:]
                if norm_ident == normalized:
                    target_device_id = device.id
                    break
            if target_device_id:
                break

        if not target_device_id:
            return None

        # Find sensor with unit 'g' on this device
        for entity in ent_reg.entities.values():
            if entity.device_id != target_device_id:
                continue
            if entity.domain != "sensor":
                continue
            if (entity.unit_of_measurement or "").lower() == "g":
                return entity.entity_id

        return None
    except Exception:
        return None
