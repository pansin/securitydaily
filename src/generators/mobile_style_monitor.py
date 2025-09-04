#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端样式监控和保护脚本
定期检查和修复新闻文件的移动端样式
"""

import os
import time
import glob
from datetime import datetime
from style_protection import validate_mobile_styles, auto_fix_existing_files, ensure_mobile_responsive

class MobileStyleMonitor:
    def __init__(self):
        self.check_interval = 300  # 5分钟检查一次
        self.last_check = 0
        
    def monitor_files(self):
        """
        监控新闻文件的移动端样式
        """
        print(f"🔍 [{datetime.now().strftime('%H:%M:%S')}] 开始检查移动端样式...")
        
        news_files = glob.glob("news*.html")
        if not news_files:
            print("📝 未找到新闻文件")
            return
        
        issues_found = 0
        for file_path in news_files:
            if not validate_mobile_styles(file_path):
                print(f"⚠️  {file_path} 缺失移动端样式")
                issues_found += 1
            else:
                print(f"✅ {file_path} 移动端样式正常")
        
        if issues_found > 0:
            print(f"🔧 发现 {issues_found} 个文件需要修复，开始自动修复...")
            fixed_count = auto_fix_existing_files()
            print(f"✅ 成功修复 {fixed_count} 个文件")
        else:
            print("🎉 所有文件的移动端样式都正常")
    
    def run_continuous_monitor(self):
        """
        持续监控模式
        """
        print("🚀 启动移动端样式持续监控...")
        print(f"⏰ 检查间隔: {self.check_interval}秒")
        print("按 Ctrl+C 停止监控")
        
        try:
            while True:
                self.monitor_files()
                print(f"😴 等待 {self.check_interval} 秒后进行下次检查...\n")
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n👋 监控已停止")
    
    def run_single_check(self):
        """
        单次检查模式
        """
        self.monitor_files()

def main():
    """主函数"""
    import sys
    
    monitor = MobileStyleMonitor()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        monitor.run_continuous_monitor()
    else:
        print("📱 海之安新闻系统 - 移动端样式保护")
        print("=" * 50)
        monitor.run_single_check()
        print("\n💡 提示: 使用 --continuous 参数启动持续监控模式")

if __name__ == "__main__":
    main()