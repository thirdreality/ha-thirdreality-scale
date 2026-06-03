"""Helper entity creation for ThirdReality Smart Scale."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_component

from .const import (
    DOMAIN,
    DEFAULT_DAILY_TARGET,
    DEFAULT_MEAL_WARNING,
    DEFAULT_FOOD_DATABASE,
    DEFAULT_COCKTAIL_RECIPES,
)

_LOGGER = logging.getLogger(__name__)


async def setup_calorie_helpers(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Create all helper entities needed for calorie tracking."""
    prefix = "thirdreality_scale"

    helpers_to_create = [
        # input_select: food preset dropdown
        {
            "platform": "input_select",
            "name": f"{prefix}_food_preset",
            "options": list(DEFAULT_FOOD_DATABASE.keys()),
        },
        # input_text: custom food name
        {
            "platform": "input_text",
            "name": f"{prefix}_custom_food_name",
            "max": 100,
            "initial": "",
        },
        # input_number: custom cal per 100g
        {
            "platform": "input_number",
            "name": f"{prefix}_custom_cal_per_100g",
            "min": 0,
            "max": 2000,
            "step": 1,
            "initial": 0,
            "mode": "box",
        },
        # input_number: meal calories
        {
            "platform": "input_number",
            "name": f"{prefix}_meal_calories",
            "min": 0,
            "max": 10000,
            "step": 1,
            "initial": 0,
            "mode": "box",
        },
        # input_number: today calories
        {
            "platform": "input_number",
            "name": f"{prefix}_today_calories",
            "min": 0,
            "max": 20000,
            "step": 1,
            "initial": 0,
            "mode": "box",
        },
        # input_number: daily calorie target
        {
            "platform": "input_number",
            "name": f"{prefix}_daily_calorie_target",
            "min": 500,
            "max": 5000,
            "step": 100,
            "initial": DEFAULT_DAILY_TARGET,
            "mode": "slider",
            "unit_of_measurement": "kcal",
        },
        # input_number: meal calorie warning
        {
            "platform": "input_number",
            "name": f"{prefix}_meal_calorie_warning",
            "min": 200,
            "max": 3000,
            "step": 100,
            "initial": DEFAULT_MEAL_WARNING,
            "mode": "slider",
            "unit_of_measurement": "kcal",
        },
        # input_text: calorie status
        {
            "platform": "input_text",
            "name": f"{prefix}_calorie_status",
            "max": 255,
            "initial": "",
        },
        # input_text: meal log
        {
            "platform": "input_text",
            "name": f"{prefix}_meal_log",
            "max": 255,
            "initial": "Empty",
        },
        # input_button: add food
        {
            "platform": "input_button",
            "name": f"{prefix}_add_food",
        },
        # input_button: finish meal
        {
            "platform": "input_button",
            "name": f"{prefix}_finish_meal",
        },
        # input_button: reset today
        {
            "platform": "input_button",
            "name": f"{prefix}_reset_today",
        },
    ]

    for helper in helpers_to_create:
        await _create_helper(hass, helper)

    _LOGGER.info("Calorie tracking helpers created successfully")


async def setup_cocktail_helpers(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Create all helper entities needed for cocktail mixing."""
    prefix = "thirdreality_scale"

    helpers_to_create = [
        # input_select: cocktail selector
        {
            "platform": "input_select",
            "name": f"{prefix}_select_cocktail",
            "options": list(DEFAULT_COCKTAIL_RECIPES.keys()) + ["custom"],
        },
        # input_button: start cocktail making
        {
            "platform": "input_button",
            "name": f"{prefix}_start_cocktail",
        },
        # input_button: done
        {
            "platform": "input_button",
            "name": f"{prefix}_done",
        },
        # input_text: cocktail status
        {
            "platform": "input_text",
            "name": f"{prefix}_cocktail_status",
            "max": 255,
            "initial": "",
        },
        # input_text: cocktail recipe list
        {
            "platform": "input_text",
            "name": f"{prefix}_cocktail_recipe_list",
            "max": 255,
            "initial": "",
        },
        # input_select: cocktail step page
        {
            "platform": "input_select",
            "name": f"{prefix}_cocktail_step",
            "options": ["idle", "mixing", "complete"],
        },
        # input_text: custom recipe
        {
            "platform": "input_text",
            "name": f"{prefix}_custom_recipe",
            "max": 255,
            "initial": "",
        },
    ]

    for helper in helpers_to_create:
        await _create_helper(hass, helper)

    _LOGGER.info("Cocktail mixing helpers created successfully")


async def _create_helper(hass: HomeAssistant, config: dict) -> None:
    """Create a single helper entity if it doesn't already exist."""
    platform = config.pop("platform")
    name = config.get("name", "")
    entity_id = f"{platform}.{name}"

    # 检查实体是否已存在
    state = hass.states.get(entity_id)
    if state is not None:
        _LOGGER.debug("Helper %s already exists, skipping", entity_id)
        return

    try:
        if platform == "input_number":
            await hass.services.async_call(
                "input_number",
                "create" if hasattr(hass.services, "has_service") else "reload",
                {
                    "name": name,
                    "min": config.get("min", 0),
                    "max": config.get("max", 100),
                    "step": config.get("step", 1),
                    "initial": config.get("initial", 0),
                    "mode": config.get("mode", "box"),
                    "unit_of_measurement": config.get("unit_of_measurement", ""),
                },
                blocking=True,
            )
        elif platform == "input_text":
            await hass.services.async_call(
                "input_text",
                "create",
                {
                    "name": name,
                    "max": config.get("max", 255),
                    "initial": config.get("initial", ""),
                },
                blocking=True,
            )
        elif platform == "input_select":
            await hass.services.async_call(
                "input_select",
                "create",
                {
                    "name": name,
                    "options": config.get("options", []),
                },
                blocking=True,
            )
        elif platform == "input_button":
            await hass.services.async_call(
                "input_button",
                "create",
                {"name": name},
                blocking=True,
            )

        _LOGGER.debug("Created helper: %s", entity_id)
    except Exception as err:
        _LOGGER.warning("Could not create helper %s: %s", entity_id, err)
