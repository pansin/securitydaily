#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM API诊断和监控工具
"""

import os
import time
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class GLMDiagnostics:
    """GLM API诊断工具"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GLM_API_KEY')
        self.base_url = 'https://open.bigmodel.cn/api/paas/v4/chat/completions'
        self.logger = logging.getLogger(__name__)
        self.diagnostics_log = []
        
    def test_api_connectivity(self) -> Dict:
        """测试API连接性"""
        print("🔍 测试GLM API连接性...")
        
        test_result = {
            'timestamp': datetime.now().isoformat(),
            'test_type': 'connectivity',
            'success': False,
            'response_time': 0,
            'error': None
        }
        
        if not self.api_key:
            test_result['error'] = 'API密钥未设置'
            print("❌ API密钥未设置")
            return test_result
        
        test_payload = {
            "model": "glm-4-flash",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.1,
            "max_tokens": 10
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        start_time = time.time()
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=test_payload,
                timeout=30
            )
            
            response_time = time.time() - start_time
            test_result['response_time'] = response_time
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    test_result['success'] = True
                    print(f"✅ API连接成功 (响应时间: {response_time:.2f}s)")
                else:
                    test_result['error'] = "响应格式异常"
                    print("❌ 响应格式异常")
            else:
                test_result['error'] = f"HTTP {response.status_code}"
                print(f"❌ HTTP错误: {response.status_code}")
                
        except requests.exceptions.Timeout:
            test_result['error'] = "请求超时"
            print("❌ 请求超时")
        except Exception as e:
            test_result['error'] = str(e)
            print(f"❌ 错误: {e}")
        
        self.diagnostics_log.append(test_result)
        return test_result
    
    def run_full_diagnostics(self) -> Dict:
        """运行完整诊断"""
        print("🔧 开始GLM API诊断...")
        print("=" * 50)
        
        results = {'connectivity': self.test_api_connectivity()}
        
        # 生成报告
        report_content = f"""# GLM API诊断报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 连接性测试
- 状态: {'✅ 正常' if results['connectivity']['success'] else '❌ 异常'}
- 响应时间: {results['connectivity']['response_time']:.2f}s
- 错误: {results['connectivity'].get('error', '无')}

## 建议
"""
        
        if not results['connectivity']['success']:
            report_content += "- ⚠️ API连接异常，请检查网络和API密钥\n"
        else:
            report_content += "- ✅ API工作正常\n"
        
        # 保存报告
        output_dir = Path('output/diagnostics')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = output_dir / f"glm_diagnostics_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 诊断报告已保存: {report_file}")
        return results


def main():
    """主函数"""
    print("🌐 海之安新闻系统 - GLM API诊断工具")
    
    api_key = os.getenv('GLM_API_KEY')
    if not api_key:
        try:
            from config.glm_config import GLM_CONFIG
            api_key = GLM_CONFIG.get('api_key')
        except ImportError:
            pass
    
    if not api_key:
        print("❌ 未找到GLM API密钥")
        return
    
    diagnostics = GLMDiagnostics(api_key)
    results = diagnostics.run_full_diagnostics()
    
    print("\n🎯 诊断完成！")
    if results['connectivity']['success']:
        print("✅ GLM API工作正常")
    else:
        print("❌ GLM API存在问题")


if __name__ == "__main__":
    main()