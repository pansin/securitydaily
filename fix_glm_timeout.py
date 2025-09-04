#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM API超时问题快速修复脚本
"""

import os
import sys
import logging
from datetime import datetime, timedelta

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('glm_timeout_fix.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(__name__)

def check_glm_config():
    """检查GLM配置"""
    logger = logging.getLogger(__name__)
    
    try:
        from config.glm_config import GLM_CONFIG
        api_key = GLM_CONFIG.get('api_key') or os.getenv('GLM_API_KEY')
        
        if not api_key:
            logger.error("GLM API密钥未配置")
            return False
        
        logger.info("GLM配置检查通过")
        return True
        
    except ImportError as e:
        logger.error(f"无法导入GLM配置: {e}")
        return False

def test_enhanced_client():
    """测试增强版GLM客户端"""
    logger = logging.getLogger(__name__)
    
    try:
        from utils.enhanced_glm_client import create_enhanced_glm_client
        
        api_key = os.getenv('GLM_API_KEY')
        if not api_key:
            from config.glm_config import GLM_CONFIG
            api_key = GLM_CONFIG.get('api_key')
        
        if not api_key:
            logger.error("API密钥未找到")
            return False
        
        logger.info("创建增强版GLM客户端...")
        client = create_enhanced_glm_client(api_key)
        
        # 简单测试
        logger.info("测试API调用...")
        messages = [{"role": "user", "content": "Hello, this is a test."}]
        result = client.call_api(messages, retry_count=2)
        
        if result:
            logger.info("✅ 增强版GLM客户端工作正常")
            return True
        else:
            logger.error("❌ 增强版GLM客户端测试失败")
            return False
            
    except Exception as e:
        logger.error(f"增强版GLM客户端测试异常: {e}")
        return False

def run_diagnostics():
    """运行GLM诊断"""
    logger = logging.getLogger(__name__)
    
    try:
        from utils.glm_diagnostics import GLMDiagnostics
        
        api_key = os.getenv('GLM_API_KEY')
        if not api_key:
            from config.glm_config import GLM_CONFIG
            api_key = GLM_CONFIG.get('api_key')
        
        logger.info("运行GLM API诊断...")
        diagnostics = GLMDiagnostics(api_key)
        results = diagnostics.run_full_diagnostics()
        
        if results['connectivity']['success']:
            logger.info("✅ GLM API连接正常")
            return True
        else:
            logger.error(f"❌ GLM API连接失败: {results['connectivity'].get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"GLM诊断异常: {e}")
        return False

def generate_news_with_enhanced_client():
    """使用增强版客户端生成新闻"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("使用增强版GLM客户端生成新闻...")
        
        # 导入新闻生成器
        from src.core.glm_news_generator import GLMNewsGenerator
        
        api_key = os.getenv('GLM_API_KEY')
        if not api_key:
            from config.glm_config import GLM_CONFIG
            api_key = GLM_CONFIG.get('api_key')
        
        generator = GLMNewsGenerator(api_key)
        
        # 生成昨天的新闻
        yesterday = datetime.now() - timedelta(days=1)
        target_date = yesterday.strftime('%Y-%m-%d')
        
        logger.info(f"生成 {target_date} 的新闻快报...")
        result = generator.generate_daily_report(days_back=1)
        
        if result:
            logger.info("✅ 新闻生成成功")
            return True
        else:
            logger.error("❌ 新闻生成失败")
            return False
            
    except Exception as e:
        logger.error(f"新闻生成异常: {e}")
        return False

def main():
    """主函数"""
    print("🔧 GLM API超时问题快速修复工具")
    print("=" * 50)
    
    logger = setup_logging()
    
    # 步骤1: 检查GLM配置
    print("1️⃣ 检查GLM配置...")
    if not check_glm_config():
        print("❌ GLM配置检查失败，请检查API密钥设置")
        return False
    print("✅ GLM配置正常")
    
    # 步骤2: 测试增强版客户端
    print("\n2️⃣ 测试增强版GLM客户端...")
    if not test_enhanced_client():
        print("❌ 增强版客户端测试失败")
        return False
    print("✅ 增强版客户端正常")
    
    # 步骤3: 运行诊断
    print("\n3️⃣ 运行GLM API诊断...")
    if not run_diagnostics():
        print("❌ GLM API诊断发现问题")
        print("💡 建议:")
        print("   - 检查网络连接")
        print("   - 验证API密钥是否有效")
        print("   - 稍后重试")
        return False
    print("✅ GLM API诊断正常")
    
    # 步骤4: 生成新闻测试
    print("\n4️⃣ 测试新闻生成...")
    if not generate_news_with_enhanced_client():
        print("❌ 新闻生成测试失败")
        print("💡 可能的原因:")
        print("   - GLM API临时不稳定")
        print("   - 网络连接问题")
        print("   - 请求频率过高")
        return False
    print("✅ 新闻生成测试成功")
    
    print("\n🎉 GLM API超时问题修复完成！")
    print("\n📋 修复总结:")
    print("✅ 已启用增强版GLM客户端")
    print("✅ 增加了重试机制和更长的超时时间")
    print("✅ 改进了错误处理和JSON解析")
    print("✅ 添加了API诊断工具")
    
    print("\n💡 使用建议:")
    print("- 正常运行: python start.py")
    print("- API诊断: python utils/glm_diagnostics.py")
    print("- 翻译修复: python fix_translation.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)