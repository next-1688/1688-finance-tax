#!/usr/bin/env python3
"""AK 配置命令 — CLI 入口"""

COMMAND_NAME = "configure"
COMMAND_DESC = "配置 AK"

import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_output, print_error
from capabilities.configure.service import (
    validate_ak, configure_via_gateway, configure_via_file, check_existing_config,
)


def _mask_ak(api_key: str) -> str:
    if len(api_key) >= 8:
        return f"{api_key[:4]}****{api_key[-4:]}"
    return "****"


def main():
    try:
        has_existing, existing_ak = check_existing_config()

        # 无参数 → 查看状态
        if len(sys.argv) < 2:
            if has_existing:
                source = ("环境变量（已生效）" if os.environ.get("FINANCE_TAX_API_KEY")
                          else "OpenClaw 配置（新会话/重载后生效）")
                markdown = f"✅ AK 已配置: `{_mask_ak(existing_ak)}`（来源: {source}）"
            else:
                markdown = "❌ 尚未配置 AK\n\n运行: `cli.py configure YOUR_AK`"
            print_output(has_existing, markdown, {"configured": has_existing})
            return

        api_key = sys.argv[1].strip()
        is_valid, error_message = validate_ak(api_key)
        if not is_valid:
            print_output(False, f"❌ {error_message}", {"configured": False})
            return

        write_ok = configure_via_gateway(api_key) or configure_via_file(api_key)
        if not write_ok:
            print_output(
                False,
                "❌ AK 写入失败，请检查 Gateway 状态或文件权限",
                {"configured": False},
            )
            return

        markdown = (
            f"✅ AK 已保存: `{_mask_ak(api_key)}`\n\n"
            "后续由 OpenClaw 配置注入生效。\n\n"
            "若当前会话仍提示 AK 未配置，请新开会话或执行：`openclaw secrets reload`"
        )
        print_output(True, markdown, {"configured": True})
    except Exception as exc:
        print_error(exc, {"configured": False})


if __name__ == "__main__":
    main()
