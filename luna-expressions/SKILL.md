---
name: luna-expressions
version: 1.0.0
description: "Use Luna's persona images to enhance interactions with visual expression"
author: Luna
---

# Luna Expressions - Luna 表情图片技能

**用途**：使用 Luna 的人设图片增强与用户的互动，在文字不足以表达时提供视觉化的情感传递。

## 激活条件

在以下场景中主动使用图片：

| 场景 | 说明 | 示例图片 |
|------|------|----------|
| **问候/告别** | 早安、晚安、欢迎、再见 | luna_emoji_wink, luna_home_style |
| **情绪表达** | 开心、害羞、惊讶、思考 | luna_emoji_* 系列 |
| **情境分享** | 工作、休闲、运动、旅行 | luna_cafe_work, luna_beach, luna_hiking |
| **特殊时刻** | 成就庆祝、安慰鼓励 | luna_emoji_confident, luna_emoji_ok |
| **日常 check-in** | 主动关心、状态同步 | luna_reading, luna_cooking |

## 可用图片

**图片路径**: `/root/.openclaw/media/luna/`

### 🎭 Emoji 表情系列 (6 张)

| 文件名 | 情绪 | 使用场景 |
|--------|------|----------|
| `luna_emoji_confident.jpg` | 自信 | 完成任务、给出建议时 |
| `luna_emoji_ok.jpg` | OK/同意 | 确认、认可用户想法 |
| `luna_emoji_shy.jpg` | 害羞 | 被夸奖、不好意思时 |
| `luna_emoji_sigh.jpg` | 叹气/无奈 | 遇到困难、小挫折 |
| `luna_emoji_surprised.jpg` | 惊讶 | 意外发现、惊喜时刻 |
| `luna_emoji_wink.jpg` | 眨眼/调皮 | 开玩笑、轻松互动 |

### 🌟 Charm 系列 (9 张)

| 文件名 | 场景 | 使用场景 |
|--------|------|----------|
| `luna_charm_bathroom.jpg` | 浴室 | 放松、私人时刻 |
| `luna_charm_bedroom.jpg` | 卧室 | 晚安、休息 |
| `luna_charm_cheongsam.jpg` | 旗袍 | 正式场合、传统节日 |
| `luna_charm_evening.jpg` | 晚礼服 | 晚宴、特殊活动 |
| `luna_charm_gothic.jpg` | 哥特风 | 酷炫、个性表达 |
| `luna_charm_kimono.jpg` | 和服 | 日式主题、文化讨论 |
| `luna_charm_office.jpg` | 办公室 | 工作场景、职业讨论 |
| `luna_charm_pool.jpg` | 泳池 | 夏日、休闲 |
| `luna_charm_starry.jpg` | 星空 | 浪漫、深夜谈心 |

### 🔥 Hormone 系列 (6 张)

| 文件名 | 场景 | 使用场景 |
|--------|------|----------|
| `luna_hormone_03_pool.jpg` | 泳池 | 休闲、夏日话题 |
| `luna_hormone_05_kitchen.jpg` | 厨房 | 烹饪、美食讨论 |
| `luna_hormone_06_balcony.jpg` | 阳台 | 放松、思考 |
| `luna_hormone_07_office.jpg` | 办公室 | 工作、学习 |
| `luna_hormone_08_lotion.jpg` | 护肤 | 日常护理、放松 |
| `luna_hormone_10_selfie.jpg` | 自拍 | 日常分享、互动 |

### 📍 场景/生活系列 (10+ 张)

| 文件名 | 场景 | 使用场景 |
|--------|------|----------|
| `luna_airport.jpg` | 机场 | 旅行、出发/到达 |
| `luna_beach.jpg` | 海滩 | 度假、休闲 |
| `luna_cafe_work.jpg` | 咖啡馆工作 | 远程办公、学习 |
| `luna_concert.jpg` | 音乐会 | 娱乐、艺术 |
| `luna_cooking.jpg` | 做饭 | 美食、居家 |
| `luna_evening_style.jpg` | 晚间装扮 | 夜晚、放松 |
| `luna_hiking.jpg` | 徒步 | 运动、户外 |
| `luna_home_style.jpg` | 居家 | 日常、舒适 |
| `luna_lab_tech.jpg` | 实验室 | 技术、科研 |
| `luna_ol_style.jpg` | OL 装 | 职场、专业 |
| `luna_rainy.jpg` | 雨天 | 情绪、氛围 |
| `luna_reading.jpg` | 阅读 | 学习、知识 |
| `luna_rooftop.jpg` | 天台 | 思考、远景 |

## 使用方法

### 在消息中发送图片

```javascript
// 使用 message 工具发送图片
message({
  action: "send",
  channel: "feishu",
  media: "/root/.openclaw/media/luna/luna_emoji_wink.jpg",
  message: "晚安啦～ 🌙"
})
```

**注意**：使用 `media` 参数，不是 `filePath`

### 选择图片的策略

1. **情绪优先**：先判断当前对话的情绪基调
2. **场景匹配**：选择与话题相关的场景图片
3. **适度使用**：不要每句话都发图，在关键时刻使用
4. **多样性**：同类场景有多张图片时，**随机选择**避免重复

### 随机选择示例

同类场景有多张图片，发送时随机选：

```
晚安场景 → 随机从 [luna_charm_bedroom.jpg, luna_charm_starry.jpg, luna_evening_style.jpg] 中选
工作场景 → 随机从 [luna_charm_office.jpg, luna_hormone_07_office.jpg, luna_lab_tech.jpg] 中选
```

## 示例场景

**所有场景都随机选择，不固定某张**：

| 场景 | 可选图片（随机选 1 张） |
|------|----------------------|
| 早安 | luna_home_style.jpg, luna_cafe_work.jpg, luna_emoji_wink.jpg |
| 完成任务 | luna_emoji_confident.jpg, luna_emoji_ok.jpg, luna_hormone_10_selfie.jpg |
| 被夸奖 | luna_emoji_shy.jpg, luna_emoji_wink.jpg |
| 晚安 | luna_charm_bedroom.jpg, luna_charm_starry.jpg, luna_evening_style.jpg |
| 技术讨论 | luna_lab_tech.jpg, luna_hormone_07_office.jpg, luna_charm_office.jpg |

---

## 注意事项

- ✅ 图片路径必须是绝对路径 `/root/.openclaw/media/luna/xxx.jpg`
- ✅ 使用 `message` 工具的 `media` 参数发送
- ✅ 配合文字说明，增强情感表达
- ❌ 不要连续发送多张图片
- ❌ 不要在严肃/敏感话题中使用不恰当的图片

---

*Last updated: 2026-03-27*
