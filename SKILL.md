---
name: 1688-finance-tax
description: 财税税负测算专家技能。帮助用户计算商品含税定价、评估整体税负。支持增值税测算、四税联算（增值税+附加税+印花税+所得税）、整体税负分析等场景。用户提到税务、税率、含税定价、税负、增值税、所得税、发票、纳税人等测算问题时使用。
metadata: {"openclaw": {"emoji": "💰", "requires": {"bins": ["python3"]}, "primaryEnv": "FINANCE_TAX_API_KEY"}}
---

# 财税税负测算

统一入口：`python3 {baseDir}/cli.py <command> [options]`

## 命令速查

| 命令 | 说明 | 示例 |
|------|------|------|
| `calc-vat` | 商品含税定价（仅增值税） | `cli.py calc-vat --taxpayer-type SMALL_SCALE_TAXPAYER --invoice-requirement ORDINARY_INVOICE --invoice-tax-rate RATE_3_PERCENT --original-price 1000 --upstream-cost 600 --calculation-mode EXPECTED_PROFIT --expected-profit 400` |
| `calc-all-taxes` | 商品含税定价（四税联算） | `cli.py calc-all-taxes --taxpayer-type SMALL_SCALE_TAXPAYER ... --registration-type LIMITED_COMPANY --city-tax-rate 7% --is-small-profit-enterprise true` |
| `calc-overall` | 整体税负测算 | `cli.py calc-overall --taxpayer-type SMALL_SCALE_TAXPAYER --annual-sales-amount 300 --annual-profit-amount 50 --registration-type LIMITED_COMPANY --city-tax-rate 7% --is-small-profit-enterprise true` |
| `configure` | 配置 AK | `cli.py configure YOUR_AK` |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

**展示时直接输出 `markdown` 字段，Agent 分析追加在后面，不得混入其中。**

## 工具码与命令映射

| ClawHub 工具码 | CLI 命令 | 说明 |
|---------------|---------|------|
| `ai_tax_calc_vat` | `calc-vat` | 商品含税定价（仅增值税） |
| `ai_tax_calc_all` | `calc-all-taxes` | 商品含税定价（四税联算） |
| `ai_tax_calc_overall` | `calc-overall` | 整体税负测算 |

测算类功能通过 ClawHub 工具码调用（与上表 CLI 对应）。

## 意图识别与文档索引

根据用户提问意图，跳转到对应的业务流程文档：

| 用户提问意图 | 对应文档 |
|-------------|---------|
| 商品含税定价、增值税测算、加价点数、含税报价计算 | [references/tax-calculation.md](references/tax-calculation.md#1-商品含税定价仅增值税) |
| 四税联算、增值税+附加税+印花税+所得税、综合含税定价 | [references/tax-calculation.md](references/tax-calculation.md#2-商品含税定价四税联算) |
| 整体税负、年度税负、年度税费总额、税负率、企业综合税务成本 | [references/tax-calculation.md](references/tax-calculation.md#3-整体税负测算) |

## 执行前置（首次命中能力时必须）

- 首次执行 `calc-vat` 前：先完整阅读 [references/tax-calculation.md](references/tax-calculation.md#1-商品含税定价仅增值税)
- 首次执行 `calc-all-taxes` 前：先完整阅读 [references/tax-calculation.md](references/tax-calculation.md#2-商品含税定价四税联算)
- 首次执行 `calc-overall` 前：先完整阅读 [references/tax-calculation.md](references/tax-calculation.md#3-整体税负测算)
- 同一会话内后续重复调用同一能力可复用已加载知识；仅在规则冲突或文档更新时重读。

## 通用规则

执行任何业务前，完整阅读并遵守 [references/common/common-rules.md](references/common/common-rules.md)。其中对 **对客中文**、**不暴露请求**、**免责声明**、**数据验证** 等为**硬性要求**。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" | 输出下方 **AK 引导话术** |
| "参数错误" / "400" | 检查用户输入是否正确，引导修正 |
| "限流" / "429" | 建议用户等待 1-2 分钟后重试 |
| "服务异常" / "500" | 建议用户稍后重试 |
| 其他 | 仅输出 markdown 即可 |

## AK 引导话术

> "需要先配置 AK 才能使用财税测算功能。请登录 [ClawHub](https://clawhub.1688.com/)，点击右上角钥匙按钮获取 AK，然后告诉我：'我的AK是 xxx'"

## 免责声明

每次回答末尾增加：

> 以上测算结果仅供参考，具体以税务机关与实务为准。