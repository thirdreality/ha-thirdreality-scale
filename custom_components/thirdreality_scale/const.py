"""Constants for the ThirdReality Smart Scale integration."""

DOMAIN = "thirdreality_scale"
CONF_PLATFORM = "platform"
CONF_Z2M_TOPIC = "z2m_topic"
CONF_ZHA_IEEE = "zha_ieee"
CONF_FEATURES = "features"
CONF_TTS_SPEAKER = "tts_speaker"
CONF_TTS_ENGINE = "tts_engine"

PLATFORM_Z2M = "z2m"
PLATFORM_ZHA = "zha"

FEATURE_COCKTAIL = "cocktail"
FEATURE_CALORIE = "calorie"

# Default values
DEFAULT_DAILY_TARGET = 2000
DEFAULT_MEAL_WARNING = 800
DEFAULT_TTS_ENGINE = "tts.piper"

# Food database (calories per 100g)
DEFAULT_FOOD_DATABASE = {
    "Apple": 52,
    "Banana": 89,
    "Orange": 47,
    "Strawberry": 32,
    "Blueberry": 57,
    "Grapes": 69,
    "Watermelon": 30,
    "Avocado": 160,
    "Chicken Breast": 165,
    "Ground Beef": 250,
    "Salmon": 208,
    "Shrimp": 85,
    "Tuna": 130,
    "Bacon": 541,
    "Turkey": 135,
    "Egg": 155,
    "Rice (cooked)": 130,
    "Pasta (cooked)": 131,
    "Bread (white)": 265,
    "Bread (wheat)": 247,
    "Oatmeal": 68,
    "Cereal": 379,
    "Potato": 77,
    "Sweet Potato": 86,
    "Corn": 96,
    "Broccoli": 34,
    "Carrot": 41,
    "Spinach": 23,
    "Tomato": 18,
    "Lettuce": 15,
    "Onion": 40,
    "Cheese (cheddar)": 403,
    "Milk (whole)": 61,
    "Milk (skim)": 34,
    "Yogurt (plain)": 59,
    "Butter": 717,
    "Peanut Butter": 588,
    "Almonds": 579,
    "Walnuts": 654,
    "Olive Oil": 884,
    "Honey": 304,
    "Sugar": 387,
    "Chocolate": 546,
    "Ice Cream": 207,
    "Pizza": 266,
    "Hamburger": 295,
    "French Fries": 312,
    "Hot Dog": 290,
    "Steak": 271,
    "Tofu": 76,
}

# Default cocktail recipes
DEFAULT_COCKTAIL_RECIPES = {
    "strawberry_daiquiri": "White Rum:45,Fresh Strawberry Puree:80,Fresh Lemon Juice:20,Simple Syrup:15",
    "mojito": "White Rum:40,Fresh Lime Juice:30,Fresh Mint Leaves:10,Simple Syrup:10,Club Soda:190",
}
