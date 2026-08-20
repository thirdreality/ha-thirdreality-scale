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

# Food database (calories per 100g) - USDA FoodData Central
DEFAULT_FOOD_DATABASE = {
    # ── Fruits ──
    "Apple": 52,
    "Banana": 89,
    "Orange": 47,
    "Strawberry": 32,
    "Blueberry": 57,
    "Raspberry": 52,
    "Grapes": 69,
    "Watermelon": 30,
    "Cantaloupe": 34,
    "Pineapple": 50,
    "Mango": 60,
    "Peach": 39,
    "Pear": 57,
    "Cherry": 63,
    "Kiwi": 61,
    "Avocado": 160,
    "Lemon": 29,
    "Grapefruit": 42,
    # ── Vegetables ──
    "Broccoli": 34,
    "Carrot": 41,
    "Spinach": 23,
    "Kale": 49,
    "Tomato": 18,
    "Lettuce": 15,
    "Cucumber": 15,
    "Bell Pepper": 31,
    "Onion": 40,
    "Garlic": 149,
    "Mushroom": 22,
    "Zucchini": 17,
    "Cauliflower": 25,
    "Green Beans": 31,
    "Asparagus": 20,
    "Celery": 14,
    "Cabbage": 25,
    "Potato": 77,
    "Sweet Potato": 86,
    "Corn": 96,
    "Peas": 81,
    # ── Protein (Meat & Fish) ──
    "Chicken Breast": 165,
    "Chicken Thigh": 209,
    "Chicken Wing": 203,
    "Ground Beef (80/20)": 254,
    "Ground Beef (90/10)": 176,
    "Ground Turkey": 149,
    "Turkey Breast": 135,
    "Pork Chop": 231,
    "Pork Tenderloin": 143,
    "Bacon": 541,
    "Ham": 145,
    "Steak (sirloin)": 183,
    "Steak (ribeye)": 291,
    "Lamb": 294,
    "Salmon": 208,
    "Tuna": 130,
    "Shrimp": 85,
    "Cod": 82,
    "Tilapia": 96,
    "Crab": 83,
    "Lobster": 89,
    # ── Eggs & Dairy ──
    "Egg": 155,
    "Egg White": 52,
    "Cheese (cheddar)": 403,
    "Cheese (mozzarella)": 280,
    "Cheese (parmesan)": 431,
    "Cream Cheese": 342,
    "Cottage Cheese": 98,
    "Milk (whole)": 61,
    "Milk (2%)": 50,
    "Milk (skim)": 34,
    "Greek Yogurt": 59,
    "Yogurt (plain)": 59,
    "Heavy Cream": 340,
    "Sour Cream": 198,
    "Butter": 717,
    # ── Grains & Carbs ──
    "Rice (white, cooked)": 130,
    "Rice (brown, cooked)": 112,
    "Pasta (cooked)": 131,
    "Quinoa (cooked)": 120,
    "Bread (white)": 265,
    "Bread (wheat)": 247,
    "Bagel": 270,
    "Tortilla (flour)": 312,
    "Tortilla (corn)": 218,
    "English Muffin": 227,
    "Pancake": 227,
    "Waffle": 291,
    "Oatmeal (cooked)": 68,
    "Granola": 471,
    "Cereal": 379,
    "Crackers": 421,
    "Couscous (cooked)": 112,
    # ── Legumes & Plant Protein ──
    "Tofu": 76,
    "Black Beans (cooked)": 132,
    "Chickpeas (cooked)": 164,
    "Lentils (cooked)": 116,
    "Edamame": 121,
    "Hummus": 166,
    # ── Nuts & Seeds ──
    "Almonds": 579,
    "Walnuts": 654,
    "Cashews": 553,
    "Peanuts": 567,
    "Peanut Butter": 588,
    "Almond Butter": 614,
    "Sunflower Seeds": 584,
    "Chia Seeds": 486,
    "Flax Seeds": 534,
    "Pistachios": 560,
    "Pecans": 691,
    "Trail Mix": 462,
    # ── Oils & Fats ──
    "Olive Oil": 884,
    "Coconut Oil": 862,
    "Vegetable Oil": 884,
    "Mayonnaise": 680,
    # ── Sweeteners & Condiments ──
    "Honey": 304,
    "Sugar": 387,
    "Maple Syrup": 260,
    "Ketchup": 101,
    "Mustard": 66,
    "Soy Sauce": 53,
    "BBQ Sauce": 172,
    "Ranch Dressing": 463,
    "Salsa": 36,
    "Guacamole": 160,
    # ── Snacks & Sweets ──
    "Chocolate (dark)": 546,
    "Chocolate (milk)": 535,
    "Ice Cream": 207,
    "Cookies": 488,
    "Brownie": 405,
    "Chips (potato)": 536,
    "Popcorn (air-popped)": 387,
    "Pretzels": 380,
    "Protein Bar": 350,
    "Granola Bar": 471,
    # ── Prepared Foods ──
    "Pizza": 266,
    "Hamburger": 295,
    "French Fries": 312,
    "Hot Dog": 290,
    "Burrito": 206,
    "Taco": 226,
    "Sushi (California Roll)": 150,
    "Fried Rice": 163,
    "Mac and Cheese": 164,
    "Chicken Nuggets": 296,
    "Fish Sticks": 220,
    # ── Beverages (per 100ml) ──
    "Orange Juice": 45,
    "Apple Juice": 46,
    "Coca Cola": 42,
    "Beer": 43,
    "Wine (red)": 85,
}

# Default cocktail recipes
DEFAULT_COCKTAIL_RECIPES = {
    "strawberry_daiquiri": "White Rum:45,Fresh Strawberry Puree:80,Fresh Lemon Juice:20,Simple Syrup:15",
    "mojito": "White Rum:40,Fresh Lime Juice:30,Fresh Mint Leaves:10,Simple Syrup:10,Club Soda:190",
}
