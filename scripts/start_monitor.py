#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻监控启动脚本
简化版本，只生成一次index.html然后退出
"""

import os
import re
import glob
from datetime import datetime
from bs4 import BeautifulSoup

def extract_news_info(filepath):
    """从新闻文件中提取信息"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 提取标题
        title_elem = soup.find('title')
        title = title_elem.text if title_elem else "海之安每日网络安全快报"
        
        # 从文件名提取日期
        filename = os.path.basename(filepath)
        date_match = re.search(r'news(\d{8})\.html', filename)
        if date_match:
            date_str = date_match.group(1)
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            formatted_date = date_obj.strftime('%Y年%m月%d日')
        else:
            formatted_date = "未知日期"
            date_obj = datetime.now()
        
        # 提取摘要
        summary = ""
        summary_elem = soup.find('div', class_='summary-content')
        if summary_elem:
            summary = summary_elem.get_text().strip()[:200] + "..."
        else:
            # 尝试提取第一条新闻标题作为摘要
            news_title = soup.find('h3', class_='news-title') or soup.find('div', class_='news-title')
            if news_title:
                summary = news_title.get_text().strip()
        
        return {
            'filepath': filepath,
            'filename': filename,
            'title': title,
            'date': formatted_date,
            'date_obj': date_obj,
            'summary': summary
        }
    except Exception as e:
        print(f"解析文件 {filepath} 时出错: {e}")
        return None

def categorize_news_by_date(news_list):
    """按日期分类新闻"""
    now = datetime.now()
    
    categories = {
        'latest': [],      # 最新（今日）
        'this_week': [],   # 本周
        'this_month': [],  # 本月
        'this_year': [],   # 今年
        'older': []        # 更早
    }
    
    for news in news_list:
        date_diff = now - news['date_obj']
        
        if date_diff.days == 0:
            categories['latest'].append(news)
        elif date_diff.days <= 7:
            categories['this_week'].append(news)
        elif date_diff.days <= 30:
            categories['this_month'].append(news)
        elif date_diff.days <= 365:
            categories['this_year'].append(news)
        else:
            categories['older'].append(news)
    
    return categories

def generate_index():
    """更新index.html文件内容（保持现代化设计）"""
    # 获取所有news开头的HTML文件，但排除模板文件
    all_news_files = glob.glob('news*.html')
    news_files = [f for f in all_news_files if re.search(r'news\d{8}\.html', f)]
    
    if not news_files:
        print("未找到新闻文件")
        return
    
    # 提取新闻信息
    news_list = []
    for filepath in news_files:
        news_info = extract_news_info(filepath)
        if news_info:
            news_list.append(news_info)
    
    # 按日期排序（最新的在前）
    news_list.sort(key=lambda x: x['date_obj'], reverse=True)
    
    # 分类
    categories = categorize_news_by_date(news_list)
    
    # 获取最新新闻作为主要新闻
    latest_news = news_list[0] if news_list else None
    
    # 检查是否存在现代化的index.html模板
    if not os.path.exists('index.html'):
        print("❌ index.html模板不存在，无法更新")
        return
    
    try:
        # 读取现有的现代化模板
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 只更新动态内容，保持现代化设计
        current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
        
        # 更新最新新闻内容
        if latest_news:
            # 更新今日要闻的标题和内容
            import re
            
            # 更新新闻标题
            html_content = re.sub(
                r'<div class="news-title">.*?</div>',
                f'<div class="news-title">{latest_news["title"]}</div>',
                html_content,
                count=1
            )
            
            # 更新新闻日期
            html_content = re.sub(
                r'<div class="news-date">.*?</div>',
                f'<div class="news-date">{latest_news["date"]}</div>',
                html_content,
                count=1
            )
            
            # 更新新闻摘要
            summary = latest_news['summary'][:300] + "..." if len(latest_news['summary']) > 300 else latest_news['summary']
            html_content = re.sub(
                r'<div class="news-summary">.*?</div>',
                f'<div class="news-summary">{summary}</div>',
                html_content,
                count=1,
                flags=re.DOTALL
            )
            
            # 更新点击链接
            html_content = re.sub(
                r'onclick="window\.open\(\'[^\']*\', \'_blank\'\)"',
                f'onclick="window.open(\'{latest_news["file"]}\', \'_blank\')"',
                html_content,
                count=1
            )
        
        # 更新统计信息
        news_count = len(news_files)
        html_content = re.sub(
            r'共收录 \d+ 篇安全快报',
            f'共收录 {news_count} 篇安全快报',
            html_content
        )
        
        # 更新侧边栏新闻链接
        if news_list:
            # 更新本周新闻链接
            week_news = news_list[0] if news_list else None
            if week_news:
                html_content = re.sub(
                    r'<a href="[^"]*" class="news-link" target="_blank">\s*<div class="news-link-title">.*?</div>\s*<div class="news-link-date">.*?</div>\s*</a>',
                    f'<a href="{week_news["file"]}" class="news-link" target="_blank">\n                                <div class="news-link-title">{week_news["title"]}</div>\n                                <div class="news-link-date">{week_news["date"]}</div>\n                            </a>',
                    html_content,
                    count=1,
                    flags=re.DOTALL
                )
        
        # 保存更新后的文件
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 已更新现代化主页内容")
        print(f"📰 处理了 {len(news_list)} 个新闻文件")
        if latest_news:
            print(f"📋 最新新闻: {latest_news['title'][:50]}...")
        
    except Exception as e:
        print(f"❌ 更新主页失败: {e}")
        # 如果更新失败，不要生成旧版本，保持现有文件不变
        return
    

if __name__ == "__main__":
    generate_index()