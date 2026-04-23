#!/usr/bin/env python3
"""
1688-finance-tax 全局常量

所有模块统一从这里 import，禁止各模块自定义同名常量。
"""

import os
from pathlib import Path

# Skill 版本
SKILL_VERSION = "1.0.0"
SKILL_NAME = "1688-finance-tax"
SITE = "1688"

# ── OpenClaw 配置文件路径（唯一权威来源）──────────────────────────────────────
OPENCLAW_CONFIG_PATH: Path = Path(
    os.environ.get("OPENCLAW_CONFIG_DIR", Path.home() / ".openclaw")
) / "openclaw.json"

# 环境变量名称
ENV_AK_NAME = "FINANCE_TAX_API_KEY"
# 可选：网关/工具若要求 body 带 userId 时配置（与源舟 __userId__ 对应）
ENV_USER_ID_NAME = "FINANCE_TAX_USER_ID"

# 预发 1688 网关：测算类工具统一 POST /api/{toolCode}/1.0.0（与 ClawHub 工具码一致，见 SKILL.md）
TOOL_CODE_CALC_VAT = "ai_tax_calc_vat"
TOOL_CODE_CALC_ALL_TAXES = "ai_tax_calc_all"
TOOL_CODE_CALC_OVERALL = "ai_tax_calc_overall"
GATEWAY_TOOL_CALC_VAT = f"/api/{TOOL_CODE_CALC_VAT}/1.0.0"
GATEWAY_TOOL_CALC_ALL_TAXES = f"/api/{TOOL_CODE_CALC_ALL_TAXES}/1.0.0"
GATEWAY_TOOL_CALC_OVERALL = f"/api/{TOOL_CODE_CALC_OVERALL}/1.0.0"
