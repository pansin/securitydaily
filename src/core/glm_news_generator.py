#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于智谱GLM的网络安全新闻生成器
参考：https://docs.bigmodel.cn/cn/best-practice/creativepractice/aimorningnewspaper
"""

import requests
import json
from datetime import datetime, timedelta
import logging
import os
from typing import List, Dict
import feedparser
from bs4 import BeautifulSoup
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('glm_news.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GLMNewsGenerator:
    def __init__(self, api_key: str = None):
        """
        初始化GLM新闻生成器
        
        Args:
            api_key: 智谱GLM API密钥
        """
        self.api_key = api_key or os.getenv('GLM_API_KEY')
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 加载新闻源配置
        try:
            from src.core.news_sources_loader import NewsSourcesLoader
            self.sources_loader = NewsSourcesLoader()
            self.news_sources = self.sources_loader.get_enabled_sources()
            logger.info(f"✅ 从配置文件加载了 {len(self.news_sources)} 个新闻源")
        except ImportError:
            try:
                from news_sources_loader import NewsSourcesLoader
                self.sources_loader = NewsSourcesLoader()
                self.news_sources = self.sources_loader.get_enabled_sources()
                logger.info(f"✅ 从配置文件加载了 {len(self.news_sources)} 个新闻源")
            except ImportError:
                logger.warning("⚠️ 新闻源配置加载器未找到，使用默认配置")
                # 备用默认配置
                self.news_sources = [
                    {
                        'name': '安全客',
                        'rss_url': 'https://api.anquanke.com/data/v1/rss',
                        'weight': 1.0,
                        'language': 'zh',
                        'region': '中国',
                        'category': '综合安全',
                        'enabled': True
                    },
                    {
                        'name': 'FreeBuf',
                        'rss_url': 'https://www.freebuf.com/feed',
                        'weight': 1.0,
                        'language': 'zh',
                        'region': '中国',
                        'category': '综合安全',
                        'enabled': True
                    },
                    {
                        'name': '嘶吼',
                        'rss_url': 'https://www.4hou.com/feed',
                        'weight': 1.0,
                        'language': 'zh',
                        'region': '中国',
                        'category': '综合安全',
                        'enabled': True
                    }
                ]
            # 备用默认配置
            self.news_sources = [
                {
                    'name': '安全客',
                    'rss_url': 'https://api.anquanke.com/data/v1/rss',
                    'weight': 1.0,
                    'language': 'zh',
                    'region': '中国',
                    'category': '综合安全',
                    'enabled': True
                },
                {
                    'name': 'FreeBuf',
                    'rss_url': 'https://www.freebuf.com/feed',
                    'weight': 1.0,
                    'language': 'zh',
                    'region': '中国',
                    'category': '综合安全',
                    'enabled': True
                },
                {
                    'name': '嘶吼',
                    'rss_url': 'https://www.4hou.com/feed',
                    'weight': 1.0,
                    'language': 'zh',
                    'region': '中国',
                    'category': '综合安全',
                    'enabled': True
                }
            ]
        
        self.security_keywords = [
            '安全', '漏洞', '攻击', '黑客', '病毒', '恶意软件', '勒索', '渗透',
            '防护', '防御', '加密', '解密', '隐私', '数据泄露', '网络安全',
            'APT', 'DDoS', '钓鱼', '木马', '后门', '提权', 'CVE', 'RCE'
        ]
    
    def call_glm_api(self, prompt: str, model: str = "glm-4-flash") -> str:
        """
        调用智谱GLM API
        
        Args:
            prompt: 输入提示词
            model: 使用的模型名称
            
        Returns:
            生成的文本内容
        """
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                logger.error(f"GLM API调用失败: {response.status_code} - {response.text}")
                return ""
                
        except Exception as e:
            logger.error(f"GLM API调用异常: {e}")
            return ""
    
    def fetch_article_content(self, url: str, max_length: int = 3000) -> Dict:
        """
        使用增强型爬虫抓取文章完整内容
        
        Args:
            url: 文章链接
            max_length: 最大内容长度
            
        Returns:
            包含完整文章信息的字典
        """
        try:
            from src.crawlers.enhanced_crawler import EnhancedNewsCrawler
            crawler = EnhancedNewsCrawler()
            result = crawler.extract_article_content(url, max_length)
            
            if result['success']:
                logger.info(f"成功提取文章内容: {result['title'][:50]}... ({result['char_count']}字符)")
                return result
            else:
                logger.warning(f"增强爬虫提取失败，使用备用方法: {url}")
                return self._fallback_content_extraction(url, max_length)
                
        except ImportError:
            try:
                from enhanced_crawler import EnhancedNewsCrawler
                crawler = EnhancedNewsCrawler()
                result = crawler.extract_article_content(url, max_length)
                
                if result['success']:
                    logger.info(f"成功提取文章内容: {result['title'][:50]}... ({result['char_count']}字符)")
                    return result
                else:
                    logger.warning(f"增强爬虫提取失败，使用备用方法: {url}")
                    return self._fallback_content_extraction(url, max_length)
                    
            except ImportError:
                logger.warning("增强爬虫模块未找到，使用备用方法")
                return self._fallback_content_extraction(url, max_length)
        except Exception as e:
            logger.warning(f"增强爬虫提取失败: {e}，使用备用方法")
            return self._fallback_content_extraction(url, max_length)
            return self._fallback_content_extraction(url, max_length)
        except Exception as e:
            logger.warning(f"增强爬虫提取失败: {e}，使用备用方法")
            return self._fallback_content_extraction(url, max_length)
    
    def _fallback_content_extraction(self, url: str, max_length: int = 3000) -> Dict:
        """
        备用内容提取方法
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除不需要的标签
            for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
                tag.decompose()
            
            # 尝试找到主要内容区域
            content_selectors = [
                'article', '.article-content', '.post-content', '.entry-content',
                '.content', '.main-content', '.article-body', '.post-body',
                '[role="main"]', '.story-body', '.article-text'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = elements[0].get_text(strip=True)
                    break
            
            # 如果没有找到特定的内容区域，使用整个body
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(strip=True)
            
            # 清理和截断内容
            if content:
                # 移除多余的空白字符
                content = ' '.join(content.split())
                # 截断到指定长度
                if len(content) > max_length:
                    content = content[:max_length] + "..."
            
            # 提取标题
            title = ""
            title_tag = soup.find('title')
            if title_tag:
                title = title_tag.get_text(strip=True)
            
            return {
                'title': title,
                'content': content,
                'summary': content[:200] + "..." if len(content) > 200 else content,
                'char_count': len(content),
                'word_count': len(content.split()),
                'success': True,
                'url': url
            }
            
        except Exception as e:
            logger.warning(f"备用方法也失败 {url}: {e}")
            return {
                'title': '',
                'content': '',
                'summary': '',
                'char_count': 0,
                'word_count': 0,
                'success': False,
                'url': url,
                'error': str(e)
            }
    
    def fetch_security_news(self, days_back: int = 1) -> List[Dict]:
        """
        抓取网络安全新闻
        
        Args:
            days_back: 抓取几天前的新闻
            
        Returns:
            新闻列表
        """
        target_date = (datetime.now() - timedelta(days=days_back)).date()
        all_news = []
        
        logger.info(f"开始抓取 {target_date} 的网络安全新闻...")
        
        for source in self.news_sources:
            if not source.get('enabled', True):
                continue
                
            try:
                logger.info(f"正在抓取 {source['name']} ({source.get('region', 'Unknown')}) 的RSS源...")
                
                # 设置请求头
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # 获取RSS内容
                response = requests.get(source['rss_url'], headers=headers, timeout=15)
                feed = feedparser.parse(response.content)
                source_news = []
                
                for entry in feed.entries:
                    # 解析发布时间
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6]).date()
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        pub_date = datetime(*entry.updated_parsed[:6]).date()
                    
                    # 检查是否为目标日期的新闻（允许3天内的新闻）
                    if pub_date and (datetime.now().date() - pub_date).days <= 3:
                        # 检查是否为安全相关新闻
                        title = entry.title.lower()
                        summary = getattr(entry, 'summary', '').lower()
                        
                        # 扩展关键词匹配逻辑
                        is_security_related = any(keyword.lower() in title or keyword.lower() in summary 
                                                for keyword in self.security_keywords)
                        
                        if is_security_related:
                            # 获取文章完整内容
                            article_data = {'content': '', 'title': entry.title, 'summary': ''}
                            
                            if hasattr(entry, 'content') and entry.content:
                                # RSS中包含内容
                                rss_content = entry.content[0].value if isinstance(entry.content, list) else str(entry.content)
                                # 清理HTML标签
                                soup = BeautifulSoup(rss_content, 'html.parser')
                                article_data['content'] = soup.get_text(strip=True)
                                article_data['summary'] = article_data['content'][:200] + "..." if len(article_data['content']) > 200 else article_data['content']
                            elif entry.link:
                                # 使用增强型爬虫抓取完整文章内容
                                logger.info(f"正在使用增强爬虫抓取: {entry.title[:50]}...")
                                article_data = self.fetch_article_content(entry.link)
                                
                                # 如果增强爬虫获取的标题更好，使用它
                                if article_data.get('title') and len(article_data['title']) > len(entry.title):
                                    entry.title = article_data['title']
                            
                            # 使用RSS摘要作为备选
                            if not article_data.get('summary'):
                                article_data['summary'] = getattr(entry, 'summary', '')
                            
                            news_item = {
                                'title': entry.title,
                                'link': entry.link,
                                'summary': article_data.get('summary', ''),
                                'content': article_data.get('content', ''),
                                'enhanced_content': article_data.get('success', False),  # 标记是否使用了增强抓取
                                'char_count': article_data.get('char_count', 0),
                                'word_count': article_data.get('word_count', 0),
                                'metadata': article_data.get('metadata', {}),
                                'published_date': pub_date,
                                'source': source['name'],
                                'weight': source['weight'],
                                'language': source.get('language', 'en'),
                                'region': source.get('region', 'Unknown')
                            }
                            source_news.append(news_item)
                
                logger.info(f"从 {source['name']} 获取到 {len(source_news)} 条安全新闻")
                all_news.extend(source_news)
                
                # 避免请求过于频繁
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"抓取 {source['name']} 失败: {e}")
                continue
        
        # 去重和排序
        unique_news = []
        seen_titles = set()
        
        for news in all_news:
            # 使用标题的前50个字符进行去重，避免完全相同的标题
            title_key = news['title'][:50].lower()
            if title_key not in seen_titles:
                unique_news.append(news)
                seen_titles.add(title_key)
        
        # 按权重和时间排序，取前15条（增加数量以获得更好的选择）
        unique_news.sort(key=lambda x: (x['weight'], x['published_date']), reverse=True)
        
        logger.info(f"总共获取到 {len(unique_news)} 条不重复的安全新闻")
        return unique_news[:15]
    
    def select_top_news(self, news_list: List[Dict]) -> List[Dict]:
        """
        使用GLM从所有新闻中精选出最重要的10篇
        
        Args:
            news_list: 全部新闻列表
            
        Returns:
            精选的10篇新闻
        """
        if len(news_list) <= 10:
            return news_list
        
        # 构建新闻信息用于GLM分析
        news_details = []
        for i, news in enumerate(news_list):
            content_preview = ""
            if news.get('content'):
                content_preview = news['content'][:200] + "..." if len(news['content']) > 200 else news['content']
            elif news.get('summary'):
                content_preview = news['summary'][:200] + "..." if len(news['summary']) > 200 else news['summary']
            
            news_detail = f"{i+1}. 【{news['source']} - {news.get('region', 'Unknown')}】{news['title']}\n"
            if content_preview:
                news_detail += f"   内容: {content_preview}\n"
            news_details.append(news_detail)
        
        news_text = "\n".join(news_details)
        
        # 使用GLM精选新闻
        try:
            from config.glm_config import PROMPT_TEMPLATES
        except ImportError:
            # 备用导入路径
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from config.glm_config import PROMPT_TEMPLATES
        select_prompt = PROMPT_TEMPLATES['select_top_news'].format(news_text=news_text)
        
        select_result = self.call_glm_api(select_prompt)
        
        # 解析精选结果
        selected_indices = []
        try:
            result_data = json.loads(select_result)
            selected_news = result_data.get('selected_news', [])
            
            # 根据标题匹配找到对应的新闻索引
            for selected in selected_news:
                selected_title = selected['title']
                for i, news in enumerate(news_list):
                    if selected_title in news['title'] or news['title'] in selected_title:
                        if i not in selected_indices:
                            selected_indices.append(i)
                        break
            
        except Exception as e:
            logger.warning(f"新闻精选结果解析失败: {e}，使用默认选择")
            # 默认选择：按权重和时间排序取前10条
            sorted_news = sorted(enumerate(news_list), 
                               key=lambda x: (x[1].get('weight', 0), x[1].get('published_date', datetime.min.date())), 
                               reverse=True)
            selected_indices = [i for i, _ in sorted_news[:10]]
        
        # 确保选择了10篇新闻
        if len(selected_indices) < 10:
            remaining_indices = [i for i in range(len(news_list)) if i not in selected_indices]
            selected_indices.extend(remaining_indices[:10-len(selected_indices)])
        
        selected_news = [news_list[i] for i in selected_indices[:10]]
        logger.info(f"成功精选出 {len(selected_news)} 篇全球安全新闻")
        
        return selected_news

    def generate_news_analysis(self, news_list: List[Dict]) -> Dict:
        """
        使用GLM生成新闻分析和摘要
        
        Args:
            news_list: 新闻列表
            
        Returns:
            包含分析内容的字典
        """
        if not news_list:
            return {"summary": "今日暂无网络安全新闻", "categories": {}}
        
        # 首先精选10篇最重要的新闻
        logger.info("正在使用GLM精选全球重要安全新闻...")
        selected_news = self.select_top_news(news_list)
        
        # 构建精选新闻的详细信息 - 利用增强爬虫获取的丰富内容
        news_details = []
        for i, news in enumerate(selected_news):
            content_preview = ""
            
            # 优先使用增强爬虫获取的完整内容
            if news.get('enhanced_content') and news.get('content'):
                content_preview = news['content'][:500] + "..." if len(news['content']) > 500 else news['content']
                content_quality = "增强内容"
            elif news.get('summary'):
                content_preview = news['summary']
                content_quality = "RSS摘要"
            else:
                content_preview = "内容获取失败"
                content_quality = "无内容"
            
            news_detail = f"{i+1}. 【{news['source']} - {news.get('region', 'Unknown')}】{news['title']}\n"
            news_detail += f"   内容质量: {content_quality} ({news.get('char_count', 0)}字符)\n"
            if content_preview:
                news_detail += f"   详细内容: {content_preview}\n"
            news_detail += f"   语言: {news.get('language', 'unknown')}\n"
            
            # 如果有元数据，也包含进来
            if news.get('metadata'):
                metadata = news['metadata']
                if metadata.get('author'):
                    news_detail += f"   作者: {metadata['author']}\n"
                if metadata.get('publish_time'):
                    news_detail += f"   发布时间: {metadata['publish_time']}\n"
            
            news_details.append(news_detail)
        
        news_text = "\n".join(news_details)
        
        # 生成全球安全态势摘要
        try:
            from config.glm_config import PROMPT_TEMPLATES
        except ImportError:
            # 备用导入路径
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from config.glm_config import PROMPT_TEMPLATES
        summary_prompt = PROMPT_TEMPLATES['summary'].format(news_text=news_text)
        summary = self.call_glm_api(summary_prompt)
        
        # 按四个维度分类并生成完整要素总结
        category_prompt = PROMPT_TEMPLATES['categorize_and_summarize'].format(news_text=news_text)
        category_result = self.call_glm_api(category_prompt)
        
        # 解析分类结果
        categories = {}
        try:
            categories = json.loads(category_result)
            logger.info("成功使用GLM进行四维度新闻分类和要素总结")
        except Exception as e:
            logger.warning(f"分类结果解析失败: {e}，使用默认分类")
            categories = self._default_categorize_news_four_dimensions(selected_news)
        
        # 统计增强内容的效果
        enhanced_count = sum(1 for news in selected_news if news.get('enhanced_content', False))
        total_chars = sum(news.get('char_count', 0) for news in selected_news)
        
        return {
            "summary": summary,
            "categories": categories,
            "total_news": len(selected_news),
            "original_count": len(news_list),
            "enhanced_count": enhanced_count,
            "total_chars": total_chars,
            "sources": list(set([news['source'] for news in selected_news])),
            "regions": list(set([news.get('region', 'Unknown') for news in selected_news])),
            "languages": list(set([news.get('language', 'unknown') for news in selected_news]))
        }
    
    def _default_categorize_news_four_dimensions(self, news_list: List[Dict]) -> Dict:
        """
        默认四维度新闻分类逻辑（当AI分类失败时使用）
        """
        categories = {
            "安全风险": [],
            "安全事件": [],
            "安全舆情": [],
            "安全趋势": []
        }
        
        # 基于关键词的四维度分类
        for news in news_list:
            title_lower = news['title'].lower()
            content_lower = (news.get('content', '') + news.get('summary', '')).lower()
            
            # 生成包含关键要素的总结
            summary_text = ""
            if news.get('content'):
                summary_text = news['content'][:150] + "..."
            elif news.get('summary'):
                summary_text = news['summary'][:150] + "..."
            else:
                summary_text = f"来自{news['source']}的安全新闻，详细内容请查看原文。"
            
            # 翻译英文标题（简单处理）
            display_title = news['title']
            if news.get('language') == 'en':
                display_title = f"[国际] {news['title']}"
            
            item = {
                "title": display_title,
                "source": news['source'],
                "region": news.get('region', 'Unknown'),
                "summary": summary_text,
                "key_points": [
                    f"来源：{news['source']}",
                    f"地区：{news.get('region', 'Unknown')}",
                    "详细分析请查看原文"
                ],
                "impact_level": "中"
            }
            
            # 四维度关键词分类
            if any(keyword in title_lower or keyword in content_lower for keyword in 
                   ['vulnerability', 'cve', 'exploit', '漏洞', '威胁', 'threat', 'risk', '风险']):
                categories["安全风险"].append(item)
            elif any(keyword in title_lower or keyword in content_lower for keyword in 
                     ['breach', 'attack', 'hack', '攻击', '泄露', '入侵', '勒索', 'incident']):
                categories["安全事件"].append(item)
            elif any(keyword in title_lower or keyword in content_lower for keyword in 
                     ['policy', 'regulation', 'compliance', '政策', '法规', '合规', '报告', 'report']):
                categories["安全舆情"].append(item)
            else:
                categories["安全趋势"].append(item)
        
        return categories
    
    def translate_english_news(self, news: Dict) -> Dict:
        """
        翻译英文新闻为中文并进行分析
        
        Args:
            news: 英文新闻字典
            
        Returns:
            翻译和分析后的新闻字典
        """
        if news.get('language') != 'en' or not news.get('content'):
            return news
        
        try:
            from config.glm_config import PROMPT_TEMPLATES
        except ImportError:
            # 备用导入路径
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from config.glm_config import PROMPT_TEMPLATES
            translate_prompt = PROMPT_TEMPLATES['translate_and_analyze'].format(
                title=news['title'],
                content=news.get('content', '')[:1000],  # 限制长度避免超时
                source=news['source']
            )
            
            translate_result = self.call_glm_api(translate_prompt)
            result_data = json.loads(translate_result)
            
            # 更新新闻信息
            news['chinese_title'] = result_data.get('chinese_title', news['title'])
            news['translated_summary'] = result_data.get('summary', '')
            news['key_points'] = result_data.get('key_points', [])
            news['impact_analysis'] = result_data.get('impact_analysis', '')
            news['threat_level'] = result_data.get('threat_level', '中危')
            
            logger.info(f"成功翻译英文新闻: {news['title'][:50]}...")
            
        except Exception as e:
            logger.warning(f"翻译英文新闻失败: {e}")
        
        return news
    
    def generate_html_report(self, analysis_result: Dict, date_str: str) -> str:
        """
        生成HTML格式的新闻快报
        
        Args:
            analysis_result: 分析结果
            date_str: 日期字符串
            
        Returns:
            HTML内容
        """
        current_time = datetime.now().strftime('%Y年%m月%d日')
        
        # 导入样式保护模块
        try:
            from style_protection import get_mobile_responsive_css, ensure_mobile_responsive
            mobile_css = get_mobile_responsive_css()
            logger.info("✅ 成功加载移动端样式保护模块")
        except ImportError:
            # 如果导入失败，使用内置的移动端样式
            mobile_css = self._get_fallback_mobile_css()
            logger.warning("⚠️ 样式保护模块未找到，使用内置备用样式")
        
        html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>海之安网络安全日报 - {current_time}</title>
  
  <style>
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    body {{
      font-family: 'Microsoft YaHei', 'SimHei', 'Arial', sans-serif;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
      color: #f1f5f9;
      min-height: 100vh;
      padding: 20px;
      line-height: 1.6;
    }}
    
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid rgba(59, 130, 246, 0.3);
      border-radius: 16px;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8);
      overflow: hidden;
    }}
    
    .header {{
      background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
      border-bottom: 1px solid rgba(59, 130, 246, 0.3);
      padding: 40px;
      text-align: center;
      position: relative;
    }}
    
    .header::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
      background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
    }}
    
    .logo {{
      width: 200px;
      height: auto;
      margin-bottom: 20px;
    }}
    
    .title {{
      font-size: 36px;
      font-weight: 700;
      background: linear-gradient(135deg, #3b82f6, #8b5cf6);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      margin-bottom: 16px;
    }}
    
    .subtitle {{
      font-size: 18px;
      color: #94a3b8;
      margin-bottom: 8px;
    }}
    
    .content {{
      padding: 40px;
    }}
    
    .summary-section {{
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 32px;
    }}
    
    .summary-title {{
      font-size: 20px;
      font-weight: 600;
      color: #3b82f6;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    
    .summary-title::before {{
      content: '📊';
      font-size: 24px;
    }}
    
    .summary-content {{
      color: #cbd5e1;
      line-height: 1.8;
      font-size: 16px;
    }}
    
    .category-section {{
      margin-bottom: 40px;
      background: rgba(30, 41, 59, 0.4);
      border-radius: 12px;
      border: 1px solid rgba(59, 130, 246, 0.15);
      overflow: hidden;
    }}
    
    .category-header {{
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(147, 51, 234, 0.2));
      padding: 20px 24px;
      border-bottom: 1px solid rgba(59, 130, 246, 0.3);
    }}
    
    .category-title {{
      font-size: 24px;
      font-weight: 600;
      color: #e2e8f0;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    
    .category-news {{
      padding: 24px;
    }}
    
    .news-item {{
      background: rgba(51, 65, 85, 0.6);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      transition: all 0.3s ease;
      position: relative;
    }}
    
    .news-item::before {{
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: linear-gradient(180deg, #3b82f6, #8b5cf6);
      border-radius: 2px 0 0 2px;
    }}
    
    .news-item:hover {{
      border-color: rgba(59, 130, 246, 0.4);
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }}
    
    .news-title {{
      font-size: 18px;
      font-weight: 600;
      color: #f1f5f9;
      margin-bottom: 12px;
      line-height: 1.4;
    }}
    
    .news-analysis {{
      color: #cbd5e1;
      line-height: 1.7;
      font-size: 15px;
    }}
    
    .footer {{
      background: rgba(15, 23, 42, 0.8);
      border-top: 1px solid rgba(59, 130, 246, 0.3);
      padding: 24px 40px;
      text-align: center;
      color: #64748b;
      font-size: 14px;
    }}
    
    .stats-section {{
      margin-bottom: 32px;
    }}
    
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 20px;
    }}
    
    .stat-card {{
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(59, 130, 246, 0.2);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
      border-color: rgba(59, 130, 246, 0.4);
      transform: translateY(-2px);
    }}
    
    .stat-number {{
      font-size: 32px;
      font-weight: 700;
      color: #3b82f6;
      margin-bottom: 8px;
    }}
    
    .stat-label {{
      font-size: 14px;
      color: #94a3b8;
      margin-bottom: 4px;
    }}
    
    .stat-detail {{
      font-size: 12px;
      color: #64748b;
    }}
    
    .source-list {{
      margin-top: 24px;
      padding: 20px;
      background: rgba(30, 41, 59, 0.8);
      border-radius: 12px;
      border: 1px solid rgba(59, 130, 246, 0.2);
    }}
    
    .source-list h3 {{
      color: #3b82f6;
      font-size: 16px;
      margin-bottom: 12px;
    }}
    
    .source-tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}
    
    .source-tag {{
      background: rgba(59, 130, 246, 0.1);
      color: #93c5fd;
      padding: 6px 12px;
      border-radius: 16px;
      font-size: 12px;
      border: 1px solid rgba(59, 130, 246, 0.2);
    }}
    
    .enhancement-info {{
      margin-top: 24px;
      padding: 20px;
      background: rgba(34, 197, 94, 0.1);
      border-radius: 12px;
      border: 1px solid rgba(34, 197, 94, 0.2);
    }}
    
    .enhancement-info h3 {{
      color: #22c55e;
      font-size: 16px;
      margin-bottom: 12px;
    }}
    
    .enhancement-stats {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    
    .enhancement-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      border-bottom: 1px solid rgba(34, 197, 94, 0.1);
    }}
    
    .enhancement-item:last-child {{
      border-bottom: none;
    }}
    
    .enhancement-label {{
      color: #94a3b8;
      font-size: 14px;
    }}
    
    .enhancement-value {{
      color: #22c55e;
      font-weight: 600;
      font-size: 14px;
    }}
    
    .content-quality-badge {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      margin-left: 8px;
    }}
    
    .quality-enhanced {{
      background: rgba(34, 197, 94, 0.2);
      color: #86efac;
      border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    
    .quality-rss {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .quality-failed {{
      background: rgba(239, 68, 68, 0.2);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    .news-header {{
      margin-bottom: 12px;
    }}
    
    .news-meta {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 8px;
      font-size: 12px;
    }}
    
    .news-source {{
      color: #94a3b8;
      background: rgba(59, 130, 246, 0.1);
      padding: 4px 8px;
      border-radius: 4px;
    }}
    
    .severity-badge {{
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: 600;
      font-size: 11px;
    }}
    
    .severity-high {{
      background: rgba(239, 68, 68, 0.2);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    .severity-medium {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .severity-low {{
      background: rgba(34, 197, 94, 0.2);
      color: #86efac;
      border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    
    .severity-info {{
      background: rgba(59, 130, 246, 0.2);
      color: #93c5fd;
      border: 1px solid rgba(59, 130, 246, 0.3);
    }}
    
    .news-summary {{
      color: #cbd5e1;
      line-height: 1.7;
      font-size: 15px;
      margin-bottom: 12px;
    }}
    
    .key-points {{
      margin: 12px 0;
      padding-left: 20px;
      color: #94a3b8;
      font-size: 14px;
    }}
    
    .key-points li {{
      margin-bottom: 4px;
      line-height: 1.4;
    }}
    
    .region-badge {{
      background: rgba(34, 197, 94, 0.1);
      color: #86efac;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
      margin: 0 4px;
    }}
    
    .impact-badge {{
      padding: 4px 8px;
      border-radius: 4px;
      font-weight: 600;
      font-size: 11px;
    }}
    
    .impact-high {{
      background: rgba(239, 68, 68, 0.2);
      color: #fca5a5;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    .impact-medium {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.3);
    }}
    
    .impact-low {{
      background: rgba(34, 197, 94, 0.2);
      color: #86efac;
      border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    
    .icon-risk::before {{ content: '⚠️'; }}
    .icon-event::before {{ content: '🚨'; }}
    .icon-opinion::before {{ content: '📢'; }}
    .icon-trend::before {{ content: '📈'; }}
    .icon-focus::before {{ content: '🎯'; }}
    
    /* 移动端适配样式 - 重要：请勿删除或覆盖 */
    @media (max-width: 768px) {{
      .container {{
        margin: 0;
        padding: 10px;
        border-radius: 0;
      }}
      
      .header {{
        padding: 20px 15px;
        border-radius: 0;
      }}
      
      .logo {{
        width: 150px;
        margin-bottom: 15px;
      }}
      
      .title {{
        font-size: 24px;
        margin-bottom: 12px;
      }}
      
      .subtitle {{
        font-size: 14px;
        margin-bottom: 6px;
      }}
      
      .content {{
        padding: 20px 15px;
      }}
      
      .summary-section {{
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 8px;
      }}
      
      .summary-title {{
        font-size: 16px;
        margin-bottom: 12px;
      }}
      
      .summary-content {{
        font-size: 14px;
        line-height: 1.6;
      }}
      
      .stats-section {{
        margin-bottom: 20px;
      }}
      
      .stats-grid {{
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }}
      
      .stat-card {{
        padding: 15px;
        border-radius: 8px;
      }}
      
      .stat-number {{
        font-size: 24px;
        margin-bottom: 6px;
      }}
      
      .stat-label {{
        font-size: 12px;
      }}
      
      .stat-detail {{
        font-size: 10px;
      }}
      
      .enhancement-info {{
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
      }}
      
      .enhancement-info h3 {{
        font-size: 14px;
        margin-bottom: 10px;
      }}
      
      .enhancement-item {{
        padding: 6px 0;
      }}
      
      .enhancement-label,
      .enhancement-value {{
        font-size: 12px;
      }}
      
      .source-list {{
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
      }}
      
      .source-list h3 {{
        font-size: 14px;
        margin-bottom: 10px;
      }}
      
      .source-tag {{
        padding: 4px 8px;
        font-size: 10px;
        margin: 2px;
      }}
      
      .category-section {{
        margin-bottom: 25px;
        border-radius: 8px;
      }}
      
      .category-header {{
        padding: 15px 20px;
      }}
      
      .category-title {{
        font-size: 18px;
      }}
      
      .category-news {{
        padding: 15px;
      }}
      
      .news-item {{
        padding: 15px;
        margin-bottom: 15px;
        border-radius: 6px;
      }}
      
      .news-title {{
        font-size: 16px;
        margin-bottom: 10px;
        line-height: 1.3;
      }}
      
      .news-meta {{
        flex-direction: column;
        align-items: flex-start;
        gap: 6px;
        margin-top: 6px;
      }}
      
      .news-source,
      .region-badge,
      .impact-badge,
      .content-quality-badge {{
        font-size: 10px;
        padding: 3px 6px;
        margin: 2px 4px 2px 0;
      }}
      
      .news-summary {{
        font-size: 13px;
        line-height: 1.5;
        margin-bottom: 10px;
      }}
      
      .key-points {{
        margin: 10px 0;
        padding-left: 15px;
        font-size: 12px;
      }}
      
      .key-points li {{
        margin-bottom: 3px;
        line-height: 1.3;
      }}
      
      .footer {{
        padding: 15px;
        border-radius: 0;
        font-size: 12px;
      }}
    }}
    
    /* 超小屏幕适配 (iPhone SE等) */
    @media (max-width: 480px) {{
      .container {{
        padding: 5px;
      }}
      
      .header {{
        padding: 15px 10px;
      }}
      
      .logo {{
        width: 120px;
      }}
      
      .title {{
        font-size: 20px;
      }}
      
      .subtitle {{
        font-size: 12px;
      }}
      
      .content {{
        padding: 15px 10px;
      }}
      
      .stats-grid {{
        grid-template-columns: 1fr;
        gap: 8px;
      }}
      
      .stat-card {{
        padding: 12px;
      }}
      
      .stat-number {{
        font-size: 20px;
      }}
      
      .category-title {{
        font-size: 16px;
      }}
      
      .news-title {{
        font-size: 14px;
      }}
      
      .news-summary {{
        font-size: 12px;
      }}
    }}
    
    /* 横屏适配 */
    @media (max-width: 768px) and (orientation: landscape) {{
      .stats-grid {{
        grid-template-columns: repeat(4, 1fr);
      }}
      
      .category-section {{
        margin-bottom: 20px;
      }}
      
      .news-item {{
        padding: 12px;
        margin-bottom: 12px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <svg class="logo" viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="logoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#8B5CF6;stop-opacity:1" />
            <stop offset="50%" style="stop-color:#3B82F6;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#06B6D4;stop-opacity:1" />
          </linearGradient>
        </defs>
        <circle cx="40" cy="60" r="25" fill="url(#logoGradient)" opacity="0.8"/>
        <circle cx="25" cy="35" r="15" fill="url(#logoGradient)" opacity="0.9"/>
        <circle cx="55" cy="35" r="12" fill="url(#logoGradient)" opacity="0.7"/>
        <circle cx="35" cy="75" r="10" fill="url(#logoGradient)" opacity="0.6"/>
        <circle cx="60" cy="75" r="8" fill="url(#logoGradient)" opacity="0.8"/>
        <text x="90" y="45" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#3b82f6">ocean security</text>
        <text x="90" y="70" font-family="Arial, sans-serif" font-size="12" fill="#94a3b8">海之安，数字安全专家</text>
      </svg>
      <h1 class="title">海之安网络安全日报</h1>
      <div class="subtitle">{current_time} · AI智能生成</div>
    </div>
    
    <div class="content">
      <div class="summary-section">
        <h2 class="summary-title">今日摘要</h2>
        <div class="summary-content">{analysis_result.get('summary', '今日暂无网络安全新闻摘要')}</div>
      </div>
"""
        
        # 添加统计信息 - 包含增强爬虫的效果统计
        sources = analysis_result.get('sources', [])
        regions = analysis_result.get('regions', [])
        languages = analysis_result.get('languages', [])
        enhanced_count = analysis_result.get('enhanced_count', 0)
        total_chars = analysis_result.get('total_chars', 0)
        
        html_template += f"""
      <div class="stats-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-number">{analysis_result.get('total_news', 0)}</div>
            <div class="stat-label">精选新闻</div>
            <div class="stat-detail">从{analysis_result.get('original_count', 0)}条中精选</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{enhanced_count}</div>
            <div class="stat-label">增强内容</div>
            <div class="stat-detail">深度抓取成功</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{total_chars:,}</div>
            <div class="stat-label">内容字符</div>
            <div class="stat-detail">丰富可读</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">4</div>
            <div class="stat-label">分析维度</div>
            <div class="stat-detail">风险·事件·舆情·趋势</div>
          </div>
        </div>
        <div class="enhancement-info">
          <h3>🚀 内容增强效果</h3>
          <div class="enhancement-stats">
            <div class="enhancement-item">
              <span class="enhancement-label">深度抓取成功率:</span>
              <span class="enhancement-value">{(enhanced_count/analysis_result.get('total_news', 1)*100):.1f}%</span>
            </div>
            <div class="enhancement-item">
              <span class="enhancement-label">平均内容长度:</span>
              <span class="enhancement-value">{total_chars//analysis_result.get('total_news', 1):,}字符</span>
            </div>
            <div class="enhancement-item">
              <span class="enhancement-label">内容质量:</span>
              <span class="enhancement-value">{'优秀' if enhanced_count > 5 else '良好' if enhanced_count > 2 else '一般'}</span>
            </div>
          </div>
        </div>
        <div class="source-list">
          <h3>📰 全球新闻来源</h3>
          <div class="source-tags">
"""
        
        # 添加来源标签
        for source in sources:
            html_template += f'<span class="source-tag">{source}</span>'
        
        html_template += """
          </div>
        </div>
      </div>
"""
        
        # 添加分类新闻 - 四维度分类
        icon_map = {
            "安全风险": "icon-risk",
            "安全事件": "icon-event", 
            "安全舆情": "icon-opinion",
            "安全趋势": "icon-trend"
        }
        
        for category, news_items in analysis_result.get('categories', {}).items():
            if news_items:
                icon_class = icon_map.get(category, "icon-focus")
                html_template += f"""
      <div class="category-section">
        <div class="category-header">
          <h2 class="category-title {icon_class}">{category}</h2>
        </div>
        <div class="category-news">
"""
                
                for item in news_items:
                    impact_level = item.get('impact_level', '中')
                    impact_class = {
                        '高': 'impact-high',
                        '中': 'impact-medium', 
                        '低': 'impact-low'
                    }.get(impact_level, 'impact-medium')
                    
                    # 处理关键点列表
                    key_points_html = ""
                    if item.get('key_points'):
                        key_points_html = "<ul class='key-points'>"
                        for point in item['key_points'][:3]:  # 最多显示3个关键点
                            key_points_html += f"<li>{point}</li>"
                        key_points_html += "</ul>"
                    
                    # 添加内容质量标识
                    quality_badge = ""
                    if hasattr(item, 'enhanced_content') and item.get('enhanced_content'):
                        quality_badge = '<span class="content-quality-badge quality-enhanced">深度内容</span>'
                    elif item.get('char_count', 0) > 500:
                        quality_badge = '<span class="content-quality-badge quality-rss">RSS内容</span>'
                    else:
                        quality_badge = '<span class="content-quality-badge quality-failed">简要内容</span>'
                    
                    html_template += f"""          <div class="news-item">
            <div class="news-header">
              <div class="news-title">{item['title']}{quality_badge}</div>
              <div class="news-meta">
                <span class="news-source">{item.get('source', '未知来源')}</span>
                <span class="region-badge">{item.get('region', 'Unknown')}</span>
                <span class="impact-badge {impact_class}">影响: {impact_level}</span>
              </div>
            </div>
            <div class="news-summary">
              <strong>内容要素：</strong>{item.get('summary', '暂无详细总结')}
            </div>
            {key_points_html}
          </div>
"""
                
                html_template += """        </div>
      </div>
"""
        
        # 添加footer
        html_template += f"""    </div>
    
    <div class="footer">
      <p>© 2025 海之安（中国）科技有限公司 | 基于智谱GLM AI生成</p>
      <p>共分析 {analysis_result.get('total_news', 0)} 条安全新闻 | 官网：<a href="https://www.oceansecurity.cn" style="color: #3b82f6;">www.oceansecurity.cn</a></p>
    </div>
  </div>
</body>
</html>"""
        
        # 确保包含移动端样式保护
        try:
            from style_protection import ensure_mobile_responsive
            html_template = ensure_mobile_responsive(html_template)
            logger.info("✅ 移动端样式保护已应用")
        except ImportError:
            # 如果保护模块不可用，手动检查和添加
            if "@media (max-width: 768px)" not in html_template:
                fallback_css = self._get_fallback_mobile_css()
                html_template = html_template.replace("</style>", fallback_css + "\n  </style>")
                logger.info("✅ 备用移动端样式已应用")
        
        return html_template
    
    def _get_fallback_mobile_css(self) -> str:
        """
        备用移动端CSS样式
        """
        return """
    /* 移动端适配样式 - 重要：请勿删除或覆盖 */
    @media (max-width: 768px) {
      .container { margin: 0; padding: 10px; border-radius: 0; }
      .header { padding: 20px 15px; border-radius: 0; }
      .logo { width: 150px; margin-bottom: 15px; }
      .title { font-size: 24px; margin-bottom: 12px; }
      .subtitle { font-size: 14px; margin-bottom: 6px; }
      .content { padding: 20px 15px; }
      .summary-section { padding: 15px; margin-bottom: 20px; border-radius: 8px; }
      .summary-title { font-size: 16px; margin-bottom: 12px; }
      .summary-content { font-size: 14px; line-height: 1.6; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
      .stat-card { padding: 15px; border-radius: 8px; }
      .stat-number { font-size: 24px; margin-bottom: 6px; }
      .stat-label { font-size: 12px; }
      .category-section { margin-bottom: 25px; border-radius: 8px; }
      .category-header { padding: 15px 20px; }
      .category-title { font-size: 18px; }
      .category-news { padding: 15px; }
      .news-item { padding: 15px; margin-bottom: 15px; border-radius: 6px; }
      .news-title { font-size: 16px; margin-bottom: 10px; line-height: 1.3; }
      .news-meta { flex-direction: column; align-items: flex-start; gap: 6px; margin-top: 6px; }
      .news-source, .region-badge, .impact-badge, .content-quality-badge { font-size: 10px; padding: 3px 6px; margin: 2px 4px 2px 0; }
      .news-summary { font-size: 13px; line-height: 1.5; margin-bottom: 10px; }
      .key-points { margin: 10px 0; padding-left: 15px; font-size: 12px; }
      .key-points li { margin-bottom: 3px; line-height: 1.3; }
      .footer { padding: 15px; border-radius: 0; font-size: 12px; }
    }
    @media (max-width: 480px) {
      .container { padding: 5px; }
      .header { padding: 15px 10px; }
      .logo { width: 120px; }
      .title { font-size: 20px; }
      .subtitle { font-size: 12px; }
      .content { padding: 15px 10px; }
      .stats-grid { grid-template-columns: 1fr; gap: 8px; }
      .stat-card { padding: 12px; }
      .stat-number { font-size: 20px; }
      .category-title { font-size: 16px; }
      .news-title { font-size: 14px; }
      .news-summary { font-size: 12px; }
    }
        """
    
    def generate_daily_report(self, days_back: int = 1) -> str:
        """
        生成每日安全快报
        
        Args:
            days_back: 生成几天前的报告
            
        Returns:
            生成的HTML文件路径
        """
        try:
            # 1. 抓取新闻
            news_list = self.fetch_security_news(days_back)
            
            if not news_list:
                logger.warning("未获取到任何新闻，无法生成报告")
                return ""
            
            # 2. 使用GLM生成分析
            logger.info("正在使用GLM生成新闻分析...")
            analysis_result = self.generate_news_analysis(news_list)
            
            # 3. 生成HTML报告
            target_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y%m%d')
            html_content = self.generate_html_report(analysis_result, target_date)
            
            # 4. 保存文件
            filename = f"news{target_date}.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ 成功生成AI智能新闻快报: {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"生成报告失败: {e}")
            return ""

def main():
    """主函数"""
    # 从环境变量获取API密钥，或者在这里直接设置
    api_key = os.getenv('GLM_API_KEY')
    
    if not api_key:
        print("⚠️  请设置GLM_API_KEY环境变量或在代码中配置API密钥")
        print("获取API密钥：https://open.bigmodel.cn/")
        return
    
    generator = GLMNewsGenerator(api_key)
    
    # 生成昨天的新闻快报
    result = generator.generate_daily_report(days_back=1)
    
    if result:
        print(f"🎉 AI智能新闻快报生成成功: {result}")
    else:
        print("❌ 新闻快报生成失败")

if __name__ == "__main__":
    main()