# 海之安网络安全新闻系统

基于智谱GLM AI的网络安全新闻自动抓取和生成系统，参考[智谱GLM最佳实践](https://docs.bigmodel.cn/cn/best-practice/creativepractice/aimorningnewspaper)构建。

## 🌟 功能特性

### 📰 新闻抓取
- **多源抓取**: 支持安全客、FreeBuf、嘶吼等主流安全媒体RSS源
- **智能过滤**: 基于关键词自动筛选网络安全相关新闻
- **去重处理**: 自动去除重复新闻，确保内容质量

### 🤖 AI增强功能
- **智能摘要**: 使用智谱GLM生成专业的每日安全态势摘要
- **自动分类**: AI自动将新闻分类为焦点事件、漏洞威胁、产业动态
- **深度分析**: 为每条新闻生成专业的安全分析和影响评估

### 📊 可视化展示
- **响应式设计**: 适配桌面和移动设备
- **现代化界面**: 渐变背景、卡片设计、动画效果
- **智能索引**: 自动生成新闻索引页面，按时间分类展示

## 🚀 快速开始

### 环境要求
```bash
Python 3.7+
pip install requests feedparser beautifulsoup4 watchdog
```

### 基础使用
```bash
# 1. 运行新闻抓取器（基础版）
python3 news_scraper.py

# 2. 生成新闻索引
python3 start_monitor.py

# 3. 一键运行（推荐）
python3 run_glm_news.py
```

### AI增强版使用

1. **获取智谱GLM API密钥**
   - 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
   - 注册账号并获取API密钥

2. **配置API密钥**
   ```bash
   # 方法1: 环境变量
   export GLM_API_KEY="your_api_key_here"
   
   # 方法2: 配置文件
   # 编辑 glm_config.py，填入API密钥
   ```

3. **运行AI增强版**
   ```bash
   python3 run_glm_news.py
   ```

## 📁 项目结构

```
securitydaily/
├── news_scraper.py          # 基础新闻抓取器
├── glm_news_generator.py    # GLM AI增强版生成器
├── start_monitor.py         # 索引生成器
├── news_monitor.py          # 实时监控器
├── run_glm_news.py         # 一键运行脚本
├── scraper_config.py       # 抓取器配置
├── glm_config.py           # GLM配置
├── index.html              # 新闻索引页面
├── news*.html              # 生成的新闻文件
└── README.md               # 说明文档
```

## 🔧 配置说明

### 新闻源配置
编辑 `scraper_config.py` 或 `glm_config.py` 中的 `NEWS_SOURCES`：

```python
NEWS_SOURCES = [
    {
        'name': '安全客',
        'rss_url': 'https://api.anquanke.com/data/v1/rss',
        'enabled': True,
        'weight': 1.0
    },
    # 添加更多新闻源...
]
```

### 关键词过滤
修改 `SECURITY_KEYWORDS` 列表来调整新闻筛选条件：

```python
SECURITY_KEYWORDS = [
    '安全', '漏洞', '攻击', '黑客', 
    'security', 'vulnerability', 'CVE',
    # 添加更多关键词...
]
```

## 📊 生成的文件

### 新闻文件
- **命名格式**: `news20250729.html`
- **内容包含**: 
  - 专业的安全态势摘要
  - 分类新闻（焦点事件、漏洞威胁、产业动态）
  - AI生成的专业分析

### 索引页面
- **文件名**: `index.html`
- **功能**:
  - 最新新闻展示
  - 按时间分类的历史新闻
  - 响应式设计
  - 企业品牌信息

## 🤖 AI功能详解

### 智能摘要生成
使用GLM-4模型分析当日新闻标题，生成：
- 安全态势总体特点
- 重点威胁和趋势
- 专业权威的表述

### 自动新闻分类
AI自动将新闻分为三大类：
- **🎯 焦点安全事件**: 重大攻击、数据泄露等
- **⚠️ 漏洞与威胁**: CVE漏洞、威胁分析等  
- **🚀 产业动态**: 产品发布、政策法规等

### 深度分析
为每条新闻生成50字专业分析，包括：
- 威胁等级评估
- 影响范围分析
- 技术要点总结

## 🔄 自动化运行

### 定时任务设置
```bash
# 添加到crontab，每天早上8点自动生成新闻
0 8 * * * cd /path/to/securitydaily && python3 run_glm_news.py
```

### 实时监控
```bash
# 启动实时文件监控
python3 news_monitor.py
```

## 🎨 界面特性

- **现代化设计**: 深色主题，渐变背景
- **品牌标识**: 海之安logo和企业信息
- **响应式布局**: 适配各种设备
- **交互动画**: 悬停效果和过渡动画
- **智能分类**: 按时间自动组织新闻

## 📈 系统优势

1. **高效自动化**: 全自动抓取、分析、生成
2. **AI增强**: 智谱GLM提供专业分析
3. **多源整合**: 整合多个权威安全媒体
4. **专业输出**: 生成企业级新闻快报
5. **易于部署**: 简单配置即可运行

## 🔗 相关链接

- [智谱AI开放平台](https://open.bigmodel.cn/)
- [GLM最佳实践文档](https://docs.bigmodel.cn/cn/best-practice/creativepractice/aimorningnewspaper)
- [海之安官网](https://www.oceansecurity.cn)

## 📝 更新日志

### v2.0.0 (2025-07-29)
- ✨ 集成智谱GLM AI功能
- 🎨 全新界面设计
- 📊 智能新闻分类
- 🤖 AI生成专业分析

### v1.0.0 (2025-07-22)
- 🚀 基础新闻抓取功能
- 📰 HTML新闻生成
- 📋 自动索引生成
- 🔄 实时监控功能

## 📄 许可证

© 2025 海之安（中国）科技有限公司. 保持警惕，守护安全.

---

**海之安，数字安全专家** | [www.oceansecurity.cn](https://www.oceansecurity.cn)