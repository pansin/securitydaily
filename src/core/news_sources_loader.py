#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻源配置加载器
负责加载和管理新闻数据源配置
"""

import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class NewsSourcesLoader:
    def __init__(self, config_file: str = None):
        if config_file is None:
            # 尝试不同的配置文件路径
            possible_paths = [
                "config/news_sources_config.json",
                "news_sources_config.json",
                os.path.join(os.path.dirname(__file__), "..", "..", "config", "news_sources_config.json")
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    config_file = path
                    break
            else:
                config_file = "config/news_sources_config.json"
        """
        初始化新闻源配置加载器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = None
        self.load_config()
    
    def load_config(self) -> bool:
        """
        加载新闻源配置
        
        Returns:
            bool: 是否加载成功
        """
        try:
            if not os.path.exists(self.config_file):
                logger.error(f"配置文件不存在: {self.config_file}")
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            logger.info(f"✅ 成功加载新闻源配置: {len(self.config.get('news_sources', []))} 个数据源")
            return True
            
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            return False
    
    def get_enabled_sources(self) -> List[Dict]:
        """
        获取启用的新闻源列表
        
        Returns:
            List[Dict]: 启用的新闻源配置列表
        """
        if not self.config:
            return []
        
        enabled_sources = []
        for source in self.config.get('news_sources', []):
            if source.get('enabled', True):
                enabled_sources.append(source)
        
        logger.info(f"📰 获取到 {len(enabled_sources)} 个启用的新闻源")
        return enabled_sources
    
    def get_sources_by_region(self, region: str) -> List[Dict]:
        """
        按地区筛选新闻源
        
        Args:
            region: 地区名称
            
        Returns:
            List[Dict]: 指定地区的新闻源列表
        """
        enabled_sources = self.get_enabled_sources()
        return [source for source in enabled_sources if source.get('region') == region]
    
    def get_sources_by_language(self, language: str) -> List[Dict]:
        """
        按语言筛选新闻源
        
        Args:
            language: 语言代码 (zh/en)
            
        Returns:
            List[Dict]: 指定语言的新闻源列表
        """
        enabled_sources = self.get_enabled_sources()
        return [source for source in enabled_sources if source.get('language') == language]
    
    def get_sources_by_category(self, category: str) -> List[Dict]:
        """
        按类别筛选新闻源
        
        Args:
            category: 类别名称
            
        Returns:
            List[Dict]: 指定类别的新闻源列表
        """
        enabled_sources = self.get_enabled_sources()
        return [source for source in enabled_sources if source.get('category') == category]
    
    def get_high_priority_sources(self) -> List[Dict]:
        """
        获取高优先级新闻源（权重 >= 1.1）
        
        Returns:
            List[Dict]: 高优先级新闻源列表
        """
        enabled_sources = self.get_enabled_sources()
        return [source for source in enabled_sources if source.get('weight', 1.0) >= 1.1]
    
    def get_official_sources(self) -> List[Dict]:
        """
        获取官方权威新闻源
        
        Returns:
            List[Dict]: 官方新闻源列表
        """
        official_categories = ['官方警报', '官方指导', '标准规范']
        enabled_sources = self.get_enabled_sources()
        return [source for source in enabled_sources if source.get('category') in official_categories]
    
    def get_source_statistics(self) -> Dict:
        """
        获取新闻源统计信息
        
        Returns:
            Dict: 统计信息
        """
        if not self.config:
            return {}
        
        all_sources = self.config.get('news_sources', [])
        enabled_sources = self.get_enabled_sources()
        
        # 按地区统计
        regions = {}
        for source in enabled_sources:
            region = source.get('region', 'Unknown')
            regions[region] = regions.get(region, 0) + 1
        
        # 按语言统计
        languages = {}
        for source in enabled_sources:
            language = source.get('language', 'unknown')
            languages[language] = languages.get(language, 0) + 1
        
        # 按类别统计
        categories = {}
        for source in enabled_sources:
            category = source.get('category', 'Unknown')
            categories[category] = categories.get(category, 0) + 1
        
        return {
            'total_sources': len(all_sources),
            'enabled_sources': len(enabled_sources),
            'disabled_sources': len(all_sources) - len(enabled_sources),
            'regions': regions,
            'languages': languages,
            'categories': categories,
            'high_priority_count': len(self.get_high_priority_sources()),
            'official_sources_count': len(self.get_official_sources())
        }
    
    def validate_source(self, source: Dict) -> bool:
        """
        验证新闻源配置的完整性
        
        Args:
            source: 新闻源配置
            
        Returns:
            bool: 是否有效
        """
        required_fields = ['name', 'rss_url', 'weight', 'language', 'region', 'category', 'enabled']
        
        for field in required_fields:
            if field not in source:
                logger.warning(f"新闻源 {source.get('name', 'Unknown')} 缺少必需字段: {field}")
                return False
        
        # 验证权重范围
        weight = source.get('weight', 1.0)
        if not (0.5 <= weight <= 1.5):
            logger.warning(f"新闻源 {source['name']} 权重超出范围: {weight}")
            return False
        
        return True
    
    def add_source(self, source: Dict) -> bool:
        """
        添加新的新闻源
        
        Args:
            source: 新闻源配置
            
        Returns:
            bool: 是否添加成功
        """
        if not self.config:
            logger.error("配置未加载，无法添加新闻源")
            return False
        
        if not self.validate_source(source):
            logger.error(f"新闻源配置无效: {source.get('name', 'Unknown')}")
            return False
        
        # 检查是否已存在
        existing_names = [s['name'] for s in self.config['news_sources']]
        if source['name'] in existing_names:
            logger.warning(f"新闻源已存在: {source['name']}")
            return False
        
        self.config['news_sources'].append(source)
        logger.info(f"✅ 成功添加新闻源: {source['name']}")
        return True
    
    def disable_source(self, source_name: str) -> bool:
        """
        禁用指定的新闻源
        
        Args:
            source_name: 新闻源名称
            
        Returns:
            bool: 是否操作成功
        """
        if not self.config:
            return False
        
        for source in self.config['news_sources']:
            if source['name'] == source_name:
                source['enabled'] = False
                logger.info(f"🚫 已禁用新闻源: {source_name}")
                return True
        
        logger.warning(f"未找到新闻源: {source_name}")
        return False
    
    def enable_source(self, source_name: str) -> bool:
        """
        启用指定的新闻源
        
        Args:
            source_name: 新闻源名称
            
        Returns:
            bool: 是否操作成功
        """
        if not self.config:
            return False
        
        for source in self.config['news_sources']:
            if source['name'] == source_name:
                source['enabled'] = True
                logger.info(f"✅ 已启用新闻源: {source_name}")
                return True
        
        logger.warning(f"未找到新闻源: {source_name}")
        return False
    
    def save_config(self) -> bool:
        """
        保存配置到文件
        
        Returns:
            bool: 是否保存成功
        """
        if not self.config:
            return False
        
        try:
            # 更新最后修改时间
            self.config['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 配置已保存到: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False
    
    def print_statistics(self):
        """
        打印新闻源统计信息
        """
        stats = self.get_source_statistics()
        
        print("📊 新闻源统计信息")
        print("=" * 40)
        print(f"总数据源: {stats['total_sources']}")
        print(f"启用数据源: {stats['enabled_sources']}")
        print(f"禁用数据源: {stats['disabled_sources']}")
        print(f"高优先级源: {stats['high_priority_count']}")
        print(f"官方权威源: {stats['official_sources_count']}")
        
        print("\n🌍 地区分布:")
        for region, count in stats['regions'].items():
            print(f"  {region}: {count}")
        
        print("\n🗣️ 语言分布:")
        for language, count in stats['languages'].items():
            lang_name = "中文" if language == "zh" else "英文" if language == "en" else language
            print(f"  {lang_name}: {count}")
        
        print("\n📂 类别分布:")
        for category, count in stats['categories'].items():
            print(f"  {category}: {count}")

def main():
    """主函数 - 用于测试和管理新闻源配置"""
    import sys
    
    loader = NewsSourcesLoader()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "stats":
            loader.print_statistics()
        elif command == "list":
            sources = loader.get_enabled_sources()
            print(f"📰 启用的新闻源 ({len(sources)} 个):")
            for source in sources:
                print(f"  • {source['name']} ({source['region']}) - {source['category']}")
        elif command == "official":
            sources = loader.get_official_sources()
            print(f"🏛️ 官方权威源 ({len(sources)} 个):")
            for source in sources:
                print(f"  • {source['name']} - {source['description']}")
        elif command == "high-priority":
            sources = loader.get_high_priority_sources()
            print(f"⭐ 高优先级源 ({len(sources)} 个):")
            for source in sources:
                print(f"  • {source['name']} (权重: {source['weight']})")
        else:
            print("用法: python3 news_sources_loader.py [stats|list|official|high-priority]")
    else:
        loader.print_statistics()

if __name__ == "__main__":
    main()