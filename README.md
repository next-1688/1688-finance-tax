# 1688-finance-tax

财税税负测算专家技能 —— 帮你算清商品的含税定价与企业的整体税负，支持增值税测算、四税联算、整体税负分析。

## 能做什么

- **含税定价（仅增值税）**：根据纳税人类型、开票要求、期望利润/利润率，倒推含税报价与加价点数
- **含税定价（四税联算）**：增值税 + 附加税 + 印花税 + 所得税 一次算清，给出综合含税报价
- **整体税负测算**：按年销售额、年利润、支出结构，评估企业年度综合税负率与税费明细

## 安装

在 Claw 对话框里直接输入下面这段话，让 OpenClaw 帮你自动安装：

```text
请帮我安装这个 skill：https://github.com/your-org/1688-finance-tax.git
```

## 使用前准备

1. 登录 [ClawHub](https://clawhub.1688.com/)
2. 点击右上角钥匙按钮，在弹框中点击重新生成，复制你的 AK（Access Key）
3. 对 AI 说："我的AK是 xxx"

配置完成后就可以开始使用财税测算功能了。

## 快速上手

直接用自然语言和 AI 对话即可：

- "我是小规模纳税人，开 3% 专票，原价 1000 块，上游成本 600，期望利润 400，帮我算含税报价"
- "四税联算一下，我是有限责任公司，小型微利，城建税 7%"
- "帮我评估一下整体税负，我是一般纳税人，年销售额 800 万，年利润 150 万"

## 命令行（CLI）

本仓库提供统一入口 `cli.py`，需本机已安装 **Python 3**。环境变量 `FINANCE_TAX_API_KEY` 或由命令 `configure` 写入的配置需与 ClawHub 中的 AK 一致。

```bash
python3 cli.py <command> [options]
```

| 命令 | 说明 | 示例 |
|------|------|------|
| `calc-vat` | 商品含税定价（仅增值税） | `python3 cli.py calc-vat --taxpayer-type SMALL_SCALE_TAXPAYER --invoice-requirement ORDINARY_INVOICE --invoice-tax-rate RATE_3_PERCENT --original-price 1000 --upstream-cost 600 --calculation-mode EXPECTED_PROFIT --expected-profit 400` |
| `calc-all-taxes` | 商品含税定价（四税联算） | `python3 cli.py calc-all-taxes --taxpayer-type SMALL_SCALE_TAXPAYER ... --registration-type LIMITED_COMPANY --city-tax-rate 7% --is-small-profit-enterprise true` |
| `calc-overall` | 整体税负测算 | `python3 cli.py calc-overall --taxpayer-type SMALL_SCALE_TAXPAYER --annual-sales-amount 300 --annual-profit-amount 50 --registration-type LIMITED_COMPANY --city-tax-rate 7% --is-small-profit-enterprise true` |
| `configure` | 配置 AK | `python3 cli.py configure YOUR_AK` |

所有命令 stdout 为 JSON：`{"success": bool, "markdown": str, "data": {...}}`。人类可读说明一般在 `markdown` 字段。**Agent / Skill 编排约定** 见根目录 [`SKILL.md`](./SKILL.md)（含意图识别、异常处理与各能力参考文档路径）。

## 支持场景

| 场景 | 小规模纳税人 | 一般纳税人 |
|------|-------------|-----------|
| 含税定价（仅增值税） | ✅ | ✅ |
| 含税定价（四税联算） | ✅ | ✅ |
| 整体税负测算 | ✅ | ✅ |



## 业务限制

- **仅用于测算参考**：结果不作为纳税申报依据，具体以税务机关与实务为准



## 常见问题

**Q: AK 是什么？怎么获取？**
AK 是你访问财税测算网关的身份凭证。在 [ClawHub](https://clawhub.1688.com/) 中点击右上角钥匙按钮获取。

**Q: 为什么提示"AK 未配置"？**
命令未能在环境变量或 OpenClaw 配置中找到 AK。执行 `python3 cli.py configure YOUR_AK` 保存，或导出环境变量 `FINANCE_TAX_API_KEY=YOUR_AK`。

**Q: 小规模纳税人和一般纳税人有什么区别？**
小规模纳税人按销售额乘征收率简易计税，一般纳税人按销项减进项计税。技能会根据 `taxpayer-type` 自动套用对应公式。

**Q: 「含税定价」和「整体税负测算」怎么选？**
- 只想知道某笔商品要卖多少钱才能覆盖税和利润 → `calc-vat` 或 `calc-all-taxes`
- 想看全年下来公司综合要交多少税、税负率多少 → `calc-overall`

**Q: 结果和税务局口径不一致怎么办？**
测算口径为通用场景，不覆盖所有地区性优惠和特殊行业政策，具体以当地税务机关与实务为准。

## 反馈与支持

使用中遇到问题，可以联系 1688 财税技能技术支持。

---

**免责声明**：以上测算结果仅供参考，具体以税务机关与实务为准。若与您实际申报/核定情况不一致，请以税务机关为准。
