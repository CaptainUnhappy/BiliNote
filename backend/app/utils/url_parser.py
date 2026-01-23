import re
from typing import Optional
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def extract_video_id(url: str, platform: str) -> Optional[str]:
    """
    从视频链接中提取视频 ID

    :param url: 视频链接
    :param platform: 平台名（bilibili / youtube / douyin）
    :return: 提取到的视频 ID 或 None
    """
    if platform == "bilibili":
        # 如果包含中文括号，则先清除括号及其内容
        url = re.sub(r"【.*?】", "", url).strip()

        # 如果是短链接，则解析真实链接
        if "b23.tv" in url:
            # 提取短链接 https://b23.tv/xxxxxx
            short_url_match = re.search(r"https?://b23\.tv/[0-9A-Za-z]+", url)
            if short_url_match:
                resolved_url = resolve_bilibili_short_url(short_url_match.group(0))
                if resolved_url:
                    url = resolved_url

        # 匹配 BV号（如 BV1vc411b7Wa）
        match = re.search(r"BV([0-9A-Za-z]+)", url)
        if match:
            bv_id = f"BV{match.group(1)}"
            # 检查是否有分P参数
            p_match = re.search(r"p=(\d+)", url)
            if p_match:
                return f"{bv_id}?p={p_match.group(1)}"
            return bv_id
        return None

    elif platform == "youtube":
        # 匹配 v=xxxxx 或 youtu.be/xxxxx，ID 长度通常为 11
        match = re.search(r"(?:v=|youtu\.be/)([0-9A-Za-z_-]{11})", url)
        return match.group(1) if match else None

    elif platform == "douyin":
        # 匹配 douyin.com/video/1234567890123456789
        match = re.search(r"/video/(\d+)", url)
        return match.group(1) if match else None

    return None


def resolve_bilibili_short_url(short_url: str) -> Optional[str]:
    """
    解析哔哩哔哩短链接以获取真实视频链接

    :param short_url: Bilibili短链接（如"https://b23.tv/xxxxxx"）
    :return: 真实的视频链接或None
    """
    try:
        response = requests.head(short_url, allow_redirects=True)
        final_url = response.url
        
        # 清理追踪参数，保留 p 参数
        parsed_url = urlparse(final_url)
        params = parse_qs(parsed_url.query)
        
        # 构造新的查询参数，只保留 p
        new_params = {}
        if 'p' in params:
            new_params['p'] = params['p']
            
        # 重新组合 URL
        new_query = urlencode(new_params, doseq=True)
        clean_url = urlunparse(parsed_url._replace(query=new_query))
        
        return clean_url
    except requests.RequestException as e:
        print(f"Error resolving short URL: {e}")
        return None


def normalize_bilibili_url(url: str) -> str:
    """
    标准化 Bilibili URL，处理短链接和中文括号
    
    :param url: 原始 URL
    :return: 标准化后的 URL
    """
    # 清除中文括号
    url = re.sub(r"【.*?】", "", url).strip()
    
    # 如果是短链接，解析为完整 URL
    if "b23.tv" in url:
        short_url_match = re.search(r"https?://b23\.tv/[0-9A-Za-z]+", url)
        if short_url_match:
            resolved_url = resolve_bilibili_short_url(short_url_match.group(0))
            if resolved_url:
                return resolved_url
    
    return url
