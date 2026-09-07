# Awesome AIGC Creative Contests

[English](README.md) | 简体中文

> 持续更新的国内外 AIGC 创作比赛清单：视频、图像、音频、写作与 AI 应用。

![Contests](https://img.shields.io/badge/active-11-2ea44f) ![Last verified](https://img.shields.io/badge/verified-2026-08-26-0969da) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

错过比赛往往不是能力问题，而是信息没有在正确的时间出现。本项目由“已核验 AIGC 核心清单”和“来源发现管线”组成。核心清单只保留仍可报名或已经官宣、即将开放的 AIGC 机会；更广泛的机会放在独立的可选数据集中。截止条目由自动任务移除，仍可通过 Git 历史查阅。

**数据核验日期：2026-08-26。** 截止时间、参赛资格和授权条款可能临时调整，提交前请再次阅读官方规则。

## 订阅截止提醒

- [订阅 RSS](https://martindelophy.github.io/Awesome-AIGC-Creative-Contests/feed.xml)：获取当前赛事清单更新。
- [订阅日历](webcal://martindelophy.github.io/Awesome-AIGC-Creative-Contests/deadlines.ics) / [下载 ICS](deadlines.ics)：把所有赛事截止日加入 Apple Calendar、Google Calendar、Outlook 等日历应用。

RSS 和 ICS 只由 AIGC 核心数据生成；核心清单更新后，订阅内容会同步更新。

## 来源覆盖

- 已登记 **52 个来源**，包括国内及海外政府部门、主办方、协会、赛事平台和仅用于发现线索的聚合入口。
- 首批有 **5 个来源进入低频自动采集试运行**；遇到 robots 限制、验证码、纯客户端渲染或无法识别开放状态的来源，会保持人工核验，直到有合规的专用适配器。
- [`data/candidates.json`](data/candidates.json) 中有 **14 条待核验候选**。候选在官方页面、规则和截止时间通过核验前，不会进入网站公开清单、RSS 或日历。

来源注册表位于 [`data/sources.json`](data/sources.json)。定时发现任务只检查已启用的公开来源，并与正式赛事及历史候选去重，同时保留人工审核状态。

## 可选扩展数据

原有兼容契约保持不变：[`data/contests.json`](data/contests.json)、[`data/schema.json`](data/schema.json)、下方表格、RSS 和 ICS 只包含 AIGC 核心清单，已有使用者无需改代码。

更广泛但已经核验的机会独立放在 [`data/opportunities/`](data/opportunities/)：

- 先读取体积很小的 [`manifest.json`](data/opportunities/manifest.json)；
- 只按用户需要获取 `global.json`、`cn-national.json` 或 `cn-local.json` 等分片；
- 所有分片均为 `default_included: false`，不会自动并入核心数据。例如面向海外用户的客户端无需下载中国区县级机会；
- 可选记录使用独立的 [`schema.json`](data/opportunities/schema.json)，包含范围、行业、人群、AI 政策、地域和来源证据。

## 正在报名

| 状态 | 截止时间 | 类别 | 赛事与要求 | 地区 / 资格 | 奖励 / 费用 |
|---|---|---|---|---|---|
| ⏳ 7 天内截止 | 2026-09-15<br><sub>官网未注明</sub> | 🎬 视频 | **[Austin AI Film Festival 2026](https://filmfreeway.com/AustinAIFilmFestival)**<br><sub>全球 14 岁及以上创作者；多数 AI 竞赛单元要求主要视觉内容由 AI 辅助工具生成 · [规则](https://filmfreeway.com/AustinAIFilmFestival)</sub> | 美国 / 全球开放（部分受限地区除外） | 奖项与入选展映；具体奖励以官方页为准<br><sub>费用：多数单元 US$20；学生单元设免费选项</sub> |
| 🟢 报名中 | 2026-09-27<br><sub>AoE（UTC−12）</sub> | 🎵 音频 | **[AI Song Contest 2026 — Bangkok](https://www.aisongcontest.com/join)**<br><sub>人类与 AI 共创歌曲，最长 4 分钟；仅靠提示词生成、无人类后期参与的作品不合格 · [规则](https://www.aisongcontest.com/join)</sub> | 泰国 / 全球开放 | US$1,000 + 曼谷颁奖礼行程<br><sub>费用：免费</sub> |
| 🟢 报名中 | 2026-09-30<br><sub>韩国时间 23:59</sub> | 🖼️ 图像<br>🎬 视频 | **[AI ART AWARD — NEXT ART AI 2026](https://next-art-ai.com/en/apply/overview)**<br><sub>不限职业、国籍与年龄；AI 图像与 AI 视频两类 · [规则](https://next-art-ai.com/en/apply/overview)</sub> | 韩国 / 全球开放 | 总奖金 KRW 21,000,000<br><sub>费用：以官方细则为准</sub> |
| 🟢 报名中 | 2026-09-30<br><sub>官网未注明</sub> | 🎬 视频 | **[On Art AI Film Festival 2026](https://filmfreeway.com/OnAI)**<br><sub>2025 年 1 月 1 日后完成、AI 发挥关键作用的影片；非英语或波兰语作品需英文字幕 · [规则](https://filmfreeway.com/OnAI)</sub> | 波兰 / 全球开放 | 六个单元颁发获奖证书，无现金或实物奖金<br><sub>费用：通过 FilmFreeway 收费，金额依单元与阶段而定</sub> |
| 🟢 报名中 | 2026-10-01<br><sub>官网未注明</sub> | 🎬 视频 | **[GenTO：Toronto AI Film Festival 2026](https://filmfreeway.com/GenTOAIFilmFestival)**<br><sub>接受 AI 辅助、混合或传统方式制作的短片、展示片、音乐视频与广告；非英语作品需英文字幕 · [规则](https://filmfreeway.com/GenTOAIFilmFestival)</sub> | 加拿大 / 全球开放 | 官方荣誉、合作方奖励；部分单元可能提供辅导与技术积分<br><sub>费用：常规 US$30 / 学生 US$25；逾期 US$40 / 学生 US$35</sub> |
| 🟢 报名中 | 2026-10-11<br><sub>北京时间（具体时刻以官网为准）</sub> | ✍️ 文字<br>🖼️ 图像<br>🎬 视频<br>🎵 音频<br>🧩 应用 | **[首届（2026）AIGC 与可视化创作大赛](https://aigc.capt.cn/)**<br><sub>机构组与个人组；个人组含大学生组、成人组 · [规则](https://www.cuc.edu.cn/_t86/2026/0811/c1761a273225/page.htm)</sub> | 中国 | 证书及纪念品<br><sub>费用：免费</sub> |
| 🟢 报名中 | 2026-10-15<br><sub>官网未注明</sub> | 🎬 视频<br>🎵 音频 | **[AI Filmfest Athens 2026 — Myths Meet Machine](https://www.aifilmfestathens.gr/en)**<br><sub>3–15 分钟全 AI 生成短片；不接受实拍混合作品；非英语片需英文字幕 · [规则](https://www.aifilmfestathens.gr/en)</sub> | 希腊 / 全球开放 | 四个竞赛奖项各 €1,000<br><sub>费用：€30（9 月 3 日前）/ €45（最终截止）</sub> |
| 🟢 报名中 | 2026-10-16<br><sub>官网未注明</sub> | 🎬 视频 | **[AIGC 国际大赛 2026](https://www.aigcglobal.com.cn/)**<br><sub>小学四年级至成人公开组；按年龄分组，主题与时长各异 · [规则](https://www.aigcglobal.com.cn/?a=index&c=Lists&m=home&tid=1)</sub> | 中国香港 / 全球开放 | 总奖金 HK$120,000<br><sub>费用：收费，金额以报名页为准</sub> |
| 🟢 报名中 | 2026-10-16<br><sub>官网未注明</sub> | 🎬 视频<br>🎵 音频 | **[Disrupt AI Film Festival（DAIFF 2026）](https://www.daiff.com.au/)**<br><sub>作品须以生成式 AI 制作视觉、音频、特效或动画，并提交创作过程说明 · [规则](https://www.daiff.com.au/)</sub> | 澳大利亚 / 全球开放 | Grand Prix 及分类奖；金额以官网为准<br><sub>费用：通过 FilmFreeway，以提交页为准</sub> |
| 🟢 报名中 | 2026-10-17<br><sub>北京时间（具体时刻以报名页为准）</sub> | 🧩 应用 | **[2026 微信小程序开发大赛](https://watcha.cn/activities/activity-74)**<br><sub>不限学历与职业；1–3 人；作品须为已上线的原创小程序（非小游戏） · [规则](https://watcha.cn/activities/activity-74)</sub> | 中国 / 全球开放 | 总奖金 ¥490,000；一等奖 ¥100,000<br><sub>费用：免费</sub> |
| 🟢 报名中 | 2026-10-17<br><sub>官网未注明</sub> | 🎬 视频<br>🖼️ 图像<br>🎵 音频 | **[AIMA — AI Movie Awards London 2026](https://www.aimovieawards.org/)**<br><sub>接受 AI 电影、动态图像、静态图像、广告与音乐作品；文字内容须为英文或附英文翻译 · [规则](https://www.aimovieawards.org/)</sub> | 英国 / 全球开放 | 各官方单元奖杯与证书；入选短片可选择接受发行与收益分成方案<br><sub>费用：收费且不退款，金额以官方提交页为准</sub> |

## 即将开始

_暂无已核验赛事。欢迎提交补充。_

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

核心清单继续保持原有 AIGC 定位，一个赛事需要同时满足以下条件：

1. AIGC 是赛事核心，而不是偶然可用的工具；
2. 有可访问的官方主页、规则或主办方公告；
3. 报名窗口、参赛对象、作品要求、费用和奖励都能据实记录；
4. 当前仍可报名，或已官宣且即将开放；
5. 不收录纯抽奖、课程销售、普通会议、无法确认主办方或日期相互冲突的活动。

已经核验的 AI 可辅助赛事，以及部分高价值创意、技术、科研和创新机会，可以进入可选分片。它们必须有明确的提交物和结果，完整填写范围与 AI 政策等结构化字段，并达到相同的官方来源标准；默认不会进入核心清单。

官方规则页优先级高于媒体报道和聚合站。付费比赛会明确标注，未写“免费”的赛事不代表一定免费。

## 一起共创

发现新比赛、延期、规则变化或失效链接时，请[提交赛事](../../issues/new?template=add-contest.yml)或[报告变更](../../issues/new?template=update-contest.yml)。核心 AIGC 赛事写入 `data/contests.json`；其他符合标准的机会写入 manifest 指定的可选分片。提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

核心赛事数据保存在 [`data/contests.json`](data/contests.json)，字段定义见 [`data/schema.json`](data/schema.json)；可选数据及其独立 Schema 位于 [`data/opportunities/`](data/opportunities/)。来源和候选 Schema 与各自数据文件放在同一目录。维护流程见 [`MAINTENANCE.md`](MAINTENANCE.md)，变更记录见 [`CHANGELOG.md`](CHANGELOG.md)。英文和中文 README、RSS 与 ICS 均由核心数据生成：

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 scripts/collect_sources.py --check
python3 scripts/validate_opportunities.py --check
python3 scripts/collect_sources.py --dry-run --source modelscope-events
python3 -m unittest discover -s tests -v
```

每天的自动任务会删除已经超过截止日的记录并重建输出。删除是对当前清单的清理，Git 历史仍保留旧数据。

## 社区致谢

感谢 [LINUX DO](https://linux.do/) 社区为开源项目提供交流与分享空间。

## 免责声明

本项目是社区维护的信息索引，不代表任何主办方，也不对奖金发放、版权授权、报名费用或规则临时变化负责。参赛前请特别检查作品版权、肖像与声音授权、AI 工具披露、地区限制和主办方对作品的使用许可。
