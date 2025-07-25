import { DailyReport } from '../types/index';

// 生成内联CSS样式
function generateInlineCSS(): string {
  return `
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      
      body {
        font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        color: #f1f5f9;
        min-height: 100vh;
        padding: 20px;
        line-height: 1.6;
      }
      
      .container {
        max-width: 1200px;
        margin: 0 auto;
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 
                    0 0 0 1px rgba(59, 130, 246, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        overflow: hidden;
      }
      
      .header {
        background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
        border-bottom: 1px solid rgba(59, 130, 246, 0.3);
        padding: 40px;
        text-align: center;
        position: relative;
      }
      
      .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
      }
      
      .logo {
        width: 120px;
        height: auto;
        margin-bottom: 20px;
        filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.3));
      }
      
      .title {
        font-size: 36px;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
        text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
      }
      
      .subtitle {
        font-size: 18px;
        color: #94a3b8;
        margin-bottom: 8px;
      }
      
      .content {
        padding: 40px;
      }
      
      .summary-section {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 32px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
      }
      
      .summary-title {
        font-size: 20px;
        font-weight: 600;
        color: #3b82f6;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      
      .summary-title::before {
        content: '📊';
        font-size: 24px;
      }
      
      .summary-content {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 16px;
      }
      
      .category-section {
        margin-bottom: 40px;
        background: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        border: 1px solid rgba(59, 130, 246, 0.15);
        overflow: hidden;
      }
      
      .category-header {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 51, 234, 0.2));
        padding: 20px 24px;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3);
      }
      
      .category-title {
        font-size: 24px;
        font-weight: 600;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 12px;
      }
      
      .category-news {
        padding: 24px;
      }
      
      .news-item {
        background: rgba(51, 65, 85, 0.6);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        position: relative;
      }
      
      .news-item::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        border-radius: 2px 0 0 2px;
      }
      
      .news-item:hover {
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
      }
      
      .news-title {
        font-size: 18px;
        font-weight: 600;
        color: #f1f5f9;
        margin-bottom: 12px;
        line-height: 1.4;
      }
      
      .news-analysis {
        color: #cbd5e1;
        line-height: 1.7;
        font-size: 15px;
      }
      
      .footer {
        background: rgba(15, 23, 42, 0.8);
        border-top: 1px solid rgba(59, 130, 246, 0.3);
        padding: 24px 40px;
        text-align: center;
        color: #64748b;
        font-size: 14px;
      }
      
      /* 图标样式 */
      .icon-focus::before { content: '🎯'; }
      .icon-risk::before { content: '⚠️'; }
      .icon-innovation::before { content: '🚀'; }
      
      /* 移动端响应式样式 */
      @media (max-width: 768px) {
        body {
          padding: 10px;
          font-size: 14px;
        }
        
        .container {
          max-width: 100%;
          border-radius: 8px;
          margin: 0;
        }
        
        .header {
          padding: 20px 15px;
        }
        
        .logo {
          width: 80px;
          margin-bottom: 15px;
        }
        
        .title {
          font-size: 24px;
          margin-bottom: 12px;
        }
        
        .subtitle {
          font-size: 14px;
        }
        
        .content {
          padding: 20px 15px;
        }
        
        .summary-section {
          padding: 15px;
          margin-bottom: 20px;
        }
        
        .summary-title {
          font-size: 16px;
          margin-bottom: 12px;
        }
        
        .summary-content {
          font-size: 14px;
          line-height: 1.6;
        }
        
        .category-section {
          margin-bottom: 25px;
        }
        
        .category-header {
          padding: 15px;
        }
        
        .category-title {
          font-size: 18px;
          gap: 8px;
        }
        
        .category-news {
          padding: 15px;
        }
        
        .news-item {
          padding: 15px;
          margin-bottom: 15px;
        }
        
        .news-title {
          font-size: 16px;
          margin-bottom: 10px;
          line-height: 1.3;
        }
        
        .news-analysis {
          font-size: 13px;
          line-height: 1.5;
        }
        
        .footer {
          padding: 15px;
          font-size: 12px;
        }
      }
      
      /* 小屏幕优化 */
      @media (max-width: 480px) {
        body {
          padding: 5px;
          font-size: 13px;
        }
        
        .container {
          border-radius: 4px;
        }
        
        .header {
          padding: 15px 10px;
        }
        
        .logo {
          width: 60px;
        }
        
        .title {
          font-size: 20px;
        }
        
        .content {
          padding: 15px 10px;
        }
        
        .summary-section,
        .category-header,
        .category-news {
          padding: 12px;
        }
        
        .news-item {
          padding: 12px;
        }
        
        .news-title {
          font-size: 15px;
        }
        
        .news-analysis {
          font-size: 12px;
        }
      }
      
      /* 打印样式 */
      @media print {
        body {
          background: white;
          color: black;
          padding: 0;
          font-size: 12px;
        }
        
        .container {
          box-shadow: none;
          border: none;
          background: white;
          max-width: 100%;
        }
        
        .header {
          background: #f8f9fa;
          border-bottom: 2px solid #dee2e6;
          padding: 20px;
        }
        
        .title {
          color: #2563eb !important;
          -webkit-text-fill-color: #2563eb !important;
        }
        
        .summary-section,
        .category-section,
        .news-item {
          background: white;
          border: 1px solid #dee2e6;
          color: black;
        }
        
        .summary-title,
        .category-title {
          color: #2563eb;
        }
        
        .news-title {
          color: #1f2937;
        }
        
        .news-analysis,
        .summary-content {
          color: #374151;
        }
        
        .content {
          padding: 20px;
        }
      }
    </style>
  `;
}

// 生成HTML文档
export function generateHTMLReport(report: DailyReport): string {
  // 分类映射：从英文key到中文标题
  const categoryMapping: { [key: string]: string } = {
    'focus': '焦点安全事件',
    'risk': '重大风险与预警', 
    'innovation': '产业创新与政策'
  };

  const categoryIcons: { [key: string]: string } = {
    '焦点安全事件': 'icon-focus',
    '重大风险与预警': 'icon-risk',
    '产业创新与政策': 'icon-innovation'
  };

  // 按分类组织新闻
  const categorizedNews: { [key: string]: typeof report.news } = {
    '焦点安全事件': [],
    '重大风险与预警': [],
    '产业创新与政策': []
  };

  report.news.forEach(newsItem => {
    const chineseCategory = categoryMapping[newsItem.category] || newsItem.category;
    if (categorizedNews[chineseCategory]) {
      categorizedNews[chineseCategory].push(newsItem);
    }
  });

  const categorySections = Object.entries(categorizedNews)
    .filter(([_, news]) => news.length > 0)
    .map(([category, news]) => {
      const newsItems = news.map(item => `
        <div class="news-item">
          <div class="news-title">${item.title}</div>
          <div class="news-analysis"><strong>分析与影响：</strong> ${item.content}</div>
        </div>
      `).join('');

      return `
        <div class="category-section">
          <div class="category-header">
            <h2 class="category-title ${categoryIcons[category]}">${category}</h2>
          </div>
          <div class="category-news">
            ${newsItems}
          </div>
        </div>
      `;
    }).join('');

  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>海之安安全每日快报 - ${report.date} - 第${report.issue}期</title>
  ${generateInlineCSS()}
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="./ocean_security_logo.png" alt="Ocean Security Logo" class="logo">
      <h1 class="title">海之安安全每日快报</h1>
      <div class="subtitle">${report.date} · 第${report.issue}期</div>
    </div>
    
    <div class="content">
      ${report.summary ? `
        <div class="summary-section">
          <h2 class="summary-title">今日摘要</h2>
          <div class="summary-content">${report.summary}</div>
        </div>
      ` : ''}
      
      ${categorySections}
    </div>
    
    <div class="footer">
      <p>© ${new Date().getFullYear()} Ocean Security · 海之安安全每日快报</p>
      <p>Generated on ${new Date().toLocaleString('zh-CN')}</p>
    </div>
  </div>
</body>
</html>
  `.trim();
}

// 日期格式化函数：将日期转换为YYYYMMDD格式
function formatDateToFileName(dateStr: string): string {
  try {
    // 尝试多种日期格式
    let date: Date;
    
    // 处理中文日期格式："2025年7月21日"
    if (dateStr.includes('年') && dateStr.includes('月') && dateStr.includes('日')) {
      const match = dateStr.match(/(\d{4})年(\d{1,2})月(\d{1,2})日/);
      if (match) {
        const year = match[1];
        const month = match[2].padStart(2, '0');
        const day = match[3].padStart(2, '0');
        return `${year}${month}${day}`;
      }
    }
    
    // 处理ISO日期格式："2025-07-21"
    if (dateStr.includes('-')) {
      date = new Date(dateStr);
    } else {
      // 处理其他格式
      date = new Date(dateStr);
    }
    
    if (isNaN(date.getTime())) {
      // 如果日期解析失败，使用当前日期
      date = new Date();
    }
    
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    
    return `${year}${month}${day}`;
  } catch (error) {
    console.warn('日期解析失败，使用当前日期:', error);
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');
    return `${year}${month}${day}`;
  }
}

// 触发HTML文件下载
export function downloadHTMLReport(report: DailyReport): void {
  console.log('开始生成HTML下载...');
  console.log('报告数据:', report);
  
  try {
    const htmlContent = generateHTMLReport(report);
    console.log('HTML内容生成成功，长度:', htmlContent.length);
    
    const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' });
    console.log('Blob对象创建成功，大小:', blob.size);
    
    // 生成文件名：news + YYYYMMDD.html
    const dateFormatted = formatDateToFileName(report.date);
    const fileName = `news${dateFormatted}.html`;
    console.log('生成文件名:', fileName);
    
    // 创建下载链接
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    console.log('下载链接创建成功:', link.href);
    
    // 检查浏览器支持
    if (link.download !== undefined) {
      console.log('浏览器支持download属性');
    } else {
      console.warn('浏览器不支持download属性');
    }
    
    // 触发下载
    document.body.appendChild(link);
    console.log('链接已添加到DOM');
    
    link.click();
    console.log('已触发点击事件');
    
    document.body.removeChild(link);
    console.log('链接已从DOM移除');
    
    // 清理URL对象
    URL.revokeObjectURL(link.href);
    console.log('URL对象已清理');
    
    console.log(`✅ HTML快报已生成并下载: ${fileName}`);
    
    // 添加用户提示
    if (typeof window !== 'undefined' && window.alert) {
      setTimeout(() => {
        alert(`快报已下载: ${fileName}\n请检查浏览器的下载文件夹。`);
      }, 100);
    }
    
  } catch (error) {
    console.error('❌ HTML下载失败:', error);
    if (typeof window !== 'undefined' && window.alert) {
      alert('下载失败，请查看控制台了解详细错误信息。');
    }
  }
}