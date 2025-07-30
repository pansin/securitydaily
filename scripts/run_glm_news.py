#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行GLM新闻生成器
如果没有API密钥，将使用基础版本生成新闻
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_glm_api_key():
    """检查GLM API密钥是否可用"""
    api_key = os.getenv('GLM_API_KEY')
    if not api_key:
        try:
            from config.glm_config import GLM_CONFIG
            api_key = GLM_CONFIG.get('api_key')
        except ImportError:
            pass
    
    return api_key and api_key.strip()

def run_with_glm():
    """使用GLM API运行增强版新闻生成器"""
    try:
        from src.core.glm_news_generator import GLMNewsGenerator
        
        api_key = os.getenv('GLM_API_KEY')
        if not api_key:
            from config.glm_config import GLM_CONFIG
            api_key = GLM_CONFIG.get('api_key')
        
        generator = GLMNewsGenerator(api_key)
        result = generator.generate_daily_report(days_back=1)
        
        if result:
            print(f"🎉 AI智能新闻快报生成成功: {result}")
            return True
        else:
            print("❌ AI新闻快报生成失败")
            return False
            
    except Exception as e:
        print(f"❌ GLM新闻生成器运行失败: {e}")
        return False

def run_basic_scraper():
    """运行基础版新闻抓取器"""
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'news_scraper.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ 基础新闻抓取完成")
            print(result.stdout)
            return True
        else:
            print("❌ 基础新闻抓取失败")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 基础新闻抓取器运行失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 海之安网络安全新闻生成器")
    print("=" * 50)
    
    # 检查GLM API密钥
    if check_glm_api_key():
        print("🤖 检测到GLM API密钥，使用AI增强版生成器...")
        success = run_with_glm()
    else:
        print("📰 未检测到GLM API密钥，使用基础版生成器...")
        print("💡 提示：设置GLM_API_KEY环境变量或配置glm_config.py可启用AI增强功能")
        print("🔗 获取API密钥：https://open.bigmodel.cn/")
        print()
        success = run_basic_scraper()
    
    if success:
        # 更新动态主页
        try:
            import subprocess
            result = subprocess.run([sys.executable, 'src/core/generate_index.py'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ 动态主页已更新")
            else:
                print("⚠️ 动态主页更新失败，使用默认版本")
        except Exception as e:
            print(f"⚠️ 动态主页生成器执行失败: {e}")
        
        # 更新索引
        try:
            import subprocess
            subprocess.run([sys.executable, 'scripts/start_monitor.py'], check=True)
            print("📋 新闻索引已更新")
        except:
            print("⚠️  新闻索引更新失败，请手动运行 python3 start_monitor.py")
    
    print("=" * 50)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"⏰ 任务完成时间: {current_time}")

if __name__ == "__main__":
    main()