#!/usr/bin/env python3
"""整体税负测算服务 — 调用 API 计算综合税务成本"""

from typing import List, Dict, Any, Optional

from _http import api_post
from _const import GATEWAY_TOOL_CALC_OVERALL, TOOL_CODE_CALC_OVERALL
from _gateway_body import merge_gateway_skill_fields
from _errors import ParamError, ServiceError


def _build_markdown(calculation_results: List[Dict[str, Any]]) -> str:
    """将整体税负测算结果格式化为 Markdown"""
    if not calculation_results:
        return "未返回测算结果。"

    registration_type_labels = {
        "LIMITED_COMPANY": "有限责任公司",
        "INDIVIDUAL_BUSINESS": "个体工商户（查账征收）",
    }

    all_parts: List[str] = ["## 整体税负测算结果\n"]

    for result_item in calculation_results:
        reg_type = result_item.get("registrationType", "")
        reg_label = registration_type_labels.get(reg_type, reg_type)
        overall_burden = result_item.get("comprehensiveTaxBurdenRate", "—")
        annual_tax = result_item.get("totalTaxAmount", "—")

        all_parts.append(f"### {reg_label}\n")
        all_parts.append("**概览**")
        all_parts.append(f"- **综合税负率**：{overall_burden}%")
        all_parts.append(f"- **税额合计**：{annual_tax} 万元")
        all_parts.append("")
        all_parts.append("**详情**")
        all_parts.append("")
        all_parts.append("| 项目 | 金额 | 计算公式 |")
        all_parts.append("|------|------|---------|")

        calculation_items = result_item.get("calculationItems", [])
        for item in calculation_items:
            item_name = item.get("itemName", "")
            item_formula = item.get("itemFormula", "")
            item_amount = item.get("itemAmount", "—")
            formula_display = f"`{item_formula}`" if item_formula else "—"

            all_parts.append(
                f"| {item_name} | {item_amount} 万元 | {formula_display} |"
            )

        all_parts.append("")

    all_parts.append("> 以上测算结果仅供参考，具体以税务机关与实务为准。")
    return "\n".join(all_parts)


def calculate_overall_tax(
    taxpayer_type: str,
    annual_sales_amount: float,
    annual_profit_amount: float,
    registration_type: str,
    city_tax_rate: str,
    calculation_method: Optional[str] = None,
    is_small_profit_enterprise: Optional[bool] = None,
    taxable_income_range: Optional[str] = None,
    special_invoice_13_percent_amount: Optional[float] = None,
    special_invoice_9_percent_amount: Optional[float] = None,
    special_invoice_6_percent_amount: Optional[float] = None,
    special_invoice_3_percent_amount: Optional[float] = None,
    special_invoice_1_percent_amount: Optional[float] = None,
    ordinary_invoice_amount: Optional[float] = None,
    purchase_goods_amount: Optional[float] = None,
    purchase_goods_invoice_ratio: Optional[float] = None,
    logistics_amount: Optional[float] = None,
    logistics_invoice_ratio: Optional[float] = None,
    service_fee_amount: Optional[float] = None,
    service_fee_invoice_ratio: Optional[float] = None,
    labor_amount: Optional[float] = None,
    labor_invoice_ratio: Optional[float] = None,
    other_operating_expenses: Optional[float] = None,
) -> dict:
    """
    整体税负测算

    Returns:
        {"success": bool, "markdown": str, "data": dict}
    """
    if annual_sales_amount <= 0:
        raise ParamError("年销售额必须大于 0")
    if annual_profit_amount < 0:
        raise ParamError("年利润总额不能为负数")
    if annual_profit_amount > annual_sales_amount:
        raise ParamError("年利润总额不能大于年销售额")

    body: Dict[str, Any] = {
        "scene": "OVERALL_TAX_BURDEN",
        "taxpayerType": taxpayer_type,
        "annualSalesAmount": annual_sales_amount,
        "annualProfitAmount": annual_profit_amount,
        "registrationType": registration_type,
        "cityTaxRate": city_tax_rate,
    }

    if is_small_profit_enterprise is not None:
        body["isSmallProfitEnterprise"] = is_small_profit_enterprise
    if taxable_income_range:
        body["taxableIncomeRange"] = taxable_income_range
    if calculation_method:
        body["calculationMethod"] = calculation_method

    # 按税率方式的字段
    rate_fields = {
        "specialInvoice13PercentAmount": special_invoice_13_percent_amount,
        "specialInvoice9PercentAmount": special_invoice_9_percent_amount,
        "specialInvoice6PercentAmount": special_invoice_6_percent_amount,
        "specialInvoice3PercentAmount": special_invoice_3_percent_amount,
        "specialInvoice1PercentAmount": special_invoice_1_percent_amount,
        "ordinaryInvoiceAmount": ordinary_invoice_amount,
    }
    for field_name, field_value in rate_fields.items():
        if field_value is not None:
            body[field_name] = field_value

    # 按类目方式的字段
    category_fields = {
        "purchaseGoodsAmount": purchase_goods_amount,
        "purchaseGoodsInvoiceRatio": purchase_goods_invoice_ratio,
        "logisticsAmount": logistics_amount,
        "logisticsInvoiceRatio": logistics_invoice_ratio,
        "serviceFeeAmount": service_fee_amount,
        "serviceFeeInvoiceRatio": service_fee_invoice_ratio,
        "laborAmount": labor_amount,
        "laborInvoiceRatio": labor_invoice_ratio,
        "otherOperatingExpenses": other_operating_expenses,
    }
    for field_name, field_value in category_fields.items():
        if field_value is not None:
            body[field_name] = field_value

    payload = merge_gateway_skill_fields(body, TOOL_CODE_CALC_OVERALL)
    data = api_post(GATEWAY_TOOL_CALC_OVERALL, body=payload)

    result_data = data
    calculation_results = result_data.get("calculationResults", [])
    if not calculation_results:
        error_message = "未返回测算结果"
        raise ServiceError(error_message)
    markdown = _build_markdown(calculation_results)

    return {"success": True, "markdown": markdown, "data": result_data}
