# 📰 海之安新闻系统 - 数据源配置管理

## 🎯 概述

本系统将新闻数据源配置独立出来，支持国际权威网络安全信息源，并提供完善的配置管理和保护机制。

## 📁 文件结构

```
├── news_sources_config.json     # 主配置文件
├── news_sources_loader.py       # 配置加载器
├── manage_news_sources.py       # 配置管理脚本
├── test_news_sources.py         # 数据源测试脚本
├── config_protection.py         # 配置保护机制
└── .config_backups/             # 自动备份目录
```

## 🌍 数据源覆盖

### 官方权威源 (5个)
- **CISA Alerts** - 美国网络安全和基础设施安全局
- **US-CERT Alerts** - 美国计算机应急响应小组
- **NIST Cybersecurity** - 美国国家标准与技术研究院
- **NCSC UK** - 英国国家网络安全中心
- **ACSC Australia** - 澳大利亚网络安全中心

### 权威媒体源 (16个)
- **Krebs on Security** - Brian Krebs权威安全博客
- **Schneier on Security** - Bruce Schneier安全专家博客
- **The Hacker News** - 全球知名安全新闻平台
- **Dark Reading** - 企业安全专业媒体
- **SANS Internet Storm Center** - SANS威胁情报中心
- 等等...

### 厂商安全源 (6个)
- **Microsoft Security Blog** - 微软安全博客
- **Google Security Blog** - 谷歌安全博客
- **FireEye Threat Research** - FireEye威胁研究
- **Kaspersky Securelist** - 卡巴斯基安全研究
- **Trend Micro Security Intelligence** - 趋势科技情报
- **Apple Security Updates** - 苹果安全更新

### 国内安全源 (3个)
- **安全客** - 国内知名安全媒体
- **FreeBuf** - 国内领先安全门户
- **嘶吼** - 专业安全媒体平台

## 🚀 使用方法

### 1. 查看配置统计
```bash
python3 news_sources_loader.py stats
```

### 2. 列出新闻源
```bash
# 列出所有启用的源
python3 manage_news_sources.py list

# 按地区筛选
python3 manage_news_sources.py list region 美国

# 按语言筛选
python3 manage_news_sources.py list language en

# 按类别筛选
python3 manage_news_sources.py list category 官方警报
```

### 3. 测试数据源
```bash
# 快速测试
python3 test_news_sources.py quick

# 测试所有源
python3 test_news_sources.py all

# 测试官方源
python3 test_news_sources.py official

# 测试指定地区
python3 test_news_sources.py region 美国
```

### 4. 管理数据源
```bash
# 添加新数据源
python3 manage_news_sources.py add

# 启用数据源
python3 manage_news_sources.py enable "Krebs on Security"

# 禁用数据源
python3 manage_news_sources.py disable "某个源名称"

# 备份配置
python3 manage_news_sources.py backup
```

### 5. 配置保护
```bash
# 启用保护
python3 config_protection.py protect

# 检查变化
python3 config_protection.py check

# 创建备份
python3 config_protection.py backup

# 恢复配置
python3 config_protection.py restore
```

## ⚙️ 配置文件结构

```json
{
  "version": "1.0",
  "last_updated": "2025-07-30",
  "news_sources": [
    {
      "name": "数据源名称",
      "rss_url": "RSS链接",
      "weight": 1.2,
      "language": "en",
      "region": "美国",
      "category": "官方警报",
      "enabled": true,
      "description": "描述信息"
    }
  ]
}
```

### 字段说明
- **name**: 数据源名称（必需）
- **rss_url**: RSS订阅链接（必需）
- **weight**: 权重值 0.5-1.5，越高优先级越高（必需）
- **language**: 语言代码 zh/en（必需）
- **region**: 地区名称（必需）
- **category**: 类别名称（必需）
- **enabled**: 是否启用（必需）
- **description**: 描述信息（可选）

## 🛡️ 保护机制

### 自动备份
- 每次修改配置时自动创建备份
- 备份文件保存在 `.config_backups/` 目录
- 支持从备份恢复配置

### 完整性验证
- MD5校验和验证文件完整性
- JSON结构验证确保配置有效
- 必需字段检查防止配置错误

### 版本控制
- 配置文件包含版本信息
- 支持配置升级和迁移
- 变更历史追踪

## 📊 数据源分类

### 按优先级
- **最高优先级** (权重 ≥ 1.3): 官方警报源
- **高优先级** (权重 ≥ 1.1): 权威媒体和研究机构
- **中等优先级** (权重 = 1.0): 一般安全媒体
- **低优先级** (权重 < 1.0): 补充信息源

### 按类别
- **官方警报**: 政府机构发布的安全警报
- **威胁情报**: 专业威胁情报和分析
- **威胁研究**: 深度威胁研究报告
- **综合安全**: 综合性安全新闻
- **企业安全**: 企业级安全解决方案
- **技术分析**: 技术深度分析文章

### 按地区
- **中国**: 3个源 (安全客、FreeBuf、嘶吼)
- **美国**: 16个源 (包括CISA、NIST等官方源)
- **国际**: 3个源 (跨国安全媒体)
- **其他**: 欧盟、英国、澳大利亚等

## 🔧 集成到新闻生成器

新闻生成器会自动加载配置文件中的数据源：

```python
from glm_news_generator import GLMNewsGenerator

# 自动加载配置文件中的所有启用源
generator = GLMNewsGenerator(api_key)
print(f"加载了 {len(generator.news_sources)} 个数据源")
```

## 📈 性能优化

### 智能筛选
- 按权重优先抓取高质量源
- 按地区和语言智能分配
- 官方源优先处理

### 并发控制
- 合理的请求间隔避免被封
- 超时控制防止阻塞
- 错误重试机制

### 缓存机制
- RSS内容缓存减少重复请求
- 配置文件缓存提高加载速度
- 智能更新检测

## 🚨 故障排除

### 配置文件损坏
```bash
# 检查配置完整性
python3 config_protection.py check

# 从备份恢复
python3 config_protection.py restore
```

### 数据源无法访问
```bash
# 测试特定源
python3 test_news_sources.py quick

# 禁用问题源
python3 manage_news_sources.py disable "问题源名称"
```

### 权限问题
```bash
# 检查文件权限
ls -la news_sources_config.json

# 修复权限
chmod 644 news_sources_config.json
```

## 📝 添加新数据源

### 交互式添加
```bash
python3 manage_news_sources.py add
```

### 手动添加
1. 编辑 `news_sources_config.json`
2. 在 `news_sources` 数组中添加新配置
3. 运行测试验证: `python3 test_news_sources.py quick`
4. 启用保护: `python3 config_protection.py protect`

### 推荐新源
如果您发现优质的网络安全信息源，欢迎通过以下方式添加：
- 确保RSS链接有效
- 内容质量高且更新频繁
- 符合网络安全主题
- 权重设置合理

## 🎉 总结

通过独立的配置文件系统，海之安新闻系统现在支持：

✅ **30个国际权威数据源** - 覆盖全球主要安全信息  
✅ **智能分类管理** - 按地区、语言、类别组织  
✅ **完善的保护机制** - 防止配置被意外覆盖  
✅ **灵活的管理工具** - 轻松添加、测试、管理数据源  
✅ **自动集成** - 新闻生成器无缝使用新配置  

现在您可以获取到更全面、更权威的全球网络安全资讯！🌍🔒

---

*© 2025 海之安（中国）科技有限公司*