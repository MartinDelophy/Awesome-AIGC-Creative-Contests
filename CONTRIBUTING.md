# 共创指南

[English contribution guide](README.md#contributing) | 简体中文

感谢你一起维护这份不会悄悄过期的 AIGC 比赛清单。

## 提交新赛事

优先使用 GitHub 的“提交赛事”Issue 表单。若直接提交 Pull Request，请在 `data/contests.json` 增加记录，不要手工编辑 `README.md`。

每条记录必须包含：

- 唯一、稳定的英文 `id`；
- 赛事名称、地区、类别与主办方；
- `YYYY-MM-DD` 格式的开放日、截止日和核验日；
- 时区或“官网未注明”；
- 参赛资格、费用和奖励；
- 官方活动页与规则页，且必须是 HTTPS 链接。
- `en` 对象中的英文赛事名、地区、主办方、时区、资格、费用和奖励。

可用类别只有 `video`、`image`、`audio`、`text`、`app`。

完整字段定义和约束见 [`data/schema.json`](data/schema.json)。生成脚本还会检查未知字段、重复类别、空文本、日期顺序和 URL 格式。

## 信息源优先级

1. 官方规则、主办方公告；
2. 官方活动页或报名页；
3. 主办方认证社交账号；
4. 媒体报道；
5. 聚合站与社区转发。

如果不同来源的截止日期冲突，请先向主办方核实，不要猜测。没有官方入口、主办方身份不清或主要目的是售卖课程的活动不会收录。

## 报告延期、截止或失效

请使用“报告变更”Issue 表单，并附上能证明变更的官方链接。维护者确认后更新日期或删除记录。每日自动任务也会在截止日结束后移除条目。

## 本地检查

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 -m unittest discover -s tests -v
```

如果修改了企业微信摘要脚本，请额外运行以下命令预览完整消息。该命令不需要配置 webhook，也不会真正发送通知：

```bash
python3 scripts/send_wecom.py --dry-run
```

提交 PR 时，请一并提交更新后的 `README.md`、`README.zh-CN.md`、`feed.xml` 和 `deadlines.ics`。维护者的复核与发布流程见 [`MAINTENANCE.md`](MAINTENANCE.md)。
