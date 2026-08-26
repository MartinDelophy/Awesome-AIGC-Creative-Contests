# Awesome AIGC Creative Contests

[English](README.en.md) | 简体中文

> 持续更新的国内外 AIGC 创作比赛清单：视频、图像、音频、写作与 AI 应用。

![Contests](https://img.shields.io/badge/active-{{COUNT}}-2ea44f) ![Last verified](https://img.shields.io/badge/verified-{{UPDATED_AT}}-0969da) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

错过比赛往往不是能力问题，而是信息没有在正确的时间出现。这个项目只保留仍可报名或已经官宣、即将开放的 AIGC 创作赛事；截止条目由自动任务从清单中移除，仍可通过 Git 历史查阅。

**数据核验日期：{{UPDATED_AT}}。** 截止时间、参赛资格和授权条款可能临时调整，提交前请再次阅读官方规则。

## 订阅截止提醒

- [订阅 RSS](https://raw.githubusercontent.com/MartinDelophy/Awesome-AIGC-Creative-Contests/main/feed.xml)：获取当前赛事清单更新。
- [订阅日历](webcal://raw.githubusercontent.com/MartinDelophy/Awesome-AIGC-Creative-Contests/main/deadlines.ics) / [下载 ICS](deadlines.ics)：把所有赛事截止日加入 Apple Calendar、Google Calendar、Outlook 等日历应用。

RSS 和 ICS 均由赛事数据自动生成；清单更新后，订阅内容会同步更新。

## 正在报名

{{OPEN_TABLE}}

## 即将开始

{{UPCOMING_TABLE}}

## 类别说明

- 🎬 视频 / 电影 / 动画 / 微短剧
- 🖼️ 图像 / 视觉艺术
- 🎵 音频 / 音乐 / 歌曲
- ✍️ 文字 / 剧本 / 数据新闻
- 🧩 应用 / 交互作品 / 小程序

## 长期关注入口

这些入口本身长期有效，不代表往届比赛仍可投稿。

- [芒果灵创赛事中心](https://aigc.mgtv.com/challenges/)：国内 AI 视频、微短剧与动漫创作赛事。
- [ModelScope 活动与竞赛](https://modelscope.cn/events)：国内模型、开发与 AIGC 创作活动。
- [Runway AI Festival](https://aif.runwayml.com/)：覆盖电影、设计、广告、时尚、游戏和新媒体的年度赛事。
- [Reply AI Film Festival](https://challenges.reply.com/challenges/creative/aifilmfestival/home/)：面向全球 AI 电影创作者的年度电影节。
- [World AI Film Festival](https://worldaifilmfestival.com/)：以生成式 AI 电影为核心的国际赛事。
- [AI Film Contests](https://aifilmcontests.com/)：第三方 AI 电影赛事日历；发现赛事后仍需回到官网核验。
- [AI Music Events Deadlines](https://aimusic.events/deadlines)：第三方 AI 音乐机会日历；报名条件以主办方为准。

## 收录标准

一个赛事需要同时满足以下条件：

1. AIGC 是作品创作或评审的核心，而不是只在宣传文案中提到 AI；
2. 有可访问的官方主页、规则或主办方公告；
3. 能核验报名窗口、参赛对象与作品要求；
4. 当前仍可报名，或已官宣且即将开放；
5. 不收录纯抽奖、课程销售、无法确认主办方或日期相互冲突的活动。

官方规则页优先级高于媒体报道和聚合站。付费比赛会明确标注，未写“免费”的赛事不代表一定免费。

## 一起共创

发现新比赛、延期、规则变化或失效链接时，请[提交赛事](../../issues/new?template=add-contest.yml)或[报告变更](../../issues/new?template=update-contest.yml)。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

赛事数据保存在 [`data/contests.json`](data/contests.json)，字段定义见 [`data/schema.json`](data/schema.json)，维护流程见 [`MAINTENANCE.md`](MAINTENANCE.md)，变更记录见 [`CHANGELOG.md`](CHANGELOG.md)。README、RSS 和 ICS 由脚本生成：

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
```

每天的自动任务会删除已经超过截止日的记录并重建 README。删除是对当前清单的清理，Git 历史仍保留旧数据。

## 免责声明

本项目是社区维护的信息索引，不代表任何主办方，也不对奖金发放、版权授权、报名费用或规则临时变化负责。参赛前请特别检查作品版权、肖像与声音授权、AI 工具披露、地区限制和主办方对作品的使用许可。
