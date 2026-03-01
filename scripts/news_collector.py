#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻收集脚本
从各大新闻源的RSS获取新闻内容
"""

import feedparser
import json
import os
from datetime import datetime
import hashlib
import time

# 新闻源配置（使用更可靠的RSS源）
NEWS_SOURCES = {
    "bbc_chinese": {
        "name": "BBC中文网",
        "url": "https://feeds.bbci.co.uk/zhongwen/simp/rss.xml",
        "category": "国际"
    },
    "reuters_world": {
        "name": "路透社国际",
        "url": "https://www.reutersagency.com/feed/?taxonomy=best-regions&post_type=best",
        "category": "国际"
    },
    "ap_news": {
        "name": "美联社新闻",
        "url": "https://apnews.com/apf-intlnews.rss",
        "category": "国际"
    },
    "nytimes_world": {
        "name": "纽约时报国际",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "category": "国际"
    },
    "the_guardian": {
        "name": "卫报国际",
        "url": "https://www.theguardian.com/world/rss",
        "category": "国际"
    },
    "techcrunch": {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "category": "科技"
    },
    "hacker_news": {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/rss",
        "category": "科技"
    }
}

def fetch_news_from_rss(source_name, source_config):
    """从RSS源获取新闻"""
    try:
        print(f"正在从 {source_config['name']} 获取新闻...")
        feed = feedparser.parse(source_config['url'])
        
        news_items = []
        for entry in feed.entries[:10]:  # 每个源取前10条
            # 生成唯一ID
            news_id = hashlib.md5(entry.link.encode()).hexdigest()[:8]
            
            news_item = {
                "id": news_id,
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get('summary', entry.get('description', '')),
                "published": entry.get('published', entry.get('updated', datetime.now().isoformat())),
                "source": source_config['name'],
                "category": source_config['category'],
                "collected_at": datetime.now().isoformat()
            }
            news_items.append(news_item)
        
        print(f"从 {source_config['name']} 获取到 {len(news_items)} 条新闻")
        return news_items
        
    except Exception as e:
        print(f"从 {source_config['name']} 获取新闻失败: {e}")
        return []

def deduplicate_news(news_list):
    """去重新闻（基于链接）"""
    seen_links = set()
    deduplicated = []
    
    for news in news_list:
        if news['link'] not in seen_links:
            seen_links.add(news['link'])
            deduplicated.append(news)
    
    print(f"去重前: {len(news_list)} 条, 去重后: {len(deduplicated)} 条")
    return deduplicated

def save_news_to_file(news_list, filename):
    """保存新闻到JSON文件"""
    # 确保目录存在
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # 读取现有数据（如果有）
    existing_data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except:
            existing_data = []
    
    # 合并数据（保留最新的）
    all_news = news_list + existing_data
    # 按时间排序，最新的在前
    all_news.sort(key=lambda x: x.get('published', ''), reverse=True)
    # 只保留最近1000条
    all_news = all_news[:1000]
    
    # 保存到文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)
    
    print(f"已保存 {len(all_news)} 条新闻到 {filename}")

def main():
    """主函数"""
    print("=" * 50)
    print("开始新闻收集任务")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    all_news = []
    
    # 从每个新闻源获取新闻
    for source_name, source_config in NEWS_SOURCES.items():
        news_items = fetch_news_from_rss(source_name, source_config)
        all_news.extend(news_items)
        time.sleep(1)  # 避免请求过快
    
    # 去重
    all_news = deduplicate_news(all_news)
    
    # 保存到文件
    today = datetime.now().strftime('%Y-%m-%d')
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    daily_file = os.path.join(data_dir, f'news_{today}.json')
    master_file = os.path.join(data_dir, 'news_master.json')
    
    save_news_to_file(all_news, daily_file)
    save_news_to_file(all_news, master_file)
    
    print("=" * 50)
    print(f"新闻收集完成！共收集 {len(all_news)} 条新闻")
    print("=" * 50)
    
    return all_news

if __name__ == "__main__":
    main()