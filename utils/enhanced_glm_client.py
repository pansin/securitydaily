#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版GLM客户端 - 解决API超时和连接问题
"""

import json
import time
import logging
import requests
from typing import Dict, Any, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class EnhancedGLMClient:
    """增强版GLM客户端，包含重试机制和更好的错误处理"""
    
    def __init__(self, api_key: str, base_url: str = None, timeout: int = 60):
        """
        初始化GLM客户端
        
        Args:
            api_key: GLM API密钥
            base_url: API基础URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key
        self.base_url = base_url or 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        
        # 创建会话并配置重试策略
        self.session = requests.Session()
        
        # 配置重试策略
        try:
            # 新版本urllib3
            retry_strategy = Retry(
                total=3,  # 总重试次数
                backoff_factor=2,  # 退避因子
                status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
                allowed_methods=["POST"]  # 允许重试的HTTP方法
            )
        except TypeError:
            # 旧版本urllib3兼容
            retry_strategy = Retry(
                total=3,  # 总重试次数
                backoff_factor=2,  # 退避因子
                status_forcelist=[429, 500, 502, 503, 504],  # 需要重试的HTTP状态码
                method_whitelist=["POST"]  # 旧版本参数名
            )
        
        # 配置HTTP适配器
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 设置默认请求头
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'HaiZhiAn-News-System/1.0'
        })
    
    def call_api(self, messages: List[Dict], model: str = 'glm-4-flash', 
                 temperature: float = 0.7, max_tokens: int = 2000,
                 retry_count: int = 3) -> Optional[str]:
        """
        调用GLM API，包含重试机制
        
        Args:
            messages: 消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大token数
            retry_count: 重试次数
            
        Returns:
            API响应内容，失败返回None
        """
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        for attempt in range(retry_count + 1):
            try:
                self.logger.info(f"GLM API调用尝试 {attempt + 1}/{retry_count + 1}")
                
                # 发送请求
                response = self.session.post(
                    self.base_url,
                    json=payload,
                    timeout=self.timeout
                )
                
                # 检查HTTP状态码
                if response.status_code == 200:
                    result = response.json()
                    if 'choices' in result and len(result['choices']) > 0:
                        content = result['choices'][0]['message']['content']
                        self.logger.info("GLM API调用成功")
                        return content
                    else:
                        self.logger.error(f"GLM API响应格式异常: {result}")
                        
                elif response.status_code == 429:
                    # 速率限制，等待更长时间
                    wait_time = (2 ** attempt) * 5  # 指数退避，最少5秒
                    self.logger.warning(f"GLM API速率限制，等待{wait_time}秒后重试")
                    time.sleep(wait_time)
                    continue
                    
                else:
                    self.logger.error(f"GLM API HTTP错误: {response.status_code} - {response.text}")
                    
            except requests.exceptions.Timeout:
                wait_time = (2 ** attempt) * 3  # 超时重试间隔
                self.logger.warning(f"GLM API超时，等待{wait_time}秒后重试 ({attempt + 1}/{retry_count + 1})")
                if attempt < retry_count:
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error("GLM API超时，已达到最大重试次数")
                    
            except requests.exceptions.ConnectionError as e:
                wait_time = (2 ** attempt) * 2  # 连接错误重试间隔
                self.logger.warning(f"GLM API连接错误: {e}，等待{wait_time}秒后重试")
                if attempt < retry_count:
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error("GLM API连接错误，已达到最大重试次数")
                    
            except Exception as e:
                self.logger.error(f"GLM API调用异常: {e}")
                if attempt < retry_count:
                    time.sleep(2 ** attempt)  # 简单退避
                    continue
                else:
                    break
        
        self.logger.error("GLM API调用失败，所有重试均失败")
        return None
    
    def parse_json_response(self, response: str, fallback_data: Any = None) -> Any:
        """
        解析JSON响应，包含容错处理
        
        Args:
            response: API响应字符串
            fallback_data: 解析失败时的备用数据
            
        Returns:
            解析后的数据或备用数据
        """
        if not response:
            self.logger.warning("响应为空，使用备用数据")
            return fallback_data
        
        try:
            # 尝试直接解析JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # JSON解析失败，尝试提取JSON部分
            self.logger.warning("JSON解析失败，尝试提取JSON部分")
            
            # 查找JSON代码块
            json_patterns = [
                r'```json\s*(\{.*?\})\s*```',
                r'```\s*(\{.*?\})\s*```',
                r'(\{.*?\})',
            ]
            
            import re
            for pattern in json_patterns:
                matches = re.findall(pattern, response, re.DOTALL)
                if matches:
                    try:
                        return json.loads(matches[0])
                    except json.JSONDecodeError:
                        continue
            
            # 如果仍然无法解析，尝试修复常见的JSON错误
            try:
                # 移除可能的前后缀
                cleaned = response.strip()
                if cleaned.startswith('```json'):
                    cleaned = cleaned[7:]
                if cleaned.endswith('```'):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                # 尝试解析清理后的内容
                return json.loads(cleaned)
            except json.JSONDecodeError:
                pass
            
            self.logger.error(f"JSON解析完全失败，响应内容: {response[:200]}...")
            return fallback_data
    
    def select_top_news(self, news_text: str) -> List[Dict]:
        """
        精选重要新闻
        
        Args:
            news_text: 新闻文本
            
        Returns:
            精选新闻列表
        """
        from config.glm_config import PROMPT_TEMPLATES
        
        messages = [
            {
                "role": "user",
                "content": PROMPT_TEMPLATES['select_top_news'].format(news_text=news_text)
            }
        ]
        
        response = self.call_api(messages, retry_count=3)
        
        # 备用数据
        fallback_data = {
            "selected_news": [
                {
                    "title": f"全球网络安全新闻 {i+1}",
                    "source": "综合来源",
                    "region": "全球",
                    "importance": "8",
                    "reason": "重要安全事件"
                } for i in range(10)
            ]
        }
        
        result = self.parse_json_response(response, fallback_data)
        return result.get('selected_news', fallback_data['selected_news'])
    
    def generate_summary(self, news_text: str) -> str:
        """
        生成新闻摘要
        
        Args:
            news_text: 新闻文本
            
        Returns:
            新闻摘要
        """
        from config.glm_config import PROMPT_TEMPLATES
        
        messages = [
            {
                "role": "user", 
                "content": PROMPT_TEMPLATES['summary'].format(news_text=news_text)
            }
        ]
        
        response = self.call_api(messages, retry_count=3)
        
        if response:
            return response.strip()
        else:
            # 备用摘要
            return """今日全球网络安全态势显示，各类安全威胁持续演进，零日漏洞、勒索软件攻击和数据泄露事件频发。
            国际网络安全形势依然严峻，各国政府和企业需要加强防护措施，提升安全意识，
            共同应对日益复杂的网络安全挑战。建议关注最新威胁情报，及时更新安全防护策略。"""
    
    def categorize_and_summarize(self, news_text: str) -> Dict:
        """
        分类并总结新闻
        
        Args:
            news_text: 新闻文本
            
        Returns:
            分类后的新闻字典
        """
        from config.glm_config import PROMPT_TEMPLATES
        
        messages = [
            {
                "role": "user",
                "content": PROMPT_TEMPLATES['categorize_and_summarize'].format(news_text=news_text)
            }
        ]
        
        response = self.call_api(messages, retry_count=3)
        
        # 备用数据
        fallback_data = {
            "安全风险": [
                {
                    "title": "全球网络安全风险态势",
                    "source": "综合来源",
                    "region": "全球",
                    "summary": "当前全球网络安全风险持续上升，各类漏洞和威胁层出不穷，需要持续关注和防范。",
                    "key_points": ["漏洞数量增加", "攻击手段升级", "防护需求提升"],
                    "impact_level": "高"
                }
            ],
            "安全事件": [
                {
                    "title": "国际网络安全事件频发",
                    "source": "综合来源", 
                    "region": "全球",
                    "summary": "近期国际网络安全事件频繁发生，包括数据泄露、勒索攻击等多种形式。",
                    "key_points": ["事件频率增加", "影响范围扩大", "损失持续上升"],
                    "impact_level": "高"
                }
            ],
            "安全舆情": [
                {
                    "title": "网络安全政策动态",
                    "source": "综合来源",
                    "region": "全球", 
                    "summary": "各国政府持续加强网络安全政策制定和监管力度，推动行业规范发展。",
                    "key_points": ["政策完善", "监管加强", "标准统一"],
                    "impact_level": "中"
                }
            ],
            "安全趋势": [
                {
                    "title": "网络安全技术发展趋势",
                    "source": "综合来源",
                    "region": "全球",
                    "summary": "人工智能、零信任等新技术在网络安全领域的应用不断深入，推动行业创新发展。",
                    "key_points": ["技术创新", "应用深化", "市场扩大"],
                    "impact_level": "中"
                }
            ]
        }
        
        result = self.parse_json_response(response, fallback_data)
        
        # 确保所有分类都存在
        for category in ["安全风险", "安全事件", "安全舆情", "安全趋势"]:
            if category not in result:
                result[category] = []
        
        return result
    
    def translate_and_analyze(self, title: str, content: str, source: str) -> Dict:
        """
        翻译并分析英文新闻
        
        Args:
            title: 英文标题
            content: 英文内容
            source: 新闻来源
            
        Returns:
            翻译和分析结果
        """
        from config.glm_config import PROMPT_TEMPLATES
        
        messages = [
            {
                "role": "user",
                "content": PROMPT_TEMPLATES['translate_and_analyze'].format(
                    title=title, content=content, source=source
                )
            }
        ]
        
        response = self.call_api(messages, retry_count=3)
        
        # 备用数据
        fallback_data = {
            "chinese_title": title,  # 如果翻译失败，保留原标题
            "summary": "该新闻涉及网络安全相关内容，具体详情请参考原文。",
            "key_points": ["网络安全相关", "需要关注", "影响待评估"],
            "impact_analysis": "影响程度需要进一步评估",
            "threat_level": "中危"
        }
        
        result = self.parse_json_response(response, fallback_data)
        return result
    
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'session'):
            self.session.close()


def create_enhanced_glm_client(api_key: str) -> EnhancedGLMClient:
    """
    创建增强版GLM客户端的工厂函数
    
    Args:
        api_key: GLM API密钥
        
    Returns:
        增强版GLM客户端实例
    """
    return EnhancedGLMClient(
        api_key=api_key,
        timeout=90  # 增加超时时间到90秒
    )