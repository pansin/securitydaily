#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试全球新闻源的可用性
"""

import requests
import feedparser
import time
from datetime import datetime
from glm_config import NEWS_SOURCES

def test_rss_source(source):
    """测试单个RSS源"""
    try:
        print(f"测试 {source['name']} ({source.get('region', 'Unknown')})...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        start_time = time.time()
        response = requests.get(source['rss_url'], headers=headers, timeout=15)
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                latest_entry = feed.entries[0]
                print(f"  ✅ 成功 - 响应时间: {response_time:.2f}s")
                print(f"     文章数量: {len(feed.entries)}")
                print(f"     最新文章: {latest_entry.title[:60]}...")
                print(f"     发布时间: {getattr(latest_entry, 'published', '未知')}")
                return True
            else:
                print(f"  ⚠️  RSS源无内容")
                return False
        else:
            print(f"  ❌ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 连接失败: {e}")
        return False

def main():
    """主函数"""
    print("🌍 全球网络安全新闻源可用性测试")
    print("=" * 60)
    
    total_sources = len(NEWS_SOURCES)
    successful_sources = 0
    failed_sources = []
    
    for i, source in enumerate(NEWS_SOURCES, 1):
        print(f"\n[{i}/{total_sources}] ", end="")
        
        if test_rss_source(source):
            successful_sources += 1
        else:
            failed_sources.append(source['name'])
        
        # 避免请求过于频繁
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("📊 测试结果统计:")
    print(f"   总计: {total_sources} 个新闻源")
    print(f"   成功: {successful_sources} 个 ({successful_sources/total_sources*100:.1f}%)")
    print(f"   失败: {len(failed_sources)} 个")
    
    if failed_sources:
        print(f"\n❌ 失败的新闻源:")
        for source in failed_sources:
            print(f"   - {source}")
    
    print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()