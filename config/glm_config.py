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

翻译要求：
- 英文标题必须翻译成中文
- 技术术语统一翻译：Zero-Day→零日漏洞，Vulnerability→漏洞，Ransomware→勒索软件
- 公司产品名保留英文但加中文说明

请按以下格式输出JSON：
{{
    "selected_news": [
        {{
            "title": "中文新闻标题（如果原文是英文则翻译）",
            "source": "新闻来源",
            "region": "地区",
            "importance": "重要性评分(1-10)",
            "reason": "中文入选理由"
        }}
    ]
}}

要求：
1. 必须精选10篇新闻
2. 确保全球视野，包含国际新闻
3. 所有输出必须使用中文
4. 英文新闻标题必须翻译成中文
5. 确保JSON格式正确
""",

    'summary': """
请基于以下精选的全球网络安全新闻，生成一份专业的今日全球安全态势摘要（250字以内）：

{news_text}

要求：
1. 体现全球网络安全态势特点
2. 突出重点威胁、事件和趋势
3. 语言专业、权威、简洁
4. 体现国际视野和时效性
5. 必须使用中文回答，所有英文内容都要翻译成中文
6. 英文专业术语要提供中文翻译，如"Zero-Day"翻译为"零日漏洞"
7. 英文公司名、产品名保留原文但加中文说明，如"Microsoft SharePoint(微软SharePoint)"
""",
    
    'categorize_and_summarize': """
请将以下精选的全球网络安全新闻按照四个维度进行分类，并为每条新闻生成详细的200-300字内容总结。

重要提醒：每条新闻的summary字段必须是详细的200-300字总结，不能是简单的一句话概括！

{news_text}

重要翻译要求：
1. 所有英文内容必须翻译成中文
2. 新闻标题必须翻译成中文，如"Microsoft SharePoint Zero-Day"翻译为"微软SharePoint零日漏洞"
3. 技术术语翻译：Zero-Day→零日漏洞，Vulnerability→漏洞，Exploit→利用，Ransomware→勒索软件
4. 公司产品名保留英文但加中文说明：Microsoft SharePoint(微软SharePoint)
5. 内容总结必须用中文描述，不能出现英文句子

请按以下格式输出JSON：
{{
    "安全风险": [
        {{
            "title": "中文新闻标题",
            "source": "新闻来源",
            "region": "地区",
            "summary": "包含时间、地点、人物、事件、原因、影响的详细中文总结（200-300字，必须包含具体技术细节、影响范围、解决方案等完整信息）",
            "key_points": ["中文关键点1", "中文关键点2", "中文关键点3"],
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

关键要求（必须严格遵守）：
1. 每条新闻的summary字段必须是详细的200-300字总结，绝不能少于200字！必须包含：
   - 具体发生时间和事件背景
   - 详细的技术细节（漏洞编号、CVSS评分、影响版本等）
   - 攻击手法和技术原理的详细描述
   - 具体的影响范围和受影响的系统/用户数量
   - 厂商的具体响应措施和修复方案
   - 详细的安全建议和防护措施
   - 相关的数字、统计数据和具体信息
2. 英文新闻必须完全转换为中文阐述，不能出现任何英文句子
3. 避免简单概括，必须提供丰富的细节信息
4. 每个summary必须包含具体的数字、时间、版本号、CVE编号等关键信息
5. 确保JSON格式完全正确，不要有语法错误
6. 如果原始新闻内容不足200字，请基于技术背景进行合理扩展
""",

    'translate_and_analyze': """
请将以下英文网络安全新闻翻译成中文并进行专业分析：

标题：{title}
内容：{content}
来源：{source}

请按以下格式输出JSON：
{{
    "chinese_title": "中文标题",
    "summary": "详细中文内容摘要（200-300字，包含具体技术细节、影响范围、解决方案等完整信息）",
    "key_points": [
        "关键点1（中文）",
        "关键点2（中文）",
        "关键点3（中文）"
    ],
    "impact_analysis": "影响分析（中文）",
    "threat_level": "威胁等级（高危/中危/低危）"
}}

翻译要求：
1. 标题必须翻译成准确的中文
2. 技术术语统一翻译：
   - Zero-Day → 零日漏洞
   - Vulnerability → 漏洞  
   - Exploit → 利用
   - Ransomware → 勒索软件
   - Malware → 恶意软件
   - Phishing → 钓鱼攻击
   - APT → 高级持续性威胁
3. 公司产品名保留英文但加中文说明
4. 所有分析内容必须用中文表述
5. 确保专业性和准确性
"""
}

# 日志配置
LOG_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'glm_news.log'
}