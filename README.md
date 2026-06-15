# ThirdReality Smart Scale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

ThirdReality Smart Scale Integration is a custom component for Home Assistant that works with the ThirdReality Smart Scale (3RKS030Z). It provides a **Cocktail Mixing Assistant** and a **Calorie Tracker** with real-time weight feedback and optional voice guidance.

> Works best with ThirdReality smart speakers for a fully hands-free experience.

## Features

- **Cocktail Mixing Assistant** — step-by-step guided mixing with real-time weight tracking
- **Calorie Tracker** — weigh food, log calories per meal, and get daily intake summaries
- **Voice guidance** — audio prompts for each step (works with ThirdReality smart speakers)
- **Auto-creates all helper entities** — zero manual setup after installation
- **Supported platforms:** Zigbee2MQTT, ZHA

## Requirements

- Home Assistant >= 2024.1.0
- HACS installed and configured
- A ThirdReality Smart Scale connected via Zigbee2MQTT or ZHA

## Installation

[![Open your Home Assistant instance and open the ThirdReality Smart Scale integration inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=thirdreality&repository=ha-thirdreality-scale&category=integration)

Or manually: HACS > Integrations > Search **ThirdReality Smart Scale** > Click into it > **Download**

After download, **restart Home Assistant**.

## Configuration

### Step 1: Add Integration

After restart, go to Settings > Devices & Services > Add Integration > Search **ThirdReality Smart Scale**

[![Open your Home Assistant instance and start setting up ThirdReality Smart Scale.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=thirdreality_scale)

### Step 2: Select Platform and Device

- **Platform:** select Zigbee2MQTT or ZHA
- **Device:** select your scale from the dropdown


### Step 3: Select Features

Check the features you want to enable:
- Cocktail Mixing Assistant
- Calorie Tracker


### Step 4: Voice Settings (Optional)

- **TTS Engine:** select your TTS entity
- **Speaker:** select your `media_player` entity for voice announcements


### Step 5: Restart Again

After configuration, **restart Home Assistant one more time**.

After restart, verify:
- Sidebar shows **Calories** and **Cocktail** dashboards
- **Settings > Automations** contains 2 new automations


## Usage

### Calorie Tracker

1. Click **Calories** in the sidebar
2. Select a food from the "Select Food" dropdown (e.g. Apple, Chicken Breast) or enter a custom food name and calories per 100g
3. Place the food on the scale, the page shows real-time weight and calories
4. Click **Add +** to log this item to the current meal
5. Repeat steps 2-4 for more foods
6. When the meal is done, click **Finish Meal**, the meal total is added to today's count
7. To start a new day, click **Reset**

**Voice prompts:** confirmation on each Add, high-calorie warnings, meal summaries, daily limit alerts.


### Cocktail Mixing

1. Click **Cocktail** in the sidebar
2. Choose a cocktail from "Choose Your Cocktail" (e.g. Mojito) or select **Custom** and enter your own recipe
3. Click **Start Mixing**
4. The page shows "Place glass on scale", place your glass and click **Done**
5. Follow on-screen prompts: pour each ingredient until the target weight is reached
6. The scale auto-advances to the next step, or click **Done** manually
7. When all ingredients are added, **Cheers!** appears and auto-returns to selection after 5 seconds

**Voice prompts:** start instruction, ingredient guidance for each step, completion celebration.


### Adding Custom Cocktail Recipes

1. Go to **Developer Tools > Actions**
2. Select service `thirdreality_scale.add_cocktail`
3. Fill in the data and click **Execute**:

```yaml
service: thirdreality_scale.add_cocktail
data:
  name: "margarita"
  ingredients: "Tequila:50,Triple Sec:30,Fresh Lime Juice:25"
```

Format: `ingredient:weight_in_grams`, separated by commas.

The new cocktail appears in the Cocktail dashboard dropdown immediately.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Dashboards not showing in sidebar | Restart HA after configuration |
| Scale not in dropdown | Verify scale is connected in Zigbee2MQTT / ZHA |
| Voice not working | Check that media_player entity is available and TTS is configured |
| Automations missing | Restart HA a second time after initial setup |

## License

This project is open source. See [LICENSE](LICENSE) for details.
