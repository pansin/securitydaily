#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海之安网络安全新闻系统 - 增强版启动脚本
提供智能配置管理、系统健康检查和用户友好的交互体验
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum

# ============================================================================
# 核心数据模型
# ============================================================================

class ConfigSource(Enum):
    """配置来源枚举"""
    ENVIRONMENT = "environment"
    CONFIG_FILE = "config_file"
    INTERACTIVE = "interactive"
    NONE = "none"

class HealthStatus(Enum):
    """健康状态枚举"""
    HEALTHY = "healthy"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class IssueCategory(Enum):
    """问题分类枚举"""
    DEPENDENCY = "dependency"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    CONFIG = "config"
    API = "api"

@dataclass
class KeyInfo:
    """API密钥信息"""
    masked_key: str
    is_valid: bool
    expiry_date: Optional[datetime] = None
    usage_quota: Optional[int] = None
    remaining_quota: Optional[int] = None
    error_message: Optional[str] = None

@dataclass
class ConfigStatus:
    """配置状态"""
    glm_key_present: bool
    glm_key_valid: bool
    config_source: ConfigSource
    key_info: Optional[KeyInfo] = None
    issues: List[str] = None
    
    def __post_init__(self):
        if self.issues is None:
            self.issues = []

@dataclass
class Issue:
    """系统问题"""
    severity: HealthStatus
    category: IssueCategory
    message: str
    suggested_action: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

@dataclass
class PackageStatus:
    """包状态"""
    name: str
    required: bool
    installed: bool
    version: Optional[str] = None
    required_version: Optional[str] = None
    install_command: Optional[str] = None

@dataclass
class NetworkStatus:
    """网络状态"""
    internet_connected: bool
    api_endpoints: Dict[str, bool]
    issues: List[Issue]

@dataclass
class FileSystemStatus:
    """文件系统状态"""
    required_directories: Dict[str, bool]
    permissions: Dict[str, bool]
    disk_space_mb: float
    issues: List[Issue]

@dataclass
class HealthReport:
    """健康检查报告"""
    overall_status: HealthStatus
    dependency_status: Dict[str, PackageStatus]
    network_status: NetworkStatus
    filesystem_status: FileSystemStatus
    issues: List[Issue]
    timestamp: datetime
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class OperationMetrics:
    """操作指标"""
    name: str
    duration: float
    success: bool
    details: Dict[str, Any]
    timestamp: datetime
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class PerformanceSummary:
    """性能摘要"""
    total_duration: float
    operations: List[OperationMetrics]
    system_resources: Dict[str, Any]
    recommendations: List[str]

# ============================================================================
# 基础配置管理器
# ============================================================================

class ConfigManager:
    """配置管理器 - 负责所有配置相关操作"""
    
    def __init__(self):
        self.config_sources = [
            ConfigSource.ENVIRONMENT,
            ConfigSource.CONFIG_FILE,
            ConfigSource.INTERACTIVE
        ]
        self._cached_status = None
        self._cache_timestamp = None
        self._cache_ttl = 300  # 5分钟缓存
    
    def check_glm_config(self) -> ConfigStatus:
        """检查GLM配置状态"""
        # 检查缓存
        if self._is_cache_valid():
            return self._cached_status
        
        status = ConfigStatus(
            glm_key_present=False,
            glm_key_valid=False,
            config_source=ConfigSource.NONE
        )
        
        # 检查环境变量
        env_key = os.getenv('GLM_API_KEY')
        if env_key and env_key != 'your_api_key_here':
            status.glm_key_present = True
            status.config_source = ConfigSource.ENVIRONMENT
            # TODO: 实际验证API密钥
            status.glm_key_valid = len(env_key) > 10  # 简单验证
            status.key_info = KeyInfo(
                masked_key=self._mask_key(env_key),
                is_valid=status.glm_key_valid
            )
        
        # 检查配置文件
        if not status.glm_key_present:
            config_file_key = self._check_config_file()
            if config_file_key:
                status.glm_key_present = True
                status.config_source = ConfigSource.CONFIG_FILE
                status.glm_key_valid = len(config_file_key) > 10
                status.key_info = KeyInfo(
                    masked_key=self._mask_key(config_file_key),
                    is_valid=status.glm_key_valid
                )
        
        # 缓存结果
        self._cached_status = status
        self._cache_timestamp = time.time()
        
        return status
    
    def _is_cache_valid(self) -> bool:
        """检查缓存是否有效"""
        if not self._cached_status or not self._cache_timestamp:
            return False
        return (time.time() - self._cache_timestamp) < self._cache_ttl
    
    def _mask_key(self, key: str) -> str:
        """遮蔽API密钥"""
        if len(key) <= 8:
            return "*" * len(key)
        return key[:4] + "*" * (len(key) - 8) + key[-4:]
    
    def _check_config_file(self) -> Optional[str]:
        """检查配置文件中的API密钥"""
        config_files = [
            'glm_config.py',
            'config/glm_config.py',
            '.env'
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 简单的密钥提取逻辑
                        if 'GLM_API_KEY' in content:
                            # TODO: 实现更复杂的配置文件解析
                            pass
                except Exception:
                    continue
        return None

# ============================================================================
# 系统健康检查器
# ============================================================================

class SystemHealthChecker:
    """系统健康检查器"""
    
    def __init__(self):
        self.required_packages = {
            'requests': '>=2.31.0',
            'beautifulsoup4': '>=4.12.0',
            'feedparser': '>=6.0.10',
            'zhipuai': '>=2.0.0',
            'lxml': '>=4.9.0'
        }
        self.optional_packages = {
            'crawl4ai': '>=0.2.0',
            'python-dateutil': '>=2.8.0'
        }
    
    def run_quick_check(self) -> HealthReport:
        """运行快速健康检查"""
        issues = []
        
        # 检查Python版本
        python_version = sys.version_info
        if python_version < (3, 8):
            issues.append(Issue(
                severity=HealthStatus.ERROR,
                category=IssueCategory.DEPENDENCY,
                message=f"Python版本过低: {python_version.major}.{python_version.minor}",
                suggested_action="请升级到Python 3.8或更高版本"
            ))
        
        # 检查必需依赖
        dependency_status = {}
        for package, version in self.required_packages.items():
            status = self._check_package(package, version, required=True)
            dependency_status[package] = status
            if not status.installed:
                issues.append(Issue(
                    severity=HealthStatus.ERROR,
                    category=IssueCategory.DEPENDENCY,
                    message=f"缺少必需包: {package}",
                    suggested_action=f"运行: {status.install_command}"
                ))
        
        # 基础网络检查
        network_status = NetworkStatus(
            internet_connected=self._check_internet(),
            api_endpoints={},
            issues=[]
        )
        
        # 基础文件系统检查
        filesystem_status = FileSystemStatus(
            required_directories={'scripts': os.path.exists('scripts')},
            permissions={},
            disk_space_mb=self._get_disk_space(),
            issues=[]
        )
        
        # 确定整体状态
        overall_status = HealthStatus.HEALTHY
        if any(issue.severity == HealthStatus.CRITICAL for issue in issues):
            overall_status = HealthStatus.CRITICAL
        elif any(issue.severity == HealthStatus.ERROR for issue in issues):
            overall_status = HealthStatus.ERROR
        elif any(issue.severity == HealthStatus.WARNING for issue in issues):
            overall_status = HealthStatus.WARNING
        
        return HealthReport(
            overall_status=overall_status,
            dependency_status=dependency_status,
            network_status=network_status,
            filesystem_status=filesystem_status,
            issues=issues,
            timestamp=datetime.now()
        )
    
    def _check_package(self, package_name: str, version_req: str, required: bool) -> PackageStatus:
        """检查单个包的状态"""
        try:
            __import__(package_name)
            return PackageStatus(
                name=package_name,
                required=required,
                installed=True,
                install_command=f"pip install {package_name}{version_req}"
            )
        except ImportError:
            return PackageStatus(
                name=package_name,
                required=required,
                installed=False,
                install_command=f"pip install {package_name}{version_req}"
            )
    
    def _check_internet(self) -> bool:
        """检查网络连接"""
        try:
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False
    
    def _get_disk_space(self) -> float:
        """获取磁盘空间（MB）"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(".")
            return free / (1024 * 1024)  # 转换为MB
        except Exception:
            return 0.0

# ============================================================================
# 进度跟踪器
# ============================================================================

class ProgressTracker:
    """进度跟踪器"""
    
    def __init__(self):
        self.operations = []
        self.current_operation = None
        self.start_time = None
    
    def start_operation(self, name: str, estimated_time: int = 0):
        """开始一个操作"""
        self.current_operation = {
            'name': name,
            'start_time': time.time(),
            'estimated_time': estimated_time
        }
        print(f"🔄 {name}...")
    
    def update_progress(self, percentage: float, message: str = ""):
        """更新进度"""
        if self.current_operation:
            bar_length = 30
            filled_length = int(bar_length * percentage / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            print(f"\r   [{bar}] {percentage:.1f}% {message}", end="", flush=True)
    
    def complete_operation(self, success: bool = True, message: str = ""):
        """完成操作"""
        if self.current_operation:
            duration = time.time() - self.current_operation['start_time']
            status = "✅" if success else "❌"
            operation_name = self.current_operation['name']
            
            metrics = OperationMetrics(
                name=operation_name,
                duration=duration,
                success=success,
                details={'message': message},
                timestamp=datetime.now()
            )
            self.operations.append(metrics)
            
            print(f"\r{status} {operation_name} ({duration:.1f}s) {message}")
            self.current_operation = None

# ============================================================================
# 主启动类
# ============================================================================

class EnhancedStarter:
    """增强版启动器"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.health_checker = SystemHealthChecker()
        self.progress_tracker = ProgressTracker()
        self.project_root = Path(__file__).parent
    
    def run(self):
        """运行启动流程"""
        print("🌊 海之安网络安全新闻系统 (增强版)")
        print("=" * 60)
        
        # 确保在项目根目录
        os.chdir(self.project_root)
        
        # 1. 系统健康检查
        self.progress_tracker.start_operation("系统健康检查")
        health_report = self.health_checker.run_quick_check()
        self.progress_tracker.complete_operation(
            success=health_report.overall_status != HealthStatus.CRITICAL,
            message=f"状态: {health_report.overall_status.value}"
        )
        
        # 如果有严重问题，显示并退出
        if health_report.overall_status == HealthStatus.CRITICAL:
            self._show_critical_issues(health_report.issues)
            return False
        
        # 2. GLM配置检查
        self.progress_tracker.start_operation("GLM API配置检查")
        config_status = self.config_manager.check_glm_config()
        self.progress_tracker.complete_operation(
            success=config_status.glm_key_present,
            message="AI增强模式" if config_status.glm_key_valid else "基础模式"
        )
        
        # 显示配置状态
        self._show_config_status(config_status)
        
        # 3. 运行新闻生成
        return self._run_news_generation()
    
    def _show_critical_issues(self, issues: List[Issue]):
        """显示严重问题"""
        print("\n❌ 发现严重问题，无法继续:")
        for issue in issues:
            if issue.severity == HealthStatus.CRITICAL:
                print(f"   • {issue.message}")
                if issue.suggested_action:
                    print(f"     💡 建议: {issue.suggested_action}")
    
    def _show_config_status(self, status: ConfigStatus):
        """显示配置状态"""
        if status.glm_key_valid:
            print(f"🤖 检测到GLM API密钥，使用AI增强版生成器...")
            if status.key_info:
                print(f"   密钥: {status.key_info.masked_key}")
                print(f"   来源: {status.config_source.value}")
        else:
            print("📰 未检测到GLM API密钥，使用基础版生成器...")
            print("💡 提示：设置GLM_API_KEY环境变量或配置glm_config.py可启用AI增强功能")
            print("🔗 获取API密钥：https://open.bigmodel.cn/")
    
    def _run_news_generation(self) -> bool:
        """运行新闻生成"""
        self.progress_tracker.start_operation("新闻生成")
        
        try:
            result = subprocess.run([
                sys.executable, 'scripts/run_glm_news.py'
            ], check=True, capture_output=True, text=True)
            
            self.progress_tracker.complete_operation(
                success=True,
                message="生成完成"
            )
            
            print("🎉 新闻生成完成！")
            print("📱 请打开 index.html 查看结果")
            return True
            
        except subprocess.CalledProcessError as e:
            self.progress_tracker.complete_operation(
                success=False,
                message=f"失败: {e.returncode}"
            )
            print(f"❌ 运行失败: {e}")
            print("💡 请检查配置和网络连接")
            return False
        except KeyboardInterrupt:
            self.progress_tracker.complete_operation(
                success=False,
                message="用户取消"
            )
            print("\n👋 用户取消操作")
            return False
        except Exception as e:
            self.progress_tracker.complete_operation(
                success=False,
                message=f"错误: {str(e)}"
            )
            print(f"❌ 未知错误: {e}")
            return False

# ============================================================================
# 主函数
# ============================================================================

def main():
    """主函数"""
    starter = EnhancedStarter()
    success = starter.run()
    
    # 显示性能摘要
    if starter.progress_tracker.operations:
        total_time = sum(op.duration for op in starter.progress_tracker.operations)
        print(f"\n⏰ 总耗时: {total_time:.1f}秒")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())