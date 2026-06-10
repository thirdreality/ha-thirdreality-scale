# 🍸🔥 ThirdReality Smart Scale - Home Assistant Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/thirdreality/ha-thirdreality-scale)](https://github.com/thirdreality/ha-thirdreality-scale/releases)
[![License: MIT](https://img.shields.io/github/license/thirdreality/ha-thirdreality-scale)](LICENSE)

> Turn your ThirdReality Smart Scale into a kitchen assistant — cocktail mixing guide + calorie tracking with voice announcements!

---

## ✨ Features

### 🍸 Cocktail Mixing Assistant
- Step-by-step guided cocktail mixing by weight
- Auto-advances to next ingredient when target weight is reached
- 12 preset cocktail recipes + custom recipe support
- Voice guidance at each step

### 🔥 Calorie Tracker
- ~50 preset common foods with calories per 100g
- Real-time calorie display as you weigh food
- Automatic meal and daily total accumulation
- Over-limit voice warnings
- Custom food name and calorie input support

### 🔊 Smart Voice Announcements
- Confirms each food added (name, weight, calories)
- High-calorie food warnings (>400 cal/100g)
- Meal total exceeds target alert
- Daily total exceeds target alert
- Step-by-step cocktail instructions

### 🎯 One-Click Install, Zero Configuration
- Automatically creates dashboards (Calories + Cocktail)
- Automatically creates blueprints and automations
- No manual Helper entity creation needed
- Supports both Zigbee2MQTT and ZHA

---

## 📸 Screenshots

<!-- Add your screenshots here -->
<!-- ![Calorie Dashboard](docs/images/calorie_dashboard.png) -->
<!-- ![Cocktail Dashboard](docs/images/cocktail_dashboard.png) -->

---

## 📋 Prerequisites

- Home Assistant 2024.1.0 or higher
- [HACS](https://hacs.xyz/) installed
- ThirdReality Smart Scale connected to HA (via Zigbee2MQTT or ZHA)
- (Optional) TTS-capable speaker for voice announcements

---

## 🚀 Installation

### Option 1: Via HACS (Recommended)

1. Open HACS → Integrations
2. Click `⋮` (top right) → Custom repositories
3. Enter `https://github.com/thirdreality/ha-thirdreality-scale`
4. Category: `Integration`
5. Click Add → Search "ThirdReality Smart Scale" → Download
6. Restart Home Assistant

### Option 2: Manual Installation

1. Download the [latest release](https://github.com/thirdreality/ha-thirdreality-scale/releases)
2. Copy the `custom_components/thirdreality_scale` folder to your HA `custom_components/` directory
3. Restart Home Assistant

---

## ⚙️ Configuration

1. **Settings → Devices & Services → Add Integration** → Search "ThirdReality"
2. **Select Platform**:
   - Zigbee2MQTT: Enter device topic (e.g., `0xaa97282c02b36898`)
   - ZHA: Enter IEEE address
3. **Select Features**: Check 🍸 Cocktail and/or 🔥 Calorie
4. **Voice Setup** (optional):
   - TTS Engine: e.g., `tts.piper`
   - Speaker: e.g., `media_player.your_speaker`
5. **Done** → Restart HA

After restart you will see:
- **Calories** and **Cocktail** dashboards in the sidebar
- Corresponding automations in the automation list
- Two blueprints in the blueprints page

---

## 📖 Usage

### Calorie Tracking

1. Go to the **Calories** dashboard
2. Select a food from the dropdown (or enter custom food name + calories)
3. Place food on the scale → real-time calorie display
4. Click **Add ➕** → Add to current meal
5. Click **Finish Meal ✅** → Add meal total to daily total
6. Click **Reset 🗑️** → Reset today's data

### Cocktail Mixing

1. Go to the **Cocktail** dashboard
2. Select a cocktail recipe from the dropdown
3. Click **Start Mixing ▶️**
4. Place glass on scale → Press **Done ✅** to begin
5. Follow prompts to add each ingredient (auto-advances at target weight, or press Done manually)
6. Automatically returns to selection page when complete

---

## 🍹 Custom Cocktail Recipes

You can add up to 12 preset recipes in the blueprint configuration. Format:

```
ingredient:weight(g),ingredient:weight(g),...
```

Example:
```
White Rum:45,Fresh Strawberry Puree:80,Fresh Lemon Juice:20,Simple Syrup:15
```

You can also select "custom" on the dashboard and enter a recipe on the fly.

---

## 🛠️ Advanced Configuration

### Supported TTS Engines

| TTS Engine | entity_id Example |
|-----------|-------------------|
| Piper (local) | `tts.piper` |
| Google Translate | `tts.google_translate_say` |
| Nabu Casa Cloud | `tts.cloud_say` |

### Entity List

The following entities are automatically created (prefixed with `thirdreality_smart_scale`):

| Type | Entity | Description |
|------|--------|-------------|
| button | `add_food` | Add food to meal |
| button | `finish_meal` | Finish current meal |
| button | `reset_today` | Reset today's total |
| button | `start_cocktail` | Start cocktail mixing |
| button | `done` | Confirm / Next step |
| number | `meal_calories` | Current meal calories |
| number | `today_calories` | Today's total calories |
| number | `daily_calorie_target` | Daily calorie target |
| number | `meal_calorie_warning` | Meal warning threshold |
| number | `custom_cal_per_100g` | Custom calories per 100g |
| text | `calorie_status` | Status display |
| text | `meal_log` | Meal log |
| text | `custom_food_name` | Custom food name |
| text | `cocktail_status` | Cocktail status |
| text | `cocktail_recipe_list` | Ingredient list |
| text | `custom_recipe` | Custom recipe input |
| select | `food_preset` | Food preset selector |
| select | `select_cocktail` | Cocktail selector |
| select | `cocktail_step` | Cocktail step control |

---

## ❓ FAQ

### Dashboard not showing up?
Restart HA and wait 1-2 minutes, then refresh the page. Check Settings → Dashboards if it exists.

### Automations not created?
Check your `automations.yaml` file for the entries. Try removing and re-adding the integration.

### Speaker not talking?
1. Verify TTS engine entity exists (Developer Tools → States → search "tts")
2. Verify speaker is online (media_player state is not unavailable)
3. Test TTS manually in Developer Tools

### Which scales are supported?
ThirdReality Smart Nutrition Scale (Zigbee), connected via Zigbee2MQTT or ZHA.

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

- 🐛 [Report a Bug](https://github.com/thirdreality/ha-thirdreality-scale/issues)
- 💡 [Feature Request](https://github.com/thirdreality/ha-thirdreality-scale/issues)

---

## 📄 License

[MIT License](LICENSE)

---

## 🙏 Acknowledgments

- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [ThirdReality](https://www.3reality.com/)
