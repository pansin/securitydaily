#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于智谱GLM的网络安全新闻生成器
参考：https://docs.bigmodel.cn/cn/best-practice/creativepractice/aimorningnewspaper
"""

import requests
import json
from datetime import datetime, timedelta
import logging
import os
from typing import List, Dict
import feedparser
from bs4 import BeautifulSoup
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('glm_news.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GLMNewsGenerator:
    def __init__(self, api_key: str = None):
        """
        初始化GLM新闻生成器
        
        Args:
            api_key: 智谱GLM API密钥
        """
        self.api_key = api_key or os.getenv('GLM_API_KEY')
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 新闻源配置
        self.news_sources = [
            {
                'name': '安全客',
                'rss_url': 'https://api.anquanke.com/data/v1/rss',
                'weight': 1.0
            },
            {
                'name': 'FreeBuf',
                'rss_url': 'https://www.freebuf.com/feed',
                'weight': 1.0
            },
            {
                'name': '嘶吼',
                'rss_url': 'https://www.4hou.com/feed',
                'weight': 1.0
            }
        ]
        
        self.security_keywords = [
            '安全', '漏洞', '攻击', '黑客', '病毒', '恶意软件', '勒索', '渗透',
            '防护', '防御', '加密', '解密', '隐私', '数据泄露', '网络安全',
            'APT', 'DDoS', '钓鱼', '木马', '后门', '提权', 'CVE', 'RCE'
        ]
    
    def call_glm_api(self, prompt: str, model: str = "glm-4-flash") -> str:
        """
        调用智谱GLM API
        
        Args:
            prompt: 输入提示词
            model: 使用的模型名称
            
        Returns:
            生成的文本内容
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"GLM API调用失败: {response.status_code} - {response.text}")
                return ""
                
        except Exception as e:
            logger.error(f"GLM API调用异常: {e}")
            return ""
    
    def fetch_article_content(self, url: str, max_length: int = 2000) -> str:
        """
        抓取文章完整内容
        
        Args:
            url: 文章链接
            max_length: 最大内容长度
            
        Returns:
            文章内容
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除不需要的标签
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
                tag.decompose()
            
            # 尝试找到主要内容区域
            content_selectors = [
                'article', '.article-content', '.post-content', '.entry-content',
                '.content', '.main-content', '.article-body', '.post-body',
                '[role="main"]', '.story-body', '.article-text'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = elements[0].get_text(strip=True)
                    break
            
            # 如果没有找到特定的内容区域，使用整个body
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(strip=True)
            
            # 清理和截断内容
            if content:
                # 移除多余的空白字符
                content = ' '.join(content.split())
                # 截断到指定长度
                if len(content) > max_length:
                    content = content[:max_length] + "..."
            
            return content
            
        except Exception as e:
            logger.warning(f"抓取文章内容失败 {url}: {e}")
            return ""
    
    def fetch_security_news(self, days_back: int = 1) -> List[Dict]:
        """
        抓取网络安全新闻
        
        Args:
            days_back: 抓取几天前的新闻
            
        Returns:
            新闻列表
        """
        target_date = (datetime.now() - timedelta(days=days_back)).date()
        all_news = []
        
        logger.info(f"开始抓取 {target_date} 的网络安全新闻...")
        
        for source in self.news_sources:
            if not source.get('enabled', True):
                continue
                
            try:
                logger.info(f"正在抓取 {source['name']} ({source.get('region', 'Unknown')}) 的RSS源...")
                
                # 设置请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # 获取RSS内容
                response = requests.get(source['rss_url'], headers=headers, timeout=15)
                feed = feedparser.parse(response.content)
                source_news = []
                
                for entry in feed.entries:
                    # 解析发布时间
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6]).date()
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6]).date()
                    
                    # 检查是否为目标日期的新闻（允许3天内的新闻）
                    if pub_date and (datetime.now().date() - pub_date).days <= 3:
                        # 检查是否为安全相关新闻
                        title = entry.title.lower()
                        summary = getattr(entry, 'summary', '').lower()
                        
                        # 扩展关键词匹配逻辑
                        is_security_related = any(keyword.lower() in title or keyword.lower() in summary 
                                                for keyword in self.security_keywords)
                        
                        if is_security_related:
                            # 获取文章完整内容
                            full_content = ""
                            if hasattr(entry, 'content') and entry.content:
                                # RSS中包含内容
                                full_content = entry.content[0].value if isinstance(entry.content, list) else str(entry.content)
                                # 清理HTML标签
                                soup = BeautifulSoup(full_content, 'html.parser')
                                full_content = soup.get_text(strip=True)
                            elif entry.link:
                                # 抓取完整文章内容
                                logger.info(f"正在抓取文章内容: {entry.title[:50]}...")
                                full_content = self.fetch_article_content(entry.link)
                            
                            news_item = {
                                'title': entry.title,
                                'link': entry.link,
                                'summary': getattr(entry, 'summary', ''),
                                'content': full_content,
                                'published_date': pub_date,
                                'source': source['name'],
                                'weight': source['weight'],
                                'language': source.get('language', 'en'),
                                'region': source.get('region', 'Unknown')
                            }
                            source_news.append(news_item)
                
                logger.info(f"从 {source['name']} 获取到 {len(source_news)} 条安全新闻")
                all_news.extend(source_news)
                
                # 避免请求过于频繁
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"抓取 {source['name']} 失败: {e}")
                continue
        
        # 去重和排序
        unique_news = []
        seen_titles = set()
        
        for news in all_news:
            # 使用标题的前50个字符进行去重，避免完全相同的标题
            title_key = news['title'][:50].lower()
            if title_key not in seen_titles:
                unique_news.append(news)
                seen_titles.add(title_key)
        
        # 按权重和时间排序，取前15条（增加数量以获得更好的选择）
        unique_news.sort(key=lambda x: (x['weight'], x['published_date']), reverse=True)
        
        logger.info(f"总共获取到 {len(unique_news)} 条不重复的安全新闻")
        return unique_news[:15]
    
    def generate_news_analysis(self, news_list: List[Dict]) -> Dict:
        """
        使用GLM生成新闻分析和摘要
        
        Args:
            news_list: 新闻列表
            
        Returns:
            包含分析内容的字典
        """
        if not news_list:
            return {"summary": "今日暂无网络安全新闻", "categories": {}}
        
        # 构建包含内容的新闻信息
        news_details = []
        for i, news in enumerate(news_list):
            content_preview = ""
            if news.get('content'):
                # 取内容的前300字符作为预览
                content_preview = news['content'][:300] + "..." if len(news['content']) > 300 else news['content']
            elif news.get('summary'):
                content_preview = news['summary']
            
            news_detail = f"{i+1}. 【{news['source']}】{news['title']}\n"
            if content_preview:
                news_detail += f"   内容摘要: {content_preview}\n"
            news_details.append(news_detail)
        
        news_text = "\n".join(news_details)
        
        # 生成今日摘要
        summary_prompt = f"""
请基于以下全球网络安全新闻信息，生成一份专业的今日全球安全态势摘要（250字以内）：

{news_text}

要求：
1. 总结全球网络安全态势的主要特点和趋势
2. 突出重点威胁、攻击事件和技术发展
3. 体现国际视野和专业深度
4. 语言专业、权威、简洁
5. 必须使用中文回答
"""
        
        summary = self.call_glm_api(summary_prompt)
        
        # 对新闻进行智能分类分析
        category_prompt = f"""
请将以下全球网络安全新闻按照威胁类型进行智能分类，并为每条新闻生成80字以内的专业深度分析：

{news_text}

请按以下格式输出JSON：
{{
    "重大安全事件": [
        {{"title": "新闻标题", "analysis": "深度分析内容", "source": "新闻来源", "severity": "威胁等级"}}
    ],
    "漏洞与威胁情报": [
        {{"title": "新闻标题", "analysis": "深度分析内容", "source": "新闻来源", "severity": "威胁等级"}}
    ],
    "技术与产业动态": [
        {{"title": "新闻标题", "analysis": "深度分析内容", "source": "新闻来源", "severity": "威胁等级"}}
    ],
    "政策与合规": [
        {{"title": "新闻标题", "analysis": "深度分析内容", "source": "新闻来源", "severity": "威胁等级"}}
    ]
}}

分类标准：
- 重大安全事件：数据泄露、网络攻击、安全事故等
- 漏洞与威胁情报：CVE漏洞、恶意软件、攻击技术、威胁分析等
- 技术与产业动态：安全产品、技术创新、行业发展、投资并购等
- 政策与合规：法律法规、政策标准、合规要求等

威胁等级：高危、中危、低危、信息

要求：
1. 分析要深入专业，体现技术深度
2. 突出新闻的重要性、影响范围和应对建议
3. 威胁等级评估要准确
4. 必须使用中文回答
5. 确保JSON格式正确
"""
        
        category_result = self.call_glm_api(category_prompt)
        
        # 解析分类结果
        categories = {}
        try:
            categories = json.loads(category_result)
        except Exception as e:
            logger.warning(f"分类结果解析失败: {e}，使用默认分类")
            # 默认分类逻辑
            categories = self._default_categorize_news(news_list)
        
        return {
            "summary": summary,
            "categories": categories,
            "total_news": len(news_list),
            "sources": list(set([news['source'] for news in news_list])),
            "regions": list(set([news.get('region', 'Unknown') for news in news_list]))
        }
    
    def _default_categorize_news(self, news_list: List[Dict]) -> Dict:
        """
        默认新闻分类逻辑（当AI分类失败时使用）
        """
        categories = {
            "重大安全事件": [],
            "漏洞与威胁情报": [],
            "技术与产业动态": [],
            "政策与合规": []
        }
        
        # 基于关键词的简单分类
        for news in news_list:
            title_lower = news['title'].lower()
            content_lower = (news.get('content', '') + news.get('summary', '')).lower()
            
            analysis = f"来源：{news['source']} | " + (news.get('summary', '暂无详细摘要')[:100] + "..." if len(news.get('summary', '')) > 100 else news.get('summary', '暂无详细摘要'))
            
            item = {
                "title": news['title'],
                "analysis": analysis,
                "source": news['source'],
                "severity": "中危"
            }
            
            # 简单的关键词分类
            if any(keyword in title_lower or keyword in content_lower for keyword in 
                   ['breach', 'attack', 'hack', '攻击', '泄露', '入侵', '勒索']):
                categories["重大安全事件"].append(item)
            elif any(keyword in title_lower or keyword in content_lower for keyword in 
                     ['vulnerability', 'cve', 'exploit', '漏洞', '威胁', 'malware']):
                categories["漏洞与威胁情报"].append(item)
            elif any(keyword in title_lower or keyword in content_lower for keyword in 
                     ['policy', 'regulation', 'compliance', '政策', '法规', '合规']):
                categories["政策与合规"].append(item)
            else:
                categories["技术与产业动态"].append(item)
        
        return categories
    
    def generate_html_report(self, analysis_result: Dict, date_str: str) -> str:
        """
        生成HTML格式的新闻快报
        
        Args:
            analysis_result: 分析结果
            date_str: 日期字符串
            
        Returns:
            HTML内容
        """
        current_time = datetime.now().strftime('%Y年%m月%d日')
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>海之安网络安全日报 - {current_time}</title>
  
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    body {{
      font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
      color: #f1f5f9;
      min-height: 100vh;
      padding: 20px;
      line-height: 1.6;
    }}
    
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(59, 130, 246, 0.3);
      border-radius: 16px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }}
    
    .header {{
      background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
      border-bottom: 1px solid rgba(59, 130, 246, 0.3);
      padding: 40px;
      text-align: center;
      position: relative;
    }}
    
    .header::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
    }}
    
    .logo {{
      width: 200px;
      height: auto;
      margin-bottom: 20px;
    }}
    
    .title {{
      font-size: 36px;
      font-weight: 700;
      background: linear-gradient(135deg, #3b82f6, #8b5cf6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 16px;
    }}
    
    .subtitle {{
      font-size: 18px;
      color: #94a3b8;
      margin-bottom: 8px;
    }}
    
    .content {{
      padding: 40px;
    }}
    
    .summary-section {{
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 32px;
    }}
    
    .summary-title {{
      font-size: 20px;
      font-weight: 600;
      color: #3b82f6;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    
    .summary-title::before {{
      content: '📊';
      font-size: 24px;
    }}
    
    .summary-content {{
      color: #cbd5e1;
      line-height: 1.8;
      font-size: 16px;
    }}
    
    .category-section {{
      margin-bottom: 40px;
      background: rgba(30, 41, 59, 0.4);
      border-radius: 12px;
      border: 1px solid rgba(59, 130, 246, 0.15);
      overflow: hidden;
    }}
    
    .category-header {{
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 51, 234, 0.2));
      padding: 20px 24px;
      border-bottom: 1px solid rgba(59, 130, 246, 0.3);
    }}
    
    .category-title {{
      font-size: 24px;
      font-weight: 600;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    
    .category-news {{
      padding: 24px;
    }}
    
    .news-item {{
      background: rgba(51, 65, 85, 0.6);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      transition: all 0.3s ease;
      position: relative;
    }}
    
    .news-item::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: linear-gradient(180deg, #3b82f6, #8b5cf6);
      border-radius: 2px 0 0 2px;
    }}
    
    .news-item:hover {{
      border-color: rgba(59, 130, 246, 0.4);
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }}
    
    .news-title {{
      font-size: 18px;
      font-weight: 600;
      color: #f1f5f9;
      margin-bottom: 12px;
      line-height: 1.4;
    }}
    
    .news-analysis {{
      color: #cbd5e1;
      line-height: 1.7;
      font-size: 15px;
    }}
    
    .footer {{
      background: rgba(15, 23, 42, 0.8);
      border-top: 1px solid rgba(59, 130, 246, 0.3);
      padding: 24px 40px;
      text-align: center;
      color: #64748b;
      font-size: 14px;
    }}
    
    .stats-section {{
      margin-bottom: 32px;
    }}
    
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 20px;
    }}
    
    .stat-card {{
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
      border-color: rgba(59, 130, 246, 0.4);
      transform: translateY(-2px);
    }}
    
    .stat-number {{
      font-size: 32px;
      font-weight: 700;
      color: #3b82f6;
      margin-bottom: 8px;
    }}
    
    .stat-label {{
      font-size: 14px;
      color: #94a3b8;
    }}
    
    .news-header {{
      margin-bottom: 12px;
    }}
    
    .news-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
      font-size: 12px;
    }}
    
    .news-source {{
      color: #94a3b8;
      background: rgba(59, 130, 246, 0.1);
      padding: 4px 8px;
      border-radius: 4px;
    }}
    
    .severity-badge {{
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: 600;
      font-size: 11px;
    }}
    
    .severity-high {{
      background: rgba(239, 68, 68, 0.2);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    .severity-medium {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .severity-low {{
      background: rgba(34, 197, 94, 0.2);
      color: #86efac;
      border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    
    .severity-info {{
      background: rgba(59, 130, 246, 0.2);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}
    
    .icon-critical::before {{ content: '🚨'; }}
    .icon-focus::before {{ content: '🎯'; }}
    .icon-risk::before {{ content: '⚠️'; }}
    .icon-innovation::before {{ content: '🚀'; }}
    .icon-policy::before {{ content: '📋'; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <svg class="logo" viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#3B82F6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06B6D4;stop-opacity:1" />
          </linearGradient>
        </defs>
        <circle cx="40" cy="60" r="25" fill="url(#logoGradient)" opacity="0.8"/>
        <circle cx="25" cy="35" r="15" fill="url(#logoGradient)" opacity="0.9"/>
        <circle cx="55" cy="35" r="12" fill="url(#logoGradient)" opacity="0.7"/>
        <circle cx="35" cy="75" r="10" fill="url(#logoGradient)" opacity="0.6"/>
        <circle cx="60" cy="75" r="8" fill="url(#logoGradient)" opacity="0.8"/>
        <text x="90" y="45" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#3b82f6">ocean security</text>
        <text x="90" y="70" font-family="Arial, sans-serif" font-size="12" fill="#94a3b8">海之安，数字安全专家</text>
      </svg>
      <h1 class="title">海之安网络安全日报</h1>
      <div class="subtitle">{current_time} · AI智能生成</div>
    </div>
    
    <div class="content">
      <div class="summary-section">
        <h2 class="summary-title">今日摘要</h2>
        <div class="summary-content">{analysis_result.get('summary', '今日暂无网络安全新闻摘要')}</div>
      </div>
"""
        
        # 添加统计信息
        sources = analysis_result.get('sources', [])
        regions = analysis_result.get('regions', [])
        
        html_template += f"""
      <div class="stats-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">{analysis_result.get('total_news', 0)}</div>
            <div class="stat-label">全球安全新闻</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{len(sources)}</div>
            <div class="stat-label">新闻来源</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{len(regions)}</div>
            <div class="stat-label">覆盖地区</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{len(analysis_result.get('categories', {}))}</div>
            <div class="stat-label">威胁分类</div>
          </div>
        </div>
      </div>
"""
        
        # 添加分类新闻
        icon_map = {
            "重大安全事件": "icon-critical",
            "漏洞与威胁情报": "icon-risk", 
            "技术与产业动态": "icon-innovation",
            "政策与合规": "icon-policy"
        }
        
        for category, news_items in analysis_result.get('categories', {}).items():
            if news_items:
                icon_class = icon_map.get(category, "icon-focus")
                html_template += f"""
      <div class="category-section">
        <div class="category-header">
          <h2 class="category-title {icon_class}">{category}</h2>
        </div>
        <div class="category-news">
"""
                
                for item in news_items:
                    severity = item.get('severity', '中危')
                    severity_class = {
                        '高危': 'severity-high',
                        '中危': 'severity-medium', 
                        '低危': 'severity-low',
                        '信息': 'severity-info'
                    }.get(severity, 'severity-medium')
                    
                    html_template += f"""          <div class="news-item">
            <div class="news-header">
              <div class="news-title">{item['title']}</div>
              <div class="news-meta">
                <span class="news-source">{item.get('source', '未知来源')}</span>
                <span class="severity-badge {severity_class}">{severity}</span>
              </div>
            </div>
            <div class="news-analysis"><strong>AI深度分析：</strong>{item['analysis']}</div>
          </div>
"""
                
                html_template += """        </div>
      </div>
"""
        
        # 添加footer
        html_template += f"""    </div>
    
    <div class="footer">
      <p>© 2025 海之安（中国）科技有限公司 | 基于智谱GLM AI生成</p>
      <p>共分析 {analysis_result.get('total_news', 0)} 条安全新闻 | 官网：<a href="https://www.oceansecurity.cn" style="color: #3b82f6;">www.oceansecurity.cn</a></p>
    </div>
  </div>
</body>
</html>"""
        
        return html_template
    
    def generate_daily_report(self, days_back: int = 1) -> str:
        """
        生成每日安全快报
        
        Args:
            days_back: 生成几天前的报告
            
        Returns:
            生成的HTML文件路径
        """
        try:
            # 1. 抓取新闻
            news_list = self.fetch_security_news(days_back)
            
            if not news_list:
                logger.warning("未获取到任何新闻，无法生成报告")
                return ""
            
            # 2. 使用GLM生成分析
            logger.info("正在使用GLM生成新闻分析...")
            analysis_result = self.generate_news_analysis(news_list)
            
            # 3. 生成HTML报告
            target_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y%m%d')
            html_content = self.generate_html_report(analysis_result, target_date)
            
            # 4. 保存文件
            filename = f"news{target_date}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ 成功生成AI智能新闻快报: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return ""

def main():
    """主函数"""
    # 从环境变量获取API密钥，或者在这里直接设置
    api_key = os.getenv('GLM_API_KEY')
    
    if not api_key:
        print("⚠️  请设置GLM_API_KEY环境变量或在代码中配置API密钥")
        print("获取API密钥：https://open.bigmodel.cn/")
        return
    
    generator = GLMNewsGenerator(api_key)
    
    # 生成昨天的新闻快报
    result = generator.generate_daily_report(days_back=1)
    
    if result:
        print(f"🎉 AI智能新闻快报生成成功: {result}")
    else:
        print("❌ 新闻快报生成失败")

if __name__ == "__main__":
    main()