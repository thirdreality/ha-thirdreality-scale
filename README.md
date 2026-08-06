# ThirdReality Smart Scale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

ThirdReality Smart Scale Integration is a custom component for Home Assistant that works with the ThirdReality Smart Scale (3RKS030Z). It provides a **Cocktail Mixing Assistant** and a **Calorie Tracker** with real-time weight feedback and optional voice guidance.

> Works best with ThirdReality smart speakers for a fully hands-free experience.

## Features

- **Cocktail Mixing Assistant** — step-by-step guided mixing with real-time weight tracking
- **Calorie Tracker** — weigh food, log calories per meal, and get daily intake summaries
- **Voice guidance** — audio prompts for each step (works with ThirdReality smart speakers)
- **Zero manual setup** — all entities and logic are created automatically
- **Supported platforms:** Zigbee2MQTT, ZHA

## Requirements

- Home Assistant >= 2024.1.0
- HACS installed and configured
- A ThirdReality Smart Scale connected via Zigbee2MQTT or ZHA

## Installation

[![Open your Home Assistant instance and open the ThirdReality Smart Scale integration inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=thirdreality&repository=ha-thirdreality-scale&category=integration)

Or manually: HACS > Integrations > Search **ThirdReality Smart Scale** > Click into it > **Download**

After download, **restart Home Assistant**.

## Setup (3 Steps)

### Step 1: Add Integration

Go to Settings > Devices & Services > Add Integration > Search **ThirdReality Smart Scale**

[![Open your Home Assistant instance and start setting up ThirdReality Smart Scale.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=thirdreality_scale)

Follow the wizard:
1. **Select platform** (Zigbee2MQTT or ZHA) and **select your scale** from the dropdown
2. **Choose features** (Cocktail, Calorie, or both)
3. **Configure voice** (optional) — select your TTS engine and speaker

After completing the wizard, all entities and logic are automatically created. **No blueprints or automations needed!**

### Step 2: Import Dashboard (Copy & Paste)

1. Go to **Settings > Dashboards > + Add Dashboard**
2. Name it (e.g., "Cocktail" or "Calories"), click Create
3. Open the dashboard > click **⋮ menu** (top right) > **Edit Dashboard** > **⋮ menu** > **Raw configuration editor**
4. Replace the content with the YAML below:

   - **Cocktail Dashboard:** [cocktail_dashboard.yaml](custom_components/thirdreality_scale/dashboards/cocktail_dashboard.yaml)
   - **Calorie Dashboard:** [calorie_dashboard.yaml](custom_components/thirdreality_scale/dashboards/calorie_dashboard.yaml)

5. Click **Save** — done!

> **No modifications needed.** The dashboard YAML works out-of-the-box with the entities created by this integration.

### Step 3: Use It!

That's it. Open your dashboard and start using the scale.

---

## Usage

### Calorie Tracker

1. Open the **Calories** dashboard
2. Select a food from the dropdown (e.g. Apple, Chicken Breast) or enter a custom food name and calories per 100g
3. Place the food on the scale — real-time weight and calories are shown
4. Click **Add ** to log this item to the current meal
5. Repeat for more foods
6. Click **Finish Meal ** when done — the meal total is added to today's count
7. Click **Reset ** to start a new day

**Voice prompts:** confirmation on each Add, high-calorie warnings, meal summaries, daily limit alerts.


### Cocktail Mixing

1. Open the **Cocktail** dashboard
2. Choose a cocktail (e.g. Mojito) or select **Custom** and enter your own recipe
3. Click ** Start Mixing**
4. Place your glass on the scale, click **Done **
5. Pour each ingredient until the target weight is reached — auto-advances to next step
6. When all ingredients are added, ** Cheers!** — auto-returns to selection

**Voice prompts:** start instruction, ingredient guidance for each step, completion celebration.


### Adding Custom Recipes

Go to **Developer Tools > Actions** and call:

```yaml
service: thirdreality_scale.add_cocktail
data:
  name: "margarita"
  ingredients: "Tequila:50,Triple Sec:30,Fresh Lime Juice:25"
```

The new cocktail appears in the dropdown immediately.

Similarly for food:

```yaml
service: thirdreality_scale.add_food
data:
  name: "Chicken Wings"
  calories_per_100g: 290
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Scale not in dropdown during setup | Verify scale is connected in Zigbee2MQTT / ZHA |
| Voice not working | Check that media_player and TTS entities are available |
| Weight shows 0 | Check Developer Tools > States for your original weight sensor |
| Dashboard not updating | Ensure integration is configured and HA restarted |

## License

This project is open source. See [LICENSE](LICENSE) for details.
