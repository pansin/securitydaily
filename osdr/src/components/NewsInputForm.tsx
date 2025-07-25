import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/Card';
import { Input } from './ui/Input';
import { Textarea } from './ui/Textarea';
import { Select } from './ui/Select';
import { Button } from './ui/Button';
import { NewsItem, CategoryInfo } from '../types';
import { Plus, Trash2 } from 'lucide-react';

interface NewsInputFormProps {
  onSubmit: (data: { date: string; issue: number; news: NewsItem[]; summary: string }) => void;
}

const categories: CategoryInfo[] = [
  { key: 'focus', title: '焦点安全事件', description: '当前热点安全事件和重大漏洞' },
  { key: 'risk', title: '重大风险与预警', description: '安全威胁预警和风险评估' },
  { key: 'innovation', title: '产业创新与政策', description: '行业动态、技术创新和政策法规' },
];

export const NewsInputForm: React.FC<NewsInputFormProps> = ({ onSubmit }) => {
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [issue, setIssue] = useState(1);
  const [summary, setSummary] = useState('');
  const [news, setNews] = useState<NewsItem[]>([
    {
      id: '1',
      title: '',
      content: '',
      category: 'focus',
    },
  ]);

  const addNewsItem = () => {
    const newItem: NewsItem = {
      id: Date.now().toString(),
      title: '',
      content: '',
      category: 'focus',
    };
    setNews([...news, newItem]);
  };

  const removeNewsItem = (id: string) => {
    setNews(news.filter(item => item.id !== id));
  };

  const updateNewsItem = (id: string, field: keyof NewsItem, value: string) => {
    setNews(news.map(item => 
      item.id === id ? { ...item, [field]: value } : item
    ));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // 验证必填字段
    const validNews = news.filter(item => item.title.trim() && item.content.trim());
    
    if (validNews.length === 0) {
      alert('请至少填写一条完整的新闻信息');
      return;
    }
    
    onSubmit({
      date,
      issue,
      news: validNews,
      summary,
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            快报基本信息
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              type="date"
              label="发布日期"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
            <Input
              type="number"
              label="期数"
              value={issue}
              onChange={(e) => setIssue(parseInt(e.target.value) || 1)}
              min="1"
            />
          </div>
          <div className="mt-4">
            <Textarea
              label="今日摘要（可选）"
              placeholder="请输入今日快报的总体摘要..."
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              rows={3}
            />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></div>
              新闻条目管理
            </CardTitle>
            <Button onClick={addNewsItem} size="sm" className="flex items-center gap-2">
              <Plus className="w-4 h-4" />
              添加新闻
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {news.map((item, index) => (
              <div key={item.id} className="border border-slate-700/50 rounded-lg p-4 bg-slate-900/30">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="text-lg font-medium text-white">新闻 #{index + 1}</h4>
                  {news.length > 1 && (
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
                    placeholder="请输入新闻标题..."
                    value={item.title}
                    onChange={(e) => updateNewsItem(item.id, 'title', e.target.value)}
                  />
                  
                  <Textarea
                    label="新闻内容（分析与影响）"
                    placeholder="请输入新闻的详细内容和分析评估..."
                    value={item.content}
                    onChange={(e) => updateNewsItem(item.id, 'content', e.target.value)}
                    rows={6}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-center">
        <Button onClick={handleSubmit} size="lg" className="px-12">
          生成快报预览
        </Button>
      </div>
    </div>
  );
};