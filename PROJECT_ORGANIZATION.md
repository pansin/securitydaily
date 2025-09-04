# 📁 项目目录整理完成

## 🏗️ 新的目录结构

```
oceansecurity-news/
├── src/                    # 源代码
│   ├── core/              # 核心业务逻辑
│   │   ├── glm_news_generator.py
│   │   ├── news_sources_loader.py
│   │   └── generate_index.py
│   ├── crawlers/          # 爬虫和数据抓取
│   │   ├── enhanced_crawler.py
│   │   └── news_scraper.py
│   ├── generators/        # 内容生成器
│   │   ├── mobile_protection_report.py
│   │   └── mobile_style_monitor.py
│   └── utils/             # 工具和辅助函数
│       ├── style_protection.py
│       └── config_protection.py
├── config/                # 配置文件
│   ├── glm_config.py
│   ├── scraper_config.py
│   └── news_sources_config.json
├── tests/                 # 测试文件
│   ├── test_mobile_protection.py
│   ├── test_news_sources.py
│   └── mobile_test_index.html
├── docs/                  # 文档
│   ├── ENHANCED_NEWS_SYSTEM.md
│   ├── INDEX_ENHANCEMENT_REPORT.md
│   ├── INTERNATIONAL_SOURCES_REPORT.md
│   ├── NEWS_SOURCES_README.md
│   └── MOBILE_PROTECTION_README.md
├── assets/                # 静态资源
│   ├── css/              # CSS样式文件
│   │   └── mobile_responsive.css
│   ├── js/               # JavaScript文件
│   │   └── index_enhanced.js
│   └── images/           # 图片资源
├── output/                # 输出文件
│   ├── news/             # 生成的新闻文件
│   │   ├── news20250713.html
│   │   ├── news20250715.html
│   │   └── ... (其他新闻文件)
│   └── backups/          # 备份文件
│       └── *.backup
├── scripts/               # 运行脚本
│   ├── run_glm_news.py
│   ├── run_scraper.py
│   └── start_monitor.py
├── tools/                 # 开发工具
│   ├── manage_news_sources.py
│   └── news_monitor.py
├── requirements.txt       # 依赖列表
├── setup.py              # 安装配置
├── .gitignore            # Git忽略文件
├── index.html            # 主页文件
└── README.md             # 项目说明
```

## 🎯 整理效果

- ✅ **代码按功能模块分类**: 核心逻辑、爬虫、生成器、工具分离
- ✅ **配置文件统一管理**: 所有配置集中在config目录
- ✅ **测试文件独立目录**: 测试代码与业务代码分离
- ✅ **文档集中存放**: 所有文档统一管理
- ✅ **静态资源分类管理**: CSS、JS、图片分类存放
- ✅ **输出文件独立存储**: 新闻文件和备份文件分离
- ✅ **工具脚本分离**: 运行脚本和开发工具分开
- ✅ **符合Python项目标准**: 包含setup.py、requirements.txt等

## 🚀 使用方法

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行新闻生成
```bash
python scripts/run_glm_news.py
```

### 管理新闻源
```bash
python tools/manage_news_sources.py
```

### 运行测试
```bash
python -m pytest tests/
```

### 开发安装
```bash
pip install -e .
```

## 📦 模块说明

### src/core/ - 核心业务逻辑
- `glm_news_generator.py` - GLM新闻生成器主类
- `news_sources_loader.py` - 新闻源配置加载器
- `generate_index.py` - 动态主页生成器

### src/crawlers/ - 爬虫和数据抓取
- `enhanced_crawler.py` - 增强型网页爬虫
- `news_scraper.py` - 基础新闻抓取器

### src/generators/ - 内容生成器
- `mobile_protection_report.py` - 移动端保护报告生成器
- `mobile_style_monitor.py` - 移动端样式监控器

### src/utils/ - 工具和辅助函数
- `style_protection.py` - 样式保护工具
- `config_protection.py` - 配置保护工具

### config/ - 配置文件
- `glm_config.py` - GLM API配置
- `scraper_config.py` - 爬虫配置
- `news_sources_config.json` - 新闻源配置（30个国际权威源）

### scripts/ - 运行脚本
- `run_glm_news.py` - 主运行脚本
- `run_scraper.py` - 爬虫运行脚本
- `start_monitor.py` - 监控启动脚本

### tools/ - 开发工具
- `manage_news_sources.py` - 新闻源管理工具
- `news_monitor.py` - 新闻监控工具

## 📝 注意事项

1. **导入路径更新**: 所有导入路径已更新为新的目录结构
2. **配置文件位置**: 配置文件已移至config目录
3. **静态资源路径**: CSS和JS文件已移至assets目录
4. **输出文件管理**: 新闻文件和备份文件分别存储
5. **备份保护**: 原文件已备份至.organization_backup/目录

## 🔧 开发指南

### 添加新功能
1. 在对应的src子目录中添加模块
2. 在tests目录中添加测试文件
3. 更新requirements.txt（如有新依赖）
4. 更新文档

### 配置管理
1. 所有配置文件统一放在config目录
2. 使用相对导入引用配置
3. 敏感配置使用环境变量

### 测试规范
1. 测试文件以test_开头
2. 使用pytest框架
3. 保持测试覆盖率

## 🎉 整理成果

通过本次目录整理，海之安新闻系统已经从**单文件混合项目**升级为**标准化的Python包项目**：

- 📁 **清晰的目录结构** - 按功能模块组织代码
- 🔧 **标准化配置** - 符合Python项目规范
- 📦 **包管理** - 支持pip安装和分发
- 🧪 **测试框架** - 完整的测试体系
- 📚 **文档体系** - 完善的文档管理
- 🚀 **部署就绪** - 可直接用于生产环境

现在项目具备了企业级软件的标准结构，便于维护、扩展和部署！

---
*整理完成时间: 2025-07-30 10:45*