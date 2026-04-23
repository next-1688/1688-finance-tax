# 税负测算业务流程

> 本文档涵盖三种测算场景：仅增值税、四税联算、整体税负。

## 测算类型引导

当用户需要税负测算但未明确类型时，引导选择：

1. **商品含税定价（仅增值税）** — 只算增值税对报价的影响
2. **商品含税定价（四税联算）** — 增值税 + 附加税 + 印花税 + 所得税
3. **整体税负** — 综合评估年度税务成本

也可引导用户前往页面操作：

- [仅增值税测算](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_pageKey=calculatorOnlyVat&_hex_tracelog=openSkills)
- [四税联算](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_pageKey=calculatorQuadTax&_hex_tracelog=openSkills)
- [整体税负测算](https://work.1688.com/?_path_=sellerPro/zijinguanli/taxrouter&_hex_pageKey=calculatorOverallTax&_hex_tracelog=openSkills)

## 常量映射参考

调用测算工具时需将用户中文表述转换为枚举码，详见 [reference.md](reference.md#枚举映射表)。

---

## 1. 商品含税定价（仅增值税）

### 信息收集流程

按以下顺序向用户收集信息：

1. **纳税人类型**：小规模纳税人 / 一般纳税人
2. **开票类型**：增值税普通发票 / 增值税专用发票
3. **开票税率**：根据纳税人类型和开票类型确定可选范围（见下方税率选择规则）
4. **原不含税报价**（元）
5. **支付给上游的成本**（元）
6. **从上游获票情况**（仅一般纳税人需要）
7. **计算方式**：期望利润 / 期望利润率
8. **期望利润或期望利润率**：按计算方式只填其一

### 税率选择规则

| 纳税人类型 | 开票类型 | 可选税率 |
|------------|----------|----------|
| 小规模纳税人 | 增值税普通发票 | 免税、0%、1%、3% |
| 小规模纳税人 | 增值税专用发票 | 1%、3% |
| 一般纳税人 | 任意 | 0%、6%、9%、13% |

### 工具调用

使用工具码 `ai_tax_calc_vat` 调用，参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| taxpayerType | string | 是 | 纳税人类型枚举码 |
| invoiceRequirement | string | 是 | 开票类型枚举码 |
| invoiceTaxRate | string | 是 | 开票税率枚举码 |
| originalPrice | number | 是 | 原不含税报价（元） |
| upstreamCost | number | 是 | 支付给上游的成本（元） |
| calculationMode | string | 是 | 计算方式枚举码 |
| expectedProfit | number | 条件 | 期望利润（元），calculationMode=EXPECTED_PROFIT 时必填 |
| expectedProfitRate | number | 条件 | 期望利润率（小数），calculationMode=EXPECTED_PROFIT_RATE 时必填 |
| upstreamInvoiceType | string | 条件 | 上游获票情况枚举码，仅一般纳税人必填 |

### 参数枚举映射

调用工具时需将用户中文表述转换为枚举码，详见 [reference.md](reference.md#枚举映射表)。

---

## 2. 商品含税定价（四税联算）

### 信息收集流程

按以下顺序向用户收集信息：

1. **纳税人类型**：小规模纳税人 / 一般纳税人
2. **开票类型**：增值税普通发票 / 增值税专用发票
3. **开票税率**：根据纳税人类型和开票类型确定可选范围
4. **原不含税报价**（元）
5. **支付给上游的成本**（元）
6. **从上游获票情况**（仅一般纳税人需要）
7. **注册登记类型**：有限责任公司 / 个体工商户
8. **城市维护建设税税率**：7% / 5% / 1%（根据所在地区）
9. **是否小微企业**：是 / 否（有限责任公司等场景）
10. **年应纳税所得额**：根据枚举码确定可选范围（仅个体工商户需要）
11. **计算方式**：期望利润 / 期望利润率
12. **期望利润或期望利润率**：按计算方式只填其一

### 税率选择规则

与"仅增值税"相同，见上方表格。

### 工具调用

使用工具码 `ai_tax_calc_all` 调用，参数如下：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| taxpayerType | string | 是 | 纳税人类型枚举码 |
| invoiceRequirement | string | 是 | 开票类型枚举码 |
| invoiceTaxRate | string | 是 | 开票税率枚举码 |
| originalPrice | number | 是 | 原不含税报价（元） |
| upstreamCost | number | 是 | 支付给上游的成本（元） |
| calculationMode | string | 是 | 计算方式枚举码 |
| expectedProfit | number | 条件 | 期望利润（元），calculationMode=EXPECTED_PROFIT 时必填 |
| expectedProfitRate | number | 条件 | 期望利润率（小数），calculationMode=EXPECTED_PROFIT_RATE 时必填 |
| upstreamInvoiceType | string | 条件 | 上游获票情况枚举码，仅一般纳税人必填 |
| registrationType | string | 是 | 注册登记类型枚举码 |
| taxableIncomeRange | string | 条件 | 预计年应纳税所得额枚举码，仅个体工商户时需要|
| cityTaxRate | string | 是 | 城市维护建设税税率（如 "7%"） |
| isSmallProfitEnterprise | boolean | 条件 | 是否小微企业，仅有限责任公司时需要 |

### 参数枚举映射

调用工具时需将用户中文表述转换为枚举码，详见 [reference.md](reference.md#枚举映射表)。

---

## 3. 整体税负测算

### 信息收集流程

按以下顺序向用户收集信息：

1. **纳税人类型**：小规模纳税人 / 一般纳税人
2. **年销售额**（万元）
3. **年利润总额**（万元）
4. **注册登记类型**：有限责任公司 / 个体工商户 / 不确定
5. **城市维护建设税税率**：7% / 5% / 1%（根据所在地区）
6. **是否小微企业**：是 / 否

### 工具调用

使用工具码 `ai_tax_calc_overall` 调用。参数如下：

#### 元数据（与 `scripts/_gateway_body.py` 对齐；部分由平台注入时可不在工具表单重复）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| site | string | 视平台 | 业务站点，如 `1688` |
| skillName | string | 视平台 | 技能名，如 `1688-finance-tax` |
| skillVersion | string | 视平台 | 如 `1.0.0` |
| toolCode | string | 视平台 | 固定 `ai_tax_calc_overall` |

#### 场景与核心业务（`scripts/capabilities/calc_overall/service.py` 请求体）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| scene | string | 是 | 固定 `OVERALL_TAX_BURDEN` |
| taxpayerType | string | 是 | 纳税人类型枚举码 |
| annualSalesAmount | number | 是 | 年销售额（万元），勿写成 `SalesAmount` |
| annualProfitAmount | number | 是 | 年利润总额（万元），勿写成 `ProfitAmount` |
| registrationType | string | 是 | 注册登记类型枚举码，勿写成 `istrationType` |
| cityTaxRate | string | 是 | 城建税税率：`"7%"` / `"5%"` / `"1%"` |
| isSmallProfitEnterprise | boolean | 条件 | 是否小型微利企业；仅 `LIMITED_COMPANY` / `UNCERTAIN` 时需要。 |
| calculationMethod | string | 条件 | 仅一般纳税人：`BY_RATE`（按税率）或 `BY_CATEGORY`（按类目）二选一 |

#### 一般纳税人 · 按税率 `BY_RATE`（与 `calculationMethod` 同时使用）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| specialInvoice13PercentAmount | number | 否 | 13% 专票含税总额（万元） |
| specialInvoice9PercentAmount | number | 否 | 9% 专票含税总额（万元） |
| specialInvoice6PercentAmount | number | 否 | 6% 专票含税总额（万元） |
| specialInvoice3PercentAmount | number | 否 | 3% 专票含税总额（万元） |
| specialInvoice1PercentAmount | number | 否 | 1% 专票含税总额（万元） |
| ordinaryInvoiceAmount | number | 否 | 普通发票含税总额（万元） |

#### 一般纳税人 · 按类目 `BY_CATEGORY`（与 `calculationMethod` 同时使用）

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| purchaseGoodsAmount | number | 否 | 采购商品金额（万元） |
| purchaseGoodsInvoiceRatio | number | 否 | 采购专票占比，小数如 `0.8` 表示 80% |
| logisticsAmount | number | 否 | 物流支出金额（万元） |
| logisticsInvoiceRatio | number | 否 | 物流专票占比，小数 |
| serviceFeeAmount | number | 否 | 服务费支出金额（万元） |
| serviceFeeInvoiceRatio | number | 否 | 服务费专票占比，小数 |
| laborAmount | number | 否 | 人力支出金额（万元） |
| laborInvoiceRatio | number | 否 | 人力专票占比，小数 |
| otherOperatingExpenses | number | 否 | 其他经营支出（万元） |

### 参数枚举映射

调用工具时需将用户中文表述转换为枚举码，详见 [reference.md](reference.md#枚举映射表)。
