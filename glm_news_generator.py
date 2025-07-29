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
                logger.info(f"正在抓取 {source['name']} 的RSS源...")
                
                # 获取RSS内容
                feed = feedparser.parse(source['rss_url'])
                source_news = []
                
                for entry in feed.entries:
                    # 解析发布时间
                    pub_date = None
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6]).date()
                    elif hasattr(entry, 'updated_parsed'):
                        pub_date = datetime(*entry.updated_parsed[:6]).date()
                    
                    # 检查是否为目标日期的新闻（允许3天内的新闻）
                    if pub_date and (datetime.now().date() - pub_date).days <= 3:
                        # 检查是否为安全相关新闻
                        title = entry.title.lower()
                        summary = getattr(entry, 'summary', '').lower()
                        
                        if any(keyword in title or keyword in summary for keyword in self.security_keywords):
                            news_item = {
                                'title': entry.title,
                                'link': entry.link,
                                'summary': getattr(entry, 'summary', ''),
                                'published_date': pub_date,
                                'source': source['name'],
                                'weight': source['weight']
                            }
                            source_news.append(news_item)
                
                logger.info(f"从 {source['name']} 获取到 {len(source_news)} 条安全新闻")
                all_news.extend(source_news)
                
                # 避免请求过于频繁
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"抓取 {source['name']} 失败: {e}")
                continue
        
        # 去重和排序
        unique_news = []
        seen_titles = set()
        
        for news in all_news:
            if news['title'] not in seen_titles:
                unique_news.append(news)
                seen_titles.add(news['title'])
        
        # 按权重和时间排序，取前10条
        unique_news.sort(key=lambda x: (x['weight'], x['published_date']), reverse=True)
        
        logger.info(f"总共获取到 {len(unique_news)} 条不重复的安全新闻")
        return unique_news[:10]
    
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
        
        # 构建新闻标题列表
        news_titles = [f"{i+1}. {news['title']}" for i, news in enumerate(news_list)]
        news_text = "\n".join(news_titles)
        
        # 生成今日摘要
        summary_prompt = f"""
请基于以下网络安全新闻标题，生成一份专业的今日摘要（200字以内）：

{news_text}

要求：
1. 总结今日网络安全态势的主要特点
2. 突出重点威胁和趋势
3. 语言专业、简洁
4. 体现时效性和权威性
"""
        
        summary = self.call_glm_api(summary_prompt)
        
        # 对新闻进行分类分析
        category_prompt = f"""
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
"""
        
        category_result = self.call_glm_api(category_prompt)
        
        # 解析分类结果
        categories = {}
        try:
            categories = json.loads(category_result)
        except:
            logger.warning("分类结果解析失败，使用默认分类")
            # 默认分类
            categories = {
                "焦点安全事件": [{"title": news['title'], "analysis": "暂无详细分析"} for news in news_list[:3]],
                "漏洞与威胁": [{"title": news['title'], "analysis": "暂无详细分析"} for news in news_list[3:6]],
                "产业动态": [{"title": news['title'], "analysis": "暂无详细分析"} for news in news_list[6:]]
            }
        
        return {
            "summary": summary,
            "categories": categories,
            "total_news": len(news_list)
        }
    
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
    
    .icon-focus::before {{ content: '🎯'; }}
    .icon-risk::before {{ content: '⚠️'; }}
    .icon-innovation::before {{ content: '🚀'; }}
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
        
        # 添加分类新闻
        icon_map = {
            "焦点安全事件": "icon-focus",
            "漏洞与威胁": "icon-risk", 
            "产业动态": "icon-innovation"
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
                    html_template += f"""          <div class="news-item">
            <div class="news-title">{item['title']}</div>
            <div class="news-analysis"><strong>AI分析：</strong>{item['analysis']}</div>
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