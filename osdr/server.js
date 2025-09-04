const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const port = process.env.PORT || 3000;

// 静态文件服务
app.use(express.static(path.join(__dirname, 'public')));

// 首页路由
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// 启动服务器
app.listen(port, () => {
  console.log(`安全日报生成器服务已启动，访问 http://localhost:${port}`);
  console.log('按 Ctrl+C 停止服务');
});

// 检查logo文件是否存在
const logoPath = path.join(__dirname, 'public', 'ocean_security_logo.png');
if (!fs.existsSync(logoPath)) {
  console.warn('警告: logo文件不存在 - ' + logoPath);
  console.warn('请确保logo文件已放置在正确位置，否则生成的HTML中logo将无法显示');
}