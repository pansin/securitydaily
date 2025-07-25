import React, { useRef } from 'react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { DailyReport, CategoryInfo } from '../types';
import { ArrowLeft, Download } from 'lucide-react';
import { downloadHTMLReport } from '../utils/htmlGenerator';

interface ReportPreviewProps {
  report: DailyReport;
  onBack: () => void;
}

const categories: CategoryInfo[] = [
  { key: 'focus', title: '焦点安全事件', description: '当前热点安全事件和重大漏洞' },
  { key: 'risk', title: '重大风险与预警', description: '安全威胁预警和风险评估' },
  { key: 'innovation', title: '产业创新与政策', description: '行业动态、技术创新和政策法规' },
];

export const ReportPreview: React.FC<ReportPreviewProps> = ({ report, onBack }) => {
  const printRef = useRef<HTMLDivElement>(null);

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const handleDownload = () => {
    downloadHTMLReport(report);
  };

  const groupedNews = categories.map(category => ({
    ...category,
    news: report.news.filter(item => item.category === category.key)
  })).filter(category => category.news.length > 0);

  return (
    <div className="max-w-4xl mx-auto">
      {/* 控制栏 */}
      <div className="flex items-center justify-between mb-6 bg-slate-800/30 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4">
        <Button onClick={onBack} variant="outline" className="flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" />
          返回编辑
        </Button>
        <div className="flex gap-2">
          <Button onClick={handleDownload} variant="secondary" className="flex items-center gap-2">
            <Download className="w-4 h-4" />
            下载快报
          </Button>
        </div>
      </div>

      {/* 快报内容 */}
      <Card className="bg-white text-black print:shadow-none">
        <div ref={printRef} className="p-8">
          {/* 头部logo和标题 */}
          <div className="text-center mb-8">
            <div className="mb-6">
              <img src="/ocean_security_logo.png" alt="Ocean Security" className="mx-auto max-w-xs" />
            </div>
            <h1 className="text-3xl font-bold text-blue-600 mb-2">海之安安全每日快报</h1>
            <div className="text-lg text-gray-600">
              {formatDate(report.date)} | 第 {report.issue} 期
            </div>
          </div>

          {/* 今日摘要 */}
          {report.summary && (
            <div className="mb-8">
              <h2 className="text-xl font-bold text-blue-600 mb-4 border-b-2 border-blue-600 pb-2">
                今日摘要
              </h2>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700 leading-relaxed">{report.summary}</p>
              </div>
            </div>
          )}

          {/* 新闻分类展示 */}
          {groupedNews.map((category) => (
            <div key={category.key} className="mb-8">
              <h2 className="text-xl font-bold text-blue-600 mb-4 border-b-2 border-blue-600 pb-2">
                {category.title}
              </h2>
              <div className="space-y-6">
                {category.news.map((newsItem, index) => (
                  <div key={newsItem.id} className="border border-gray-200 rounded-lg p-4">
                    <h3 className="font-bold text-gray-800 mb-3">
                      {index + 1}. {newsItem.title}
                    </h3>
                    <div className="text-gray-600">
                      <strong>分析与影响：</strong>
                      <span className="text-gray-700 leading-relaxed ml-1">{newsItem.content}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* 页脚 */}
          <div className="mt-12 pt-6 border-t border-gray-200 text-center text-gray-500 text-sm">
            <p>海之安安全每日快报 | 专业网络安全资讯平台</p>
            <p>发布日期：{formatDate(report.date)}</p>
          </div>
        </div>
      </Card>
    </div>
  );
};