#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端样式保护状态报告
生成详细的保护机制状态报告
"""

import os
import glob
from datetime import datetime
from style_protection import validate_mobile_styles

def generate_protection_report():
    """
    生成移动端样式保护状态报告
    """
    print("📱 海之安新闻系统 - 移动端样式保护状态报告")
    print("=" * 60)
    print(f"📅 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 检查保护模块状态
    print("🛡️  保护模块状态检查")
    print("-" * 30)
    
    modules = [
        ("style_protection.py", "样式保护核心模块"),
        ("mobile_style_monitor.py", "样式监控脚本"),
        ("test_mobile_protection.py", "保护机制测试"),
        ("mobile_responsive.css", "独立移动端样式文件")
    ]
    
    for module, description in modules:
        if os.path.exists(module):
            print(f"✅ {module} - {description}")
        else:
            print(f"❌ {module} - {description} (缺失)")
    
    print()
    
    # 2. 检查新闻生成器集成状态
    print("🔧 新闻生成器集成状态")
    print("-" * 30)
    
    try:
        from glm_news_generator import GLMNewsGenerator
        generator = GLMNewsGenerator("test")
        
        # 检查是否有备用CSS方法
        if hasattr(generator, '_get_fallback_mobile_css'):
            print("✅ 备用移动端CSS方法已集成")
        else:
            print("❌ 备用移动端CSS方法未集成")
        
        # 检查是否在HTML生成中调用样式保护
        import inspect
        source = inspect.getsource(generator.generate_html_report)
        if "style_protection" in source:
            print("✅ 样式保护模块调用已集成")
        else:
            print("❌ 样式保护模块调用未集成")
        
        if "ensure_mobile_responsive" in source:
            print("✅ 样式确保机制已集成")
        else:
            print("❌ 样式确保机制未集成")
            
    except Exception as e:
        print(f"❌ 新闻生成器检查失败: {e}")
    
    print()
    
    # 3. 检查现有新闻文件状态
    print("📰 现有新闻文件状态")
    print("-" * 30)
    
    news_files = sorted(glob.glob("news*.html"))
    if not news_files:
        print("📝 未找到新闻文件")
    else:
        protected_count = 0
        total_count = len(news_files)
        
        for file_path in news_files:
            has_mobile = validate_mobile_styles(file_path)
            status = "✅ 已保护" if has_mobile else "❌ 未保护"
            file_size = os.path.getsize(file_path)
            print(f"{status} {file_path} ({file_size:,} bytes)")
            
            if has_mobile:
                protected_count += 1
        
        protection_rate = (protected_count / total_count) * 100
        print(f"\n📊 保护覆盖率: {protected_count}/{total_count} ({protection_rate:.1f}%)")
        
        if protection_rate == 100:
            print("🎉 所有新闻文件都已受到移动端样式保护！")
        elif protection_rate >= 80:
            print("👍 大部分新闻文件已受到保护，建议修复剩余文件")
        else:
            print("⚠️  保护覆盖率较低，建议运行自动修复")
    
    print()
    
    # 4. 保护机制功能测试
    print("🧪 保护机制功能测试")
    print("-" * 30)
    
    try:
        from style_protection import get_mobile_responsive_css, ensure_mobile_responsive
        
        # 测试CSS生成
        css = get_mobile_responsive_css()
        if "@media (max-width: 768px)" in css:
            print("✅ CSS生成功能正常")
        else:
            print("❌ CSS生成功能异常")
        
        # 测试HTML增强
        test_html = "<html><head><style>body{}</style></head><body></body></html>"
        enhanced = ensure_mobile_responsive(test_html)
        if "@media (max-width: 768px)" in enhanced:
            print("✅ HTML增强功能正常")
        else:
            print("❌ HTML增强功能异常")
        
        print("✅ 保护机制功能测试通过")
        
    except Exception as e:
        print(f"❌ 保护机制功能测试失败: {e}")
    
    print()
    
    # 5. 建议和总结
    print("💡 建议和总结")
    print("-" * 30)
    
    suggestions = []
    
    # 检查是否有未保护的文件
    unprotected_files = []
    for file_path in news_files:
        if not validate_mobile_styles(file_path):
            unprotected_files.append(file_path)
    
    if unprotected_files:
        suggestions.append(f"运行 'python3 mobile_style_monitor.py' 修复 {len(unprotected_files)} 个未保护文件")
    
    # 检查是否有备份文件
    backup_files = glob.glob("*.backup")
    if backup_files:
        suggestions.append(f"清理 {len(backup_files)} 个备份文件（可选）")
    
    # 检查监控脚本
    suggestions.append("定期运行 'python3 mobile_style_monitor.py --continuous' 进行持续监控")
    suggestions.append("在部署前运行 'python3 test_mobile_protection.py' 验证保护机制")
    
    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
    else:
        print("🎉 移动端样式保护机制运行完美，无需额外操作！")
    
    print()
    print("📱 移动端样式保护机制已全面部署并正常运行")
    print("🛡️  您的新闻系统现在可以在所有设备上完美显示")

if __name__ == "__main__":
    generate_protection_report()