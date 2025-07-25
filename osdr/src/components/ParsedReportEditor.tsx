import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Input } from './ui/Input';
import { Textarea } from './ui/Textarea';
import { Select } from './ui/Select';
import { Button } from './ui/Button';
import { DailyReport, NewsItem, CategoryInfo } from '../types';
import { ArrowLeft, Eye, Trash2, Plus } from 'lucide-react';

interface ParsedReportEditorProps {
  report: DailyReport;
  onConfirm: (report: DailyReport) => void;
  onBack: () => void;
}

const categories: CategoryInfo[] = [
  { key: 'focus', title: '焦点安全事件', description: '当前热点安全事件和重大漏洞' },
  { key: 'risk', title: '重大风险与预警', description: '安全威胁预警和风险评估' },
  { key: 'innovation', title: '产业创新与政策', description: '行业动态、技术创新和政策法规' },
];

export const ParsedReportEditor: React.FC<ParsedReportEditorProps> = ({ report, onConfirm, onBack }) => {
  const [editedReport, setEditedReport] = useState<DailyReport>(report);
  
  const updateBasicInfo = (field: keyof DailyReport, value: string | number) => {
    setEditedReport(prev => ({ ...prev, [field]: value }));
  };
  
  const updateNewsItem = (id: string, field: keyof NewsItem, value: string) => {
    setEditedReport(prev => ({
      ...prev,
      news: prev.news.map(item => 
        item.id === id ? { ...item, [field]: value } : item
      )
    }));
  };
  
  const addNewsItem = () => {
    const newItem: NewsItem = {
      id: `news-${Date.now()}`,
      title: '',
      content: '',
      category: 'focus',
    };
    setEditedReport(prev => ({
      ...prev,
      news: [...prev.news, newItem]
    }));
  };
  
  const removeNewsItem = (id: string) => {
    setEditedReport(prev => ({
      ...prev,
      news: prev.news.filter(item => item.id !== id)
    }));
  };
  
  const handleConfirm = () => {
    // 验证必填字段
    const validNews = editedReport.news.filter(item => item.title.trim() && item.content.trim());
    
    if (validNews.length === 0) {
      alert('请至少保留一条完整的新闻信息');
      return;
    }
    
    onConfirm({
      ...editedReport,
      news: validNews
    });
  };
  
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* 控制栏 */}
      <div className="flex items-center justify-between bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4">
        <Button onClick={onBack} variant="outline" className="flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" />
          返回解析
        </Button>
        <div className="flex gap-2">
          <Button onClick={handleConfirm} className="flex items-center gap-2">
            <Eye className="w-4 h-4" />
            确认并预览
          </Button>
        </div>
      </div>
      
      {/* 基本信息编辑 */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            解析结果确认
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <Input
              type="date"
              label="发布日期"
              value={editedReport.date}
              onChange={(e) => updateBasicInfo('date', e.target.value)}
            />
            <Input
              type="number"
              label="期数"
              value={editedReport.issue}
              onChange={(e) => updateBasicInfo('issue', parseInt(e.target.value) || 1)}
              min="1"
            />
          </div>
          <Textarea
            label="今日摘要"
            value={editedReport.summary || ''}
            onChange={(e) => updateBasicInfo('summary', e.target.value)}
            placeholder="今日快报摘要..."
            rows={3}
          />
        </CardContent>
      </Card>
      
      {/* 新闻条目编辑 */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></div>
              新闻条目编辑 ({editedReport.news.length} 条)
            </CardTitle>
            <Button onClick={addNewsItem} size="sm" className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              添加新闻
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {editedReport.news.map((item, index) => (
              <div key={item.id} className="border border-slate-700/50 rounded-lg p-4 bg-slate-900/30">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-lg font-medium text-white">新闻 #{index + 1}</h4>
                  {editedReport.news.length > 1 && (
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeNewsItem(item.id)}
                      className="text-red-400 hover:text-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  )}
                </div>
                
                <div className="space-y-4">
                  <Select
                    label="新闻分类"
                    value={item.category}
                    onChange={(e) => updateNewsItem(item.id, 'category', e.target.value as any)}
                    options={categories.map(cat => ({ value: cat.key, label: cat.title }))}
                  />
                  
                  <Input
                    label="新闻标题"
                    value={item.title}
                    onChange={(e) => updateNewsItem(item.id, 'title', e.target.value)}
                    placeholder="新闻标题..."
                  />
                  
                  <Textarea
                    label="新闻内容（分析与影响）"
                    value={item.content}
                    onChange={(e) => updateNewsItem(item.id, 'content', e.target.value)}
                    placeholder="新闻的详细内容和分析评估..."
                    rows={6}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
      
      <div className="flex justify-center">
        <Button onClick={handleConfirm} size="lg" className="px-12">
          确认信息并生成快报
        </Button>
      </div>
    </div>
  );
};