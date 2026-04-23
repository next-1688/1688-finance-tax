#!/usr/bin/env python3
"""
财税技能 API 认证模块

职责：从环境变量或配置文件读取 AK，生成 CSK 签名请求头。
"""

import hashlib
import hmac
import base64
import time
import uuid
import json
import os
from typing import Optional, Dict, Tuple
from urllib.parse import urlparse, parse_qs, quote
from _const import SKILL_VERSION, SKILL_NAME, OPENCLAW_CONFIG_PATH, ENV_AK_NAME

def extract_ak_keys(raw_input: str) -> Tuple[Optional[str], Optional[str]]:
    """
    从原始输入中提取 AccessKeyID 和 AccessKeySecret

    Args:
        raw_input: AK 环境变量的值

    Returns:
        (access_key_id, access_key_secret) 或 (None, None) 如果无效
    """
    try:
        decoded = base64.urlsafe_b64decode(raw_input).decode("utf-8")
        if decoded:
            raw_input = decoded
    except Exception:
        pass

    if not raw_input or len(raw_input) < 32:
        return None, None

    access_key_secret = raw_input[:32]
    access_key_id = raw_input[32:]

    return access_key_id, access_key_secret

def _get_ak_raw_from_config() -> Optional[str]:
    """从 OPENCLAW_CONFIG_PATH 读取 AK（Gateway 未重启时的 fallback）"""
    if not OPENCLAW_CONFIG_PATH.exists():
        return None
    try:
        with open(OPENCLAW_CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
        entries = config.get("skills", {}).get("entries", {})
        skill = entries.get(SKILL_NAME, {})
        ak = skill.get("apiKey") or skill.get("env", {}).get(ENV_AK_NAME, "")
        return ak if ak else None
    except Exception:
        return None

def get_ak_from_env() -> Tuple[Optional[str], Optional[str]]:
    """读取 AK：优先环境变量（OpenClaw 注入），其次配置文件（Gateway 未重启时 fallback）"""
    raw_input = os.environ.get(ENV_AK_NAME) or _get_ak_raw_from_config()
    if not raw_input:
        return None, None
    return extract_ak_keys(raw_input)

def get_content_md5(body: str) -> str:
    """计算 body 的 MD5 并 Base64 编码"""
    if not body:
        return ""
    md5_obj = hashlib.md5(body.encode('utf-8'))
    return base64.b64encode(md5_obj.digest()).decode('utf-8')

def get_canonicalized_resource(uri: str) -> str:
    """
    规范化资源路径

    例如：/api/v1/user?name=张三&age=20
    转换为：/api/v1/user?age=20&name=%E5%BC%A0%E4%B8%89
    """
    parsed_uri = urlparse(uri)
    path = parsed_uri.path
    query = parsed_uri.query

    if not query:
        return path

    params = parse_qs(query)
    sorted_keys = sorted(params.keys())

    canonical_query = []
    for key in sorted_keys:
        values = sorted(params[key])
        for value in values:
            encoded_key = quote(key, safe='')
            encoded_val = quote(value, safe='')
            canonical_query.append(f"{encoded_key}={encoded_val}")

    return f"{path}?{'&'.join(canonical_query)}"

def build_signature(
    method: str,
    uri: str,
    body: str,
    content_type: str,
    ak_id: str,
    ak_secret: str
) -> Dict[str, str]:
    """
    构建带签名的请求头

    Args:
        method: HTTP 方法 (GET/POST)
        uri: 请求路径（包含查询参数）
        body: 请求体 JSON 字符串
        content_type: Content-Type
        ak_id: Access Key ID
        ak_secret: Access Key Secret

    Returns:
        完整的请求头字典
    """
    timestamp = str(int(time.time()))
    nonce = uuid.uuid4().hex[:8]
    content_md5 = get_content_md5(body)

    csk_headers = {
        "x-csk-ak": ak_id,
        "x-csk-time": timestamp,
        "x-csk-nonce": nonce,
        "x-csk-content-md5": content_md5,
        "x-csk-version": SKILL_VERSION,
    }

    sorted_csk_keys = sorted(csk_headers.keys())
    canonicalized_headers = ""
    for key in sorted_csk_keys:
        canonicalized_headers += f"{key.lower()}:{csk_headers[key].strip()}\n"

    string_to_sign = (
        method.upper() + "\n" +
        content_md5 + "\n" +
        content_type + "\n" +
        timestamp + "\n" +
        canonicalized_headers +
        get_canonicalized_resource(uri)
    )

    signature = hmac.new(
        ak_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    sign_base64 = base64.b64encode(signature).decode('utf-8')

    headers = {
        "Content-Type": content_type,
        "x-csk-sign": sign_base64,
        **csk_headers,
    }

    return headers

def get_auth_headers(method: str, uri: str, body: str = "") -> Optional[Dict[str, str]]:
    """
    获取认证头（便捷函数）

    Args:
        method: HTTP 方法
        uri: 请求 URI
        body: 请求体（JSON字符串）

    Returns:
        请求头字典，如果 AK 未配置则返回 None
    """
    ak_id, ak_secret = get_ak_from_env()

    if not ak_id or not ak_secret:
        return None

    return build_signature(
        method=method,
        uri=uri,
        body=body,
        content_type="application/json",
        ak_id=ak_id,
        ak_secret=ak_secret,
    )