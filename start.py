#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海之安新闻系统启动脚本
简化项目启动流程
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """主函数"""
    print("🌊 海之安网络安全新闻系统")
    print("=" * 50)
    print("🚀 正在启动系统...")
    
    # 确保在项目根目录
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # 检查依赖
    try:
        import requests
        import feedparser
        from bs4 import BeautifulSoup
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("💡 请运行: pip install -r requirements.txt")
        return
    
    # 运行新闻生成
    try:
        result = subprocess.run([
            sys.executable, 'scripts/run_glm_news.py'
        ], check=True)
        
        print("🎉 新闻生成完成！")
        print("📱 请打开 index.html 查看结果")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 运行失败: {e}")
        print("💡 请检查配置和网络连接")
    except KeyboardInterrupt:
        print("\n👋 用户取消操作")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    main()