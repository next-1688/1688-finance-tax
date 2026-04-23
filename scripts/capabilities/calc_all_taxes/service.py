#!/usr/bin/env python3
"""四税联算服务 — 调用 API 计算含税报价（增值税+附加税+印花税+所得税）"""

from typing import List, Dict, Any, Optional

from _http import api_post
from _const import GATEWAY_TOOL_CALC_ALL_TAXES, TOOL_CODE_CALC_ALL_TAXES
from _gateway_body import merge_gateway_skill_fields
from _errors import ParamError, ServiceError


def _format_calculation_item_amount(item: Dict[str, Any]) -> str:
    """详情表格「金额」列：期望利润率行单位为 %，其余为 元（与 fin-finance-tax 计算项一致）。"""
    amount = item.get("itemAmount")
    if amount in (None, ""):
        return "—"
    key = item.get("itemKey") or ""
    name = item.get("itemName") or ""
    if key == "profit_rate" or name == "期望利润率":
        return f"{amount}%"
    return f"{amount} 元"


def _build_markdown(result_data: Dict[str, Any]) -> str:
    """将四税测算结果格式化为 Markdown"""
    # API返回结构：{calculationResult: {taxIncludedPrice, priceIncreaseRate, calculationItems: [...]}}
    calculation_result = result_data.get("calculationResult", result_data)
    calculation_items = calculation_result.get("calculationItems", [])

    # 直接从 API 返回的字段取数
    tax_included_price = calculation_result.get("taxIncludedPrice", "—")
    price_increase_rate = calculation_result.get("priceIncreaseRate", "—")

    if tax_included_price != "—":
        tax_included_price = f"{tax_included_price} 元"
    if price_increase_rate != "—":
        price_increase_rate = f"{price_increase_rate}%"

    parts: List[str] = [
        "## 四税测算结果\n",
        "### 概览",
        f"- **含税报价**：{tax_included_price}",
        f"- **加价点数**：{price_increase_rate}",
        "",
        "### 详情",
        "",
        "| 项目 | 金额 | 计算公式 |",
        "|------|------|---------|",
    ]

    for item in calculation_items:
        item_name = item.get("itemName", "")
        item_formula = item.get("itemFormula", "")
        amount_cell = _format_calculation_item_amount(item)
        formula_display = f"`{item_formula}`" if item_formula else "—"

        parts.append(f"| {item_name} | {amount_cell} | {formula_display} |")

    parts.append("\n> 以上测算结果仅供参考，具体以税务机关与实务为准。")
    return "\n".join(parts)


def calculate_all_taxes(
    taxpayer_type: str,
    invoice_requirement: str,
    invoice_tax_rate: str,
    original_price: float,
    upstream_cost: float,
    calculation_mode: str,
    registration_type: str,
    city_tax_rate: str,
    upstream_invoice_type: str,
    expected_profit: float = 0,
    expected_profit_rate: float = 0,
    is_small_profit_enterprise: Optional[bool] = None,
    taxable_income_range: Optional[str] = None,
) -> dict:
    """
    商品含税定价（四税联算：增值税+附加税+印花税+所得税）

    Returns:
        {"success": bool, "markdown": str, "data": dict}
    """
    if original_price <= 0:
        raise ParamError("原不含税报价必须大于 0")
    if upstream_cost < 0:
        raise ParamError("上游成本不能为负数")
    if registration_type == "INDIVIDUAL_BUSINESS":
        if not (taxable_income_range and str(taxable_income_range).strip()):
            raise ParamError(
                "四税联算且注册登记类型为个体工商户时，必须填写预计年应纳税所得额范围，请传入 --taxable-income-range（取值见 references/reference.md）。"
            )

    body = {
        "scene": "TAX_INCLUDED_PRICE_ALL_TAXES",
        "taxpayerType": taxpayer_type,
        "invoiceRequirement": invoice_requirement,
        "invoiceTaxRate": invoice_tax_rate,
        "originalPrice": original_price,
        "upstreamCost": upstream_cost,
        "calculationMode": calculation_mode,
        "expectedProfit": expected_profit,
        "expectedProfitRate": expected_profit_rate,
        "registrationType": registration_type,
        "cityTaxRate": city_tax_rate,
        "upstreamInvoiceType": upstream_invoice_type,
    }

    if is_small_profit_enterprise is not None:
        body["isSmallProfitEnterprise"] = is_small_profit_enterprise
    if taxable_income_range:
        body["taxableIncomeRange"] = taxable_income_range

    payload = merge_gateway_skill_fields(body, TOOL_CODE_CALC_ALL_TAXES)
    data = api_post(GATEWAY_TOOL_CALC_ALL_TAXES, body=payload)
    

    result_data = data
    markdown = _build_markdown(result_data)

    return {"success": True, "markdown": markdown, "data": result_data}
