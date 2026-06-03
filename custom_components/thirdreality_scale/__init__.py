"""ThirdReality Smart Scale integration for Home Assistant."""
from __future__ import annotations

import logging
import shutil
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_FEATURES,
    CONF_PLATFORM,
    CONF_Z2M_TOPIC,
    CONF_ZHA_IEEE,
    CONF_TTS_SPEAKER,
    CONF_TTS_ENGINE,
    FEATURE_COCKTAIL,
    FEATURE_CALORIE,
    DEFAULT_TTS_ENGINE,
)
from .helpers import setup_calorie_helpers, setup_cocktail_helpers

_LOGGER = logging.getLogger(__name__)

BLUEPRINT_DIR = "thirdreality_scale"
BLUEPRINTS = {
    FEATURE_COCKTAIL: "cocktail_blueprint.yaml",
    FEATURE_CALORIE: "calorie_blueprint.yaml",
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ThirdReality Scale from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    features = entry.data.get(CONF_FEATURES, [])

    # Step 1: 自动导入 Blueprint 文件到 HA blueprints 目录
    await hass.async_add_executor_job(_install_blueprints, hass, features)

    # Step 2: 自动创建所有需要的 helper 实体
    if FEATURE_CALORIE in features:
        await setup_calorie_helpers(hass, entry)

    if FEATURE_COCKTAIL in features:
        await setup_cocktail_helpers(hass, entry)

    _LOGGER.info(
        "ThirdReality Scale integration setup complete. Features: %s", features
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True


def _install_blueprints(hass: HomeAssistant, features: list[str]) -> None:
    """Copy blueprint YAML files to HA's blueprints directory."""
    # 源文件目录（集成自带的 blueprints）
    source_dir = Path(__file__).parent / "blueprints"

    # HA blueprints 目标目录
    target_dir = Path(hass.config.path("blueprints", "automation", BLUEPRINT_DIR))
    target_dir.mkdir(parents=True, exist_ok=True)

    for feature, filename in BLUEPRINTS.items():
        if feature in features:
            source_file = source_dir / filename
            target_file = target_dir / filename

            if source_file.exists():
                # 始终覆盖（确保用户获取最新版本）
                shutil.copy2(source_file, target_file)
                _LOGGER.info("Installed blueprint: %s → %s", filename, target_file)
            else:
                _LOGGER.warning("Blueprint source not found: %s", source_file)
