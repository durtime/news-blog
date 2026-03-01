#!/bin/bash
# 设置新闻聚合博客的Cron自动化任务

echo "=========================================="
echo "新闻聚合博客自动化设置"
echo "=========================================="

# 获取项目绝对路径
PROJECT_PATH="$(cd "$(dirname "$0")" && pwd)"
echo "项目路径: $PROJECT_PATH"

# 创建日志目录
mkdir -p "$PROJECT_PATH/logs"
echo "✅ 创建日志目录: $PROJECT_PATH/logs"

# 创建Cron任务文件
CRON_FILE="$PROJECT_PATH/cron-job.txt"
cat > "$CRON_FILE" << EOF
# 新闻聚合博客自动化任务
# 每天8:00和20:00（北京时间）各运行一次

# 分钟 小时 日 月 星期 命令
0 8,20 * * * cd $PROJECT_PATH && python3 scripts/publish.py --collect --process --build >> logs/cron.log 2>&1

# 每周一早上7:00清理旧日志
0 7 * * 1 find $PROJECT_PATH/logs -name "*.log" -mtime +7 -delete
EOF

echo "✅ 创建Cron配置文件: $CRON_FILE"
echo ""
echo "=========================================="
echo "安装Cron任务的步骤："
echo "=========================================="
echo "1. 打开终端"
echo "2. 运行: crontab -e"
echo "3. 添加以下内容："
echo ""
cat "$CRON_FILE"
echo ""
echo "4. 保存并退出（在vim中按ESC，然后输入:wq）"
echo "5. 验证Cron任务: crontab -l"
echo "=========================================="
echo ""
echo "手动测试命令："
echo "cd $PROJECT_PATH"
echo "python3 scripts/publish.py --all"
echo "=========================================="