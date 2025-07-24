#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络安全新闻自动抓取程序
自动抓取当天最新的网络安全新闻并生成HTML文件
"""

import requests
import feedparser
from datetime import datetime, date
import re
import os
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin, urlparse
import logging

# 导入配置文件
try:
    from scraper_config import NEWS_SOURCES, SECURITY_KEYWORDS, USER_AGENTS, REQUEST_CONFIG, FILE_CONFIG, LOG_CONFIG
except ImportError:
    # 如果配置文件不存在，使用默认配置
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
        }
    ]
    SECURITY_KEYWORDS = [
        '安全', '漏洞', '攻击', '黑客', '病毒', '恶意软件', '勒索', '渗透',
        '防护', '防御', '加密', '解密', '隐私', '数据泄露', '网络安全',
        '信息安全', 'APT', 'DDoS', '钓鱼', '木马', '后门', '提权',
        '安全漏洞', '安全事件', '安全威胁', '安全防护', '安全检测',
        '网络安全', '网络攻击', '网络防护', '网络威胁'
    ]
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
    REQUEST_CONFIG = {
        'timeout': 10,
        'delay_range': (1, 3),
        'max_retries': 3,
        'retry_delay': 2
    }
    FILE_CONFIG = {
        'output_dir': '.',
        'filename_pattern': 'news{date}.html',
        'date_format': '%Y%m%d',
        'encoding': 'utf-8'
    }
    LOG_CONFIG = {
        'level': 'INFO',
        'format': '%(asctime)s - %(levelname)s - %(message)s',
        'file': 'news_scraper.log'
    }

# 配置日志
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['level']),
    format=LOG_CONFIG['format'],
    handlers=[
        logging.FileHandler(LOG_CONFIG['file'], encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecurityNewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS)
        })
        self.news_sources = NEWS_SOURCES
        self.today = date.today()
        self.scraped_news = []
        
    def fetch_rss_feed(self, rss_url, source_name):
        """获取RSS订阅源的新闻"""
        try:
            logger.info(f"正在抓取 {source_name} 的RSS源: {rss_url}")
            feed = feedparser.parse(rss_url)
            
            today_news = []
            for entry in feed.entries:
                # 解析发布时间
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6]).date()
                elif hasattr(entry, 'updated_parsed'):
                    pub_date = datetime(*entry.updated_parsed[:6]).date()
                
                # 只处理今天的新闻
                if pub_date and pub_date == self.today:
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'summary': getattr(entry, 'summary', ''),
                        'published_date': pub_date,
                        'source': source_name,
                        'content': ''
                    }
                    
                    # 如果有详细内容，尝试获取
                    if hasattr(entry, 'content'):
                        news_item['content'] = entry.content[0].value if entry.content else ''
                    
                    today_news.append(news_item)
            
            logger.info(f"从 {source_name} 获取到 {len(today_news)} 条今日新闻")
            return today_news
            
        except Exception as e:
            logger.error(f"抓取 {source_name} RSS源失败: {e}")
            return []
    
    def clean_html_content(self, html_content):
        """清理HTML内容，提取纯文本"""
        if not html_content:
            return ""
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            # 移除脚本和样式标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 获取文本内容
            text = soup.get_text()
            # 清理多余的空白字符
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            return text[:500] + "..." if len(text) > 500 else text
        except Exception as e:
            logger.error(f"清理HTML内容失败: {e}")
            return html_content[:300] + "..." if len(html_content) > 300 else html_content
    
    def scrape_news_content(self, news_item):
        """抓取新闻详细内容"""
        try:
            # 添加随机延时避免被反爬虫
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(news_item['link'], timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 尝试提取文章正文（不同网站可能有不同的结构）
            content_selectors = [
                'article', '.article-content', '.content', '.post-content',
                '.entry-content', '.post-body', '.article-body'
            ]
            
            content = ""
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    content = self.clean_html_content(str(content_element))
                    if len(content) > 100:  # 确保内容足够长
                        break
            
            if not content:
                # 如果没找到特定内容区域，使用整个body
                body = soup.find('body')
                if body:
                    content = self.clean_html_content(str(body))
            
            return content
        except Exception as e:
            logger.error(f"抓取新闻内容失败 {news_item['link']}: {e}")
            return ""
    
    def filter_security_news(self, news_list):
        """过滤网络安全相关新闻"""
        filtered_news = []
        for news in news_list:
            title = news['title'].lower()
            summary = news['summary'].lower()
            
            # 检查标题或摘要是否包含安全相关关键词
            is_security_related = any(keyword in title or keyword in summary 
                                    for keyword in SECURITY_KEYWORDS)
            
            if is_security_related:
                filtered_news.append(news)
        
        return filtered_news
    
    def scrape_all_sources(self):
        """从所有源抓取新闻"""
        all_news = []
        
        for source in self.news_sources:
            if not source['enabled']:
                continue
                
            try:
                news_list = self.fetch_rss_feed(source['rss_url'], source['name'])
                if news_list:
                    # 过滤网络安全相关新闻
                    security_news = self.filter_security_news(news_list)
                    all_news.extend(security_news)
                    logger.info(f"从 {source['name']} 筛选出 {len(security_news)} 条安全相关新闻")
            except Exception as e:
                logger.error(f"处理 {source['name']} 时出错: {e}")
        
        # 去重（基于标题）
        seen_titles = set()
        unique_news = []
        for news in all_news:
            title_key = news['title'].strip().lower()
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_news.append(news)
        
        self.scraped_news = unique_news
        logger.info(f"总共获取到 {len(unique_news)} 条不重复的安全新闻")
        return unique_news
    
    def generate_html_content(self, news_list):
        """生成符合现有格式的HTML内容"""
        if not news_list:
            logger.warning("没有新闻内容可生成")
            return ""
        
        # 按来源分组
        news_by_source = {}
        for news in news_list:
            source = news['source']
            if source not in news_by_source:
                news_by_source[source] = []
            news_by_source[source].append(news)
        
        # 生成摘要内容
        summary_content = "今日网络安全领域重点关注："
        for i, news in enumerate(news_list[:3], 1):
            summary_content += f"【{i}】{news['title'][:30]}{'...' if len(news['title']) > 30 else ''}；"
        summary_content = summary_content.rstrip('；')
        
        current_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        today_str = self.today.strftime('%Y-%m-%d')
        news_count = len(news_list)
        
        html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>海之安安全每日快报 - {today_str} - 第{news_count}期</title>
  
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
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 
                    0 0 0 1px rgba(59, 130, 246, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
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
        width: 120px;
        height: auto;
        margin-bottom: 20px;
        filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.3));
      }}
      
      .title {{
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
        text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
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
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
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
      
      /* 图标样式 */
      .icon-focus::before {{ content: '🎯'; }}
      .icon-risk::before {{ content: '⚠️'; }}
      .icon-innovation::before {{ content: '🚀'; }}
      
      /* 打印样式 */
      @media print {{
        body {{
          background: white;
          color: black;
          padding: 0;
        }}
        
        .container {{
          box-shadow: none;
          border: none;
          background: white;
        }}
        
        .header {{
          background: #f8f9fa;
          border-bottom: 2px solid #dee2e6;
        }}
        
        .title {{
          color: #2563eb !important;
          -webkit-text-fill-color: #2563eb !important;
        }}
        
        .summary-section,
        .category-section,
        .news-item {{
          background: white;
          border: 1px solid #dee2e6;
          color: black;
        }}
        
        .summary-title,
        .category-title {{
          color: #2563eb;
        }}
        
        .news-title {{
          color: #1f2937;
        }}
        
        .news-analysis,
        .summary-content {{
          color: #374151;
        }}
      }}
    </style>
  
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABLAAAAN0CAIAAAArnUa0AAAABmJLR0QA/wD/AP+gvaeTAAAgAElEQVR4nOzdd3zV1f3H8fP93pm9SCAhIey9BBkyFJyoOKt1b3FgW2e1WltrW2urXY627j1Q3AMHiooIsqcgG0IGJO/kru/390f6S0NIcs/33pvkwnk9H/3Dws3Nl+Te7z3vcz7nczTTNAUAAAAAQD16d18AAAAAAKB7EAgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAAUBSBEAAAAAAURSAEAAAAAEURCAEAAABAUQRCAAAAAFAUgRAAAAAAFEUgBAAAAABFEQgBAAAAQFEEQgAAAABQFIEQAAAAABRFIAQAAAAARREIAQAAAEBRBEIAAAAA......" alt="Ocean Security Logo" class="logo">
      <h1 class="title">海之安安全每日快报</h1>
      <div class="subtitle">{today_str} · 第{news_count}期</div>
    </div>
    
    <div class="content">
      
        <div class="summary-section">
          <h2 class="summary-title">今日摘要</h2>
          <div class="summary-content">{summary_content}</div>
        </div>
      
        <div class="category-section">
          <div class="category-header">
            <h2 class="category-title icon-focus">今日安全新闻</h2>
          </div>
          <div class="category-news">'''

        # 添加新闻条目
        for i, news in enumerate(news_list, 1):
            # 简化摘要内容
            summary = self.clean_html_content(news.get('summary', '') or news.get('content', ''))
            if not summary:
                summary = "暂无详细摘要内容"
            
            html_content += f'''
        <div class="news-item">
          <div class="news-title">{news['title']}</div>
          <div class="news-analysis"><strong>来源：</strong>{news['source']} | <strong>分析：</strong>{summary[:300]}{'...' if len(summary) > 300 else ''}</div>
        </div>'''

        html_content += f'''
          </div>
        </div>
      
    </div>
    
    <div class="footer">
      <p>© 2025 Ocean Security · 海之安安全每日快报</p>
      <p>Generated on {current_time}</p>
    </div>
  </div>
</body>
</html>'''
        
        return html_content
    
    def save_news_file(self, html_content, filename=None):
        """保存新闻文件"""
        if not html_content:
            logger.error("HTML内容为空，无法保存文件")
            return False
        
        if filename is None:
            filename = f"news{self.today.strftime('%Y%m%d')}.html"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"成功生成新闻文件: {filename}")
            return True
        except Exception as e:
            logger.error(f"保存文件 {filename} 失败: {e}")
            return False
    
    def run(self):
        """执行新闻抓取主流程"""
        logger.info("开始执行网络安全新闻自动抓取...")
        logger.info(f"目标日期: {self.today.strftime('%Y-%m-%d')}")
        
        # 抓取所有源的新闻
        news_list = self.scrape_all_sources()
        
        if not news_list:
            logger.warning("今日未获取到任何网络安全新闻")
            return False
        
        # 生成HTML内容
        html_content = self.generate_html_content(news_list)
        
        if not html_content:
            logger.error("生成HTML内容失败")
            return False
        
        # 保存文件
        filename = f"news{self.today.strftime('%Y%m%d')}.html"
        success = self.save_news_file(html_content, filename)
        
        if success:
            logger.info(f"新闻抓取完成，共生成 {len(news_list)} 条新闻")
            logger.info(f"文件已保存为: {filename}")
            return True
        else:
            logger.error("文件保存失败")
            return False

def main():
    """主函数"""
    scraper = SecurityNewsScraper()
    success = scraper.run()
    
    if success:
        print("✅ 网络安全新闻抓取成功完成！")
    else:
        print("❌ 网络安全新闻抓取失败或未获取到新闻内容")

if __name__ == "__main__":
    main()
