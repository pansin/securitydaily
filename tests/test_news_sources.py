#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻源测试脚本
测试配置文件中的新闻源是否可用
"""

import requests
import feedparser
import time
import logging
from datetime import datetime
from news_sources_loader import NewsSourcesLoader

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsSourceTester:
    def __init__(self):
        """初始化新闻源测试器"""
        self.loader = NewsSourcesLoader()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = 15
        
    def test_single_source(self, source: dict) -> dict:
        """
        测试单个新闻源
        
        Args:
            source: 新闻源配置
            
        Returns:
            dict: 测试结果
        """
        result = {
            'name': source['name'],
            'url': source['rss_url'],
            'region': source.get('region', 'Unknown'),
            'category': source.get('category', 'Unknown'),
            'success': False,
            'error': None,
            'feed_title': None,
            'entry_count': 0,
            'latest_entry': None,
            'response_time': 0
        }
        
        try:
            start_time = time.time()
            
            # 发送请求
            response = requests.get(
                source['rss_url'], 
                headers=self.headers, 
                timeout=self.timeout
            )
            
            response_time = time.time() - start_time
            result['response_time'] = round(response_time, 2)
            
            if response.status_code == 200:
                # 解析RSS
                feed = feedparser.parse(response.content)
                
                if feed.bozo == 0 or len(feed.entries) > 0:
                    result['success'] = True
                    result['feed_title'] = getattr(feed.feed, 'title', 'Unknown')
                    result['entry_count'] = len(feed.entries)
                    
                    if feed.entries:
                        latest = feed.entries[0]
                        result['latest_entry'] = {
                            'title': getattr(latest, 'title', 'No title'),
                            'published': getattr(latest, 'published', 'No date')
                        }
                else:
                    result['error'] = f"RSS解析失败: {feed.bozo_exception if feed.bozo else 'No entries'}"
            else:
                result['error'] = f"HTTP {response.status_code}: {response.reason}"
                
        except requests.exceptions.Timeout:
            result['error'] = f"请求超时 (>{self.timeout}s)"
        except requests.exceptions.ConnectionError:
            result['error'] = "连接错误"
        except requests.exceptions.RequestException as e:
            result['error'] = f"请求异常: {str(e)}"
        except Exception as e:
            result['error'] = f"未知错误: {str(e)}"
        
        return result
    
    def test_all_sources(self, max_concurrent: int = 5) -> list:
        """
        测试所有启用的新闻源
        
        Args:
            max_concurrent: 最大并发数
            
        Returns:
            list: 所有测试结果
        """
        sources = self.loader.get_enabled_sources()
        results = []
        
        print(f"🧪 开始测试 {len(sources)} 个新闻源...")
        print("=" * 60)
        
        for i, source in enumerate(sources, 1):
            print(f"[{i}/{len(sources)}] 测试 {source['name']} ({source.get('region', 'Unknown')})...")
            
            result = self.test_single_source(source)
            results.append(result)
            
            # 显示结果
            if result['success']:
                print(f"  ✅ 成功 - {result['entry_count']} 条新闻 ({result['response_time']}s)")
                if result['latest_entry']:
                    print(f"     最新: {result['latest_entry']['title'][:50]}...")
            else:
                print(f"  ❌ 失败 - {result['error']}")
            
            # 避免请求过于频繁
            if i < len(sources):
                time.sleep(1)
        
        return results
    
    def test_by_region(self, region: str) -> list:
        """
        测试指定地区的新闻源
        
        Args:
            region: 地区名称
            
        Returns:
            list: 测试结果
        """
        sources = self.loader.get_sources_by_region(region)
        if not sources:
            print(f"❌ 未找到地区为 '{region}' 的新闻源")
            return []
        
        print(f"🌍 测试 {region} 地区的 {len(sources)} 个新闻源...")
        results = []
        
        for source in sources:
            result = self.test_single_source(source)
            results.append(result)
            
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {source['name']} - {result.get('error', 'OK')}")
        
        return results
    
    def test_official_sources(self) -> list:
        """
        测试官方权威新闻源
        
        Returns:
            list: 测试结果
        """
        sources = self.loader.get_official_sources()
        if not sources:
            print("❌ 未找到官方权威新闻源")
            return []
        
        print(f"🏛️ 测试 {len(sources)} 个官方权威新闻源...")
        results = []
        
        for source in sources:
            result = self.test_single_source(source)
            results.append(result)
            
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {source['name']} ({source.get('region', 'Unknown')})")
            if not result['success']:
                print(f"      错误: {result['error']}")
        
        return results
    
    def generate_test_report(self, results: list) -> dict:
        """
        生成测试报告
        
        Args:
            results: 测试结果列表
            
        Returns:
            dict: 报告统计
        """
        if not results:
            return {}
        
        total = len(results)
        successful = len([r for r in results if r['success']])
        failed = total - successful
        
        # 按地区统计
        regions = {}
        for result in results:
            region = result['region']
            if region not in regions:
                regions[region] = {'total': 0, 'success': 0}
            regions[region]['total'] += 1
            if result['success']:
                regions[region]['success'] += 1
        
        # 按类别统计
        categories = {}
        for result in results:
            category = result['category']
            if category not in categories:
                categories[category] = {'total': 0, 'success': 0}
            categories[category]['total'] += 1
            if result['success']:
                categories[category]['success'] += 1
        
        # 响应时间统计
        response_times = [r['response_time'] for r in results if r['success']]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        report = {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'avg_response_time': round(avg_response_time, 2),
            'regions': regions,
            'categories': categories,
            'failed_sources': [r for r in results if not r['success']]
        }
        
        return report
    
    def print_test_report(self, results: list):
        """
        打印测试报告
        
        Args:
            results: 测试结果列表
        """
        report = self.generate_test_report(results)
        
        if not report:
            print("❌ 无测试结果")
            return
        
        print("\n📊 测试报告")
        print("=" * 60)
        print(f"总数据源: {report['total']}")
        print(f"成功: {report['successful']} ({report['success_rate']:.1f}%)")
        print(f"失败: {report['failed']}")
        print(f"平均响应时间: {report['avg_response_time']}秒")
        
        if report['regions']:
            print("\n🌍 地区成功率:")
            for region, stats in report['regions'].items():
                rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
                print(f"  {region}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
        
        if report['categories']:
            print("\n📂 类别成功率:")
            for category, stats in report['categories'].items():
                rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
                print(f"  {category}: {stats['success']}/{stats['total']} ({rate:.1f}%)")
        
        if report['failed_sources']:
            print(f"\n❌ 失败的数据源 ({len(report['failed_sources'])} 个):")
            for failed in report['failed_sources']:
                print(f"  • {failed['name']} ({failed['region']}) - {failed['error']}")

def main():
    """主函数"""
    import sys
    
    tester = NewsSourceTester()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "all":
            results = tester.test_all_sources()
            tester.print_test_report(results)
        elif command == "official":
            results = tester.test_official_sources()
            tester.print_test_report(results)
        elif command == "region" and len(sys.argv) > 2:
            region = sys.argv[2]
            results = tester.test_by_region(region)
            tester.print_test_report(results)
        elif command == "quick":
            # 快速测试前5个源
            sources = tester.loader.get_enabled_sources()[:5]
            print(f"🚀 快速测试前 {len(sources)} 个新闻源...")
            results = []
            for source in sources:
                result = tester.test_single_source(source)
                results.append(result)
                status = "✅" if result['success'] else "❌"
                print(f"  {status} {source['name']}")
            tester.print_test_report(results)
        else:
            print("用法:")
            print("  python3 test_news_sources.py all        # 测试所有源")
            print("  python3 test_news_sources.py official   # 测试官方源")
            print("  python3 test_news_sources.py region 美国 # 测试指定地区")
            print("  python3 test_news_sources.py quick      # 快速测试")
    else:
        # 默认快速测试
        print("🧪 新闻源配置测试")
        print("=" * 40)
        
        # 显示配置统计
        tester.loader.print_statistics()
        
        print("\n🚀 执行快速测试...")
        sources = tester.loader.get_enabled_sources()[:3]
        for source in sources:
            result = tester.test_single_source(source)
            status = "✅" if result['success'] else "❌"
            print(f"  {status} {source['name']} ({source.get('region', 'Unknown')})")
        
        print("\n💡 使用 'python3 test_news_sources.py all' 进行完整测试")

if __name__ == "__main__":
    main()