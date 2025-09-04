#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置保护机制
防止新闻源配置被意外覆盖或修改
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from typing import Dict, List

class ConfigProtection:
    def __init__(self, config_file: str = "news_sources_config.json"):
        """
        初始化配置保护
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.backup_dir = ".config_backups"
        self.checksum_file = ".config_checksum"
        
        # 确保备份目录存在
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def calculate_checksum(self, file_path: str) -> str:
        """
        计算文件校验和
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: MD5校验和
        """
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return ""
    
    def save_checksum(self, checksum: str):
        """
        保存校验和到文件
        
        Args:
            checksum: 校验和值
        """
        try:
            with open(self.checksum_file, 'w') as f:
                f.write(checksum)
        except Exception:
            pass
    
    def load_checksum(self) -> str:
        """
        从文件加载校验和
        
        Returns:
            str: 校验和值
        """
        try:
            if os.path.exists(self.checksum_file):
                with open(self.checksum_file, 'r') as f:
                    return f.read().strip()
        except Exception:
            pass
        return ""
    
    def create_backup(self) -> str:
        """
        创建配置文件备份
        
        Returns:
            str: 备份文件路径
        """
        if not os.path.exists(self.config_file):
            return ""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"news_sources_config_{timestamp}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            shutil.copy2(self.config_file, backup_path)
            print(f"✅ 配置备份已创建: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ 创建备份失败: {e}")
            return ""
    
    def verify_integrity(self) -> bool:
        """
        验证配置文件完整性
        
        Returns:
            bool: 是否完整
        """
        if not os.path.exists(self.config_file):
            print("❌ 配置文件不存在")
            return False
        
        current_checksum = self.calculate_checksum(self.config_file)
        saved_checksum = self.load_checksum()
        
        if not saved_checksum:
            # 首次运行，保存当前校验和
            self.save_checksum(current_checksum)
            print("✅ 首次运行，已保存配置校验和")
            return True
        
        if current_checksum != saved_checksum:
            print("⚠️  配置文件已被修改")
            return False
        
        print("✅ 配置文件完整性验证通过")
        return True
    
    def validate_config_structure(self) -> bool:
        """
        验证配置文件结构
        
        Returns:
            bool: 结构是否有效
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 检查必需的顶级字段
            required_fields = ['version', 'news_sources']
            for field in required_fields:
                if field not in config:
                    print(f"❌ 配置缺少必需字段: {field}")
                    return False
            
            # 检查新闻源结构
            news_sources = config.get('news_sources', [])
            if not isinstance(news_sources, list):
                print("❌ news_sources 必须是数组")
                return False
            
            required_source_fields = ['name', 'rss_url', 'enabled']
            for i, source in enumerate(news_sources):
                for field in required_source_fields:
                    if field not in source:
                        print(f"❌ 新闻源 {i+1} 缺少必需字段: {field}")
                        return False
            
            print(f"✅ 配置结构验证通过 ({len(news_sources)} 个新闻源)")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件JSON格式错误: {e}")
            return False
        except Exception as e:
            print(f"❌ 配置验证失败: {e}")
            return False
    
    def protect_config(self) -> bool:
        """
        保护配置文件
        
        Returns:
            bool: 是否保护成功
        """
        print("🛡️  启动配置保护...")
        
        # 1. 验证文件存在
        if not os.path.exists(self.config_file):
            print(f"❌ 配置文件不存在: {self.config_file}")
            return False
        
        # 2. 验证结构
        if not self.validate_config_structure():
            print("❌ 配置结构验证失败")
            return False
        
        # 3. 创建备份
        backup_path = self.create_backup()
        if not backup_path:
            print("⚠️  备份创建失败，但继续保护")
        
        # 4. 更新校验和
        current_checksum = self.calculate_checksum(self.config_file)
        self.save_checksum(current_checksum)
        
        print("✅ 配置保护已启用")
        return True
    
    def check_for_changes(self) -> Dict:
        """
        检查配置是否有变化
        
        Returns:
            Dict: 变化检查结果
        """
        result = {
            'changed': False,
            'exists': False,
            'valid_structure': False,
            'current_checksum': '',
            'saved_checksum': '',
            'source_count': 0
        }
        
        if not os.path.exists(self.config_file):
            return result
        
        result['exists'] = True
        result['valid_structure'] = self.validate_config_structure()
        
        if result['valid_structure']:
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                result['source_count'] = len(config.get('news_sources', []))
            except Exception:
                pass
        
        current_checksum = self.calculate_checksum(self.config_file)
        saved_checksum = self.load_checksum()
        
        result['current_checksum'] = current_checksum
        result['saved_checksum'] = saved_checksum
        result['changed'] = current_checksum != saved_checksum
        
        return result
    
    def restore_from_backup(self, backup_filename: str = None) -> bool:
        """
        从备份恢复配置
        
        Args:
            backup_filename: 备份文件名，如果为None则使用最新备份
            
        Returns:
            bool: 是否恢复成功
        """
        if backup_filename:
            backup_path = os.path.join(self.backup_dir, backup_filename)
        else:
            # 找到最新的备份文件
            backup_files = []
            if os.path.exists(self.backup_dir):
                for f in os.listdir(self.backup_dir):
                    if f.startswith('news_sources_config_') and f.endswith('.json'):
                        backup_files.append(f)
            
            if not backup_files:
                print("❌ 未找到备份文件")
                return False
            
            backup_files.sort(reverse=True)  # 按时间倒序
            backup_path = os.path.join(self.backup_dir, backup_files[0])
        
        if not os.path.exists(backup_path):
            print(f"❌ 备份文件不存在: {backup_path}")
            return False
        
        try:
            # 验证备份文件
            with open(backup_path, 'r', encoding='utf-8') as f:
                json.load(f)  # 验证JSON格式
            
            # 恢复配置
            shutil.copy2(backup_path, self.config_file)
            
            # 更新校验和
            new_checksum = self.calculate_checksum(self.config_file)
            self.save_checksum(new_checksum)
            
            print(f"✅ 配置已从备份恢复: {backup_path}")
            return True
            
        except Exception as e:
            print(f"❌ 恢复失败: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """
        列出所有备份文件
        
        Returns:
            List[str]: 备份文件列表
        """
        backups = []
        if os.path.exists(self.backup_dir):
            for f in os.listdir(self.backup_dir):
                if f.startswith('news_sources_config_') and f.endswith('.json'):
                    backups.append(f)
        
        backups.sort(reverse=True)  # 按时间倒序
        return backups
    
    def cleanup_old_backups(self, keep_count: int = 10):
        """
        清理旧的备份文件
        
        Args:
            keep_count: 保留的备份数量
        """
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            print(f"✅ 备份数量 ({len(backups)}) 在限制内，无需清理")
            return
        
        to_delete = backups[keep_count:]
        deleted_count = 0
        
        for backup in to_delete:
            backup_path = os.path.join(self.backup_dir, backup)
            try:
                os.remove(backup_path)
                deleted_count += 1
            except Exception as e:
                print(f"⚠️  删除备份失败 {backup}: {e}")
        
        print(f"✅ 已清理 {deleted_count} 个旧备份文件")

def main():
    """主函数"""
    import sys
    
    protection = ConfigProtection()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "protect":
            protection.protect_config()
        elif command == "check":
            result = protection.check_for_changes()
            print("🔍 配置检查结果:")
            print(f"  文件存在: {'✅' if result['exists'] else '❌'}")
            print(f"  结构有效: {'✅' if result['valid_structure'] else '❌'}")
            print(f"  新闻源数量: {result['source_count']}")
            print(f"  文件已变化: {'⚠️ 是' if result['changed'] else '✅ 否'}")
        elif command == "backup":
            protection.create_backup()
        elif command == "restore":
            if len(sys.argv) > 2:
                protection.restore_from_backup(sys.argv[2])
            else:
                protection.restore_from_backup()
        elif command == "list-backups":
            backups = protection.list_backups()
            if backups:
                print(f"📁 备份文件 ({len(backups)} 个):")
                for backup in backups:
                    print(f"  • {backup}")
            else:
                print("❌ 未找到备份文件")
        elif command == "cleanup":
            keep_count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            protection.cleanup_old_backups(keep_count)
        else:
            print("用法:")
            print("  python3 config_protection.py protect      # 启用保护")
            print("  python3 config_protection.py check        # 检查变化")
            print("  python3 config_protection.py backup       # 创建备份")
            print("  python3 config_protection.py restore      # 恢复最新备份")
            print("  python3 config_protection.py list-backups # 列出备份")
            print("  python3 config_protection.py cleanup [数量] # 清理旧备份")
    else:
        # 默认执行保护
        protection.protect_config()

if __name__ == "__main__":
    main()