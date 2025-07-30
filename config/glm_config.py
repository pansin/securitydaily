#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智谱GLM配置文件 - 修复版
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

# 新闻源配置 - 全球主流网络安全新闻网站
NEWS_SOURCES = [
    # 中文安全媒体
    {
        'name': '安全客',
        'rss_url': 'https://api.anquanke.com/data/v1/rss',
        'enabled': True,
        'weight': 1.0,
        'language': 'zh',
        'region': 'CN'
    },
    {
        'name': 'FreeBuf',
        'rss_url': 'https://www.freebuf.com/feed',
        'enabled': True,
        'weight': 1.0,
        'language': 'zh',
        'region': 'CN'
    },
    {
        'name': '嘶吼',
        'rss_url': 'https://www.4hou.com/feed',
        'enabled': True,
        'weight': 1.0,
        'language': 'zh',
        'region': 'CN'
    },
    
    # 国际顶级安全媒体
    {
        'name': 'Krebs on Security',
        'rss_url': 'https://krebsonsecurity.com/feed/',
        'enabled': True,
        'weight': 1.2,
        'language': 'en',
        'region': 'US'
    },
    {
        'name': 'The Hacker News',
        'rss_url': 'https://feeds.feedburner.com/TheHackersNews',
        'enabled': True,
        'weight': 1.1,
        'language': 'en',
        'region': 'US'
    },
    {
        'name': 'Bleeping Computer',
        'rss_url': 'https://www.bleepingcomputer.com/feed/',
        'enabled': True,
        'weight': 1.0,
        'language': 'en',
        'region': 'US'
    },
    {
        'name': 'Security Week',
        'rss_url': 'https://www.securityweek.com/feed/',
        'enabled': True,
        'weight': 1.0,
        'language': 'en',
        'region': 'US'
    },
    {
        'name': 'Dark Reading',
        'rss_url': 'https://www.darkreading.com/rss.xml',
        'enabled': True,
        'weight': 1.0,
        'language': 'en',
        'region': 'US'
    }
]

# 安全关键词
SECURITY_KEYWORDS = [
    # 中文关键词
    '安全', '漏洞', '攻击', '黑客', '病毒', '恶意软件', '勒索', '渗透',
    '防护', '防御', '加密', '解密', '隐私', '数据泄露', '网络安全',
    '信息安全', '网络攻击', '网络防护', '网络威胁', '安全漏洞',
    '安全事件', '安全威胁', '安全防护', '安全检测', '数据安全',
    
    # 英文关键词
    'security', 'vulnerability', 'attack', 'hacker', 'malware', 'ransomware',
    'penetration', 'exploit', 'breach', 'threat', 'phishing', 'trojan',
    'backdoor', 'privilege', 'escalation', 'injection', 'XSS', 'CSRF',
    'APT', 'DDoS', 'botnet', 'zero-day', 'CVE', 'RCE', 'SSRF',
    'cybersecurity', 'infosec', 'netsec'
]

# 新闻分类配置 - 四个维度
NEWS_CATEGORIES = {
    '安全风险': {
        'icon': 'warning',
        'keywords': ['漏洞', '威胁', 'CVE', 'RCE', 'vulnerability', 'threat', 'exploit', 'zero-day', '0day', '风险'],
        'description': '安全漏洞、威胁情报、风险评估等'
    },
    '安全事件': {
        'icon': 'alert',
        'keywords': ['攻击', '事件', '泄露', '入侵', '勒索', '数据泄露', 'breach', 'attack', 'incident', 'hack'],
        'description': '网络攻击事件、数据泄露、安全事故等'
    },
    '安全舆情': {
        'icon': 'megaphone',
        'keywords': ['政策', '法规', '监管', '合规', '标准', 'policy', 'regulation', 'compliance', '舆论', '报告'],
        'description': '政策法规、行业报告、舆论动态等'
    },
    '安全趋势': {
        'icon': 'trending',
        'keywords': ['趋势', '发展', '技术', '创新', '产品', '融资', 'trend', 'innovation', 'technology', '未来'],
        'description': '技术趋势、产业发展、创新动态等'
    }
}

# 提示词模板
PROMPT_TEMPLATES = {
    'select_top_news': """
请从以下全球网络安全新闻中精选出最重要的10篇新闻，要求覆盖全球视野，不能仅限于中国新闻：

{news_text}

精选标准：
1. 新闻重要性和影响力
2. 全球性和代表性
3. 时效性和关注度
4. 覆盖不同地区和类型
5. 平衡中英文新闻源

请按以下格式输出JSON：
{{
    "selected_news": [
        {{
            "title": "新闻标题",
            "source": "新闻来源",
            "region": "地区",
            "importance": "重要性评分(1-10)",
            "reason": "入选理由"
        }}
    ]
}}

要求：
1. 必须精选10篇新闻
2. 确保全球视野，包含国际新闻
3. 使用中文回答
4. 确保JSON格式正确
""",

    'summary': """
请基于以下精选的全球网络安全新闻，生成一份专业的今日全球安全态势摘要（250字以内）：

{news_text}

要求：
1. 体现全球网络安全态势特点
2. 突出重点威胁、事件和趋势
3. 语言专业、权威、简洁
4. 体现国际视野和时效性
5. 使用中文回答
""",
    
    'categorize_and_summarize': """
请将以下精选的全球网络安全新闻按照四个维度进行分类，并为每条新闻生成包含关键要素的完整内容总结：

{news_text}

请按以下格式输出JSON：
{{
    "安全风险": [
        {{
            "title": "新闻标题",
            "source": "新闻来源",
            "region": "地区",
            "summary": "包含时间、地点、人物、事件、原因、影响的完整总结（150字以内）",
            "key_points": ["关键点1", "关键点2", "关键点3"],
            "impact_level": "影响等级（高/中/低）"
        }}
    ],
    "安全事件": [],
    "安全舆情": [],
    "安全趋势": []
}}

分类标准：
- 安全风险：漏洞披露、威胁情报、风险评估等
- 安全事件：网络攻击、数据泄露、安全事故等  
- 安全舆情：政策法规、行业报告、舆论动态等
- 安全趋势：技术趋势、产业发展、创新动态等

要求：
1. 每条新闻的summary必须包含新闻关键要素（5W1H）
2. 英文新闻必须转换为中文阐述
3. 总结要专业、准确、完整
4. 确保全球视野，不仅限于中国新闻
5. 确保JSON格式正确
"""
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'glm_news.log'
}