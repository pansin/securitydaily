#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智谱GLM配置文件
"""

# 智谱GLM API配置
GLM_CONFIG = {
    # API密钥 - 请在 https://open.bigmodel.cn/ 获取
    'api_key': '',  # 请填入你的API密钥
    
    # API基础URL
    'base_url': 'https://open.bigmodel.cn/api/paas/v4/chat/completions',
    
    # 默认模型
    'default_model': 'glm-4-flash',  # 或者使用 'glm-4' 获得更好效果
    
    # 请求参数
    'temperature': 0.7,
    'max_tokens': 2000,
    'timeout': 30
}

# 新闻源配置
NEWS_SOURCES = [
    {
        'name': '安全客',
        'rss_url': 'https://api.anquanke.com/data/v1/rss',
        'enabled': True,
        'weight': 1.0
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
        'name': '安全内参',
        'rss_url': 'https://www.secrss.com/feed',
        'enabled': True,
        'weight': 0.8
    }
]

# 安全关键词
SECURITY_KEYWORDS = [
    # 中文关键词
    '安全', '漏洞', '攻击', '黑客', '病毒', '恶意软件', '勒索', '渗透',
    '防护', '防御', '加密', '解密', '隐私', '数据泄露', '网络安全',
    '信息安全', '网络攻击', '网络防护', '网络威胁', '安全漏洞',
    '安全事件', '安全威胁', '安全防护', '安全检测', '数据安全',
    '应用安全', '系统安全', '终端安全', '云安全', '移动安全',
    
    # 英文关键词
    'security', 'vulnerability', 'attack', 'hacker', 'malware', 'ransomware',
    'penetration', 'exploit', 'breach', 'threat', 'phishing', 'trojan',
    'backdoor', 'privilege', 'escalation', 'injection', 'XSS', 'CSRF',
    'APT', 'DDoS', 'botnet', 'zero-day', 'CVE', 'RCE', 'SSRF',
    'cybersecurity', 'infosec', 'netsec'
]

# 新闻分类配置
NEWS_CATEGORIES = {
    '焦点安全事件': {
        'icon': '🎯',
        'keywords': ['攻击', '事件', '泄露', '入侵', '勒索', '数据泄露', 'breach', 'attack', 'incident'],
        'description': '重大安全事件、攻击事件、数据泄露等'
    },
    '漏洞与威胁': {
        'icon': '⚠️',
        'keywords': ['漏洞', '威胁', 'CVE', 'RCE', 'vulnerability', 'threat', 'exploit'],
        'description': '新发现的漏洞、威胁分析、攻击技术等'
    },
    '产业动态': {
        'icon': '🚀',
        'keywords': ['发布', '政策', '法规', '标准', '产品', '融资', 'release', 'policy', 'regulation'],
        'description': '安全产品发布、政策法规、行业发展等'
    }
}

# 提示词模板
PROMPT_TEMPLATES = {
    'summary': """
请基于以下网络安全新闻标题，生成一份专业的今日摘要（200字以内）：

{news_text}

要求：
1. 总结今日网络安全态势的主要特点
2. 突出重点威胁和趋势
3. 语言专业、简洁
4. 体现时效性和权威性
5. 使用中文回答
""",
    
    'categorize': """
请将以下网络安全新闻按照威胁类型进行分类，并为每条新闻生成50字以内的专业分析：

{news_text}

请按以下格式输出JSON：
{{
    "焦点安全事件": [
        {{"title": "新闻标题", "analysis": "专业分析内容"}}
    ],
    "漏洞与威胁": [
        {{"title": "新闻标题", "analysis": "专业分析内容"}}
    ],
    "产业动态": [
        {{"title": "新闻标题", "analysis": "专业分析内容"}}
    ]
}}

分类标准：
- 焦点安全事件：重大安全事件、攻击事件、数据泄露等
- 漏洞与威胁：新发现的漏洞、威胁分析、攻击技术等
- 产业动态：安全产品发布、政策法规、行业发展等

要求：
1. 分析内容要专业、准确
2. 突出新闻的重要性和影响
3. 使用中文回答
4. 确保JSON格式正确
""",
    
    'analysis': """
请对以下网络安全新闻进行深度分析：

标题：{title}
摘要：{summary}

请从以下角度进行分析（100字以内）：
1. 威胁等级和影响范围
2. 技术原理和攻击手法
3. 防护建议和应对措施

要求：
1. 分析要专业、准确
2. 语言简洁明了
3. 突出实用性
4. 使用中文回答
"""
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'glm_news.log'
}