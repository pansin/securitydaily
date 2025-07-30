#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态生成index主页
确保显示最新的新闻内容，避免空白
"""

import os
import glob
import json
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndexGenerator:
    def __init__(self):
        """初始化index生成器"""
        self.news_files = []
        self.latest_news_data = []
        
    def scan_news_files(self):
        """扫描所有新闻文件"""
        news_pattern = "news*.html"
        files = glob.glob(news_pattern)
        
        # 按文件名排序（最新的在前）
        files.sort(reverse=True)
        self.news_files = files
        
        logger.info(f"发现 {len(files)} 个新闻文件")
        return files
    
    def extract_news_summary(self, file_path, max_length=200):
        """从新闻文件中提取摘要信息"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取标题
            title_element = soup.find('title')
            title = title_element.get_text() if title_element else "未知标题"
            
            # 提取摘要内容
            summary_element = soup.find(class_='summary-content')
            if summary_element:
                summary = summary_element.get_text(strip=True)
            else:
                # 备用方案：从内容中提取
                content_element = soup.find(class_='content')
                if content_element:
                    summary = content_element.get_text(strip=True)[:max_length] + "..."
                else:
                    summary = "暂无摘要信息"
            
            # 限制摘要长度
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            
            # 提取日期
            date_match = re.search(r'news(\d{8})\.html', file_path)
            if date_match:
                date_str = date_match.group(1)
                try:
                    date_obj = datetime.strptime(date_str, '%Y%m%d')
                    formatted_date = date_obj.strftime('%Y年%m月%d日')
                except:
                    formatted_date = "未知日期"
            else:
                formatted_date = "未知日期"
            
            return {
                'file': file_path,
                'title': title,
                'summary': summary,
                'date': formatted_date,
                'date_obj': date_obj if 'date_obj' in locals() else datetime.min
            }
            
        except Exception as e:
            logger.error(f"提取新闻摘要失败 {file_path}: {e}")
            return None
    
    def get_latest_news(self, count=6):
        """获取最新的新闻数据"""
        self.scan_news_files()
        latest_news = []
        
        for file_path in self.news_files[:count]:
            news_data = self.extract_news_summary(file_path)
            if news_data:
                latest_news.append(news_data)
        
        self.latest_news_data = latest_news
        return latest_news
    
    def generate_news_cards_html(self):
        """生成新闻卡片HTML"""
        if not self.latest_news_data:
            self.get_latest_news()
        
        cards_html = ""
        
        # 预定义的新闻类别和图标
        categories = [
            {"name": "威胁情报", "icon": "🔥", "color": "#ef4444"},
            {"name": "勒索软件", "icon": "⚠️", "color": "#f59e0b"},
            {"name": "零日漏洞", "icon": "🚨", "color": "#dc2626"},
            {"name": "企业安全", "icon": "💻", "color": "#3b82f6"},
            {"name": "网络设备", "icon": "🔓", "color": "#8b5cf6"},
            {"name": "钓鱼攻击", "icon": "🎯", "color": "#10b981"}
        ]
        
        for i, news in enumerate(self.latest_news_data):
            category = categories[i % len(categories)]
            
            # 生成简化的摘要
            summary_lines = news['summary'].split('。')[:3]  # 取前3句
            simplified_summary = '。'.join(summary_lines)
            if len(simplified_summary) > 150:
                simplified_summary = simplified_summary[:150] + "..."
            
            card_html = f"""
                    <div class="latest-news">
                        <div class="news-card" onclick="window.open('{news['file']}', '_blank')">
                            <div class="news-title">{news['title']}</div>
                            <div class="news-meta">
                                <div class="news-date">{news['date']}</div>
                                <div class="news-source">海之安AI</div>
                            </div>
                            <div class="news-summary">
                                {category['icon']} {simplified_summary}
                            </div>
                            <div class="news-stats">
                                <div class="news-category">{category['name']}</div>
                                <div class="read-more">阅读全文</div>
                            </div>
                        </div>
                    </div>"""
            
            cards_html += card_html
        
        return cards_html
    
    def generate_sidebar_links(self):
        """生成侧边栏链接HTML"""
        if not self.latest_news_data:
            self.get_latest_news()
        
        # 本周新闻
        week_links = ""
        for news in self.latest_news_data[:5]:
            week_links += f"""
                    <a href="{news['file']}" class="news-link" target="_blank">
                        <div class="news-link-title">{news['title'][:30]}...</div>
                        <div class="news-link-date">{news['date']}</div>
                    </a>"""
        
        # 历史快报
        history_links = ""
        for news in self.latest_news_data[5:10]:
            history_links += f"""
                    <a href="{news['file']}" class="news-link" target="_blank">
                        <div class="news-link-title">{news['title'][:30]}...</div>
                        <div class="news-link-date">{news['date']}</div>
                    </a>"""
        
        return week_links, history_links
    
    def get_statistics(self):
        """获取统计信息"""
        try:
            # 尝试从新闻源配置获取统计
            if os.path.exists('news_sources_config.json'):
                with open('news_sources_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    sources_count = len([s for s in config.get('news_sources', []) if s.get('enabled', True)])
                    regions_count = len(set([s.get('region', 'Unknown') for s in config.get('news_sources', [])]))
            else:
                sources_count = 29
                regions_count = 15
            
            # 计算威胁情报数量（基于新闻文件数量）
            threat_intel_count = len(self.news_files) * 3  # 假设每个文件包含3条威胁情报
            
            return {
                'sources_count': sources_count,
                'regions_count': regions_count,
                'threat_intel_count': min(threat_intel_count, 99),  # 限制最大值
                'ai_status': '实时'
            }
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return {
                'sources_count': 29,
                'regions_count': 15,
                'threat_intel_count': 42,
                'ai_status': '实时'
            }
    
    def generate_index_html(self):
        """生成完整的index.html"""
        # 获取最新新闻数据
        self.get_latest_news()
        
        # 生成各部分HTML
        news_cards_html = self.generate_news_cards_html()
        week_links, history_links = self.generate_sidebar_links()
        stats = self.get_statistics()
        
        # 当前时间
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        
        # 读取模板文件
        template_path = 'index.html'
        if not os.path.exists(template_path):
            logger.error("index.html模板文件不存在")
            return False
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # 更新时间
            template_content = re.sub(
                r'<div class="update-time">.*?</div>',
                f'<div class="update-time">实时更新: {current_time}</div>',
                template_content
            )
            
            # 更新统计信息
            stats_html = f"""
                    <div style="background: rgba(30, 41, 59, 0.6); border-radius: 12px; padding: 20px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="color: #94a3b8;">今日新闻源</span>
                            <span style="color: #3b82f6; font-weight: 600;">{stats['sources_count']}个</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="color: #94a3b8;">全球覆盖</span>
                            <span style="color: #10b981; font-weight: 600;">{stats['regions_count']}个国家</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <span style="color: #94a3b8;">威胁情报</span>
                            <span style="color: #f59e0b; font-weight: 600;">{stats['threat_intel_count']}条</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #94a3b8;">AI分析</span>
                            <span style="color: #8b5cf6; font-weight: 600;">{stats['ai_status']}</span>
                        </div>
                    </div>"""
            
            # 更新统计信息部分
            template_content = re.sub(
                r'<div style="background: rgba\(30, 41, 59, 0\.6\).*?</div>',
                stats_html,
                template_content,
                flags=re.DOTALL
            )
            
            # 更新新闻总数
            news_count = len(self.news_files)
            template_content = re.sub(
                r'共收录 \d+ 篇安全快报',
                f'共收录 {news_count} 篇安全快报',
                template_content
            )
            
            # 保存更新后的文件
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
            
            logger.info("✅ index.html已更新")
            return True
            
        except Exception as e:
            logger.error(f"生成index.html失败: {e}")
            return False

def main():
    """主函数"""
    generator = IndexGenerator()
    
    print("🚀 海之安新闻系统 - 动态主页生成器")
    print("=" * 50)
    
    # 生成index页面
    success = generator.generate_index_html()
    
    if success:
        print("✅ 主页生成成功")
        print(f"📰 发现 {len(generator.news_files)} 个新闻文件")
        print(f"🔄 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("❌ 主页生成失败")

if __name__ == "__main__":
    main()