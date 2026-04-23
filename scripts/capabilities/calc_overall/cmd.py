#!/usr/bin/env python3
"""整体税负测算命令 — CLI 入口"""

COMMAND_NAME = "calc-overall"
COMMAND_DESC = "整体税负测算"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _output import print_output, print_error
from capabilities.calc_overall.service import calculate_overall_tax


def _parse_bool(value: str) -> bool:
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"无法解析布尔值: {value}")


def main():
   
    parser = argparse.ArgumentParser(description="整体税负测算")
    parser.add_argument("--taxpayer-type", required=True,
                        choices=["SMALL_SCALE_TAXPAYER", "GENERAL_TAXPAYER"],
                        help="纳税人类型")
    parser.add_argument("--annual-sales-amount", required=True, type=float,
                        help="年销售额（万元）")
    parser.add_argument("--annual-profit-amount", required=True, type=float,
                        help="年利润总额（万元）")
    parser.add_argument("--registration-type", required=True,
                        choices=["UNCERTAIN", "LIMITED_COMPANY", "INDIVIDUAL_BUSINESS"],
                        help="注册登记类型")
    parser.add_argument("--city-tax-rate", required=True,
                        choices=["7%", "5%", "1%"],
                        help="城市维护建设税税率")
    parser.add_argument("--calculation-method", default=None,
                        choices=["BY_RATE", "BY_CATEGORY"],
                        help="支出结构计算方式（仅一般纳税人）")
    parser.add_argument("--is-small-profit-enterprise", type=_parse_bool, default=None,
                        help="是否小型微利企业")
    parser.add_argument("--taxable-income-range", default=None,
                        help="预计年应纳税所得额范围（仅个体工商户）")
    # 按税率方式字段
    parser.add_argument("--special-invoice-13-percent-amount", type=float, default=None)
    parser.add_argument("--special-invoice-9-percent-amount", type=float, default=None)
    parser.add_argument("--special-invoice-6-percent-amount", type=float, default=None)
    parser.add_argument("--special-invoice-3-percent-amount", type=float, default=None)
    parser.add_argument("--special-invoice-1-percent-amount", type=float, default=None)
    parser.add_argument("--ordinary-invoice-amount", type=float, default=None)
    # 按类目方式字段
    parser.add_argument("--purchase-goods-amount", type=float, default=None)
    parser.add_argument("--purchase-goods-invoice-ratio", type=float, default=None)
    parser.add_argument("--logistics-amount", type=float, default=None)
    parser.add_argument("--logistics-invoice-ratio", type=float, default=None)
    parser.add_argument("--service-fee-amount", type=float, default=None)
    parser.add_argument("--service-fee-invoice-ratio", type=float, default=None)
    parser.add_argument("--labor-amount", type=float, default=None)
    parser.add_argument("--labor-invoice-ratio", type=float, default=None)
    parser.add_argument("--other-operating-expenses", type=float, default=None)
    args = parser.parse_args()


    try:
        result = calculate_overall_tax(
            taxpayer_type=args.taxpayer_type,
            annual_sales_amount=args.annual_sales_amount,
            annual_profit_amount=args.annual_profit_amount,
            registration_type=args.registration_type,
            city_tax_rate=args.city_tax_rate,
            calculation_method=args.calculation_method,
            is_small_profit_enterprise=args.is_small_profit_enterprise,
            taxable_income_range=args.taxable_income_range,
            special_invoice_13_percent_amount=args.special_invoice_13_percent_amount,
            special_invoice_9_percent_amount=args.special_invoice_9_percent_amount,
            special_invoice_6_percent_amount=args.special_invoice_6_percent_amount,
            special_invoice_3_percent_amount=args.special_invoice_3_percent_amount,
            special_invoice_1_percent_amount=args.special_invoice_1_percent_amount,
            ordinary_invoice_amount=args.ordinary_invoice_amount,
            purchase_goods_amount=args.purchase_goods_amount,
            purchase_goods_invoice_ratio=args.purchase_goods_invoice_ratio,
            logistics_amount=args.logistics_amount,
            logistics_invoice_ratio=args.logistics_invoice_ratio,
            service_fee_amount=args.service_fee_amount,
            service_fee_invoice_ratio=args.service_fee_invoice_ratio,
            labor_amount=args.labor_amount,
            labor_invoice_ratio=args.labor_invoice_ratio,
            other_operating_expenses=args.other_operating_expenses,
        )
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as exc:
        print_error(exc)


if __name__ == "__main__":
    main()
