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
    """生成index.html文件"""
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
    
    # 生成HTML内容
    current_time = datetime.now().strftime('%Y年%m月%d日 %H:%M')
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>海之安网络安全快报 - 新闻索引</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .header h1 {{
            color: #1e3c72;
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.1rem;
            margin-bottom: 15px;
        }}
        
        .update-time {{
            color: #888;
            font-size: 0.9rem;
        }}
        
        .main-content {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .latest-news {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .latest-news h2 {{
            color: #1e3c72;
            font-size: 1.8rem;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .latest-news h2::before {{
            content: '🔥';
            font-size: 1.5rem;
        }}
        
        .news-card {{
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .news-card:hover {{
            border-color: #1e3c72;
            box-shadow: 0 5px 15px rgba(30, 60, 114, 0.2);
            transform: translateY(-2px);
        }}
        
        .news-title {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #1e3c72;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        .news-date {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }}
        
        .news-summary {{
            color: #555;
            line-height: 1.6;
            font-size: 0.95rem;
        }}
        
        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .category-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .category-title {{
            color: #1e3c72;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .news-link {{
            display: block;
            padding: 12px 15px;
            margin-bottom: 8px;
            background: #f8f9fa;
            border-radius: 8px;
            text-decoration: none;
            color: #333;
            transition: all 0.3s ease;
            border-left: 4px solid transparent;
        }}
        
        .news-link:hover {{
            background: #e3f2fd;
            border-left-color: #1e3c72;
            transform: translateX(5px);
        }}
        
        .news-link-title {{
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .news-link-date {{
            font-size: 0.8rem;
            color: #666;
        }}
        
        .footer {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            color: #666;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        @media (max-width: 768px) {{
            .main-content {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>海之安网络安全快报</h1>
            <div class="subtitle">网络安全新闻索引 · 实时更新</div>
            <div class="update-time">最后更新: {current_time}</div>
        </div>
        
        <div class="main-content">
            <div class="latest-news">
                <h2>今日要闻</h2>'''
    
    if latest_news:
        html += f'''
                <div class="news-card" onclick="window.open('{latest_news['filename']}', '_blank')">
                    <div class="news-title">{latest_news['title']}</div>
                    <div class="news-date">{latest_news['date']}</div>
                    <div class="news-summary">{latest_news['summary']}</div>
                </div>'''
    else:
        html += '''
                <div class="news-card">
                    <div class="news-title">暂无新闻</div>
                    <div class="news-summary">请添加新闻文件</div>
                </div>'''
    
    html += '''
            </div>
            
            <div class="sidebar">'''
    
    # 生成各个分类的链接
    category_configs = [
        ('this_week', '📅 本周新闻', categories['this_week']),
        ('this_month', '📆 本月新闻', categories['this_month']),
        ('this_year', '🗓️ 今年新闻', categories['this_year']),
        ('older', '📚 历史新闻', categories['older'])
    ]
    
    for category_key, category_name, news_items in category_configs:
        if news_items:
            html += f'''
                <div class="category-section">
                    <div class="category-title">{category_name}</div>'''
            
            for news in news_items[:10]:  # 最多显示10条
                html += f'''
                    <a href="{news['filename']}" class="news-link" target="_blank">
                        <div class="news-link-title">{news['title'][:50]}{'...' if len(news['title']) > 50 else ''}</div>
                        <div class="news-link-date">{news['date']}</div>
                    </a>'''
            
            html += '''
                </div>'''
    
    html += f'''
            </div>
        </div>
        
        <div class="footer">
            <p>&copy; 2025 海之安网络安全. 保持警惕，守护安全</p>
            <p>共收录 {len(news_list)} 篇安全快报</p>
        </div>
    </div>
    
    <script>
        // 自动刷新页面（每5分钟）
        setTimeout(function() {{
            location.reload();
        }}, 300000);
    </script>
</body>
</html>'''
    
    # 写入index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"已生成 index.html")
    print(f"处理了 {len(news_list)} 个新闻文件")
    if latest_news:
        print(f"最新新闻: {latest_news['title']} ({latest_news['date']})")

if __name__ == "__main__":
    generate_index()