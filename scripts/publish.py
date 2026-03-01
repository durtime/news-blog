#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化发布脚本
执行完整的新闻收集、处理、构建和发布流程
"""

import os
import sys
import subprocess
import time
from datetime import datetime
import argparse

def run_command(command, cwd=None):
    """运行shell命令"""
    print(f"执行命令: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"命令执行失败 (code: {result.returncode}):")
            print(f"错误输出: {result.stderr}")
            return False
        else:
            print(f"命令执行成功:")
            if result.stdout.strip():
                print(f"输出: {result.stdout[:500]}...")  # 只显示前500字符
            return True
            
    except Exception as e:
        print(f"执行命令时发生异常: {e}")
        return False

def install_dependencies():
    """安装Python依赖"""
    print("=" * 50)
    print("安装Python依赖...")
    print("=" * 50)
    
    dependencies = [
        "feedparser",
        "beautifulsoup4",
        "python-frontmatter",
        "markdown"
    ]
    
    for dep in dependencies:
        print(f"安装 {dep}...")
        if not run_command(f"pip3 install {dep}"):
            print(f"安装 {dep} 失败，尝试继续...")
    
    return True

def collect_news():
    """收集新闻"""
    print("=" * 50)
    print("开始收集新闻...")
    print("=" * 50)
    
    script_dir = os.path.dirname(__file__)
    collector_script = os.path.join(script_dir, "news_collector.py")
    
    return run_command(f"python3 {collector_script}")

def process_news():
    """处理新闻"""
    print("=" * 50)
    print("开始处理新闻...")
    print("=" * 50)
    
    script_dir = os.path.dirname(__file__)
    processor_script = os.path.join(script_dir, "news_processor.py")
    
    return run_command(f"python3 {processor_script}")

def build_site():
    """构建Hugo网站"""
    print("=" * 50)
    print("开始构建网站...")
    print("=" * 50)
    
    project_dir = os.path.join(os.path.dirname(__file__), "..")
    
    # 构建静态网站
    if not run_command("hugo --minify", cwd=project_dir):
        print("Hugo构建失败")
        return False
    
    print("网站构建成功！")
    return True

def test_site():
    """本地测试网站"""
    print("=" * 50)
    print("本地测试网站...")
    print("=" * 50)
    
    project_dir = os.path.join(os.path.dirname(__file__), "..")
    
    # 在后台启动Hugo服务器
    print("启动本地测试服务器 (Ctrl+C停止)...")
    try:
        # 使用subprocess.Popen在后台运行
        server_process = subprocess.Popen(
            ["hugo", "server", "-D", "--port", "1313"],
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查服务器是否运行
        if server_process.poll() is None:
            print("本地服务器已启动: http://localhost:1313")
            print("按Ctrl+C停止服务器并继续...")
            
            # 等待用户中断
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n停止本地服务器...")
                server_process.terminate()
                server_process.wait()
                print("本地服务器已停止")
        else:
            print("服务器启动失败")
            stdout, stderr = server_process.communicate()
            print(f"输出: {stdout}")
            print(f"错误: {stderr}")
            return False
            
    except Exception as e:
        print(f"本地测试失败: {e}")
        return False
    
    return True

def deploy_to_github():
    """部署到GitHub Pages"""
    print("=" * 50)
    print("部署到GitHub Pages...")
    print("=" * 50)
    
    project_dir = os.path.join(os.path.dirname(__file__), "..")
    public_dir = os.path.join(project_dir, "public")
    
    # 检查public目录是否存在
    if not os.path.exists(public_dir):
        print(f"错误: {public_dir} 目录不存在，请先构建网站")
        return False
    
    # 进入public目录
    os.chdir(public_dir)
    
    # 初始化Git仓库（如果不存在）
    if not os.path.exists(".git"):
        print("初始化Git仓库...")
        run_command("git init")
        run_command("git checkout -b gh-pages")
    
    # 添加所有文件
    run_command("git add .")
    
    # 提交
    commit_message = f"自动更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    run_command(f'git commit -m "{commit_message}"')
    
    print("=" * 50)
    print("部署说明:")
    print("1. 首先在GitHub上创建一个新仓库，例如: news-blog")
    print("2. 添加远程仓库:")
    print(f'   git remote add origin https://github.com/你的用户名/news-blog.git')
    print("3. 推送到GitHub:")
    print("   git push -u origin gh-pages")
    print("=" * 50)
    print("完成后，你的网站将在以下地址访问:")
    print("https://你的用户名.github.io/news-blog/")
    print("=" * 50)
    
    return True

def create_cron_job():
    """创建Cron任务"""
    print("=" * 50)
    print("创建自动化Cron任务...")
    print("=" * 50)
    
    script_path = os.path.abspath(__file__)
    
    cron_content = f"""# 每日新闻聚合自动化任务
# 每天8:00和20:00各运行一次

0 8,20 * * * cd {os.path.dirname(script_path)}/.. && python3 scripts/publish.py --collect --process --build >> logs/cron.log 2>&1

# 每周一早上7:00清理旧日志
0 7 * * 1 find {os.path.dirname(script_path)}/../logs -name "*.log" -mtime +7 -delete
"""
    
    cron_file = os.path.join(os.path.dirname(__file__), "cron_job.txt")
    with open(cron_file, 'w', encoding='utf-8') as f:
        f.write(cron_content)
    
    print(f"Cron配置已保存到: {cron_file}")
    print("\n安装Cron任务的步骤:")
    print("1. 打开终端")
    print("2. 运行: crontab -e")
    print("3. 添加以下内容:")
    print(cron_content)
    print("4. 保存并退出")
    
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='新闻聚合博客自动化发布脚本')
    parser.add_argument('--install', action='store_true', help='安装依赖')
    parser.add_argument('--collect', action='store_true', help='收集新闻')
    parser.add_argument('--process', action='store_true', help='处理新闻')
    parser.add_argument('--build', action='store_true', help='构建网站')
    parser.add_argument('--test', action='store_true', help='本地测试')
    parser.add_argument('--deploy', action='store_true', help='部署到GitHub')
    parser.add_argument('--cron', action='store_true', help='创建Cron任务')
    parser.add_argument('--all', action='store_true', help='执行完整流程')
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，显示帮助
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    # 执行完整流程
    if args.all:
        args.install = True
        args.collect = True
        args.process = True
        args.build = True
        args.test = True
        args.cron = True
    
    # 记录开始时间
    start_time = datetime.now()
    print("=" * 50)
    print("新闻聚合博客发布系统")
    print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # 创建日志目录
    logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    success = True
    
    # 执行各个步骤
    if args.install:
        success = install_dependencies() and success
    
    if args.collect:
        success = collect_news() and success
    
    if args.process:
        success = process_news() and success
    
    if args.build:
        success = build_site() and success
    
    if args.test:
        success = test_site() and success
    
    if args.deploy:
        success = deploy_to_github() and success
    
    if args.cron:
        success = create_cron_job() and success
    
    # 计算运行时间
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("=" * 50)
    print("发布流程完成!")
    print(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总耗时: {duration.total_seconds():.1f} 秒")
    
    if success:
        print("✅ 所有任务执行成功!")
    else:
        print("⚠️  部分任务执行失败，请检查日志")
    
    print("=" * 50)

if __name__ == "__main__":
    main()