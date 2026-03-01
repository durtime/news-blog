#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻处理脚本
将收集的新闻转换为Hugo文章格式
"""

import json
import os
import re
from datetime import datetime
import frontmatter
import markdown
from bs4 import BeautifulSoup

def load_news_data(data_dir):
    """加载新闻数据"""
    today = datetime.now().strftime('%Y-%m-%d')
    daily_file = os.path.join(data_dir, f'news_{today}.json')
    master_file = os.path.join(data_dir, 'news_master.json')
    
    # 优先使用当天的数据，如果没有则使用主文件
    for filepath in [daily_file, master_file]:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载文件 {filepath} 失败: {e}")
    
    print("未找到新闻数据文件")
    return []

def clean_html_content(html_content):
    """清理HTML内容，提取纯文本"""
    if not html_content:
        return ""
    
    # 使用BeautifulSoup提取文本
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 移除脚本和样式
    for script in soup(["script", "style"]):
        script.decompose()
    
    # 获取文本
    text = soup.get_text()
    
    # 清理多余的空格和换行
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def generate_summary(content, max_length=200):
    """生成摘要"""
    if not content:
        return ""
    
    # 清理内容
    clean_content = clean_html_content(content)
    
    # 如果内容太短，直接返回
    if len(clean_content) <= max_length:
        return clean_content
    
    # 截取到最大长度，确保在句子结束处截断
    summary = clean_content[:max_length]
    
    # 查找最后一个句号、问号或感叹号
    last_punct = max(
        summary.rfind('。'),
        summary.rfind('！'),
        summary.rfind('？'),
        summary.rfind('.'),
        summary.rfind('!'),
        summary.rfind('?')
    )
    
    if last_punct > 0:
        summary = summary[:last_punct + 1]
    
    return summary

def categorize_news(news_item):
    """根据关键词分类新闻"""
    title = news_item.get('title', '').lower()
    category = news_item.get('category', '其他')
    
    # 关键词分类
    keywords = {
        '政治': ['习近平', '政府', '政策', '外交', '国会', '选举', '领导人'],
        '经济': ['经济', '股市', '金融', '投资', 'GDP', '通胀', '就业'],
        '科技': ['科技', '人工智能', 'AI', '互联网', '手机', '电脑', '软件', '硬件'],
        '社会': ['社会', '民生', '教育', '医疗', '住房', '交通', '环境'],
        '国际': ['美国', '欧洲', '日本', '韩国', '俄罗斯', '联合国', '国际'],
        '体育': ['体育', '足球', '篮球', '奥运', '比赛', '运动员'],
        '娱乐': ['娱乐', '电影', '音乐', '明星', '综艺', '电视剧']
    }
    
    for cat, kw_list in keywords.items():
        for keyword in kw_list:
            if keyword.lower() in title:
                return cat
    
    return category

def create_hugo_post(news_item, output_dir):
    """创建Hugo文章文件"""
    # 生成文件名（使用标题和ID）
    title = news_item.get('title', '未命名新闻')
    news_id = news_item.get('id', 'unknown')
    
    # 清理文件名（移除特殊字符）
    safe_title = re.sub(r'[^\w\s-]', '', title)
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    filename = f"{datetime.now().strftime('%Y-%m-%d')}-{news_id}-{safe_title[:50]}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 处理发布时间
    published_str = news_item.get('published', '')
    try:
        # 尝试解析各种时间格式
        if 'T' in published_str:
            published_date = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
        else:
            published_date = datetime.strptime(published_str, '%a, %d %b %Y %H:%M:%S %z')
    except:
        published_date = datetime.now()
    
    # 生成摘要
    summary = generate_summary(news_item.get('summary', ''))
    
    # 确定分类
    category = categorize_news(news_item)
    
    # 创建Front Matter
    front_matter = {
        'title': title,
        'date': published_date.isoformat(),
        'draft': False,
        'summary': summary,
        'tags': [news_item.get('source', '未知'), category],
        'categories': [category],
        'source': news_item.get('source', '未知'),
        'original_url': news_item.get('link', ''),
        'news_id': news_id
    }
    
    # 创建文章内容
    content = f"""# {title}

> 来源：{news_item.get('source', '未知')} | 分类：{category} | 发布时间：{published_date.strftime('%Y年%m月%d日 %H:%M')}

{clean_html_content(news_item.get('summary', ''))}

---

**原文链接**: [{news_item.get('link', '')}]({news_item.get('link', '')})

*本文由新闻聚合系统自动生成，内容来源于{news_item.get('source', '未知')}，版权归原作者所有。*
"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        # 写入Front Matter
        f.write('---\n')
        for key, value in front_matter.items():
            if isinstance(value, list):
                f.write(f'{key}: {json.dumps(value, ensure_ascii=False)}\n')
            else:
                f.write(f'{key}: {value}\n')
        f.write('---\n\n')
        # 写入内容
        f.write(content)
    
    print(f"已创建文章: {filename}")
    return filepath

def main():
    """主函数"""
    print("=" * 50)
    print("开始新闻处理任务")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 路径配置
    script_dir = os.path.dirname(__file__)
    project_dir = os.path.join(script_dir, '..')
    data_dir = os.path.join(project_dir, 'data')
    posts_dir = os.path.join(project_dir, 'content', 'posts')
    
    # 确保目录存在
    os.makedirs(posts_dir, exist_ok=True)
    
    # 加载新闻数据
    news_data = load_news_data(data_dir)
    
    if not news_data:
        print("没有可处理的新闻数据")
        return
    
    print(f"加载到 {len(news_data)} 条新闻数据")
    
    # 处理每条新闻
    created_count = 0
    for i, news_item in enumerate(news_data[:20]):  # 每天最多处理20条
        try:
            create_hugo_post(news_item, posts_dir)
            created_count += 1
        except Exception as e:
            print(f"处理新闻失败 ({news_item.get('title', '未知标题')}): {e}")
    
    print("=" * 50)
    print(f"新闻处理完成！共创建 {created_count} 篇文章")
    print("=" * 50)

if __name__ == "__main__":
    main()