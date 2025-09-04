#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端样式保护测试脚本
测试样式保护机制的各种场景
"""

import os
import tempfile
from style_protection import (
    get_mobile_responsive_css, 
    ensure_mobile_responsive, 
    validate_mobile_styles,
    auto_fix_existing_files
)

def test_css_generation():
    """测试CSS生成功能"""
    print("🧪 测试1: CSS生成功能")
    css = get_mobile_responsive_css()
    
    # 检查关键样式是否存在
    required_styles = [
        "@media (max-width: 768px)",
        "@media (max-width: 480px)",
        "grid-template-columns: repeat(2, 1fr)",
        "orientation: landscape"
    ]
    
    all_present = True
    for style in required_styles:
        if style not in css:
            print(f"❌ 缺失样式: {style}")
            all_present = False
        else:
            print(f"✅ 包含样式: {style}")
    
    if all_present:
        print("🎉 CSS生成测试通过")
    else:
        print("❌ CSS生成测试失败")
    
    return all_present

def test_html_enhancement():
    """测试HTML增强功能"""
    print("\n🧪 测试2: HTML增强功能")
    
    # 测试场景1: 没有移动端样式的HTML
    html_without_mobile = """<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <style>
        body { font-family: Arial; }
        .container { max-width: 1200px; }
    </style>
</head>
<body>
    <div class="container">Test content</div>
</body>
</html>"""
    
    enhanced_html = ensure_mobile_responsive(html_without_mobile)
    
    if "@media (max-width: 768px)" in enhanced_html:
        print("✅ 成功添加移动端样式到无样式HTML")
    else:
        print("❌ 未能添加移动端样式到无样式HTML")
        return False
    
    # 测试场景2: 已有移动端样式的HTML
    html_with_mobile = """<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <style>
        body { font-family: Arial; }
        @media (max-width: 768px) {
            .container { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">Test content</div>
</body>
</html>"""
    
    enhanced_html2 = ensure_mobile_responsive(html_with_mobile)
    mobile_count = enhanced_html2.count("@media (max-width: 768px)")
    
    if mobile_count == 1:
        print("✅ 正确处理已有移动端样式的HTML（未重复添加）")
    else:
        print(f"❌ 处理已有移动端样式的HTML失败（重复添加，数量: {mobile_count}）")
        return False
    
    print("🎉 HTML增强测试通过")
    return True

def test_file_validation():
    """测试文件验证功能"""
    print("\n🧪 测试3: 文件验证功能")
    
    # 创建临时测试文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <style>
        body { font-family: Arial; }
        @media (max-width: 768px) {
            .container { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">Test content</div>
</body>
</html>""")
        temp_file_with_mobile = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <style>
        body { font-family: Arial; }
        .container { max-width: 1200px; }
    </style>
</head>
<body>
    <div class="container">Test content</div>
</body>
</html>""")
        temp_file_without_mobile = f.name
    
    try:
        # 测试有移动端样式的文件
        if validate_mobile_styles(temp_file_with_mobile):
            print("✅ 正确识别包含移动端样式的文件")
        else:
            print("❌ 未能识别包含移动端样式的文件")
            return False
        
        # 测试没有移动端样式的文件
        if not validate_mobile_styles(temp_file_without_mobile):
            print("✅ 正确识别不包含移动端样式的文件")
        else:
            print("❌ 错误识别不包含移动端样式的文件")
            return False
        
        print("🎉 文件验证测试通过")
        return True
        
    finally:
        # 清理临时文件
        os.unlink(temp_file_with_mobile)
        os.unlink(temp_file_without_mobile)

def test_integration():
    """测试集成功能"""
    print("\n🧪 测试4: 集成测试")
    
    # 模拟新闻生成器的使用场景
    from glm_news_generator import GLMNewsGenerator
    
    try:
        # 创建生成器实例（不需要真实API密钥进行样式测试）
        generator = GLMNewsGenerator("test_key")
        
        # 测试备用CSS方法
        fallback_css = generator._get_fallback_mobile_css()
        
        if "@media (max-width: 768px)" in fallback_css:
            print("✅ 新闻生成器备用CSS功能正常")
        else:
            print("❌ 新闻生成器备用CSS功能异常")
            return False
        
        print("🎉 集成测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("📱 海之安新闻系统 - 移动端样式保护测试")
    print("=" * 60)
    
    tests = [
        test_css_generation,
        test_html_enhancement,
        test_file_validation,
        test_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！移动端样式保护机制工作正常")
        return True
    else:
        print("⚠️  部分测试失败，请检查样式保护机制")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)