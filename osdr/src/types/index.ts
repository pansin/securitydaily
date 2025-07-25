export interface NewsItem {
  id: string;
  title: string;
  content: string;
  category: 'focus' | 'risk' | 'innovation';
}

export interface DailyReport {
  date: string;
  issue: number;
  news: NewsItem[];
  summary?: string;
}

export interface CategoryInfo {
  key: 'focus' | 'risk' | 'innovation';
  title: string;
  description: string;
}