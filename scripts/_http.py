#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
测算类 capability 使用 api_post 调用预发网关 `/api/{toolCode}/1.0.0`。
仍保留 api_get 供特殊查询场景使用。
不再各自处理 HTTP / 重试 / 错误解析。
"""

import json
import re
import time
import logging
from functools import wraps
from typing import Optional
from urllib.parse import quote

import os
import requests

from _auth import get_auth_headers
from _const import ENV_USER_ID_NAME
from _errors import AuthError, ParamError, RateLimitError, ServiceError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("finance_tax_http")

BASE_URL = "https://skills-gateway.1688.com"
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1

# ── 重试 ─────────────────────────────────────────────────────────────────────

def _with_retry(max_retries: int = MAX_RETRIES):
    """仅重试 ConnectionError / Timeout，其余异常直接传播"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError,
                        requests.exceptions.Timeout) as e:
                    last_exc = e
                    delay = min(RETRY_DELAY_BASE * (2 ** attempt), 10)
                    logger.warning("网络异常(尝试%d/%d): %s, %ds后重试",
                                   attempt + 1, max_retries, e, delay)
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            raise ServiceError(f"网络异常，已重试{max_retries}次: {last_exc}")
        return wrapper
    return decorator

# ── 错误映射 ──────────────────────────────────────────────────────────────────

def _handle_http_error(e: requests.exceptions.HTTPError):
    """HTTP 状态码 → SkillError"""
    status = e.response.status_code if e.response is not None else None
    if status == 401:
        raise AuthError("签名无效或已过期（401）")
    if status == 429:
        raise RateLimitError("请求被限流（429），请稍后重试")
    if status == 400:
        raise ParamError("请求参数不合法（400）")
    raise ServiceError(f"HTTP 错误 {status}")

def _handle_biz_error(result: dict):
    """业务错误（HTTP 200 但 success=false）→ SkillError"""
    msg_code = str(result.get("msgCode") or "")
    msg_info = result.get("msgInfo")

    code_match = re.search(r"\b(400|401|429|500)\b", msg_code)
    normalized = code_match.group(1) if code_match else ""

    if normalized == "401":
        raise AuthError("签名无效（401）")
    if normalized == "429":
        raise RateLimitError("请求被限流（429）")
    if normalized == "400":
        raise ParamError("请求参数不合法（400）")
    if normalized == "500":
        raise ServiceError("服务异常（500），请稍后重试")

    detail = (
        msg_info
        or msg_code
        or result.get("message")
        or result.get("code")
        or "未知业务错误"
    )
    raise ServiceError(str(detail))

# ── 公共请求 ──────────────────────────────────────────────────────────────────

@_with_retry()
def api_post(path: str, body: dict = None, timeout: int = 30) -> dict:
    """
    POST 请求财税 API（自动签名 + 重试 + 错误映射）

    Args:
        path:    API 路径
        body:    请求体 dict（会 json.dumps）
        timeout: 超时秒数

    Returns:
        API 响应中的 data 字段（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {}, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")
    # 勿改写 Content-Type：须与 get_auth_headers 参与签名的 application/json 完全一致，否则网关可能验签失败却只回空壳 JSON。
    user_id = os.environ.get(ENV_USER_ID_NAME, "").strip()
    if user_id:
        headers["x-api-userid"] = user_id

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()
    if result.get("success") is False:
        logger.warning(
            "网关 success=false: POST %s result=%s",
            url,
            json.dumps(result, ensure_ascii=False),
        )
        if not (headers.get("x-api-userid") or "").strip():
            logger.warning(
                "未带 x-api-userid 请求头；若平台要求用户维度，请设置环境变量 %s",
                ENV_USER_ID_NAME,
            )
        _handle_biz_error(result)

    model = result.get("data", {})
    if not isinstance(model, dict):
        raise ServiceError("API 返回结构异常（data 不是对象）")

    return model

@_with_retry()
def api_get(path: str, params: Optional[dict] = None, timeout: int = 30) -> dict:
    """
    GET 请求财税 API（自动签名 + 重试 + 错误映射）

    Args:
        path:    API 路径（含 query 时需传入完整 path+query，与签名一致）
        params:  查询参数 dict（会 json.dumps 后 URL 编码到 ?data= 参数）
        timeout: 超时秒数

    Returns:
        API 响应 JSON（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    # 将 params dict 转为 JSON 字符串，URL 编码后放到 ?data= 参数。
    # 签名串必须与真实请求的 path+query 一致，否则网关常返回 HTML 错误页，resp.json() 会失败。
    sign_uri = path
    if params:
        data_str = json.dumps(params, ensure_ascii=False)
        sign_uri = f"{path}?data={quote(data_str)}"
    url = f"{BASE_URL}{sign_uri}"

    headers = get_auth_headers("GET", sign_uri)
    if not headers:
        raise AuthError("AK 未配置")

    try:
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()

    has_error = result.get("hasError", False)
    if has_error:
        warning = result.get("warningMessage") or result.get("message") or "未知错误"
        raise ServiceError(str(warning))

    return result