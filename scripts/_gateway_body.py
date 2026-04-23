#!/usr/bin/env python3
"""
网关 POST 请求体公共字段（对齐 88syt-skill：site / skillName / skillVersion）。

测算类工具在源舟侧还要求 toolCode、可选 userId；公网调用时一并放入 body，便于网关路由与 HSF 入参组装。
"""

import os
from typing import Any, Dict

from _const import ENV_USER_ID_NAME, SITE, SKILL_NAME, SKILL_VERSION


def merge_gateway_skill_fields(payload: Dict[str, Any], tool_code: str) -> Dict[str, Any]:
    """
    在业务字段前合并技能与工具元数据，再剔除值为 None 的键。

    Args:
        payload:   业务字段（可能含 None，会在返回前统一过滤）
        tool_code: ClawHub 工具码，如 ai_tax_calc_vat
    """
    merged: Dict[str, Any] = {
        "site": SITE,
        "skillName": SKILL_NAME,
        "skillVersion": SKILL_VERSION,
        "toolCode": tool_code,
    }
    merged.update(payload)
    uid = os.environ.get(ENV_USER_ID_NAME, "").strip()
    if uid:
        merged["userId"] = uid
    return {k: v for k, v in merged.items() if v is not None}
