import { LitElement, html, css } from "lit";

class ThirdRealityScalePanel extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      narrow: { type: Boolean },
      route: { type: Object },
      panel: { type: Object },
      _activeTab: { type: String },
      _foodSearch: { type: String },
      _confirmReset: { type: Boolean },
      _confirmFinish: { type: Boolean },
      _unit: { type: String },
      _historyData: { type: Array },
    };
  }

  constructor() {
    super();
    this._activeTab = "cocktail";
    this._foodSearch = null;
    this._confirmReset = false;
    this._confirmFinish = false;
    this._unit = localStorage.getItem("tr_scale_unit") || "g";
    this._historyData = [];
    this._historyLoaded = false;
  }

  updated(changedProps) {
    if (changedProps.has("hass") && this.hass && !this._historyLoaded) {
      this._loadHistory();
      this._historyLoaded = true;
    }
  }

  async _loadHistory() {
    try {
      const result = await this.hass.callWS({ type: "thirdreality_scale/get_calorie_history" });
      this._historyData = result.history || [];
    } catch (e) {
      this._historyData = [];
    }
  }

  _toggleUnit() {
    this._unit = this._unit === "g" ? "oz" : "g";
    localStorage.setItem("tr_scale_unit", this._unit);
  }

  _displayWeight(grams) {
    if (this._unit === "oz") return `${(grams / 28.35).toFixed(1)}`;
    return `${Math.round(grams)}`;
  }

  _unitLabel() { return this._unit; }

  static get styles() {
    return css`
      :host { display: block; height: 100%; font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif); }
      * { box-sizing: border-box; }

      .panel { height: 100%; display: flex; flex-direction: column; background: var(--primary-background-color, #fafafa); }

      /* Header */
      .header { padding: 16px 24px 0; background: var(--card-background-color, white); }
      .header h1 { margin: 0 0 16px; font-size: 24px; font-weight: 400; color: var(--primary-text-color); }
      .tabs { display: flex; gap: 24px; border-bottom: 1px solid var(--divider-color, #e0e0e0); }
      .tab {
        padding: 8px 0 12px; cursor: pointer; font-size: 14px; font-weight: 500;
        color: var(--secondary-text-color); border-bottom: 2px solid transparent;
        transition: all 0.2s; user-select: none;
      }
      .tab:hover { color: var(--primary-text-color); }
      .tab.active { color: var(--primary-color); border-bottom-color: var(--primary-color); }

      /* Content */
      .content { flex: 1; overflow-y: auto; padding: 24px; }
      .content::-webkit-scrollbar { width: 4px; }
      .content::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 2px; }

      /* Section */
      .section {
        background: var(--card-background-color, white);
        border: 1px solid var(--divider-color, #e8e8e8);
        border-radius: 8px; padding: 20px; margin-bottom: 16px;
      }
      .section-title { font-size: 16px; font-weight: 500; color: var(--primary-text-color); margin: 0 0 16px; }
      .section-desc { font-size: 14px; color: var(--secondary-text-color); margin: 0 0 16px; }

      /* Form elements */
      .form-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
      .form-label { font-size: 13px; color: var(--secondary-text-color); margin-bottom: 4px; }
      .form-select, .form-input {
        width: 100%; padding: 10px 12px; font-size: 14px;
        border: 1px solid var(--divider-color, #ddd); border-radius: 6px;
        background: var(--card-background-color, white); color: var(--primary-text-color);
        outline: none; transition: border-color 0.2s;
      }
      .form-select:focus, .form-input:focus { border-color: var(--primary-color); }
      .form-input::placeholder { color: var(--disabled-text-color, #999); }

      /* Buttons */
      .btn-group { display: flex; gap: 8px; margin-top: 12px; }
      .btn {
        padding: 10px 16px; border-radius: 6px; font-size: 13px; font-weight: 500;
        cursor: pointer; transition: all 0.15s; border: 1px solid transparent;
        display: inline-flex; align-items: center; gap: 4px;
      }
      .btn:active { transform: scale(0.97); }
      .btn-filled { background: var(--primary-color); color: white; border-color: var(--primary-color); }
      .btn-filled:hover { opacity: 0.9; }
      .btn-outline { background: transparent; color: var(--primary-color); border-color: var(--primary-color); }
      .btn-outline:hover { background: rgba(3,169,244,0.05); }
      .btn-success { background: #4caf50; color: white; border-color: #4caf50; }
      .btn-danger { background: transparent; color: #f44336; border-color: #f44336; }
      .btn-danger:hover { background: rgba(244,67,54,0.05); }
      .btn-ghost { background: transparent; color: var(--secondary-text-color); border-color: var(--divider-color); }

      /* Weight inline */
      .weight-inline { display: flex; align-items: baseline; justify-content: center; padding: 8px 0; }
      .weight-num { font-size: 28px; font-weight: 300; color: var(--primary-text-color); }
      .weight-unit { font-size: 14px; color: var(--secondary-text-color); margin-left: 4px; }

      /* Progress ring */
      .progress-section { display: flex; align-items: center; gap: 20px; }
      .progress-ring { position: relative; width: 80px; height: 80px; flex-shrink: 0; }
      .progress-ring svg { transform: rotate(-90deg); }
      .progress-ring .bg { fill: none; stroke: var(--divider-color, #e0e0e0); stroke-width: 6; }
      .progress-ring .fill { fill: none; stroke-width: 6; stroke-linecap: round; transition: stroke-dashoffset 0.5s; }
      .progress-ring .center-text {
        position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        font-size: 16px; font-weight: 500; color: var(--primary-text-color);
      }
      .progress-info { flex: 1; }
      .progress-info .main { font-size: 20px; font-weight: 400; color: var(--primary-text-color); margin-bottom: 4px; }
      .progress-info .sub { font-size: 13px; color: var(--secondary-text-color); }

      /* Progress + History layout */
      .calories-top { display: flex; gap: 12px; align-items: center; }
      .calories-top-left { flex: 0 0 auto; }
      .calories-top-center { flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 0 8px; }
      .calories-top-right { flex: 1; display: flex; flex-direction: column; justify-content: center; }
      .mini-history-title { font-size: 11px; font-weight: 500; color: var(--secondary-text-color); margin-bottom: 8px; text-align: center; }
      .mini-history-chart { display: flex; align-items: flex-end; justify-content: center; gap: 4px; height: 60px; }
      .mini-history-col { display: flex; flex-direction: column; align-items: center; gap: 2px; flex: 1; max-width: 36px; }
      .mini-history-bar-v { width: 100%; min-width: 12px; border-radius: 3px 3px 0 0; transition: height 0.3s; }
      .mini-history-label { font-size: 9px; color: var(--secondary-text-color); }

      /* Status */
      .status-msg {
        padding: 10px 14px; background: var(--secondary-background-color, #f5f5f5);
        border-radius: 6px; font-size: 13px; color: var(--primary-text-color); margin-bottom: 12px;
      }

      /* List */
      .list-item {
        display: flex; align-items: center; padding: 10px 0;
        border-bottom: 1px solid var(--divider-color, #eee); font-size: 14px;
      }
      .list-item:last-child { border-bottom: none; }
      .list-num {
        width: 22px; height: 22px; border-radius: 50%; background: var(--primary-color);
        color: white; display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 600; margin-right: 12px; flex-shrink: 0;
      }
      .list-item.active { background: rgba(3,169,244,0.05); margin: 0 -20px; padding: 10px 20px; border-radius: 4px; }

      /* Meal log */
      .log-item { font-size: 13px; color: var(--secondary-text-color); padding: 6px 0; border-bottom: 1px solid var(--divider-color, #f0f0f0); }
      .log-item:last-child { border-bottom: none; }

      /* Settings row */
      .setting-row { display: flex; align-items: center; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid var(--divider-color, #eee); }
      .setting-row:last-child { border-bottom: none; }
      .setting-label { font-size: 14px; color: var(--primary-text-color); }
      .setting-value { font-size: 14px; color: var(--primary-color); font-weight: 500; }

      /* Compact settings inputs */
      .settings-compact { display: flex; gap: 12px; }
      .settings-compact > div { flex: 1; }
      .settings-compact label { display: block; font-size: 12px; color: var(--secondary-text-color); margin-bottom: 4px; }
      .settings-compact input {
        width: 100%; padding: 8px 10px; border: 1px solid var(--divider-color, #ddd);
        border-radius: 6px; font-size: 14px; color: var(--primary-text-color);
        background: var(--card-background-color); outline: none;
      }
      .settings-compact input:focus { border-color: var(--primary-color); }

      /* History styles */
      .history-day {
        margin-bottom: 16px; padding-bottom: 16px;
        border-bottom: 1px solid var(--divider-color, #eee);
      }
      .history-day:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
      .history-day-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 8px;
      }
      .history-date { font-size: 14px; font-weight: 500; color: var(--primary-text-color); }
      .history-total {
        font-size: 13px; font-weight: 600; padding: 2px 8px;
        border-radius: 12px; background: var(--primary-color); color: white;
      }
      .history-meal {
        display: flex; align-items: center; gap: 8px;
        padding: 4px 0; font-size: 13px; color: var(--secondary-text-color);
      }
      .history-meal-time { 
        font-weight: 500; color: var(--primary-text-color); min-width: 45px;
      }
      .history-meal-cal { font-weight: 500; color: var(--primary-color); }
      .history-bar {
        height: 6px; border-radius: 3px; margin-top: 6px;
        background: var(--divider-color, #e0e0e0); overflow: hidden;
      }
      .history-bar-fill {
        height: 100%; border-radius: 3px; transition: width 0.3s;
      }
      .history-empty {
        text-align: center; padding: 40px 20px; color: var(--secondary-text-color); font-size: 14px;
      }

      @media (max-width: 768px) {
        .content { padding: 16px; }
        .header { padding: 12px 16px 0; }
        .form-row { flex-direction: column; align-items: stretch; }
        .btn-group { flex-wrap: wrap; }
        .progress-section { flex-direction: column; align-items: center; text-align: center; }
        .calories-top { flex-wrap: wrap; }
        .calories-top-left { flex: 1 1 100%; margin-bottom: 12px; }
        .calories-top-right { flex: 1 1 55%; }
        .calories-top-center { flex: 1 1 40%; border-left: none !important; padding-left: 0 !important; border-top: none; flex-direction: row; justify-content: space-around; gap: 16px; }
      }
    `;
  }

  render() {
    return html`
      <div class="panel">
        <div class="header">
          <h1>Smart Scale</h1>
          <div class="tabs">
            <div class="tab ${this._activeTab === "cocktail" ? "active" : ""}" @click=${() => this._activeTab = "cocktail"}>Cocktail</div>
            <div class="tab ${this._activeTab === "calorie" ? "active" : ""}" @click=${() => this._activeTab = "calorie"}>Calories</div>
            <div class="tab ${this._activeTab === "recipes" ? "active" : ""}" @click=${() => this._activeTab = "recipes"}>Recipes</div>
            <div class="tab ${this._activeTab === "foods" ? "active" : ""}" @click=${() => this._activeTab = "foods"}>Foods</div>
          </div>
        </div>
        <div class="content">
          ${this._activeTab === "cocktail" ? this._renderCocktail()
            : this._activeTab === "calorie" ? this._renderCalorie()
            : this._activeTab === "recipes" ? this._renderRecipes()
            : this._renderFoods()}
        </div>
      </div>
    `;
  }

  // ═══════════════════════════════════════
  // COCKTAIL
  // ═══════════════════════════════════════
  _renderCocktail() {
    const step = this._getState("select.thirdreality_smart_scale_cocktail_step");
    if (step === "mixing") return this._renderMixing();
    if (step === "complete") return this._renderComplete();
    return this._renderCocktailIdle();
  }

  _renderCocktailIdle() {
    const selected = this._getState("select.thirdreality_smart_scale_select_cocktail");
    const options = this._getOptions("select.thirdreality_smart_scale_select_cocktail");
    const custom = this._getState("text.thirdreality_smart_scale_custom_recipe");
    return html`
      <div class="section">
        <h3 class="section-title">Select Recipe</h3>
        <p class="section-desc">Choose a cocktail recipe and press start to begin guided mixing.</p>
        <select class="form-select" @change=${this._onCocktailSelect}>
          ${options.map(o => html`<option value=${o} ?selected=${o === selected}>${o}</option>`)}
        </select>
        ${selected === "custom" ? html`
          <div style="margin-top:12px">
            <div class="form-label">Custom recipe (format: ingredient:weight,...)</div>
            <input class="form-input" .value=${custom || ""} placeholder="vodka:50,orange juice:100" @change=${this._onCustomRecipeChange} />
          </div>
        ` : ""}
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._startCocktail}>Start Mixing</button>
        </div>
      </div>
    `;
  }

  _renderRecipePreview(recipeName) {
    const dbRaw = this._getState("text.thirdreality_smart_scale_cocktail_recipes_database");
    if (!dbRaw) return "";
    let ingredients = "";
    for (const entry of dbRaw.split("|")) {
      const parts = entry.split("=");
      if (parts.length === 2 && parts[0].trim() === recipeName) {
        ingredients = parts[1].trim();
        break;
      }
    }
    if (!ingredients) return "";
    const items = ingredients.split(",").map(i => i.trim()).filter(i => i);
    return html`
      <div style="margin-top:12px;padding:12px;background:var(--secondary-background-color,#f9f9f9);border-radius:6px">
        <div style="font-size:12px;color:var(--secondary-text-color);margin-bottom:8px;font-weight:500">Recipe Preview:</div>
        ${items.map(item => {
          const p = item.split(":");
          return html`<div style="font-size:13px;color:var(--primary-text-color);padding:2px 0">${p[0]}${p[1] ? ` — ${p[1]}g` : ""}</div>`;
        })}
      </div>
    `;
  }

  _renderMixing() {
    const status = this._getState("text.thirdreality_smart_scale_cocktail_status");
    const list = this._getState("text.thirdreality_smart_scale_cocktail_recipe_list");
    const weight = this._getState("sensor.thirdreality_smart_scale_weight") || "0";
    const ingredients = list ? list.split(" | ").filter(i => i.trim()) : [];
    return html`
      ${status ? html`<div class="status-msg">${status}</div>` : ""}
      <div class="section">
        <div class="weight-inline">
          <span class="weight-num">${this._displayWeight(parseFloat(weight))}</span>
          <span class="weight-unit">${this._unitLabel()}</span>
          <span @click=${this._toggleUnit} style="margin-left:8px;padding:2px 8px;font-size:11px;border-radius:10px;cursor:pointer;background:var(--secondary-background-color,#eee);color:var(--secondary-text-color);border:1px solid var(--divider-color,#ddd)">${this._unit === "g" ? "→oz" : "→g"}</span>
        </div>
      </div>
      ${ingredients.length ? html`
        <div class="section">
          <h3 class="section-title">Ingredients</h3>
          ${ingredients.map((item, i) => html`
            <div class="list-item"><span class="list-num">${i + 1}</span><span>${item.replace(/^\d+\.\s*/, "")}</span></div>
          `)}
        </div>
      ` : ""}
      <div class="btn-group">
        <button class="btn btn-success" @click=${this._doneCocktail}>Done — Next Step</button>
        <button class="btn btn-ghost" @click=${this._backToIdle}>Back</button>
      </div>
    `;
  }

  _renderComplete() {
    return html`
      <div class="section" style="text-align:center;padding:40px 20px">
        <h3 class="section-title" style="font-size:20px">Cheers! Your cocktail is ready.</h3>
        <p class="section-desc">All ingredients have been added. Enjoy!</p>
        <div class="btn-group" style="justify-content:center">
          <button class="btn btn-outline" @click=${this._backToIdle}>Make Another</button>
        </div>
      </div>
    `;
  }

  // ═══════════════════════════════════════
  // CALORIES
  // ═══════════════════════════════════════
  _renderCalorie() {
    const weight = parseFloat(this._getState("sensor.thirdreality_smart_scale_weight")) || 0;
    const todayCal = parseFloat(this._getState("number.thirdreality_smart_scale_today_calories")) || 0;
    const mealCal = parseFloat(this._getState("number.thirdreality_smart_scale_meal_calories")) || 0;
    const dailyTarget = parseFloat(this._getState("number.thirdreality_smart_scale_daily_calorie_target")) || 2000;
    const selectedFood = this._getState("select.thirdreality_smart_scale_food_preset");
    const foodOptions = this._getOptions("select.thirdreality_smart_scale_food_preset");
    const status = this._getState("text.thirdreality_smart_scale_calorie_status");
    const mealLog = this._getState("text.thirdreality_smart_scale_meal_log");
    const customName = this._getState("text.thirdreality_smart_scale_custom_food_name");
    const customCal = this._getState("number.thirdreality_smart_scale_custom_cal_per_100g");
    const pct = dailyTarget > 0 ? Math.min(Math.round((todayCal / dailyTarget) * 100), 100) : 0;
    const remaining = Math.round(dailyTarget - todayCal);
    const circumference = 2 * Math.PI * 34;
    const dashoffset = circumference - (pct / 100) * circumference;
    const ringColor = pct >= 100 ? "#f44336" : pct >= 75 ? "#ff9800" : "#4caf50";

    return html`
      <!-- Progress + History side by side -->
      <div class="section">
        <div class="calories-top">
          <div class="calories-top-left">
            <div class="progress-section">
              <div class="progress-ring">
                <svg width="80" height="80" viewBox="0 0 80 80">
                  <circle class="bg" cx="40" cy="40" r="34"></circle>
                  <circle class="fill" cx="40" cy="40" r="34" stroke="${ringColor}"
                    stroke-dasharray="${circumference}" stroke-dashoffset="${dashoffset}"></circle>
                </svg>
                <span class="center-text">${pct}%</span>
              </div>
              <div class="progress-info">
                <div class="main">${Math.round(todayCal)} / ${Math.round(dailyTarget)} kcal</div>
                <div class="sub">${remaining > 0 ? `${remaining} kcal remaining` : `Exceeded by ${Math.abs(remaining)} kcal`}</div>
              </div>
            </div>
          </div>
          <div class="calories-top-right" style="flex:1">
            ${this._renderMiniHistory(dailyTarget)}
          </div>
          <div class="calories-top-center" style="border-left:1px solid var(--divider-color,#eee);padding-left:14px;min-width:100px">
            <div style="margin-bottom:6px">
              <div style="font-size:10px;color:var(--secondary-text-color);margin-bottom:2px">Current Streak</div>
              <div style="font-size:16px;font-weight:500;color:var(--primary-text-color)">${this._getStreak()} days</div>
            </div>
            <div style="margin-bottom:6px">
              <div style="font-size:10px;color:var(--secondary-text-color);margin-bottom:2px">Best Streak</div>
              <div style="font-size:16px;font-weight:500;color:var(--primary-text-color)">${this._getBestStreak()} days</div>
            </div>
            <div>
              <div style="font-size:10px;color:var(--secondary-text-color);margin-bottom:2px">Weekly Avg</div>
              <div style="font-size:16px;font-weight:500;color:var(--primary-text-color)">${this._getWeekAvg()} kcal</div>
            </div>
          </div>
        </div>
        <!-- Motivation text - prominent, left-aligned -->
        <div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--divider-color,#eee);font-size:15px;font-weight:400;color:var(--primary-text-color)">
          ${this._getMotivation(pct)}
        </div>
      </div>

      <!-- Today's Meals -->
      ${this._renderTodayMeals()}

      <!-- Daily Goals -->
      <div class="section">
        <h3 class="section-title">Daily Goals</h3>
        <div class="settings-compact">
          <div>
            <label>Daily Target (kcal)</label>
            <input type="number" .value=${dailyTarget} @change=${this._onDailyTargetChange} />
          </div>
          <div>
            <label>Meal Warning (kcal)</label>
            <input type="number" .value=${parseFloat(this._getState("number.thirdreality_smart_scale_meal_calorie_warning")) || 800} @change=${this._onMealWarningChange} />
          </div>
        </div>
      </div>

      <!-- Current Meal -->
      ${mealLog && mealLog !== "Empty" && mealLog !== "" ? html`
        <div class="section">
          <h3 class="section-title">Current Meal — ${Math.round(mealCal)} kcal</h3>
          ${mealLog.split(" | ").map(i => html`<div class="log-item">${i}</div>`)}
        </div>
      ` : ""}

      <!-- Add Food -->
      <div class="section">
        <h3 class="section-title">Add Food</h3>
        ${this._renderQuickAdd(foodOptions)}
        <div style="position:relative;margin-bottom:8px">
          <input class="form-input" placeholder="Search food..." 
            .value=${this._foodSearch !== null ? this._foodSearch : (selectedFood || "")}
            @input=${this._onFoodSearchInput}
            @focus=${() => { if (this._foodSearch === null) { this._foodSearch = ""; } this.requestUpdate(); }}
            @blur=${() => { setTimeout(() => { this._foodSearch = null; this.requestUpdate(); }, 200); }}
          />
          ${this._foodSearch !== null && this._foodSearch !== undefined ? html`
            <div style="position:absolute;top:100%;left:0;right:0;z-index:10;max-height:200px;overflow-y:auto;
              background:var(--card-background-color,white);border:1px solid var(--divider-color,#ddd);
              border-radius:0 0 6px 6px;box-shadow:0 4px 12px rgba(0,0,0,0.1)">
              ${this._filterFood(foodOptions).slice(0, 8).map(o => html`
                <div @click=${() => this._selectFoodFromSearch(o)}
                  style="padding:10px 12px;font-size:14px;cursor:pointer;
                  border-bottom:1px solid var(--divider-color,#f0f0f0);
                  color:var(--primary-text-color);
                  background:${o === selectedFood ? 'var(--secondary-background-color,#f5f5f5)' : 'transparent'}"
                >${o}</div>
              `)}
              ${this._filterFood(foodOptions).length === 0 ? html`
                <div style="padding:10px 12px;font-size:13px;color:var(--secondary-text-color)">Not found — add it in Foods tab</div>
              ` : ""}
            </div>
          ` : ""}
        </div>
        <div style="margin-top:12px">
          <div class="form-label">One-time food (not saved):</div>
          <div style="display:flex;gap:8px">
            <input class="form-input" placeholder="Food name" .value=${customName || ""} @change=${this._onCustomFoodNameChange} style="flex:2" />
            <input class="form-input" type="number" placeholder="Cal/100g" .value=${customCal && customCal !== "0" ? customCal : ""} @change=${this._onCustomCalChange} style="flex:1" />
          </div>
        </div>
        <div class="weight-inline">
          <span class="weight-num">${this._displayWeight(weight)}</span>
          <span class="weight-unit">${this._unitLabel()}</span>
          <span @click=${this._toggleUnit} style="margin-left:8px;padding:2px 8px;font-size:11px;border-radius:10px;cursor:pointer;background:var(--secondary-background-color,#eee);color:var(--secondary-text-color);border:1px solid var(--divider-color,#ddd)">${this._unit === "g" ? "→oz" : "→g"}</span>
        </div>
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._addFood}>Add</button>
          <button class="btn btn-outline" @click=${this._undoAdd}>Undo</button>
          ${this._confirmFinish
            ? html`<button class="btn btn-danger" @click=${this._confirmFinishAction}>Confirm Finish?</button>`
            : html`<button class="btn btn-success" @click=${this._finishMealConfirm}>Finish Meal</button>`
          }
        </div>
      </div>

      ${status ? html`<div class="status-msg">${status}</div>` : ""}

    `;
  }

  // ═══════════════════════════════════════
  // HISTORY & TODAY'S MEALS
  // ═══════════════════════════════════════
  _renderQuickAdd(foodOptions) {
    // Build quick add list from: 1) current meal_log foods, 2) recent from history, 3) first few options
    const mealLog = this._getState("text.thirdreality_smart_scale_meal_log");
    const selected = this._getState("select.thirdreality_smart_scale_food_preset");
    const recentFoods = [];
    const seen = new Set();

    // 1. Foods from current meal log
    if (mealLog && mealLog !== "Empty") {
      for (const entry of mealLog.split(" | ")) {
        const match = entry.match(/^(.+?)\s+\d+g=/);
        if (match && foodOptions.includes(match[1]) && !seen.has(match[1])) {
          recentFoods.push(match[1]);
          seen.add(match[1]);
        }
      }
    }

    // 2. Currently selected (if not already added)
    if (selected && foodOptions.includes(selected) && !seen.has(selected)) {
      recentFoods.push(selected);
      seen.add(selected);
    }

    // 3. Fill remaining slots with popular foods from the options list
    const popular = ["Chicken Breast", "Egg", "Rice (cooked)", "Banana", "Apple", "Salmon", "Avocado", "Oatmeal"];
    for (const p of popular) {
      if (recentFoods.length >= 5) break;
      if (foodOptions.includes(p) && !seen.has(p)) {
        recentFoods.push(p);
        seen.add(p);
      }
    }

    // 4. If still not enough, add first few options
    for (const opt of foodOptions) {
      if (recentFoods.length >= 5) break;
      if (!seen.has(opt)) {
        recentFoods.push(opt);
        seen.add(opt);
      }
    }

    if (recentFoods.length === 0) return "";

    return html`
      <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px">
        ${recentFoods.slice(0, 5).map(food => html`
          <span @click=${() => this._quickSelectFood(food)}
            style="padding:5px 12px;font-size:12px;border-radius:14px;cursor:pointer;
            background:${food === selected ? 'var(--primary-color)' : 'var(--secondary-background-color,#f0f0f0)'};
            color:${food === selected ? 'white' : 'var(--primary-text-color)'};
            border:1px solid ${food === selected ? 'var(--primary-color)' : 'var(--divider-color,#ddd)'};
            transition:all 0.15s;user-select:none"
          >${food}</span>
        `)}
      </div>
    `;
  }

  _quickSelectFood(food) {
    this.hass.callService("select", "select_option", { entity_id: "select.thirdreality_smart_scale_food_preset", option: food });
  }

  _renderTodayMeals() {
    if (!this._historyData || this._historyData.length === 0) return "";

    const todayStr = new Date().toISOString().split("T")[0];
    const today = this._historyData.find(d => d.date === todayStr);

    if (!today || !today.meals || today.meals.length === 0) return "";

    return html`
      <div class="section">
        <h3 class="section-title">Today's Meals</h3>
        ${today.meals.map((meal) => html`
          <div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid var(--divider-color, #f0f0f0)">
            <span style="font-size:13px;font-weight:500;color:var(--primary-text-color);min-width:45px">${meal.time}</span>
            <span style="flex:1"></span>
            <span style="font-size:13px;font-weight:600;color:var(--primary-color)">${meal.cal} kcal</span>
          </div>
        `)}
      </div>
    `;
  }

  _renderMiniHistory(dailyTarget) {
    const todayCal = parseFloat(this._getState("number.thirdreality_smart_scale_today_calories")) || 0;
    const today = new Date();
    const todayStr = today.toISOString().split("T")[0];

    // Build a map of date -> total from history (via WebSocket data)
    const historyMap = {};
    if (this._historyData) {
      for (const d of this._historyData) historyMap[d.date] = d.total;
    }
    // Use the higher of today_calories or history total for today
    const historyToday = historyMap[todayStr] || 0;
    historyMap[todayStr] = Math.max(Math.round(todayCal), historyToday);

    // Generate last 7 days (always show 7 slots)
    const slots = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      slots.push({ date: dateStr, total: historyMap[dateStr] || 0 });
    }

    return html`
      <div>
        <div class="mini-history-title">7-Day History</div>
        <div class="mini-history-chart">
          ${slots.map(day => {
            const hasData = day.total > 0;
            const pct = (hasData && dailyTarget > 0) ? Math.min(Math.round((day.total / dailyTarget) * 100), 100) : 0;
            const barColor = !hasData ? "var(--divider-color, #e0e0e0)" : pct >= 100 ? "#f44336" : pct >= 75 ? "#ff9800" : "#4caf50";
            const barHeight = hasData ? Math.max(pct * 0.5, 4) : 4; // empty bars are short gray
            return html`
              <div class="mini-history-col">
                <span class="mini-history-label" style="font-weight:500;${hasData ? '' : 'opacity:0.4'}">${hasData ? day.total : "—"}</span>
                <div class="mini-history-bar-v" style="height:${barHeight}px;background:${barColor}"></div>
                <span class="mini-history-label">${this._formatDateShort(day.date)}</span>
              </div>
            `;
          })}
        </div>
      </div>
    `;
  }

  _formatDateShort(dateStr) {
    try {
      const today = new Date();
      const todayStr = today.toISOString().split("T")[0];
      if (dateStr === todayStr) return "Tod";
      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      if (dateStr === yesterday.toISOString().split("T")[0]) return "Yest";
      const d = new Date(dateStr + "T00:00:00");
      const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
      return days[d.getDay()];
    } catch (e) { return dateStr.slice(-2); }
  }

  _getMotivation(pct) {
    const hour = new Date().getHours();
    if (pct === 0 && hour < 12) return "🌅 Start your day — weigh your breakfast!";
    if (pct === 0) return "📋 No meals tracked yet today";
    if (pct <= 25) return "👍 Off to a good start";
    if (pct <= 50) return "📊 On track — budget your next meal";
    if (pct <= 75) return "⚡ More than halfway! Plan your dinner.";
    if (pct < 100) return "⚠️ Almost at your limit — choose wisely";
    return "✅ Daily target reached!";
  }

  _getStreak() {
    if (!this._historyData || this._historyData.length === 0) return 0;
    const datesWithData = new Set(this._historyData.map(d => d.date));
    // Also count today if today_calories > 0
    const todayCal = parseFloat(this._getState("number.thirdreality_smart_scale_today_calories")) || 0;
    const todayStr = new Date().toISOString().split("T")[0];
    if (todayCal > 0) datesWithData.add(todayStr);

    // Count consecutive days ending today
    let streak = 0;
    const d = new Date();
    for (let i = 0; i < 30; i++) {
      const dateStr = d.toISOString().split("T")[0];
      if (datesWithData.has(dateStr)) {
        streak++;
        d.setDate(d.getDate() - 1);
      } else {
        break;
      }
    }
    return streak;
  }

  _getBestStreak() {
    if (!this._historyData || this._historyData.length === 0) return 0;
    const datesWithData = new Set(this._historyData.map(d => d.date));
    const todayCal = parseFloat(this._getState("number.thirdreality_smart_scale_today_calories")) || 0;
    if (todayCal > 0) datesWithData.add(new Date().toISOString().split("T")[0]);

    // Find all dates sorted, then find longest consecutive run
    const sortedDates = [...datesWithData].sort();
    let best = 0, current = 0;
    for (let i = 0; i < sortedDates.length; i++) {
      if (i === 0) { current = 1; }
      else {
        const prev = new Date(sortedDates[i - 1] + "T00:00:00");
        const curr = new Date(sortedDates[i] + "T00:00:00");
        const diff = (curr - prev) / (1000 * 60 * 60 * 24);
        current = diff === 1 ? current + 1 : 1;
      }
      if (current > best) best = current;
    }
    return best;
  }

  _getWeekAvg() {
    const todayCal = parseFloat(this._getState("number.thirdreality_smart_scale_today_calories")) || 0;
    const todayStr = new Date().toISOString().split("T")[0];

    const historyMap = {};
    if (this._historyData) {
      for (const d of this._historyData) historyMap[d.date] = d.total;
    }
    if (todayCal > 0) historyMap[todayStr] = todayCal;

    // Get last 7 days totals
    const today = new Date();
    let total = 0, count = 0;
    for (let i = 0; i < 7; i++) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split("T")[0];
      if (historyMap[dateStr] && historyMap[dateStr] > 0) {
        total += historyMap[dateStr];
        count++;
      }
    }
    return count > 0 ? Math.round(total / count) : 0;
  }

  _renderHistory() {
    const historyRaw = this._getState("text.thirdreality_smart_scale_calorie_history");
    const dailyTarget = parseFloat(this._getState("number.thirdreality_smart_scale_daily_calorie_target")) || 2000;

    if (!historyRaw) {
      return html`
        <div class="section">
          <div class="history-empty">
            <p style="font-size:32px;margin:0 0 12px">📊</p>
            <p>No calorie history yet.</p>
            <p style="font-size:12px">History is recorded when you finish a meal.</p>
          </div>
        </div>
      `;
    }

    // Parse compact format: date:total:meal1_time=cal,meal2_time=cal|date:total:...
    const days = this._parseHistory(historyRaw);

    if (days.length === 0) {
      return html`
        <div class="section">
          <div class="history-empty">
            <p style="font-size:32px;margin:0 0 12px">📊</p>
            <p>No calorie history yet.</p>
            <p style="font-size:12px">History is recorded when you finish a meal.</p>
          </div>
        </div>
      `;
    }

    return html`
      <div class="section">
        <h3 class="section-title">Calorie History</h3>
        <p class="section-desc">Last ${days.length} day${days.length > 1 ? "s" : ""} of tracked meals</p>
        ${days.map(day => {
          const pct = dailyTarget > 0 ? Math.min(Math.round((day.total / dailyTarget) * 100), 100) : 0;
          const barColor = pct >= 100 ? "#f44336" : pct >= 75 ? "#ff9800" : "#4caf50";
          return html`
            <div class="history-day">
              <div class="history-day-header">
                <span class="history-date">${this._formatDate(day.date)}</span>
                <span class="history-total">${day.total} kcal</span>
              </div>
              <div class="history-bar">
                <div class="history-bar-fill" style="width:${pct}%;background:${barColor}"></div>
              </div>
              ${day.meals.map(meal => html`
                <div class="history-meal">
                  <span class="history-meal-time">${meal.time}</span>
                  <span class="history-meal-cal">${meal.cal} kcal</span>
                </div>
              `)}
            </div>
          `;
        })}
      </div>
    `;
  }

  _parseHistory(raw) {
    // Format: date:total:time=cal=items,time=cal=items|date:total:...
    if (!raw) return [];
    const days = [];
    for (const dayStr of raw.split("|")) {
      const parts = dayStr.split(":");
      if (parts.length < 2) continue;
      const date = parts[0];
      const total = parseInt(parts[1]) || 0;
      const mealsStr = parts.slice(2).join(":");  // rejoin in case time has colon
      const meals = [];
      if (mealsStr) {
        for (const mealStr of mealsStr.split(",")) {
          const eqParts = mealStr.split("=");
          const time = eqParts[0] || "";
          const cal = parseInt(eqParts[1]) || 0;
          const items = eqParts.slice(2).join("=") || "";  // rejoin remaining as items
          if (time && cal) {
            meals.push({ time, cal, items });
          }
        }
      }
      days.push({ date, total, meals });
    }
    return days;
  }

  _formatDate(dateStr) {
    // Convert 2026-08-18 to "Aug 18" or "Today"
    try {
      const today = new Date();
      const todayStr = today.toISOString().split("T")[0];
      if (dateStr === todayStr) return "Today";

      const yesterday = new Date(today);
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split("T")[0];
      if (dateStr === yesterdayStr) return "Yesterday";

      const d = new Date(dateStr + "T00:00:00");
      const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
      return `${months[d.getMonth()]} ${d.getDate()}`;
    } catch (e) {
      return dateStr;
    }
  }

  // ═══════════════════════════════════════
  // RECIPES (Cocktail management)
  // ═══════════════════════════════════════
  _renderRecipes() {
    return html`
      <div class="section">
        <h3 class="section-title">Add Recipe</h3>
        <p class="section-desc">Add a cocktail recipe. Format ingredients as: ingredient:weight,ingredient:weight</p>
        <input class="form-input" id="new-cocktail-name" placeholder="Cocktail name (e.g. Margarita)" style="margin-bottom:12px" />
        <input class="form-input" id="new-cocktail-ing" placeholder="Tequila:50,Triple Sec:30,Lime Juice:25" />
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._addCocktailItem}>Add Recipe</button>
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">Remove Recipe</h3>
        <div class="form-row">
          <input class="form-input" id="remove-cocktail-name" placeholder="Cocktail name to remove" />
          <button class="btn btn-danger" @click=${this._removeCocktailItem}>Remove</button>
        </div>
      </div>
    `;
  }

  // ═══════════════════════════════════════
  // FOODS (Food database management)
  // ═══════════════════════════════════════
  _renderFoods() {
    const weightSensor = this._getState("sensor.thirdreality_smart_scale_weight");
    return html`
      <div class="section">
        <h3 class="section-title">Add Food</h3>
        <p class="section-desc">Add a food item to the calorie preset list.</p>
        <div style="display:flex;gap:8px">
          <input class="form-input" id="new-food-name" placeholder="Food name (e.g. Chicken Wings)" style="flex:2" />
          <input class="form-input" id="new-food-cal" type="number" placeholder="Cal/100g" style="flex:1" />
        </div>
        <div class="btn-group">
          <button class="btn btn-filled" @click=${this._addFoodItem}>Add Food</button>
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">Remove Food</h3>
        <div class="form-row">
          <input class="form-input" id="remove-food-name" placeholder="Food name to remove" />
          <button class="btn btn-danger" @click=${this._removeFoodItem}>Remove</button>
        </div>
      </div>

    `;
  }

  // ═══════════════════════════════════════
  // HELPERS
  // ═══════════════════════════════════════
  _getState(eid) {
    if (!this.hass?.states?.[eid]) return "";
    const s = this.hass.states[eid].state;
    return (s === "unknown" || s === "unavailable") ? "" : s;
  }
  _getOptions(eid) {
    return this.hass?.states?.[eid]?.attributes?.options || [];
  }

  // ═══════════════════════════════════════
  // ACTIONS
  // ═══════════════════════════════════════
  _onCocktailSelect(e) { this.hass.callService("select", "select_option", { entity_id: "select.thirdreality_smart_scale_select_cocktail", option: e.target.value }); }
  _onCustomRecipeChange(e) { this.hass.callService("text", "set_value", { entity_id: "text.thirdreality_smart_scale_custom_recipe", value: e.target.value }); }
  _startCocktail() { this.hass.callService("button", "press", { entity_id: "button.thirdreality_smart_scale_start_cocktail" }); }
  _doneCocktail() { this.hass.callService("button", "press", { entity_id: "button.thirdreality_smart_scale_done" }); }
  _backToIdle() { this.hass.callService("select", "select_option", { entity_id: "select.thirdreality_smart_scale_cocktail_step", option: "idle" }); }
  _onFoodSearchInput(e) { this._foodSearch = e.target.value; }
  _filterFood(options) {
    if (!this._foodSearch) return options;
    const q = this._foodSearch.toLowerCase();
    return options.filter(o => o.toLowerCase().includes(q));
  }
  _selectFoodFromSearch(food) {
    this._foodSearch = null; // close dropdown
    this.hass.callService("select", "select_option", { entity_id: "select.thirdreality_smart_scale_food_preset", option: food });
  }
  _onFoodSelect(e) { this.hass.callService("select", "select_option", { entity_id: "select.thirdreality_smart_scale_food_preset", option: e.target.value }); }
  _onCustomFoodNameChange(e) { this.hass.callService("text", "set_value", { entity_id: "text.thirdreality_smart_scale_custom_food_name", value: e.target.value }); }
  _onCustomCalChange(e) { this.hass.callService("number", "set_value", { entity_id: "number.thirdreality_smart_scale_custom_cal_per_100g", value: parseFloat(e.target.value) || 0 }); }
  _addFood() { this.hass.callService("button", "press", { entity_id: "button.thirdreality_smart_scale_add_food" }); }
  _undoAdd() { this.hass.callService("button", "press", { entity_id: "button.thirdreality_smart_scale_undo_add" }); }
  _finishMealConfirm() {
    this._confirmFinish = true;
    setTimeout(() => { this._confirmFinish = false; this.requestUpdate(); }, 3000);
  }
  _confirmFinishAction() {
    this._confirmFinish = false;
    this.hass.callService("button", "press", { entity_id: "button.thirdreality_smart_scale_finish_meal" });
    // Refresh history after finishing meal (delay to let backend save)
    setTimeout(() => this._loadHistory(), 2000);
  }
  _resetToday() {
    // First tap: show confirmation state
    this._confirmReset = true;
    // Auto-cancel after 3 seconds
    setTimeout(() => { this._confirmReset = false; }, 3000);
  }
  _confirmResetAction() {
    this._confirmReset = false;
    this.hass.callService("button", "press", { entity_id: "button.thirdreality_smart_scale_reset_today" });
  }
  _onDailyTargetChange(e) { this.hass.callService("number", "set_value", { entity_id: "number.thirdreality_smart_scale_daily_calorie_target", value: parseFloat(e.target.value) || 2000 }); }
  _onMealWarningChange(e) { this.hass.callService("number", "set_value", { entity_id: "number.thirdreality_smart_scale_meal_calorie_warning", value: parseFloat(e.target.value) || 800 }); }

  _addFoodItem() {
    const name = this.renderRoot.querySelector("#new-food-name")?.value?.trim();
    const cal = parseFloat(this.renderRoot.querySelector("#new-food-cal")?.value) || 0;
    if (!name || cal <= 0) return;
    this.hass.callService("thirdreality_scale", "add_food", { name, calories_per_100g: cal });
    this.renderRoot.querySelector("#new-food-name").value = "";
    this.renderRoot.querySelector("#new-food-cal").value = "";
  }

  _addCocktailItem() {
    const name = this.renderRoot.querySelector("#new-cocktail-name")?.value?.trim();
    const ing = this.renderRoot.querySelector("#new-cocktail-ing")?.value?.trim();
    if (!name || !ing) return;
    this.hass.callService("thirdreality_scale", "add_cocktail", { name, ingredients: ing });
    this.renderRoot.querySelector("#new-cocktail-name").value = "";
    this.renderRoot.querySelector("#new-cocktail-ing").value = "";
  }

  _removeFoodItem() {
    const name = this.renderRoot.querySelector("#remove-food-name")?.value?.trim();
    if (!name) return;
    this.hass.callService("thirdreality_scale", "remove_food", { name });
    this.renderRoot.querySelector("#remove-food-name").value = "";
  }

  _removeCocktailItem() {
    const name = this.renderRoot.querySelector("#remove-cocktail-name")?.value?.trim();
    if (!name) return;
    this.hass.callService("thirdreality_scale", "remove_cocktail", { name });
    this.renderRoot.querySelector("#remove-cocktail-name").value = "";
  }
}

customElements.define("thirdreality-scale-panel", ThirdRealityScalePanel);
