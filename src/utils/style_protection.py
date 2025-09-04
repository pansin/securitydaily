#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
样式保护模块
确保移动端响应式样式不会被覆盖
"""

def get_mobile_responsive_css():
    """
    获取移动端响应式CSS样式
    这个函数确保移动端样式始终被包含在生成的HTML中
    """
    return """
    /* 移动端适配样式 - 重要：请勿删除或覆盖 */
    @media (max-width: 768px) {
      .container {
        margin: 0;
        padding: 10px;
        border-radius: 0;
      }
      
      .header {
        padding: 20px 15px;
        border-radius: 0;
      }
      
      .logo {
        width: 150px;
        margin-bottom: 15px;
      }
      
      .title {
        font-size: 24px;
        margin-bottom: 12px;
      }
      
      .subtitle {
        font-size: 14px;
        margin-bottom: 6px;
      }
      
      .content {
        padding: 20px 15px;
      }
      
      .summary-section {
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
      }
      
      .summary-title {
        font-size: 16px;
        margin-bottom: 12px;
      }
      
      .summary-content {
        font-size: 14px;
        line-height: 1.6;
      }
      
      .stats-section {
        margin-bottom: 20px;
      }
      
      .stats-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }
      
      .stat-card {
        padding: 15px;
        border-radius: 8px;
      }
      
      .stat-number {
        font-size: 24px;
        margin-bottom: 6px;
      }
      
      .stat-label {
        font-size: 12px;
      }
      
      .stat-detail {
        font-size: 10px;
      }
      
      .enhancement-info {
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
      }
      
      .enhancement-info h3 {
        font-size: 14px;
        margin-bottom: 10px;
      }
      
      .enhancement-item {
        padding: 6px 0;
      }
      
      .enhancement-label,
      .enhancement-value {
        font-size: 12px;
      }
      
      .source-list {
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
      }
      
      .source-list h3 {
        font-size: 14px;
        margin-bottom: 10px;
      }
      
      .source-tag {
        padding: 4px 8px;
        font-size: 10px;
        margin: 2px;
      }
      
      .category-section {
        margin-bottom: 25px;
        border-radius: 8px;
      }
      
      .category-header {
        padding: 15px 20px;
      }
      
      .category-title {
        font-size: 18px;
      }
      
      .category-news {
        padding: 15px;
      }
      
      .news-item {
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 6px;
      }
      
      .news-title {
        font-size: 16px;
        margin-bottom: 10px;
        line-height: 1.3;
      }
      
      .news-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 6px;
        margin-top: 6px;
      }
      
      .news-source,
      .region-badge,
      .impact-badge,
      .content-quality-badge {
        font-size: 10px;
        padding: 3px 6px;
        margin: 2px 4px 2px 0;
      }
      
      .news-summary {
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 10px;
      }
      
      .key-points {
        margin: 10px 0;
        padding-left: 15px;
        font-size: 12px;
      }
      
      .key-points li {
        margin-bottom: 3px;
        line-height: 1.3;
      }
      
      .footer {
        padding: 15px;
        border-radius: 0;
        font-size: 12px;
      }
    }
    
    /* 超小屏幕适配 (iPhone SE等) */
    @media (max-width: 480px) {
      .container {
        padding: 5px;
      }
      
      .header {
        padding: 15px 10px;
      }
      
      .logo {
        width: 120px;
      }
      
      .title {
        font-size: 20px;
      }
      
      .subtitle {
        font-size: 12px;
      }
      
      .content {
        padding: 15px 10px;
      }
      
      .stats-grid {
        grid-template-columns: 1fr;
        gap: 8px;
      }
      
      .stat-card {
        padding: 12px;
      }
      
      .stat-number {
        font-size: 20px;
      }
      
      .category-title {
        font-size: 16px;
      }
      
      .news-title {
        font-size: 14px;
      }
      
      .news-summary {
        font-size: 12px;
      }
    }
    
    /* 横屏适配 */
    @media (max-width: 768px) and (orientation: landscape) {
      .stats-grid {
        grid-template-columns: repeat(4, 1fr);
      }
      
      .category-section {
        margin-bottom: 20px;
      }
      
      .news-item {
        padding: 12px;
        margin-bottom: 12px;
      }
    }
    """

def ensure_mobile_responsive(html_content):
    """
    确保HTML内容包含移动端响应式样式
    
    Args:
        html_content: 原始HTML内容
        
    Returns:
        包含移动端样式的HTML内容
    """
    mobile_css = get_mobile_responsive_css()
    
    # 如果HTML中没有移动端样式，添加它们
    if "@media (max-width: 768px)" not in html_content:
        # 在</style>标签前插入移动端样式
        if "</style>" in html_content:
            html_content = html_content.replace("</style>", mobile_css + "\n  </style>")
        else:
            # 如果没有style标签，在head中添加
            style_tag = f"<style>{mobile_css}</style>"
            if "</head>" in html_content:
                html_content = html_content.replace("</head>", style_tag + "\n</head>")
    
    return html_content

def auto_fix_existing_files():
    """
    自动修复现有的HTML文件，确保包含移动端样式
    """
    import glob
    import os
    
    news_files = glob.glob("news*.html")
    fixed_count = 0
    
    for file_path in news_files:
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否需要修复
            if not validate_mobile_styles(file_path):
                print(f"🔧 正在修复 {file_path}...")
                
                # 应用移动端样式
                fixed_content = ensure_mobile_responsive(content)
                
                # 备份原文件
                backup_path = f"{file_path}.backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # 写入修复后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✅ {file_path} 修复完成，备份保存为 {backup_path}")
                fixed_count += 1
            else:
                print(f"✅ {file_path} 已包含移动端样式，无需修复")
                
        except Exception as e:
            print(f"❌ 修复 {file_path} 失败: {e}")
    
    return fixed_count

def validate_mobile_styles(file_path):
    """
    验证文件是否包含移动端样式
    
    Args:
        file_path: HTML文件路径
        
    Returns:
        bool: 是否包含移动端样式
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键的移动端样式
        mobile_indicators = [
            "@media (max-width: 768px)",
            "@media (max-width: 480px)",
            "grid-template-columns: repeat(2, 1fr)"
        ]
        
        return any(indicator in content for indicator in mobile_indicators)
        
    except Exception as e:
        print(f"验证移动端样式失败: {e}")
        return False

if __name__ == "__main__":
    # 测试样式保护功能
    print("移动端样式保护模块")
    print("=" * 40)
    
    # 检查现有的新闻文件
    import glob
    news_files = glob.glob("news*.html")
    
    for file_path in news_files:
        has_mobile = validate_mobile_styles(file_path)
        status = "✅ 包含" if has_mobile else "❌ 缺失"
        print(f"{file_path}: {status} 移动端样式")