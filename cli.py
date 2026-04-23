#!/usr/bin/env python3
"""
1688-finance-tax —— 财税税负测算 统一入口

Commands:
    calc-vat        商品含税定价（仅增值税）
    calc-all-taxes  商品含税定价（四税联算）
    calc-overall    整体税负测算

面向用户展示时优先使用 markdown；Agent 追加分析时不要写入 markdown 正文。
"""

import json
import os
import sys
import importlib

SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts")
sys.path.insert(0, SCRIPTS_DIR)


def _discover_capabilities() -> dict:
    """扫描 capabilities/*/cmd.py，自动注册命令"""
    commands = {}
    capabilities_dir = os.path.join(SCRIPTS_DIR, "capabilities")

    if not os.path.isdir(capabilities_dir):
        return commands

    for name in sorted(os.listdir(capabilities_dir)):
        cmd_path = os.path.join(capabilities_dir, name, "cmd.py")
        if not os.path.isfile(cmd_path):
            continue
        module_path = f"capabilities.{name}.cmd"
        try:
            mod = importlib.import_module(module_path)
            cmd_name = getattr(mod, "COMMAND_NAME", name)
            commands[cmd_name] = module_path
        except Exception:
            pass

    return commands


def _usage(commands: dict):
    lines = ["**1688-finance-tax 用法**\n", "```"]
    for name in sorted(commands):
        try:
            mod = importlib.import_module(commands[name])
            desc = getattr(mod, "COMMAND_DESC", "")
            lines.append(f"  python3 cli.py {name:<16} {desc}")
        except Exception:
            lines.append(f"  python3 cli.py {name}")
    lines.append("```")

    print(json.dumps({
        "success": False,
        "data": {},
        "markdown": "\n".join(lines),
    }, ensure_ascii=False, indent=2))


def main():
    commands = _discover_capabilities()

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        _usage(commands)
        sys.exit(1)

    cmd = sys.argv[1]
    module_path = commands[cmd]

    # 与 88syt-skill 一致：子模块 argparse 只应看到「脚本名 + 子命令之后的参数」，避免把子命令名当成多余参数
    sys.argv = [f"cli.py {cmd}"] + sys.argv[2:]

    module = importlib.import_module(module_path)
    module.main()

    # 每次命令执行后上报埋点，失败不影响主流程
    try:
        from _tracker import report_skill_usage
        report_skill_usage()
    except Exception:
        pass

if __name__ == "__main__":
    main()
