// 海之安新闻系统 - 增强交互脚本
document.addEventListener('DOMContentLoaded', function() {
    
    // 动态时间更新
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const updateTimeElement = document.querySelector('.update-time');
        if (updateTimeElement) {
            updateTimeElement.textContent = `实时更新: ${timeString}`;
        }
    }
    
    // 每秒更新时间
    setInterval(updateTime, 1000);
    updateTime();
    
    // 新闻卡片悬停效果增强
    const newsCards = document.querySelectorAll('.news-card');
    newsCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
            this.style.boxShadow = '0 25px 50px rgba(59, 130, 246, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // 平滑滚动效果
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // 懒加载效果
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // 为所有新闻卡片添加懒加载效果
    const elementsToAnimate = document.querySelectorAll('.latest-news, .category-section');
    elementsToAnimate.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(element);
    });
    
    // 添加键盘导航支持
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            // ESC键关闭任何打开的模态框或返回顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
    
    // 页面性能监控
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log(`页面加载时间: ${Math.round(perfData.loadEventEnd - perfData.loadEventStart)}ms`);
            }, 0);
        });
    }
    
    // 自动刷新机制（可配置）
    const AUTO_REFRESH_INTERVAL = 5 * 60 * 1000; // 5分钟
    let refreshTimer;
    
    function startAutoRefresh() {
        refreshTimer = setTimeout(function() {
            // 显示刷新提示
            showRefreshNotification();
        }, AUTO_REFRESH_INTERVAL);
    }
    
    function showRefreshNotification() {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(15, 23, 42, 0.95);
            color: #e2e8f0;
            padding: 15px 20px;
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 1000;
            backdrop-filter: blur(10px);
            animation: slideInRight 0.3s ease;
        `;
        
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span>🔄</span>
                <span>发现新内容，是否刷新页面？</span>
                <button onclick="location.reload()" style="
                    background: #3b82f6;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 6px;
                    cursor: pointer;
                    margin-left: 10px;
                ">刷新</button>
                <button onclick="this.parentElement.parentElement.remove()" style="
                    background: transparent;
                    color: #94a3b8;
                    border: 1px solid rgba(148, 163, 184, 0.3);
                    padding: 5px 10px;
                    border-radius: 6px;
                    cursor: pointer;
                ">稍后</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // 10秒后自动移除通知
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 10000);
    }
    
    // 启动自动刷新
    startAutoRefresh();
    
    // 页面可见性API - 当页面重新获得焦点时检查更新
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            // 页面重新可见，可以检查是否有新内容
            updateTime();
        }
    });
});

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        from {
            transform: translateY(30px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease forwards;
    }
`;
document.head.appendChild(style);