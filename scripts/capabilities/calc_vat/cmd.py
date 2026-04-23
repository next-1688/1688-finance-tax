#!/usr/bin/env python3
"""仅增值税测算命令 — CLI 入口"""

COMMAND_NAME = "calc-vat"
COMMAND_DESC = "商品含税定价（仅增值税）"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

import argparse
from _output import print_output, print_error
from capabilities.calc_vat.service import calculate_vat_only


def main():
    parser = argparse.ArgumentParser(description="商品含税定价（仅增值税）")
    parser.add_argument("--taxpayer-type", required=True,
                        choices=["SMALL_SCALE_TAXPAYER", "GENERAL_TAXPAYER"],
                        help="纳税人类型")
    parser.add_argument("--invoice-requirement", required=True,
                        choices=["ORDINARY_INVOICE", "SPECIAL_INVOICE"],
                        help="开票类型")
    parser.add_argument("--invoice-tax-rate", required=True,
                        help="开票税率（如 TAX_FREE, RATE_1_PERCENT 等）")
    parser.add_argument("--original-price", required=True, type=float,
                        help="原不含税报价（元）")
    parser.add_argument("--upstream-cost", required=True, type=float,
                        help="支付给上游的成本（元）")
    parser.add_argument("--calculation-mode", required=True,
                        choices=["EXPECTED_PROFIT", "EXPECTED_PROFIT_RATE"],
                        help="计算方式")
    parser.add_argument("--expected-profit", type=float, default=0,
                        help="期望利润（元）")
    parser.add_argument("--expected-profit-rate", type=float, default=0,
                        help="期望利润率（小数）")
    parser.add_argument("--upstream-invoice-type", default=None,
                        help="上游开票情况（仅一般纳税人需要）")
    args = parser.parse_args()

    try:
        result = calculate_vat_only(
            taxpayer_type=args.taxpayer_type,
            invoice_requirement=args.invoice_requirement,
            invoice_tax_rate=args.invoice_tax_rate,
            original_price=args.original_price,
            upstream_cost=args.upstream_cost,
            calculation_mode=args.calculation_mode,
            expected_profit=args.expected_profit,
            expected_profit_rate=args.expected_profit_rate,
            upstream_invoice_type=args.upstream_invoice_type,
        )
        print_output(result["success"], result["markdown"], result["data"])
    except Exception as exc:
        print_error(exc)


if __name__ == "__main__":
    main()
