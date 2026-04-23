# 财税测算字段映射参考

## 通用字段映射

### 纳税人类型 (taxpayerType)
- 小规模纳税人: `SMALL_SCALE_TAXPAYER`
- 一般纳税人: `GENERAL_TAXPAYER`

### 开票类型 (invoiceRequirement)
- 增值税普通发票: `ORDINARY_INVOICE`
- 增值税专用发票: `SPECIAL_INVOICE`

### 开票税率 (invoiceTaxRate)
- 免税: `TAX_FREE`
- 0%: `RATE_0_PERCENT`
- 1%: `RATE_1_PERCENT`
- 3%: `RATE_3_PERCENT`
- 6%: `RATE_6_PERCENT`
- 9%: `RATE_9_PERCENT`
- 13%: `RATE_13_PERCENT`

### 税率选择规则
| 纳税人类型 | 开票类型 | 可选税率 |
|------------|----------|----------|
| 小规模纳税人 | 增值税普通发票 | 免税、0%、1%、3% |
| 小规模纳税人 | 增值税专用发票 | 1%、3% |
| 一般纳税人 | 任意 | 0%、6%、9%、13% |

### 上游开票情况 (upstreamInvoiceType)
- 未获得发票: `NO_INVOICE`
- 能获得普通发票: `ORDINARY_INVOICE`
- 能获得13%的专用发票: `SPECIAL_INVOICE_13_PERCENT`
- 能获得9%的专用发票: `SPECIAL_INVOICE_9_PERCENT`
- 能获得6%的专用发票: `SPECIAL_INVOICE_6_PERCENT`
- 能获得3%的专用发票: `SPECIAL_INVOICE_3_PERCENT`
- 能获得1%的专用发票: `SPECIAL_INVOICE_1_PERCENT`

### 计算方式 (calculationMode)
- 期望利润: `EXPECTED_PROFIT`
- 期望利润率: `EXPECTED_PROFIT_RATE`

## 四税测算专用字段

### 注册登记类型 (registrationType)
- 不确定: `UNCERTAIN`
- 有限责任公司: `LIMITED_COMPANY`
- 个体工商户（查账征收）: `INDIVIDUAL_BUSINESS`

### 是否小型微利企业 (isSmallProfitEnterprise)
- 是: `true`
- 否: `false`

**小型微利企业定义**：
1. 年度应纳税所得额不超过300万元
2. 从业人数不超过300人
3. 资产总额不超过5000万元

### 预计年应纳税所得额范围 (taxableIncomeRange)
- 不超过3万: `UNDER_30000`
- 3万~9万: `RANGE_30000_TO_90000`
- 9万~30万: `RANGE_90000_TO_300000`
- 30万~50万: `RANGE_300000_TO_500000`
- 50万~200万: `RANGE_500000_TO_2000000`
- 200万以上: `OVER_2000000`

### 城市维护建设税税率 (cityTaxRate)
- 7%（市区）: `"7%"`
- 5%（县城、镇）: `"5%"`
- 1%（其他）: `"1%"`

## 整体税负测算专用字段

### 计算方式 (calculationMethod)
- 按税率: `BY_RATE`
- 按类目: `BY_CATEGORY`

### 按税率方式字段
- 13%税率专用发票含税总额: `specialInvoice13PercentAmount`
- 9%税率专用发票含税总额: `specialInvoice9PercentAmount`
- 6%税率专用发票含税总额: `specialInvoice6PercentAmount`
- 3%税率专用发票含税总额: `specialInvoice3PercentAmount`
- 1%税率专用发票含税总额: `specialInvoice1PercentAmount`
- 普通发票含税总额: `ordinaryInvoiceAmount`

### 按类目方式字段
- 采购商品金额: `purchaseGoodsAmount`
- 采购商品专票占比: `purchaseGoodsInvoiceRatio`
- 物流支出金额: `logisticsAmount`
- 物流支出专票占比: `logisticsInvoiceRatio`
- 服务费支出金额: `serviceFeeAmount`
- 服务费支出专票占比: `serviceFeeInvoiceRatio`
- 人力支出金额: `laborAmount`
- 人力支出专票占比: `laborInvoiceRatio`
- 其他经营支出: `otherOperatingExpenses`

**注意**：所有占比字段输入时需要除以100转换为小数（例如：80% → 0.8）

## 场景标识 (scene)

### 固定场景值
- 仅增值税测算: `TAX_INCLUDED_PRICE_ONLY_VAT`（仅小规模纳税人时使用，一般纳税人为null）
- 四税测算: `TAX_INCLUDED_PRICE_ALL_TAXES`
- 整体税负: `OVERALL_TAX_BURDEN`

## 条件字段出现规则

### 上游获票情况
- **仅增值税测算**：仅一般纳税人需要填写
- **四税测算**：所有用户都需要填写
- **整体税负测算**：不需要填写

### 是否小型微利企业
- 仅当注册登记类型为"有限责任公司"或"不确定"时出现

### 预计年应纳税所得额范围
- 四税联算并且个体工商户时需要

### 支出结构
- 仅一般纳税人在整体税负测算时需要填写
- 必须选择"按税率"或"按类目"方式之一