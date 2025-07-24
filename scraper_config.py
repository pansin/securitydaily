#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络安全新闻爬虫配置文件
"""

# RSS新闻源配置
NEWS_SOURCES = [
    {
        'name': '安全客',
        'rss_url': 'https://api.anquanke.com/data/v1/rss',
        'enabled': True,
        'weight': 1.0  # 权重，用于排序
    },
    {
        'name': 'FreeBuf',
        'rss_url': 'https://www.freebuf.com/feed',
        'enabled': True,
        'weight': 1.0
    },
    {
        'name': '嘶吼',
        'rss_url': 'https://www.4hou.com/feed',
        'enabled': True,
        'weight': 1.0
    },
    {
        'name': 'CSDN安全',
        'rss_url': 'https://www.csdn.net/rss/news',
        'enabled': False,  # 默认禁用，可根据需要启用
        'weight': 0.8
    }
]

# 安全关键词过滤
SECURITY_KEYWORDS = [
    # 基础安全词汇
    '安全', '漏洞', '攻击', '黑客', '病毒', '恶意软件', '勒索', '渗透',
    '防护', '防御', '加密', '解密', '隐私', '数据泄露', '网络安全',
    '信息安全', 'APT', 'DDoS', '钓鱼', '木马', '后门', '提权',
    
    # 英文安全词汇
    'security', 'vulnerability', 'attack', 'hacker', 'malware', 'ransomware',
    'phishing', 'encryption', 'decryption', 'privacy', 'breach', 'cyber',
    
    # 具体安全事件类型
    '安全漏洞', '安全事件', '安全威胁', '安全防护', '安全检测',
    '网络安全', '网络攻击', '网络防护', '网络威胁',
    '系统安全', '应用安全', '数据安全', '云安全',
    
    # 新兴威胁
    'AI安全', '人工智能安全', '机器学习安全', '深度学习安全',
    '区块链安全', '物联网安全', 'IoT安全', '移动安全',
    '零日漏洞', 'Zero-day', '供应链攻击', '供应链安全'
]

# 用户代理列表（轮换使用避免被封）
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
]

# 请求配置
REQUEST_CONFIG = {
    'timeout': 10,          # 请求超时时间（秒）
    'delay_range': (1, 3),  # 随机延时范围（秒）
    'max_retries': 3,       # 最大重试次数
    'retry_delay': 2        # 重试间隔（秒）
}

# 文件配置
FILE_CONFIG = {
    'output_dir': '.',                    # 输出目录
    'filename_pattern': 'news{date}.html', # 文件名模式
    'date_format': '%Y%m%d',              # 日期格式
    'encoding': 'utf-8'                   # 文件编码
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'news_scraper.log'
}
