import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Textarea } from './ui/Textarea';
import { Button } from './ui/Button';
import { parseContent, resetIssueCounter, setIssueNumber } from '../utils/contentParser';
import { DailyReport } from '../types';
import { FileText, Zap, RotateCcw, Settings } from 'lucide-react';
import { Input } from './ui/Input';

interface ContentParserProps {
  onParsed: (report: DailyReport) => void;
}

export const ContentParser: React.FC<ContentParserProps> = ({ onParsed }) => {
  const [rawContent, setRawContent] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [manualIssue, setManualIssue] = useState('');
  
  const handleParse = async () => {
    if (!rawContent.trim()) {
      alert('请输入要解析的内容');
      return;
    }
    
    setIsLoading(true);
    
    try {
      // 模拟解析过程的延迟
      await new Promise(resolve => setTimeout(resolve, 800));
      
      const parsedData = parseContent(rawContent);
      
      if (parsedData.news.length === 0) {
        alert('未能解析出有效的新闻条目，请检查内容格式');
        return;
      }
      
      onParsed(parsedData);
    } catch (error) {
      console.error('解析错误:', error);
      alert('内容解析失败，请检查格式后重试');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleResetIssue = () => {
    resetIssueCounter();
    alert('期数计数器已重置');
  };
  
  const handleSetIssue = () => {
    const issue = parseInt(manualIssue, 10);
    if (isNaN(issue) || issue < 1) {
      alert('请输入有效的期数（大于0的整数）');
      return;
    }
    setIssueNumber(issue);
    alert(`下次解析将从第 ${issue + 1} 期开始`);
    setManualIssue('');
  };
  
  const exampleContent = `海之安安全每日快报

2025年7月21日 | 第 108 期

今日摘要：本期快报聚焦三大关键安全领域：首先是焦点安全事件...

**1. 【重大数据泄露】某大型企业遭受APT攻击导致客户数据泄露**

* 某知名企业近日发生严重数据泄露事件，影响超过100万用户。攻击者通过APT技术手段渗透企业内网，窃取了大量敏感客户信息。

* **分析与影响：** 此次事件暴露了企业在网络安全防护方面的薄弱环节，提醒各组织需要加强APT防护能力建设。

**2. 【关键漏洞预警】Windows系统发现新的零日漏洞**

* 安全研究人员发现Windows操作系统存在新的零日漏洞，该漏洞可能被恶意利用进行权限提升攻击。

* **分析与影响：** 建议用户立即关注官方安全更新，及时安装补丁程序，避免成为攻击目标。`;
  
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <FileText className="w-6 h-6 text-blue-400" />
              智能内容解析
            </CardTitle>
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => setShowSettings(!showSettings)}
              className="flex items-center gap-2"
            >
              <Settings className="w-4 h-4" />
              设置
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                快报内容
              </label>
              <Textarea
                placeholder={`请粘贴完整的快报内容，系统将自动解析日期、期数、摘要和新闻条目...

示例格式：
${exampleContent}`}
                value={rawContent}
                onChange={(e) => setRawContent(e.target.value)}
                rows={20}
                className="font-mono text-sm"
              />
            </div>
            
            {showSettings && (
              <Card className="bg-slate-900/50">
                <CardHeader>
                  <CardTitle className="text-sm">解析设置</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex items-center gap-4">
                      <Button 
                        variant="outline" 
                        size="sm" 
                        onClick={handleResetIssue}
                        className="flex items-center gap-2"
                      >
                        <RotateCcw className="w-4 h-4" />
                        重置期数计数器
                      </Button>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <Input
                        type="number"
                        placeholder="手动设置期数"
                        value={manualIssue}
                        onChange={(e) => setManualIssue(e.target.value)}
                        className="flex-1"
                        min="1"
                      />
                      <Button onClick={handleSetIssue} size="sm">
                        设置
                      </Button>
                    </div>
                    
                    <p className="text-xs text-slate-400">
                      期数会根据解析次数自动递增。如需调整起始期数，请使用上述设置。
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}
            
            <div className="flex justify-center">
              <Button 
                onClick={handleParse} 
                size="lg" 
                disabled={isLoading || !rawContent.trim()}
                className="px-12 flex items-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    正在解析...
                  </>
                ) : (
                  <>
                    <Zap className="w-5 h-5" />
                    智能解析并生成快报
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
      
      <Card className="bg-slate-800/20 border-blue-500/30">
        <CardContent className="p-4">
          <h3 className="text-sm font-medium text-blue-400 mb-2">📋 支持的内容格式</h3>
          <ul className="text-xs text-slate-400 space-y-1">
            <li>• <strong>日期：</strong> "2025年7月21日" 或 "2025-07-21"</li>
            <li>• <strong>摘要：</strong> "今日摘要：内容..."</li>
            <li>• <strong>新闻：</strong> "**1. 【类型】标题**" + 内容段落</li>
            <li>• <strong>分析：</strong> "* **分析与影响：** 分析内容"</li>
            <li>• <strong>期数：</strong> 自动递增（可手动设置）</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};