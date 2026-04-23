# 1688-finance-tax 分发说明

## 内容物

- **`SKILL.md`**：技能入口，列出能力范围并指向 `references/`。
- **`cli.py`**：统一 CLI 入口，自动发现并路由到各 capability。
- **`scripts/`**：Python 脚本层，包含 HTTP 客户端、认证、打点、各能力实现。
- **`references/`**：各场景操作细则与参数说明。
- **`reference.md`**：完整字段映射表（保留兼容）。
- **`examples.md`**：API 示例和响应格式（保留兼容）。

## 使用方（智能体 / 平台）

1. 将 **`SKILL.md`、`cli.py`、`scripts/` 与 `references/` 目录** 一并部署或挂载为同一路径层级，保证 `SKILL.md` 内相对链接可访问。
2. 对客侧须遵守技能内 **中文输出**、**免责声明**、**不暴露请求细节** 等约束。

## 版本与标识

- 技能包内常量固定：`SKILL_NAME: 1688-finance-tax`，`SKILL_VERSION: 1.0.0`。
- 升级接口或字段时，应同步更新 `references/` 中对应文件及本说明中的版本描述。

## TOOL 占位说明

当前版本中以下模块使用临时实现，后续 TOOL 上架后将替换：

| 模块 | 当前实现 | 后续替换为 |
|------|---------|-----------|
| `scripts/_http.py` | 直接 HTTP GET 调用预发 API | TOOL 调用 |
| `scripts/_tracker.py` | HTTP GET 打点上报 | TOOL 调用 |

替换时只需修改对应模块内部实现，各 `cmd.py` 调用方式不变。

## 维护流程建议

1. 修改能力参数或新增能力时，同步更新 `references/capabilities/` 中对应文档和 `SKILL.md` 命令速查表。
2. 发布前检查：`SKILL.md` 链接均可打开；`DISTRIBUTION.md` 与包内容一致。
