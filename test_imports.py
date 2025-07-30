#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入是否正常
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试各种导入"""
    print("🧪 测试项目导入...")
    
    # 测试配置导入
    try:
        from config.glm_config import GLM_CONFIG, PROMPT_TEMPLATES
        print("✅ GLM配置导入成功")
    except ImportError as e:
        print(f"❌ GLM配置导入失败: {e}")
    
    # 测试新闻源加载器
    try:
        from src.core.news_sources_loader import NewsSourcesLoader
        loader = NewsSourcesLoader()
        sources = loader.get_enabled_sources()
        print(f"✅ 新闻源加载器导入成功，加载了 {len(sources)} 个源")
    except ImportError as e:
        print(f"❌ 新闻源加载器导入失败: {e}")
    except Exception as e:
        print(f"⚠️ 新闻源加载器运行失败: {e}")
    
    # 测试GLM新闻生成器
    try:
        from src.core.glm_news_generator import GLMNewsGenerator
        print("✅ GLM新闻生成器导入成功")
    except ImportError as e:
        print(f"❌ GLM新闻生成器导入失败: {e}")
    except Exception as e:
        print(f"⚠️ GLM新闻生成器导入异常: {e}")
    
    # 测试增强爬虫
    try:
        from src.crawlers.enhanced_crawler import EnhancedNewsCrawler
        print("✅ 增强爬虫导入成功")
    except ImportError as e:
        print(f"❌ 增强爬虫导入失败: {e}")
    
    print("🧪 导入测试完成")

if __name__ == "__main__":
    test_imports()