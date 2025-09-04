#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强型网页内容抓取器
借鉴crawl4ai的思路，专门用于新闻内容提取
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import logging
from typing import Dict, Optional, List
from urllib.parse import urljoin, urlparse
import json

logger = logging.getLogger(__name__)

class EnhancedNewsCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # 新闻内容选择器 - 针对不同网站的内容提取规则
        self.content_selectors = {
            # 通用选择器
            'generic': [
                'article', '.article-content', '.post-content', '.entry-content',
                '.content', '.main-content', '.article-body', '.post-body',
                '[role="main"]', '.story-body', '.article-text', '.news-content'
            ],
            
            # 中文安全媒体特定选择器
            'anquanke.com': ['.article-content', '.post-content', '.content'],
            'freebuf.com': ['.article-content', '.post-content', '.content-detail'],
            '4hou.com': ['.article-content', '.post-content', '.detail-content'],
            
            # 国际安全媒体特定选择器
            'krebsonsecurity.com': ['.entry-content', '.post-content'],
            'thehackernews.com': ['.articlebody', '.story-content'],
            'bleepingcomputer.com': ['.articleBody', '.article_section'],
            'securityweek.com': ['.field-item', '.article-content'],
            'darkreading.com': ['.article-content', '.body-content'],
            'schneier.com': ['.entry-content', '.post-content']
        }
        
        # 需要移除的元素
        self.remove_selectors = [
            'script', 'style', 'nav', 'header', 'footer', 'aside', 
            '.advertisement', '.ads', '.social-share', '.related-posts',
            '.comments', '.comment', '.sidebar', '.menu', '.navigation',
            '.breadcrumb', '.tags', '.author-info', '.share-buttons'
        ]
    
    def extract_article_content(self, url: str, max_length: int = 3000) -> Dict:
        """
        提取文章完整内容
        
        Args:
            url: 文章链接
            max_length: 最大内容长度
            
        Returns:
            包含标题、内容、摘要等信息的字典
        """
        try:
            logger.info(f"正在抓取文章内容: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 提取标题
            title = self._extract_title(soup)
            
            # 提取主要内容
            content = self._extract_main_content(soup, url)
            
            # 提取摘要
            summary = self._extract_summary(soup, content)
            
            # 提取关键信息
            metadata = self._extract_metadata(soup)
            
            # 清理和截断内容
            if content and len(content) > max_length:
                content = content[:max_length] + "..."
            
            result = {
                'title': title,
                'content': content,
                'summary': summary,
                'word_count': len(content.split()) if content else 0,
                'char_count': len(content) if content else 0,
                'metadata': metadata,
                'url': url,
                'success': True
            }
            
            logger.info(f"成功提取内容: {title[:50]}... ({result['char_count']}字符)")
            return result
            
        except Exception as e:
            logger.error(f"抓取文章内容失败 {url}: {e}")
            return {
                'title': '',
                'content': '',
                'summary': '',
                'word_count': 0,
                'char_count': 0,
                'metadata': {},
                'url': url,
                'success': False,
                'error': str(e)
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """提取文章标题"""
        # 尝试多种标题选择器
        title_selectors = [
            'h1.article-title', 'h1.post-title', 'h1.entry-title',
            'h1.title', '.article-header h1', '.post-header h1',
            'h1', 'title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 10:  # 确保标题有意义
                    return title
        
        # 如果都没找到，使用页面title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return "未知标题"
    
    def _extract_main_content(self, soup: BeautifulSoup, url: str) -> str:
        """提取主要内容"""
        # 移除不需要的元素
        for selector in self.remove_selectors:
            for element in soup.select(selector):
                element.decompose()
        
        # 根据域名选择特定的选择器
        domain = urlparse(url).netloc.lower()
        selectors = self.content_selectors.get(domain, self.content_selectors['generic'])
        
        # 尝试使用特定选择器
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                content_parts = []
                for element in elements:
                    text = element.get_text(separator='\n', strip=True)
                    if text and len(text) > 100:  # 确保内容有意义
                        content_parts.append(text)
                
                if content_parts:
                    content = '\n\n'.join(content_parts)
                    # 清理内容
                    content = self._clean_content(content)
                    return content
        
        # 如果特定选择器没找到内容，使用通用方法
        return self._extract_content_generic(soup)
    
    def _extract_content_generic(self, soup: BeautifulSoup) -> str:
        """通用内容提取方法"""
        # 查找最可能包含主要内容的元素
        content_candidates = []
        
        # 查找包含大量文本的div或p标签
        for tag in ['div', 'section', 'article']:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text(strip=True)
                if len(text) > 200:  # 至少200字符
                    content_candidates.append((element, len(text)))
        
        if content_candidates:
            # 选择文本最长的元素
            best_element = max(content_candidates, key=lambda x: x[1])[0]
            content = best_element.get_text(separator='\n', strip=True)
            return self._clean_content(content)
        
        # 最后的备选方案：提取所有p标签
        paragraphs = soup.find_all('p')
        if paragraphs:
            content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            return self._clean_content(content)
        
        return ""
    
    def _clean_content(self, content: str) -> str:
        """清理内容"""
        if not content:
            return ""
        
        # 移除多余的空白字符
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = re.sub(r' +', ' ', content)
        
        # 移除常见的无用文本
        unwanted_patterns = [
            r'点击.*?查看',
            r'更多.*?请.*?关注',
            r'本文.*?转载',
            r'声明.*?版权',
            r'Copyright.*?\d{4}',
            r'All rights reserved',
            r'Subscribe.*?newsletter',
            r'Follow.*?Twitter',
            r'Like.*?Facebook'
        ]
        
        for pattern in unwanted_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        return content.strip()
    
    def _extract_summary(self, soup: BeautifulSoup, content: str) -> str:
        """提取摘要"""
        # 尝试从meta标签提取描述
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'].strip()
        
        # 尝试从Open Graph标签提取
        og_desc = soup.find('meta', attrs={'property': 'og:description'})
        if og_desc and og_desc.get('content'):
            return og_desc['content'].strip()
        
        # 如果没有meta描述，从内容中提取前200字符作为摘要
        if content:
            sentences = content.split('。')
            summary = ""
            for sentence in sentences:
                if len(summary + sentence) < 200:
                    summary += sentence + "。"
                else:
                    break
            return summary.strip()
        
        return ""
    
    def _extract_metadata(self, soup: BeautifulSoup) -> Dict:
        """提取元数据"""
        metadata = {}
        
        # 提取发布时间
        time_selectors = [
            'time[datetime]', '.publish-time', '.post-date', 
            '.article-date', '[datetime]'
        ]
        
        for selector in time_selectors:
            element = soup.select_one(selector)
            if element:
                if element.get('datetime'):
                    metadata['publish_time'] = element['datetime']
                else:
                    metadata['publish_time'] = element.get_text(strip=True)
                break
        
        # 提取作者
        author_selectors = [
            '.author', '.byline', '.post-author', '.article-author'
        ]
        
        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                metadata['author'] = element.get_text(strip=True)
                break
        
        # 提取标签
        tag_selectors = [
            '.tags a', '.post-tags a', '.article-tags a'
        ]
        
        for selector in tag_selectors:
            elements = soup.select(selector)
            if elements:
                metadata['tags'] = [tag.get_text(strip=True) for tag in elements]
                break
        
        return metadata
    
    def batch_extract_articles(self, urls: List[str], delay: float = 1.0) -> List[Dict]:
        """
        批量提取文章内容
        
        Args:
            urls: 文章链接列表
            delay: 请求间隔时间
            
        Returns:
            提取结果列表
        """
        results = []
        
        for i, url in enumerate(urls):
            try:
                result = self.extract_article_content(url)
                results.append(result)
                
                # 避免请求过于频繁
                if i < len(urls) - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                logger.error(f"批量提取失败 {url}: {e}")
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e)
                })
        
        return results

# 测试函数
def test_crawler():
    """测试爬虫功能"""
    crawler = EnhancedNewsCrawler()
    
    # 测试URL
    test_urls = [
        'https://www.anquanke.com/post/id/310614',
        'https://krebsonsecurity.com/2025/07/phishers-target-aviation-execs-to-scam-customers/'
    ]
    
    for url in test_urls:
        print(f"\n测试URL: {url}")
        result = crawler.extract_article_content(url)
        
        if result['success']:
            print(f"标题: {result['title']}")
            print(f"内容长度: {result['char_count']} 字符")
            print(f"摘要: {result['summary'][:100]}...")
        else:
            print(f"提取失败: {result.get('error', '未知错误')}")

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    test_crawler()