#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新闻收集脚本
"""

import feedparser
from datetime import datetime

# 测试一个简单的RSS源
test_url = "https://rsshub.app/36kr/news"

print(f"测试RSS源: {test_url}")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 50)

try:
    feed = feedparser.parse(test_url)
    
    print(f"状态: {feed.status}")
    print(f"条目数: {len(feed.entries)}")
    print("=" * 50)
    
    # 显示前3条新闻
    for i, entry in enumerate(feed.entries[:3]):
        print(f"\n{i+1}. {entry.title}")
        print(f"   链接: {entry.link}")
        print(f"   发布时间: {entry.get('published', '未知')}")
        if hasattr(entry, 'summary'):
            summary = entry.summary[:100] + "..." if len(entry.summary) > 100 else entry.summary
            print(f"   摘要: {summary}")
    
    print("=" * 50)
    print("✅ RSS源测试成功!")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")