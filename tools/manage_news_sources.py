#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻源管理脚本
用于管理新闻数据源配置
"""

import json
import sys
from datetime import datetime
from news_sources_loader import NewsSourcesLoader

class NewsSourceManager:
    def __init__(self):
        """初始化新闻源管理器"""
        self.loader = NewsSourcesLoader()
    
    def list_sources(self, filter_type: str = None, filter_value: str = None):
        """
        列出新闻源
        
        Args:
            filter_type: 过滤类型 (region/language/category/enabled)
            filter_value: 过滤值
        """
        if filter_type == "region":
            sources = self.loader.get_sources_by_region(filter_value)
            title = f"🌍 {filter_value} 地区的新闻源"
        elif filter_type == "language":
            sources = self.loader.get_sources_by_language(filter_value)
            lang_name = "中文" if filter_value == "zh" else "英文" if filter_value == "en" else filter_value
            title = f"🗣️ {lang_name} 新闻源"
        elif filter_type == "category":
            sources = self.loader.get_sources_by_category(filter_value)
            title = f"📂 {filter_value} 类别的新闻源"
        elif filter_type == "enabled":
            if filter_value.lower() in ['true', '1', 'yes']:
                sources = self.loader.get_enabled_sources()
                title = "✅ 启用的新闻源"
            else:
                all_sources = self.loader.config.get('news_sources', [])
                sources = [s for s in all_sources if not s.get('enabled', True)]
                title = "🚫 禁用的新闻源"
        else:
            sources = self.loader.get_enabled_sources()
            title = "📰 所有启用的新闻源"
        
        print(title)
        print("=" * 60)
        
        if not sources:
            print("❌ 未找到匹配的新闻源")
            return
        
        for i, source in enumerate(sources, 1):
            status = "✅" if source.get('enabled', True) else "🚫"
            weight_star = "⭐" if source.get('weight', 1.0) >= 1.1 else ""
            
            print(f"{i:2d}. {status} {source['name']} {weight_star}")
            print(f"     地区: {source.get('region', 'Unknown')} | "
                  f"语言: {source.get('language', 'unknown')} | "
                  f"类别: {source.get('category', 'Unknown')}")
            print(f"     权重: {source.get('weight', 1.0)} | "
                  f"RSS: {source['rss_url']}")
            if source.get('description'):
                print(f"     描述: {source['description']}")
            print()
    
    def add_source(self):
        """交互式添加新闻源"""
        print("➕ 添加新的新闻源")
        print("=" * 40)
        
        try:
            name = input("新闻源名称: ").strip()
            if not name:
                print("❌ 名称不能为空")
                return
            
            rss_url = input("RSS链接: ").strip()
            if not rss_url:
                print("❌ RSS链接不能为空")
                return
            
            print("\n可选地区: 中国, 美国, 英国, 欧盟, 国际, 等")
            region = input("地区 [国际]: ").strip() or "国际"
            
            print("\n可选语言: zh (中文), en (英文)")
            language = input("语言 [en]: ").strip() or "en"
            
            print("\n可选类别: 综合安全, 威胁情报, 官方警报, 企业安全, 等")
            category = input("类别 [综合安全]: ").strip() or "综合安全"
            
            weight_str = input("权重 (0.5-1.5) [1.0]: ").strip() or "1.0"
            try:
                weight = float(weight_str)
                if not (0.5 <= weight <= 1.5):
                    print("⚠️ 权重超出范围，使用默认值 1.0")
                    weight = 1.0
            except ValueError:
                print("⚠️ 权重格式错误，使用默认值 1.0")
                weight = 1.0
            
            description = input("描述 (可选): ").strip()
            
            enabled_str = input("启用 [y/N]: ").strip().lower()
            enabled = enabled_str in ['y', 'yes', '1', 'true']
            
            # 创建新闻源配置
            new_source = {
                "name": name,
                "rss_url": rss_url,
                "weight": weight,
                "language": language,
                "region": region,
                "category": category,
                "enabled": enabled,
                "description": description
            }
            
            # 添加到配置
            if self.loader.add_source(new_source):
                print(f"\n✅ 成功添加新闻源: {name}")
                
                save = input("保存到配置文件? [y/N]: ").strip().lower()
                if save in ['y', 'yes', '1', 'true']:
                    if self.loader.save_config():
                        print("✅ 配置已保存")
                    else:
                        print("❌ 保存失败")
            else:
                print(f"\n❌ 添加新闻源失败")
                
        except KeyboardInterrupt:
            print("\n\n❌ 操作已取消")
        except Exception as e:
            print(f"\n❌ 添加失败: {e}")
    
    def toggle_source(self, source_name: str, enable: bool):
        """
        启用或禁用新闻源
        
        Args:
            source_name: 新闻源名称
            enable: True为启用，False为禁用
        """
        if enable:
            success = self.loader.enable_source(source_name)
            action = "启用"
        else:
            success = self.loader.disable_source(source_name)
            action = "禁用"
        
        if success:
            print(f"✅ 成功{action}新闻源: {source_name}")
            
            save = input("保存到配置文件? [y/N]: ").strip().lower()
            if save in ['y', 'yes', '1', 'true']:
                if self.loader.save_config():
                    print("✅ 配置已保存")
                else:
                    print("❌ 保存失败")
        else:
            print(f"❌ {action}新闻源失败: {source_name}")
    
    def show_statistics(self):
        """显示统计信息"""
        self.loader.print_statistics()
    
    def export_config(self, filename: str):
        """
        导出配置到文件
        
        Args:
            filename: 导出文件名
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.loader.config, f, ensure_ascii=False, indent=2)
            print(f"✅ 配置已导出到: {filename}")
        except Exception as e:
            print(f"❌ 导出失败: {e}")
    
    def backup_config(self):
        """备份当前配置"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"news_sources_config_backup_{timestamp}.json"
        self.export_config(backup_filename)
    
    def show_help(self):
        """显示帮助信息"""
        print("📰 新闻源管理脚本")
        print("=" * 50)
        print("用法: python3 manage_news_sources.py [命令] [参数]")
        print()
        print("命令:")
        print("  list                    - 列出所有启用的新闻源")
        print("  list region 美国        - 列出指定地区的新闻源")
        print("  list language zh        - 列出指定语言的新闻源")
        print("  list category 官方警报  - 列出指定类别的新闻源")
        print("  list enabled false      - 列出禁用的新闻源")
        print("  add                     - 交互式添加新闻源")
        print("  enable <名称>           - 启用指定新闻源")
        print("  disable <名称>          - 禁用指定新闻源")
        print("  stats                   - 显示统计信息")
        print("  backup                  - 备份当前配置")
        print("  export <文件名>         - 导出配置到文件")
        print("  help                    - 显示此帮助信息")
        print()
        print("示例:")
        print("  python3 manage_news_sources.py list region 美国")
        print("  python3 manage_news_sources.py enable 'Krebs on Security'")
        print("  python3 manage_news_sources.py backup")

def main():
    """主函数"""
    manager = NewsSourceManager()
    
    if len(sys.argv) < 2:
        manager.show_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "list":
            if len(sys.argv) >= 4:
                filter_type = sys.argv[2]
                filter_value = sys.argv[3]
                manager.list_sources(filter_type, filter_value)
            else:
                manager.list_sources()
        
        elif command == "add":
            manager.add_source()
        
        elif command == "enable":
            if len(sys.argv) >= 3:
                source_name = sys.argv[2]
                manager.toggle_source(source_name, True)
            else:
                print("❌ 请指定新闻源名称")
        
        elif command == "disable":
            if len(sys.argv) >= 3:
                source_name = sys.argv[2]
                manager.toggle_source(source_name, False)
            else:
                print("❌ 请指定新闻源名称")
        
        elif command == "stats":
            manager.show_statistics()
        
        elif command == "backup":
            manager.backup_config()
        
        elif command == "export":
            if len(sys.argv) >= 3:
                filename = sys.argv[2]
                manager.export_config(filename)
            else:
                print("❌ 请指定导出文件名")
        
        elif command == "help":
            manager.show_help()
        
        else:
            print(f"❌ 未知命令: {command}")
            manager.show_help()
    
    except KeyboardInterrupt:
        print("\n\n👋 操作已取消")
    except Exception as e:
        print(f"❌ 执行失败: {e}")

if __name__ == "__main__":
    main()