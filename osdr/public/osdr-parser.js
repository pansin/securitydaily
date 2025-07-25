// 从本地存储获取上次的期数
function getLastIssueNumber() {
  const lastIssue = localStorage.getItem('ocean-security-last-issue');
  return lastIssue ? parseInt(lastIssue, 10) : 0;
}

// 保存当前期数到本地存储
function saveIssueNumber(issue) {
  localStorage.setItem('ocean-security-last-issue', issue.toString());
}

// 提取日期 - 支持多种格式
function extractDate(content) {
  // 匹配标题中的日期格式：### **海之安每日网络安全快报 (YYYY年MM月DD日)**
  const titleDatePattern = /###\s*\*\*[^\(]*\((\d{4})年(\d{1,2})月(\d{1,2})日\)\*\*/;
  const titleMatch = titleDatePattern.exec(content);
  
  if (titleMatch) {
    const year = titleMatch[1];
    const month = titleMatch[2].padStart(2, '0');
    const day = titleMatch[3].padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
  
  // 备用日期格式匹配
  const datePatterns = [
    /(\d{4})年(\d{1,2})月(\d{1,2})日/g,
    /(\d{4})-(\d{1,2})-(\d{1,2})/g,
    /(\d{4})\/(\d{1,2})\/(\d{1,2})/g,
  ];
  
  for (const pattern of datePatterns) {
    const match = pattern.exec(content);
    if (match) {
      const year = match[1];
      const month = match[2].padStart(2, '0');
      const day = match[3].padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  }
  
  // 如果没有找到日期，返回今天的日期
  return new Date().toISOString().split('T')[0];
}

// 提取摘要 - 从 **今日摘要：** 到 --- 之间的内容
function extractSummary(content) {
  console.log('开始提取摘要...');
  
  // 匹配 **今日摘要：** 后面到 --- 或下一个 ### 之间的内容
  const summaryPattern = /\*\*今日摘要：\*\*([\s\S]*?)(?=---|###|$)/i;
  
  const match = summaryPattern.exec(content);
  
  if (match) {
    const summary = match[1].trim();
    console.log(`成功提取摘要，长度: ${summary.length}`);
    return summary;
  }
  
  // 尝试更宽松的模式
  const altSummaryPattern = /今日摘要[:：]([\s\S]*?)(?=---|###|一、|$)/i;
  const altMatch = altSummaryPattern.exec(content);
  
  if (altMatch) {
    const summary = altMatch[1].trim();
    console.log(`备用模式成功提取摘要，长度: ${summary.length}`);
    return summary;
  }
  
  console.log('未找到摘要内容');
  return '';
}

// 根据分类标题确定类别
function getCategoryByTitle(sectionTitle) {
  if (sectionTitle.includes('焦点安全事件')) {
    return 'focus';
  } else if (sectionTitle.includes('重大风险与预警')) {
    return 'risk';
  } else if (sectionTitle.includes('产业创新与政策')) {
    return 'innovation';
  }
  
  // 默认分类
  return 'focus';
}

// 解析新闻条目 - 精确按markdown结构解析
function parseNewsItems(content) {
  console.log('开始解析新闻条目...');
  const newsItems = [];
  
  // 首先按三级标题分割内容 - 修正正则表达式
  const sectionPattern = /###\s*\*\*[一二三]、\s*[^\*]+\*\*/g;
  const sectionMatches = content.match(sectionPattern);
  
  // 如果原始模式失败，尝试更宽松的模式
  if (!sectionMatches || sectionMatches.length === 0) {
    const alternativePattern = /###\s*\*\*[一二三].*?\*\*/g;
    const altMatches = content.match(alternativePattern);
    console.log('尝试备用分类标题模式:', alternativePattern);
    console.log('备用模式找到的分类标题:', altMatches);
  }
  
  if (!sectionMatches || sectionMatches.length === 0) {
    console.log('没有找到标准的三级标题，使用备用解析方法');
    return parseNewsItemsFallback(content);
  }
  
  // 按分类分割内容
  const sections = content.split(sectionPattern);
  console.log('分割后的版块数量:', sections.length);
  
  // 解析每个分类下的新闻
  for (let i = 1; i < sections.length; i++) {
    const sectionContent = sections[i];
    const sectionTitle = sectionMatches[i - 1] || '';
    const category = getCategoryByTitle(sectionTitle);
    
    console.log(`解析版块 ${i}: ${sectionTitle.substring(0, 50)}...`);
    
    // 在每个分类中查找新闻条目 - 优化正则表达式
    const newsPattern = /\*\*(\d+)\. 【[^】]*】([^\*]+)\*\*([\s\S]*?)(?=\*\*\d+\.|$)/g;
    
    let match;
    let matchCount = 0;
    
    // 重置正则表达式的lastIndex
    newsPattern.lastIndex = 0;
    
    while ((match = newsPattern.exec(sectionContent)) !== null) {
      matchCount++;
      const newsNumber = match[1];
      const title = match[2].trim();
      const contentBlock = match[3].trim();
      
      // 提取完整内容 - 查找"分析与影响"部分的内容
      let content = '';
      
      // 查找分析与影响部分，将其内容作为完整的新闻内容
      const analysisMatch = contentBlock.match(/\*\s*\*\*分析与影响：\*\*([\s\S]*)/i);
      if (analysisMatch) {
        content = analysisMatch[1].trim();
      } else {
        // 如果没有找到"分析与影响"标识，使用整个内容块
        content = contentBlock
          .replace(/^\*\s*/, '') // 移除开头的星号
          .replace(/\n\*\s*/g, ' ') // 将多行内容合并
          .trim();
      }
      
      if (title && content) {
        newsItems.push({
          id: `news-${newsNumber}`,
          title: title,
          content: content,
          category: category,
        });
      }
    }
  }
  
  console.log(`主解析方法完成，共解析出 ${newsItems.length} 条新闻`);
  return newsItems;
}

// 备用解析方法 - 当标准格式解析失败时使用
function parseNewsItemsFallback(content) {
  console.log('使用备用解析方法...');
  const newsItems = [];
  
  // 匹配新闻条目的多种格式
  const newsPatterns = [
    // 格式1: **数字. 【标签】标题**
    /\*\*(\d+)\. 【[^】]*】([^\*]+)\*\*([\s\S]*?)(?=\*\*\d+\.|$)/g,
    // 格式2: **数字. 标题**
    /\*\*(\d+)\. ([^\*]+)\*\*([\s\S]*?)(?=\*\*\d+\.|$)/g,
  ];
  
  for (let patternIndex = 0; patternIndex < newsPatterns.length; patternIndex++) {
    const pattern = newsPatterns[patternIndex];
    console.log(`尝试解析模式 ${patternIndex + 1}`);
    const matches = Array.from(content.matchAll(pattern));
    console.log(`模式 ${patternIndex + 1} 找到 ${matches.length} 个匹配`);
    
    for (const match of matches) {
      const newsNumber = match[1];
      const title = match[2].trim();
      const contentBlock = match[3].trim();
      
      // 提取完整内容
      let content = '';
      
      // 查找分析与影响部分，将其内容作为完整的新闻内容
      const analysisMatch = contentBlock.match(/\*\s*\*\*分析与影响：\*\*([\s\S]*)/i);
      if (analysisMatch) {
        content = analysisMatch[1].trim();
      } else {
        // 如果没有找到"分析与影响"标识，使用整个内容块
        content = contentBlock
          .replace(/^\*\s*/, '') // 移除开头的星号
          .replace(/\n\*\s*/g, ' ') // 将多行内容合并
          .trim();
      }
      
      // 智能分类
      const category = identifyCategory(title, content);
      
      if (title && content) {
        newsItems.push({
          id: `news-${newsNumber}`,
          title: title,
          content: content,
          category: category,
        });
      }
    }
    
    if (newsItems.length > 0) {
      console.log(`备用方法成功解析出 ${newsItems.length} 条新闻`);
      break; // 如果找到了新闻条目，就不再尝试其他格式
    }
  }
  
  console.log(`备用解析方法完成，共解析出 ${newsItems.length} 条新闻`);
  return newsItems;
}

// 智能识别新闻分类 - 备用方法
function identifyCategory(title, content) {
  const focusKeywords = ['事件', '攻击', '漏洞', '泄露', '入侵', '勒索', '恶意软件', '钓鱼', '数据泄露', '黑客'];
  const riskKeywords = ['风险', '预警', '威胁', '警告', '安全隐患', '漏洞警报', '风险评估', '威胁情报'];
  const innovationKeywords = ['政策', '法规', '创新', '技术', '产业', '发布', '更新', '新功能', '投资', '合作', '协议'];
  
  const fullText = `${title} ${content}`.toLowerCase();
  
  let focusScore = 0;
  let riskScore = 0;
  let innovationScore = 0;
  
  focusKeywords.forEach(keyword => {
    if (fullText.includes(keyword)) focusScore++;
  });
  
  riskKeywords.forEach(keyword => {
    if (fullText.includes(keyword)) riskScore++;
  });
  
  innovationKeywords.forEach(keyword => {
    if (fullText.includes(keyword)) innovationScore++;
  });
  
  if (riskScore > focusScore && riskScore > innovationScore) {
    return 'risk';
  } else if (innovationScore > focusScore && innovationScore > riskScore) {
    return 'innovation';
  } else {
    return 'focus';
  }
}

// 主解析函数
export function parseContent(rawContent) {
  const date = extractDate(rawContent);
  const lastIssue = getLastIssueNumber();
  const issue = lastIssue + 1;
  const summary = extractSummary(rawContent);
  const news = parseNewsItems(rawContent);
  
  // 输出调试信息
  console.log('解析调试信息:');
  console.log('- 日期:', date);
  console.log('- 期数:', issue);
  console.log('- 摘要长度:', summary.length);
  console.log('- 新闻数量:', news.length);
  
  if (news.length < 5) {
    console.warn('解析的新闻数量较少:', news.length, '条');
  }
  
  // 保存当前期数
  saveIssueNumber(issue);
  
  return {
    date,
    issue,
    summary,
    news,
  };
}

// 重置期数计数器
export function resetIssueCounter() {
  localStorage.removeItem('ocean-security-last-issue');
}

// 手动设置期数
export function setIssueNumber(issue) {
  saveIssueNumber(issue - 1); // 保存前一个数字，下次解析时会自动加1
}