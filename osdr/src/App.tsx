import React, { useState } from 'react';
import { ContentParser } from './components/ContentParser';
import { ParsedReportEditor } from './components/ParsedReportEditor';
import { ReportPreview } from './components/ReportPreview';
import { DailyReport } from './types';
import { Shield, Zap, FileText } from 'lucide-react';

type AppMode = 'parser' | 'editor' | 'preview';

function App() {
  const [currentReport, setCurrentReport] = useState<DailyReport | null>(null);
  const [mode, setMode] = useState<AppMode>('parser');

  const handleContentParsed = (report: DailyReport) => {
    setCurrentReport(report);
    setMode('editor');
  };

  const handleReportConfirmed = (report: DailyReport) => {
    setCurrentReport(report);
    setMode('preview');
  };

  const handleBackToParser = () => {
    setMode('parser');
  };

  const handleBackToEditor = () => {
    setMode('editor');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* 背景装饰 */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-blue-600/5 rounded-full blur-2xl"></div>
      </div>
      
      {/* 网格背景 */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(59,130,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.03)_1px,transparent_1px)] bg-[size:100px_100px] pointer-events-none"></div>
      
      <div className="relative z-10">
        {/* 头部导航 */}
        {(mode === 'parser' || mode === 'editor') && (
          <header className="border-b border-slate-700/50 bg-slate-900/30 backdrop-blur-sm">
            <div className="max-w-6xl mx-auto px-4 py-6">
              <div className="flex items-center justify-center space-x-3">
                <div className="flex items-center space-x-2">
                  <Shield className="w-8 h-8 text-blue-400" />
                  {mode === 'parser' && <FileText className="w-6 h-6 text-cyan-400 animate-pulse" />}
                  {mode === 'editor' && <Zap className="w-6 h-6 text-green-400 animate-pulse" />}
                </div>
                <div>
                  <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                    海之安安全每日快报
                  </h1>
                  <p className="text-slate-400 text-sm mt-1">
                    {mode === 'parser' && '智能内容解析平台'}
                    {mode === 'editor' && '解析结果编辑与确认'}
                  </p>
                </div>
              </div>
            </div>
          </header>
        )}
        
        {/* 主要内容区域 */}
        <main className="px-4 py-8">
          {mode === 'parser' && (
            <div>
              <div className="max-w-4xl mx-auto mb-8">
                <div className="text-center space-y-4">
                  <h2 className="text-2xl font-semibold text-white">
                    智能快报内容解析
                  </h2>
                  <p className="text-slate-400 max-w-2xl mx-auto">
                    只需粘贴完整的快报内容，系统将自动识别日期、期数、摘要和新闻条目，生成专业格式的安全快报。
                  </p>
                </div>
              </div>
              <ContentParser onParsed={handleContentParsed} />
            </div>
          )}
          
          {mode === 'editor' && currentReport && (
            <ParsedReportEditor 
              report={currentReport}
              onConfirm={handleReportConfirmed}
              onBack={handleBackToParser}
            />
          )}
          
          {mode === 'preview' && currentReport && (
            <ReportPreview 
              report={currentReport} 
              onBack={handleBackToEditor}
            />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;