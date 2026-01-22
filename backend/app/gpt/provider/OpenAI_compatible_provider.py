import os
from typing import Optional, Union

import httpx
from openai import OpenAI

from app.utils.logger import get_logger

logging = get_logger(__name__)

# 需要使用代理的 API 域名列表
PROXY_DOMAINS = [
    "googleapis.com",
    "generativelanguage.googleapis.com",
    "openai.com",
    "api.openai.com",
]


def _needs_proxy(base_url: str) -> bool:
    """检查 base_url 是否需要使用代理"""
    if not base_url:
        return False
    for domain in PROXY_DOMAINS:
        if domain in base_url:
            return True
    return False


def _get_http_client(base_url: str) -> Optional[httpx.Client]:
    """根据 base_url 返回合适的 HTTP 客户端（带代理或不带）"""
    if not _needs_proxy(base_url):
        return None

    # 从环境变量获取代理配置
    proxy_url = os.getenv("LLM_PROXY") or os.getenv("HTTPS_PROXY") or os.getenv("HTTP_PROXY")
    if not proxy_url:
        return None

    logging.info(f"使用代理 {proxy_url} 访问 {base_url}")
    return httpx.Client(proxy=proxy_url)


class OpenAICompatibleProvider:
    def __init__(self, api_key: str, base_url: str, model: Union[str, None] = None):
        http_client = _get_http_client(base_url)
        self.client = OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
        self.model = model

    @property
    def get_client(self):
        return self.client

    @staticmethod
    def test_connection(api_key: str, base_url: str) -> bool:
        try:
            http_client = _get_http_client(base_url)
            client = OpenAI(api_key=api_key, base_url=base_url, http_client=http_client)
            model = client.models.list()
            logging.info("连通性测试成功")
            return True
        except Exception as e:
            logging.info(f"连通性测试失败：{e}")
            return False