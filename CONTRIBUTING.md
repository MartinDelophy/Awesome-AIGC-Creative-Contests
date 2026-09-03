# 共创指南

[English contribution guide](README.md#contributing) | 简体中文

感谢你一起维护这份不会悄悄过期的 AIGC 比赛清单。

## 提交新赛事

优先使用 GitHub 的“提交赛事”Issue 表单。若直接提交 Pull Request，请先判断记录应进入哪一层：

- AIGC 是赛事核心：写入 `data/contests.json`；
- AI 只是允许使用的工具，或属于其他高价值创意、技术、科研与创新机会：写入 `data/opportunities/manifest.json` 指定的可选分片；
- 地方机会只写入对应地区分片，不要并入核心或全球分片。

不要手工编辑 `README.md`、`README.zh-CN.md`、RSS 或 ICS；这些输出只由核心清单生成。

每条记录必须包含：

- 唯一、稳定的英文 `id`；
- 赛事名称、地区、类别与主办方；
- `YYYY-MM-DD` 格式的开放日、截止日和核验日；
- 时区或“官网未注明”；
- 参赛资格、费用和奖励；
- 官方活动页与规则页，且必须是 HTTPS 链接。
- `en` 对象中的英文赛事名、地区、主办方、时区、资格、费用和奖励。

核心清单的字段和作品形式保持不变，可用类别仍为 `video`、`image`、`audio`、`text`、`app`。核心记录不得加入扩展字段，以保证已有数据消费者兼容。

可选分片中的每条记录还必须完整提供 `scope`、机会类型、行业、适用人群、AI 使用政策、举办地以及来源证据；它们使用独立的 [`data/opportunities/schema.json`](data/opportunities/schema.json)。分片列表、地区覆盖和记录数登记在 [`data/opportunities/manifest.json`](data/opportunities/manifest.json)，所有分片的 `default_included` 必须为 `false`。

核心字段定义见 [`data/schema.json`](data/schema.json)。两个校验器会检查未知字段、重复类别、空文本、日期顺序、URL、跨分片重复项、来源引用以及 manifest 记录数。

## 信息源优先级

1. 官方规则、主办方公告；
2. 官方活动页或报名页；
3. 主办方认证社交账号；
4. 媒体报道；
5. 聚合站与社区转发。

聚合站只能用来发现线索，最终记录必须包含主办方或官方规则链接。来源登记在 `data/sources.json`，自动发现的待审链接保存在 `data/candidates.json`，候选不会自动进入公开清单。

## 提交新来源

可以使用“推荐来源”Issue，或修改 `data/sources.json` 提交 PR。来源需要说明覆盖地区、行业、主体类型和可信等级。只有在公开页面允许低频访问、无需绕过登录或验证码，并且解析规则不会混入大量历史内容时，才能设置 `enabled: true`。

新增自动采集规则时必须同时补充 `tests/test_collect_sources.py`，并先运行 dry-run 检查候选质量：

```bash
python3 scripts/collect_sources.py --check
python3 scripts/collect_sources.py --dry-run --source <source-id>
```

## 审核候选

1. 在 `data/candidates.json` 将候选设为 `reviewing`；
2. 找到主办方官方页面与完整规则，核验报名状态、日期、资格、费用、奖励及 AI 政策；
3. 信息完整后，根据上述边界把 AIGC 核心赛事写入 `data/contests.json`，或把更广泛的机会写入对应可选分片；
4. 信息不可靠时设为 `rejected`，通过 `review_notes` 记录原因，防止后续任务重复添加。

如果不同来源的截止日期冲突，请先向主办方核实，不要猜测。没有官方入口、主办方身份不清或主要目的是售卖课程的活动不会收录。

## 报告延期、截止或失效

请使用“报告变更”Issue 表单，并附上能证明变更的官方链接。维护者确认后更新日期或删除记录。每日自动任务也会在截止日结束后移除条目。

## 本地检查

```bash
python3 scripts/build_readme.py
python3 scripts/build_readme.py --check
python3 scripts/collect_sources.py --check
python3 scripts/validate_opportunities.py --check
python3 -m unittest discover -s tests -v
```

如果修改了企业微信摘要脚本，请额外运行以下命令预览完整消息。该命令不需要配置 webhook，也不会真正发送通知：

```bash
python3 scripts/send_wecom.py --dry-run
```

修改核心清单时，请一并提交更新后的 `README.md`、`README.zh-CN.md`、`feed.xml` 和 `deadlines.ics`。只修改可选分片时，这四个核心输出不应发生变化。维护者的复核与发布流程见 [`MAINTENANCE.md`](MAINTENANCE.md)。
