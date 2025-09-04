#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目文件整理脚本
按照发布标准整理目录结构
"""

import os
import shutil
import glob
from pathlib import Path

class ProjectOrganizer:
    def __init__(self):
        """初始化项目整理器"""
        self.root_dir = Path('.')
        self.backup_dir = Path('.organization_backup')
        
        # 定义目录结构
        self.structure = {
            'src': {
                'core': '核心业务逻辑',
                'crawlers': '爬虫和数据抓取',
                'generators': '内容生成器',
                'utils': '工具和辅助函数'
            },
            'config': '配置文件',
            'tests': '测试文件',
            'docs': '文档',
            'assets': {
                'css': 'CSS样式文件',
                'js': 'JavaScript文件',
                'images': '图片资源'
            },
            'output': {
                'news': '生成的新闻文件',
                'backups': '备份文件'
            },
            'scripts': '运行脚本',
            'tools': '开发工具'
        }
        
        # 文件分类规则
        self.file_rules = {
            # 核心业务逻辑
            'src/core': [
                'glm_news_generator.py',
                'news_sources_loader.py',
                'generate_index.py'
            ],
            
            # 爬虫和数据抓取
            'src/crawlers': [
                'enhanced_crawler.py',
                'news_scraper.py'
            ],
            
            # 内容生成器
            'src/generators': [
                'mobile_protection_report.py',
                'mobile_style_monitor.py'
            ],
            
            # 工具和辅助函数
            'src/utils': [
                'style_protection.py',
                'config_protection.py'
            ],
            
            # 配置文件
            'config': [
                'glm_config.py',
                'scraper_config.py',
                'news_sources_config.json'
            ],
            
            # 测试文件
            'tests': [
                'test_mobile_protection.py',
                'test_news_sources.py',
                'mobile_test_index.html'
            ],
            
            # 文档
            'docs': [
                '*.md',
                '!README.md'  # 排除根目录的README
            ],
            
            # CSS样式文件
            'assets/css': [
                'mobile_responsive.css'
            ],
            
            # JavaScript文件
            'assets/js': [
                'index_enhanced.js'
            ],
            
            # 新闻文件
            'output/news': [
                'news*.html',
                '!index*.html'  # 排除index文件
            ],
            
            # 备份文件
            'output/backups': [
                '*.backup',
                '.config_backups/*'
            ],
            
            # 运行脚本
            'scripts': [
                'run_glm_news.py',
                'run_scraper.py',
                'start_monitor.py'
            ],
            
            # 开发工具
            'tools': [
                'manage_news_sources.py',
                'news_monitor.py'
            ]
        }
    
    def create_directories(self):
        """创建目录结构"""
        def create_dir_recursive(structure, parent_path=''):
            for name, desc in structure.items():
                if isinstance(desc, dict):
                    # 递归创建子目录
                    dir_path = Path(parent_path) / name
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"📁 创建目录: {dir_path}")
                    create_dir_recursive(desc, dir_path)
                else:
                    # 创建叶子目录
                    dir_path = Path(parent_path) / name
                    dir_path.mkdir(parents=True, exist_ok=True)
                    print(f"📁 创建目录: {dir_path} - {desc}")
        
        print("🏗️  创建项目目录结构...")
        create_dir_recursive(self.structure)
    
    def backup_current_state(self):
        """备份当前状态"""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        self.backup_dir.mkdir()
        print(f"💾 创建备份目录: {self.backup_dir}")
        
        # 备份重要文件
        important_files = [
            'index.html',
            'README.md',
            'glm_news_generator.py',
            'news_sources_config.json'
        ]
        
        for file in important_files:
            if Path(file).exists():
                shutil.copy2(file, self.backup_dir / file)
                print(f"💾 备份文件: {file}")
    
    def move_files(self):
        """移动文件到对应目录"""
        print("📦 开始整理文件...")
        
        for target_dir, patterns in self.file_rules.items():
            target_path = Path(target_dir)
            
            for pattern in patterns:
                if pattern.startswith('!'):
                    # 排除规则，跳过
                    continue
                
                # 处理通配符
                if '*' in pattern:
                    files = glob.glob(pattern)
                else:
                    files = [pattern] if Path(pattern).exists() else []
                
                for file_path in files:
                    source = Path(file_path)
                    if source.exists() and source.is_file():
                        destination = target_path / source.name
                        
                        # 确保目标目录存在
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        
                        try:
                            shutil.move(str(source), str(destination))
                            print(f"📦 移动文件: {source} → {destination}")
                        except Exception as e:
                            print(f"❌ 移动失败: {source} - {e}")
    
    def create_init_files(self):
        """创建__init__.py文件"""
        python_dirs = [
            'src',
            'src/core',
            'src/crawlers', 
            'src/generators',
            'src/utils'
        ]
        
        for dir_path in python_dirs:
            init_file = Path(dir_path) / '__init__.py'
            if not init_file.exists():
                init_file.write_text('# -*- coding: utf-8 -*-\n')
                print(f"📄 创建: {init_file}")
    
    def create_project_files(self):
        """创建项目标准文件"""
        
        # 创建requirements.txt
        requirements_content = """# 海之安网络安全新闻系统依赖
requests>=2.31.0
beautifulsoup4>=4.12.0
feedparser>=6.0.10
zhipuai>=2.0.0
crawl4ai>=0.2.0
lxml>=4.9.0
python-dateutil>=2.8.0
"""
        
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        print("📄 创建: requirements.txt")
        
        # 创建.gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Config
.env
*.key

# Backups
*.backup
.organization_backup/
.config_backups/

# Output
output/news/*.html
!output/news/.gitkeep

# Cache
.cache/
.pytest_cache/
"""
        
        with open('.gitignore', 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        print("📄 创建: .gitignore")
        
        # 创建setup.py
        setup_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oceansecurity-news",
    version="1.0.0",
    author="海之安（中国）科技有限公司",
    author_email="contact@oceansecurity.cn",
    description="海之安网络安全新闻系统 - 全球安全资讯聚合平台",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oceansecurity/news-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "feedparser>=6.0.10",
        "zhipuai>=2.0.0",
        "crawl4ai>=0.2.0",
        "lxml>=4.9.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "oceansec-news=scripts.run_glm_news:main",
        ],
    },
)
'''
        
        with open('setup.py', 'w', encoding='utf-8') as f:
            f.write(setup_content)
        print("📄 创建: setup.py")
    
    def create_readme_files(self):
        """创建各目录的README文件"""
        readme_contents = {
            'src/README.md': """# 源代码目录

## 目录结构

- `core/` - 核心业务逻辑
- `crawlers/` - 爬虫和数据抓取
- `generators/` - 内容生成器  
- `utils/` - 工具和辅助函数
""",
            
            'config/README.md': """# 配置文件目录

## 文件说明

- `glm_config.py` - GLM API配置
- `scraper_config.py` - 爬虫配置
- `news_sources_config.json` - 新闻源配置
""",
            
            'tests/README.md': """# 测试文件目录

## 测试说明

- `test_mobile_protection.py` - 移动端保护测试
- `test_news_sources.py` - 新闻源测试
- `mobile_test_index.html` - 移动端页面测试
""",
            
            'docs/README.md': """# 文档目录

## 文档列表

- 系统设计文档
- API文档
- 部署指南
- 用户手册
""",
            
            'assets/README.md': """# 静态资源目录

## 目录结构

- `css/` - CSS样式文件
- `js/` - JavaScript文件
- `images/` - 图片资源
""",
            
            'output/README.md': """# 输出文件目录

## 目录结构

- `news/` - 生成的新闻文件
- `backups/` - 备份文件
""",
            
            'scripts/README.md': """# 运行脚本目录

## 脚本说明

- `run_glm_news.py` - 主运行脚本
- `run_scraper.py` - 爬虫运行脚本
- `start_monitor.py` - 监控启动脚本
""",
            
            'tools/README.md': """# 开发工具目录

## 工具说明

- `manage_news_sources.py` - 新闻源管理工具
- `news_monitor.py` - 新闻监控工具
"""
        }
        
        for file_path, content in readme_contents.items():
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            print(f"📄 创建: {file_path}")
    
    def create_gitkeep_files(self):
        """为空目录创建.gitkeep文件"""
        empty_dirs = [
            'assets/images',
            'output/news',
            'output/backups'
        ]
        
        for dir_path in empty_dirs:
            gitkeep_file = Path(dir_path) / '.gitkeep'
            gitkeep_file.parent.mkdir(parents=True, exist_ok=True)
            gitkeep_file.write_text('')
            print(f"📄 创建: {gitkeep_file}")
    
    def update_import_paths(self):
        """更新文件中的导入路径"""
        print("🔧 更新导入路径...")
        
        # 需要更新的文件和对应的导入映射
        import_updates = {
            'scripts/run_glm_news.py': {
                'from glm_news_generator import': 'from src.core.glm_news_generator import',
                'from glm_config import': 'from config.glm_config import'
            }
        }
        
        for file_path, updates in import_updates.items():
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for old_import, new_import in updates.items():
                        content = content.replace(old_import, new_import)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"🔧 更新导入路径: {file_path}")
                except Exception as e:
                    print(f"❌ 更新失败: {file_path} - {e}")
    
    def generate_project_summary(self):
        """生成项目整理总结"""
        summary = """# 📁 项目目录整理完成

## 🏗️ 新的目录结构

```
oceansecurity-news/
├── src/                    # 源代码
│   ├── core/              # 核心业务逻辑
│   ├── crawlers/          # 爬虫和数据抓取
│   ├── generators/        # 内容生成器
│   └── utils/             # 工具和辅助函数
├── config/                # 配置文件
├── tests/                 # 测试文件
├── docs/                  # 文档
├── assets/                # 静态资源
│   ├── css/              # CSS样式文件
│   ├── js/               # JavaScript文件
│   └── images/           # 图片资源
├── output/                # 输出文件
│   ├── news/             # 生成的新闻文件
│   └── backups/          # 备份文件
├── scripts/               # 运行脚本
├── tools/                 # 开发工具
├── requirements.txt       # 依赖列表
├── setup.py              # 安装配置
├── .gitignore            # Git忽略文件
└── README.md             # 项目说明
```

## 🎯 整理效果

- ✅ 代码按功能模块分类
- ✅ 配置文件统一管理
- ✅ 测试文件独立目录
- ✅ 文档集中存放
- ✅ 静态资源分类管理
- ✅ 输出文件独立存储
- ✅ 工具脚本分离
- ✅ 符合Python项目标准

## 🚀 使用方法

```bash
# 安装依赖
pip install -r requirements.txt

# 运行新闻生成
python scripts/run_glm_news.py

# 管理新闻源
python tools/manage_news_sources.py

# 运行测试
python -m pytest tests/
```

## 📝 注意事项

1. 导入路径已更新，使用相对导入
2. 配置文件移至config目录
3. 静态资源移至assets目录
4. 输出文件移至output目录
5. 备份文件已保存至.organization_backup/

---
*整理完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        from datetime import datetime
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        summary = summary.replace('{datetime.now().strftime(\'%Y-%m-%d %H:%M:%S\')}', current_time)
        
        with open('PROJECT_ORGANIZATION.md', 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print("📄 创建: PROJECT_ORGANIZATION.md")
    
    def organize(self):
        """执行完整的项目整理"""
        print("🚀 开始项目目录整理...")
        print("=" * 60)
        
        # 1. 备份当前状态
        self.backup_current_state()
        
        # 2. 创建目录结构
        self.create_directories()
        
        # 3. 移动文件
        self.move_files()
        
        # 4. 创建Python包文件
        self.create_init_files()
        
        # 5. 创建项目标准文件
        self.create_project_files()
        
        # 6. 创建README文件
        self.create_readme_files()
        
        # 7. 创建.gitkeep文件
        self.create_gitkeep_files()
        
        # 8. 更新导入路径
        self.update_import_paths()
        
        # 9. 生成整理总结
        self.generate_project_summary()
        
        print("=" * 60)
        print("🎉 项目目录整理完成！")
        print("📁 新的目录结构已创建")
        print("💾 原文件已备份至 .organization_backup/")
        print("📄 查看 PROJECT_ORGANIZATION.md 了解详细信息")

def main():
    """主函数"""
    organizer = ProjectOrganizer()
    
    # 确认操作
    print("📁 海之安新闻系统 - 项目目录整理工具")
    print("=" * 50)
    print("⚠️  此操作将重新组织项目文件结构")
    print("💾 原文件将备份至 .organization_backup/")
    print()
    
    confirm = input("是否继续？(y/N): ").strip().lower()
    if confirm in ['y', 'yes', '1']:
        organizer.organize()
    else:
        print("❌ 操作已取消")

if __name__ == "__main__":
    main()