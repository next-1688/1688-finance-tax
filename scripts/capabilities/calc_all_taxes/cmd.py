#!/usr/bin/env python3
"""四税联算命令 — CLI 入口"""

COMMAND_NAME = "calc-all-taxes"
COMMAND_DESC = "商品含税定价（四税联算）"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _output import print_output, print_error
from capabilities.calc_all_taxes.service import calculate_all_taxes


def _parse_bool(value: str) -> bool:
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"无法解析布尔值: {value}")


def main():
    parser = argparse.ArgumentParser(description="商品含税定价（四税联算）")
    parser.add_argument("--taxpayer-type", required=True,
                        choices=["SMALL_SCALE_TAXPAYER", "GENERAL_TAXPAYER"],
                        help="纳税人类型")
    parser.add_argument("--invoice-requirement", required=True,
                        choices=["ORDINARY_INVOICE", "SPECIAL_INVOICE"],
                        help="开票类型")
    parser.add_argument("--invoice-tax-rate", required=True,
                        help="开票税率")
    parser.add_argument("--original-price", required=True, type=float,
                        help="原不含税报价（元）")
    parser.add_argument("--upstream-cost", required=True, type=float,
                        help="支付给上游的成本（元）")
    parser.add_argument("--calculation-mode", required=True,
                        choices=["EXPECTED_PROFIT", "EXPECTED_PROFIT_RATE"],
                        help="计算方式")
    parser.add_argument("--registration-type", required=True,
                        choices=["LIMITED_COMPANY", "INDIVIDUAL_BUSINESS"],
                        help="注册登记类型")
    parser.add_argument("--city-tax-rate", required=True,
                        choices=["7%", "5%", "1%"],
                        help="城市维护建设税税率")
    parser.add_argument("--upstream-invoice-type", required=True,
                        help="上游开票情况")
    parser.add_argument("--expected-profit", type=float, default=0,
                        help="期望利润（元）")
    parser.add_argument("--expected-profit-rate", type=float, default=0,
                        help="期望利润率（小数）")
    parser.add_argument("--is-small-profit-enterprise", type=_parse_bool, default=None,
                        help="是否小型微利企业（仅有限责任公司）")
    parser.add_argument("--taxable-income-range", default=None,
                        help="预计年应纳税所得额范围（仅个体工商户）")
    args = parser.parse_args()

    try:
        result = calculate_all_taxes(
            taxpayer_type=args.taxpayer_type,
            invoice_requirement=args.invoice_requirement,
            invoice_tax_rate=args.invoice_tax_rate,
            original_price=args.original_price,
            upstream_cost=args.upstream_cost,
            calculation_mode=args.calculation_mode,
            registration_type=args.registration_type,
            city_tax_rate=args.city_tax_rate,
            upstream_invoice_type=args.upstream_invoice_type,
            expected_profit=args.expected_profit,
            expected_profit_rate=args.expected_profit_rate,
            is_small_profit_enterprise=args.is_small_profit_enterprise,
            taxable_income_range=args.taxable_income_range,
        )
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as exc:
        print_error(exc)


if __name__ == "__main__":
    main()
