# ThirdReality Smart Scale

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)

ThirdReality Smart Scale Integration is a custom component for Home Assistant that works with the ThirdReality Smart Scale (3RKS030Z). It provides a **Cocktail Mixing Assistant** and a **Calorie Tracker** with real-time weight feedback, 7-day history, and optional voice guidance through a built-in sidebar panel.

> Works best with ThirdReality smart speakers for a fully hands-free experience.

## Features

- **Built-in Sidebar Panel** — "Smart Scale" appears in the sidebar automatically
- **Cocktail Mixing Assistant** — step-by-step guided mixing with real-time weight tracking and auto-advance
- **Calorie Tracker** — weigh food, log calories per meal, track daily intake with progress ring and 7-day history chart
- **160+ Food Presets** — common foods with accurate calorie data (USDA-based), plus custom food support
- **Quick Add** — recently used foods shown as chips for one-tap selection
- **Streak & Weekly Average** — tracks consecutive days of use and weekly calorie average
- **g / oz Unit Toggle** — switch display units on the fly, all internal calculations stay in grams
- **Voice Guidance** — audio prompts for each step (works with ThirdReality smart speakers )
- **Daily Auto-Reset** — today's calorie count resets at midnight automatically
- **Auto-creates all entities** — zero manual setup after installation
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


### Step 5: Done

After configuration, "Smart Scale" appears in the Home Assistant sidebar. No additional dashboard setup is required.

The panel has four tabs:
- **Cocktail** — select and mix cocktails
- **Calories** — track food and daily calorie intake
- **Recipes** — add or remove cocktail recipes
- **Foods** — add or remove food presets


## Usage

### Calorie Tracker

1. Click **Smart Scale** in the sidebar, then the **Calories** tab
2. Search for a food using the search box, or tap a Quick Add chip at the top
3. Place the food on the scale — the page shows real-time weight
4. Click **Add** to log this item to the current meal
5. Repeat steps 2-4 for more foods
6. When the meal is done, click **Finish Meal** — the meal total is added to today's count and saved to history
7. The progress ring, 7-day chart, streak counter, and weekly average update automatically

**One-time food:** If a food isn't in the preset list, use the "One-time food" fields below the search box. Enter a name and calories per 100g. This entry is used once and not saved permanently.

**Adding foods permanently:** Go to the **Foods** tab to add items that will appear in the search dropdown for future use.

**Unit toggle:** Tap the `→oz` or `→g` button next to the weight display to switch between grams and ounces.

**Clear Today:** Resets today's calorie count to zero. Your meal history is preserved.

**Daily auto-reset:** At midnight, today's count resets automatically so you start fresh each day.

**Voice prompts:** confirmation on each Add, high-calorie warnings, meal summaries, daily limit alerts.


### Cocktail Mixing

1. Click **Smart Scale** in the sidebar, then the **Cocktail** tab
2. Choose a cocktail from the dropdown (e.g. Mojito) or select **custom** and enter your own recipe
3. Click **Start Mixing**
4. The page shows "Place glass on scale" — place your glass and click **Done**
5. Follow on-screen prompts: pour each ingredient until the target weight is reached
6. The scale auto-advances to the next step, or click **Done** manually
7. When all ingredients are added, **Cheers!** appears and auto-returns to selection after 5 seconds

**Voice prompts:** start instruction, ingredient guidance for each step, completion celebration.


### Managing Recipes

Go to the **Recipes** tab to add or remove cocktail recipes.

Recipe format: `ingredient:weight_in_grams`, separated by commas.

Example: `Tequila:50,Triple Sec:30,Lime Juice:25`

Or via service call:

```yaml
action: thirdreality_scale.add_cocktail
data:
  name: pina_colada
  ingredients: White Rum:50,Pineapple Juice:80,Coconut Cream:30
```

### Managing Foods

Go to the **Foods** tab to add or remove food presets.

Enter the food name and its calories per 100 grams. The new food appears in the search dropdown immediately.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Scale not in dropdown | Verify scale is connected in Zigbee2MQTT / ZHA |
| Voice not working | Check that media_player entity is available and TTS is configured |
| Weight not updating | The integration auto-starts reporting on boot. Try restarting HA. |
| Panel not in sidebar | Restart HA after install. Check the integration loaded without errors in Settings > Integrations. |

## License

This project is open source. See [LICENSE](LICENSE) for details.
