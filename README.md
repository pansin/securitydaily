# 🌊 海之安网络安全新闻系统

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Production-brightgreen.svg)]()

> 全球网络安全资讯聚合平台 | AI驱动的智能新闻生成系统

## 🎯 项目简介

海之安网络安全新闻系统是一个基于AI技术的全球网络安全资讯聚合平台，集成了30个国际权威安全信息源，提供实时的威胁情报分析和安全态势感知。

### ✨ 核心特性

- 🌍 **全球覆盖**: 30个国际权威数据源，覆盖15个国家
- 🤖 **AI驱动**: 基于智谱GLM的智能内容生成和分析
- 📱 **响应式设计**: 完美适配桌面、平板、手机等所有设备
- 🔄 **实时更新**: 自动抓取、分析、生成最新安全资讯
- 🛡️ **威胁情报**: 四维度分析（风险、事件、舆情、趋势）
- 🎨 **现代化UI**: 科技感十足的深色主题设计

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 智谱GLM API密钥（可选，用于AI增强功能）

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/oceansecurity/news-system.git
cd news-system
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置API密钥**（可选）
```bash
export GLM_API_KEY="your_api_key_here"
```

4. **运行系统**
```bash
python scripts/run_glm_news.py
```

5. **查看结果**
```bash
# 打开浏览器访问生成的index.html
open index.html
```

## 📁 项目结构

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
├── output/                # 输出文件
├── scripts/               # 运行脚本
└── tools/                 # 开发工具
```

## 🌍 数据源覆盖

### 官方权威源 (5个)
- **CISA** - 美国网络安全和基础设施安全局
- **US-CERT** - 美国计算机应急响应小组
- **NIST** - 美国国家标准与技术研究院
- **NCSC UK** - 英国国家网络安全中心
- **ACSC Australia** - 澳大利亚网络安全中心

### 权威媒体源 (16个)
- **Krebs on Security** - Brian Krebs权威安全博客
- **Schneier on Security** - Bruce Schneier安全专家博客
- **The Hacker News** - 全球知名安全新闻平台
- **Dark Reading** - 企业安全专业媒体
- 等等...

### 厂商安全源 (6个)
- Microsoft Security Blog
- Google Security Blog
- FireEye Threat Research
- Kaspersky Securelist
- 等等...

### 国内优质源 (3个)
- 安全客、FreeBuf、嘶吼

## 🛠️ 使用指南

### 基础使用

```bash
# 生成今日新闻
python scripts/run_glm_news.py

# 管理新闻源
python tools/manage_news_sources.py list

# 测试数据源
python tests/test_news_sources.py
```

### 高级功能

```bash
# 添加新数据源
python tools/manage_news_sources.py add

# 移动端测试
open tests/mobile_test_index.html

# 样式保护检查
python src/utils/style_protection.py
```

## 📊 功能特性

### AI智能分析
- 🧠 智谱GLM驱动的内容生成
- 📈 四维度威胁分析（风险、事件、舆情、趋势）
- 🎯 智能新闻精选和分类
- 📝 自动摘要生成

### 响应式设计
- 📱 完美移动端适配
- 🎨 现代化科技美感
- ⚡ 流畅的交互动画
- 🌙 深色主题设计

### 数据管理
- 🔄 自动数据源管理
- 🛡️ 配置保护机制
- 💾 自动备份功能
- 📊 实时统计监控

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/

# 移动端适配测试
open tests/mobile_test_index.html

# 数据源连通性测试
python tests/test_news_sources.py all
```

## 📚 文档

- [系统架构文档](docs/ENHANCED_NEWS_SYSTEM.md)
- [移动端适配指南](docs/MOBILE_PROTECTION_README.md)
- [数据源管理手册](docs/NEWS_SOURCES_README.md)
- [国际化部署报告](docs/INTERNATIONAL_SOURCES_REPORT.md)

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🏢 关于我们

**海之安（中国）科技有限公司**

- 🌐 官网: [www.oceansecurity.cn](https://www.oceansecurity.cn)
- 📧 邮箱: contact@oceansecurity.cn
- 🔒 专注: 数字安全解决方案

## 🙏 致谢

感谢以下开源项目和服务：

- [智谱GLM](https://open.bigmodel.cn/) - AI内容生成
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML解析
- [Requests](https://requests.readthedocs.io/) - HTTP库
- [Feedparser](https://feedparser.readthedocs.io/) - RSS解析

---

<div align="center">

**🌊 守护数字安全，共建网络未来 🛡️**

Made with ❤️ by Ocean Security Team

</div>