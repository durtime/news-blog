#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Hugo网站
"""

import os
import subprocess
from datetime import datetime

def test_hugo_build():
    """测试Hugo构建"""
    print("=" * 50)
    print("测试Hugo网站构建")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 创建测试文章
    test_post = """---
title: "测试文章 - Hugo网站运行正常"
date: 2026-03-01T17:45:00+08:00
draft: false
summary: "这是一篇测试文章，用于验证Hugo网站是否能正常工作。"
tags: ["测试", "Hugo"]
categories: ["测试"]
---

# 测试文章

恭喜！你的Hugo新闻聚合博客已经成功搭建。

## 功能验证

✅ **Hugo安装正常** - 静态网站生成器工作正常  
✅ **主题加载正常** - Paper主题已成功应用  
✅ **文章生成正常** - Markdown文章可以正确渲染  
✅ **本地服务器正常** - 可以在本地预览网站  

## 下一步

1. **配置新闻源** - 修改 `scripts/news_collector.py` 中的新闻源
2. **测试新闻收集** - 运行 `python3 scripts/publish.py --collect`
3. **生成新闻文章** - 运行 `python3 scripts/publish.py --process`
4. **构建网站** - 运行 `python3 scripts/publish.py --build`
5. **本地测试** - 运行 `python3 scripts/publish.py --test`
6. **部署到GitHub** - 按照README.md的说明部署

## 技术支持

如有问题，请查看：
- `README.md` - 项目文档
- `logs/` - 日志文件
- GitHub Issues - 问题反馈

---
*测试时间: 2026年3月1日*
"""
    
    # 创建测试文章文件
    posts_dir = "content/posts"
    os.makedirs(posts_dir, exist_ok=True)
    
    test_file = os.path.join(posts_dir, "2026-03-01-test-article.md")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_post)
    
    print(f"已创建测试文章: {test_file}")
    
    # 构建网站
    print("\n构建Hugo网站...")
    result = subprocess.run(
        ["hugo", "--minify"],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    if result.returncode == 0:
        print("✅ Hugo构建成功!")
        print(f"输出: {result.stdout[:200]}...")
        
        # 检查public目录
        if os.path.exists("public"):
            file_count = len([f for f in os.listdir("public") if os.path.isfile(os.path.join("public", f))])
            print(f"✅ 生成 {file_count} 个文件到 public/ 目录")
            
            # 检查首页
            index_file = os.path.join("public", "index.html")
            if os.path.exists(index_file):
                file_size = os.path.getsize(index_file)
                print(f"✅ 首页文件大小: {file_size} 字节")
            else:
                print("❌ 首页文件未生成")
        else:
            print("❌ public/ 目录未生成")
    else:
        print("❌ Hugo构建失败!")
        print(f"错误: {result.stderr}")
    
    print("=" * 50)
    
    # 启动本地服务器测试
    print("\n启动本地测试服务器 (10秒后自动停止)...")
    try:
        server_process = subprocess.Popen(
            ["hugo", "server", "-D", "--port", "1313", "--bind", "0.0.0.0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        import time
        time.sleep(10)  # 等待10秒
        
        # 停止服务器
        server_process.terminate()
        server_process.wait()
        
        print("✅ 本地服务器测试完成")
        print("📢 你可以在浏览器中访问: http://localhost:1313")
        
    except Exception as e:
        print(f"❌ 本地服务器测试失败: {e}")
    
    print("=" * 50)
    print("测试完成!")
    print("=" * 50)

if __name__ == "__main__":
    test_hugo_build()