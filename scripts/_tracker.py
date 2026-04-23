#!/usr/bin/env python3
"""
Skill 埋点上报

职责：每次 CLI 命令执行时，向 skill 网关上报一次调用记录，用于统计 skill 调用次数。
上报失败不影响主流程，静默处理。

环境变量（从项目根目录 .env 读取）：
    SKILL_NAME     skill 名称，默认 1688-finance-tax
    SKILL_VERSION  skill 版本，默认 1.0.0
    SKILL_CHANNEL  发布渠道，默认 clawhub
"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger("finance_tax_tracker")

# 项目根目录（scripts/ 的上一级）
_ROOT_DIR = Path(__file__).parent.parent

def _load_env_file() -> None:
    """解析项目根目录的 .env 文件，将变量注入 os.environ（已有环境变量不覆盖）。"""
    env_path = _ROOT_DIR / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key and key not in os.environ:
                os.environ[key] = value

# 模块加载时解析一次 .env
_load_env_file()

def _get_skill_env() -> tuple:
    """读取 skill 基础信息，返回 (skill_name, skill_version, channel)。"""
    skill_name = os.environ.get("SKILL_NAME", "1688-finance-tax")
    skill_version = os.environ.get("SKILL_VERSION", "1.0.0")
    channel = os.environ.get("SKILL_CHANNEL", "clawhub")
    return skill_name, skill_version, channel

def report_skill_usage() -> None:
    """
    上报 skill 调用次数到网关。

    调用时机：每次 CLI 命令执行时调用一次（在 cli.py 的 main() 中触发）。
    失败时静默处理，不抛出异常，不影响主流程。
    """
    try:
        from _http import api_post
        skill_name, skill_version, channel = _get_skill_env()
        api_post(
            "/api/reportSkillsUsage/1.0.0",
            {
                "apiName": None,
                "skillsName": skill_name,
                "version": skill_version,
                "scene": "CLI",
                "channel": channel,
            },
        )
    except Exception as exc:
        logger.debug("埋点上报失败（已忽略）: %s", exc)