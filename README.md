# 🍸🔥 ThirdReality Smart Scale - Home Assistant 集成

[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/thirdreality/ha-thirdreality-scale)](https://github.com/thirdreality/ha-thirdreality-scale/releases)
[![License: MIT](https://img.shields.io/github/license/thirdreality/ha-thirdreality-scale)](LICENSE)

> 让你的 ThirdReality 智能秤变成厨房助手 —— 鸡尾酒调制 + 卡路里追踪，支持语音播报！

---

## ✨ 功能特色

### 🍸 鸡尾酒调制助手
- 分步引导你按配方称量每种配料
- 达到目标重量自动跳转下一步
- 预设 12 种鸡尾酒配方，支持自定义配方
- 语音播报每一步操作提示

### 🔥 卡路里追踪器
- 预设 ~50 种常见食物（每100g 卡路里值）
- 实时显示当前食物的卡路里
- 自动累计每餐和每日总量
- 超标语音警告
- 支持自定义食物名称和卡路里值

### 🔊 智能语音播报
- 添加食物时确认播报（食物名、重量、卡路里）
- 高热量食物警告（>400 cal/100g）
- 单餐超标提醒
- 每日总量超标提醒
- 鸡尾酒每步操作引导

### 🎯 一键安装，零配置
- 安装后自动创建仪表盘（Calories + Cocktail）
- 自动创建蓝图和自动化脚本
- 无需手动创建任何 Helper 实体
- 支持 Zigbee2MQTT 和 ZHA 双平台

---

## 📸 界面预览

<!-- 在这里添加你的截图 -->
<!-- ![卡路里仪表盘](docs/images/calorie_dashboard.png) -->
<!-- ![鸡尾酒仪表盘](docs/images/cocktail_dashboard.png) -->

---

## 📋 前置要求

- Home Assistant 2024.1.0 或更高版本
- [HACS](https://hacs.xyz/) 已安装
- ThirdReality 智能秤已接入 HA（通过 Zigbee2MQTT 或 ZHA）
- （可选）支持 TTS 的音箱用于语音播报

---

## 🚀 安装方法

### 方式一：通过 HACS 安装（推荐）

1. 打开 HACS → 集成
2. 点击右上角 `⋮` → 自定义存储库
3. 输入 `https://github.com/thirdreality/ha-thirdreality-scale`
4. 类别选择 `集成`
5. 点击添加 → 搜索 "ThirdReality Smart Scale" → 下载
6. 重启 Home Assistant

### 方式二：手动安装

1. 下载 [最新 Release](https://github.com/thirdreality/ha-thirdreality-scale/releases)
2. 解压后将 `custom_components/thirdreality_scale` 文件夹复制到你 HA 的 `custom_components/` 目录
3. 重启 Home Assistant

---

## ⚙️ 配置步骤

1. **设置 → 设备与服务 → 添加集成** → 搜索 "ThirdReality"
2. **选择平台**：
   - Zigbee2MQTT：填入设备 Topic（如 `0xaa97282c02b36898`）
   - ZHA：填入 IEEE 地址
3. **选择功能**：勾选 🍸 Cocktail 和/或 🔥 Calorie
4. **语音配置**（可选）：
   - TTS Engine：如 `tts.piper`
   - Speaker：如 `media_player.your_speaker`
5. **完成** → 重启 HA

重启后你会看到：
- 侧边栏出现 **Calories** 和 **Cocktail** 仪表盘
- 自动化列表中出现对应的自动化脚本
- 蓝图页面中出现两个蓝图

---

## 📖 使用说明

### 卡路里追踪

1. 进入 **Calories** 仪表盘
2. 从下拉框选择食物（或输入自定义食物名+卡路里值）
3. 将食物放在秤上 → 实时显示卡路里
4. 点击 **Add ➕** → 添加到当前餐
5. 点击 **Finish Meal ✅** → 累加到今日总量
6. 点击 **Reset 🗑️** → 重置今日数据

### 鸡尾酒调制

1. 进入 **Cocktail** 仪表盘
2. 从下拉框选择鸡尾酒配方
3. 点击 **Start Mixing ▶️**
4. 将杯子放到秤上 → 按 **Done ✅** 开始
5. 按提示逐步添加配料（达到目标重量自动下一步，或手动点 Done）
6. 完成后自动返回选择页

---

## 🍹 自定义鸡尾酒配方

在蓝图配置中可以添加最多 12 种预设配方，格式为：

```
配料名:重量(克),配料名:重量(克),...
```

示例：
```
White Rum:45,Fresh Strawberry Puree:80,Fresh Lemon Juice:20,Simple Syrup:15
```

也可以在仪表盘中选择 "custom" 并实时输入配方。

---

## 🛠️ 高级配置

### 支持的 TTS 引擎

| TTS 引擎 | entity_id 示例 |
|----------|---------------|
| Piper (本地) | `tts.piper` |
| Google Translate | `tts.google_translate_say` |
| Nabu Casa Cloud | `tts.cloud_say` |

### 实体列表

安装后会自动创建以下实体（以 `thirdreality_smart_scale` 为前缀）：

| 类型 | 实体 | 说明 |
|------|------|------|
| button | `add_food` | 添加食物 |
| button | `finish_meal` | 结束当餐 |
| button | `reset_today` | 重置今日 |
| button | `start_cocktail` | 开始调酒 |
| button | `done` | 确认/下一步 |
| number | `meal_calories` | 当餐卡路里 |
| number | `today_calories` | 今日总卡路里 |
| number | `daily_calorie_target` | 每日目标 |
| number | `meal_calorie_warning` | 单餐警告阈值 |
| number | `custom_cal_per_100g` | 自定义卡路里值 |
| text | `calorie_status` | 状态显示 |
| text | `meal_log` | 餐食记录 |
| text | `custom_food_name` | 自定义食物名 |
| text | `cocktail_status` | 鸡尾酒状态 |
| text | `cocktail_recipe_list` | 配料清单 |
| text | `custom_recipe` | 自定义配方 |
| select | `food_preset` | 食物预设 |
| select | `select_cocktail` | 选择鸡尾酒 |
| select | `cocktail_step` | 调酒步骤控制 |

---

## ❓ 常见问题

### 仪表盘没有出现？
重启 HA 后等 1-2 分钟刷新页面。如果仍没有，检查 设置 → 仪表盘 中是否存在。

### 自动化没有创建？
检查 `automations.yaml` 文件中是否有对应条目。可以删除集成重新添加。

### 音箱不说话？
1. 确认 TTS 引擎实体存在（开发者工具 → 状态 → 搜索 "tts"）
2. 确认音箱在线（media_player 状态不是 unavailable）
3. 在开发者工具中手动测试 TTS 是否正常

### 支持哪些秤？
ThirdReality 智能营养秤（Zigbee），需通过 Zigbee2MQTT 或 ZHA 接入 HA。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

- 🐛 [报告 Bug](https://github.com/thirdreality/ha-thirdreality-scale/issues)
- 💡 [功能建议](https://github.com/thirdreality/ha-thirdreality-scale/issues)

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🙏 致谢

- [Home Assistant](https://www.home-assistant.io/)
- [HACS](https://hacs.xyz/)
- [ThirdReality](https://www.3reality.com/)
