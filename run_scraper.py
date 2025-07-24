#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络安全新闻爬虫定时执行脚本
"""

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper_scheduler.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_news_scraper():
    """运行新闻爬虫"""
    try:
        logger.info("开始执行网络安全新闻爬虫...")
        
        # 运行新闻爬虫脚本
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'news_scraper.py')
        ], capture_output=True, text=True, timeout=300)  # 5分钟超时
        
        if result.returncode == 0:
            logger.info("新闻爬虫执行成功")
            logger.debug(f"输出: {result.stdout}")
            
            # 如果爬虫成功执行，运行索引生成器更新首页
            logger.info("正在更新新闻索引...")
            index_result = subprocess.run([
                sys.executable,
                os.path.join(os.path.dirname(__file__), 'start_monitor.py')
            ], capture_output=True, text=True, timeout=60)
            
            if index_result.returncode == 0:
                logger.info("新闻索引更新成功")
            else:
                logger.error(f"新闻索引更新失败: {index_result.stderr}")
        else:
            logger.error(f"新闻爬虫执行失败: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logger.error("新闻爬虫执行超时")
    except Exception as e:
        logger.error(f"执行新闻爬虫时发生错误: {e}")

def main():
    """主函数"""
    logger.info("网络安全新闻爬虫定时任务启动")
    logger.info(f"当前工作目录: {os.getcwd()}")
    
    # 立即执行一次
    run_news_scraper()
    
    # 安排定时任务
    # 每天上午9点执行
    schedule.every().day.at("09:00").do(run_news_scraper)
    
    # 每天下午3点执行
    schedule.every().day.at("15:00").do(run_news_scraper)
    
    logger.info("定时任务已设置:")
    logger.info("- 每天上午9:00执行")
    logger.info("- 每天下午3:00执行")
    logger.info("按 Ctrl+C 停止定时任务")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logger.info("定时任务已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
