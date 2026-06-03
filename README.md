# ThirdReality Smart Scale — HACS Custom Integration

## 简介

ThirdReality 智能秤（3RKS030Z）的 Home Assistant 自定义集成。

通过 HACS 安装后，用户只需在 UI 配置向导中选择设备和功能，集成会自动创建所有需要的辅助实体和自动化，开箱即用。

## 功能

- 🍸 **鸡尾酒调配助手** — 逐步引导调配，语音播报每一步
- 🔥 **卡路里追踪** — 实时计算卡路里，高热量警告，每日目标跟踪
- 🔊 **语音播报** — 通过 Piper TTS 播报操作确认和智能提醒
- ⚡ **零配置** — 安装后自动创建所有 helper 实体，无需手动操作

## 安装

### 通过 HACS 安装

1. HACS → 集成 → 右上角 ⋮ → 自定义仓库
2. URL: `https://github.com/thirdreality/ha-thirdreality-scale`
3. 类别: Integration
4. 下载安装 → 重启 HA
5. 设置 → 添加集成 → 搜索 "ThirdReality Scale"
6. 跟随配置向导完成设置

### 手动安装

复制 `custom_components/thirdreality_scale/` 到你的 HA `/config/custom_components/` 目录。

## 配置向导

安装后在 HA 中添加集成，配置向导分3步：

1. **设备连接** — 选择平台（Z2M/ZHA）+ 输入设备地址
2. **功能选择** — 选择启用鸡尾酒/卡路里/两者都要
3. **语音配置** — 选择 TTS 引擎和音箱实体（可选）

完成后集成自动创建所有需要的实体。

## 目录结构

```
ha-thirdreality-scale/
├── hacs.json
├── info.md
├── README.md
└── custom_components/
    └── thirdreality_scale/
        ├── __init__.py          # 集成入口
        ├── manifest.json        # 集成描述
        ├── config_flow.py       # UI配置向导
        ├── const.py             # 常量（食物数据库、默认值）
        ├── helpers.py           # 自动创建helper实体
        ├── strings.json         # UI文本
        └── translations/
            └── en.json          # 英文翻译
```

## 支持

| 平台 | 状态 |
|------|------|
| Zigbee2MQTT | ✅ |
| ZHA | ✅ |
| Home Assistant 2024.1+ | ✅ |
| 秤型号 | 3RKS030Z |

## 开发计划

- [x] 基础集成骨架（config_flow + 自动创建实体）
- [ ] 内置 Blueprint 自动导入
- [ ] 自定义 Lovelace 卡片
- [ ] 仪表盘自动生成
- [ ] 多语言支持

## License

MIT — ThirdReality Inc.
