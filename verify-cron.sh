#!/bin/bash
# Cron任务验证脚本

echo "=========================================="
echo "Cron任务配置验证"
echo "=========================================="
echo "验证时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查1: Cron服务状态
echo "1. 检查Cron服务状态..."
if pgrep -x "cron" > /dev/null || pgrep -x "crond" > /dev/null; then
    echo -e "   ${GREEN}✅ Cron服务正在运行${NC}"
else
    echo -e "   ${RED}❌ Cron服务未运行${NC}"
    echo "   启动命令:"
    echo "   - macOS: sudo launchctl load /System/Library/LaunchDaemons/com.vix.cron.plist"
    echo "   - Linux: sudo service cron start"
fi
echo ""

# 检查2: Cron任务是否存在
echo "2. 检查新闻聚合博客Cron任务..."
CRON_JOBS=$(crontab -l 2>/dev/null | grep -c "新闻聚合博客")
if [ "$CRON_JOBS" -gt 0 ]; then
    echo -e "   ${GREEN}✅ 找到 $CRON_JOBS 个相关Cron任务${NC}"
    echo "   任务详情:"
    crontab -l | grep -A 1 -B 1 "新闻聚合博客"
else
    echo -e "   ${RED}❌ 未找到新闻聚合博客的Cron任务${NC}"
fi
echo ""

# 检查3: 项目路径有效性
echo "3. 检查项目路径..."
PROJECT_PATH="/Users/durtimemr/.openclaw/workspace/news-blog"
if [ -d "$PROJECT_PATH" ]; then
    echo -e "   ${GREEN}✅ 项目路径存在: $PROJECT_PATH${NC}"
    
    # 检查关键文件
    FILES=("scripts/publish.py" "scripts/news_collector.py" "scripts/news_processor.py" "hugo.toml")
    MISSING_FILES=0
    for file in "${FILES[@]}"; do
        if [ -f "$PROJECT_PATH/$file" ]; then
            echo -e "   ${GREEN}   ✅ $file 存在${NC}"
        else
            echo -e "   ${RED}   ❌ $file 不存在${NC}"
            MISSING_FILES=$((MISSING_FILES + 1))
        fi
    done
    
    if [ "$MISSING_FILES" -eq 0 ]; then
        echo -e "   ${GREEN}✅ 所有关键文件都存在${NC}"
    else
        echo -e "   ${RED}❌ 缺少 $MISSING_FILES 个关键文件${NC}"
    fi
else
    echo -e "   ${RED}❌ 项目路径不存在${NC}"
fi
echo ""

# 检查4: Python环境
echo "4. 检查Python环境..."
if command -v python3 > /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "   ${GREEN}✅ Python3 已安装 (版本: $PYTHON_VERSION)${NC}"
    
    # 检查Python包
    PACKAGES=("feedparser" "bs4" "yaml")
    MISSING_PACKAGES=0
    for package in "${PACKAGES[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            echo -e "   ${GREEN}   ✅ $package 包已安装${NC}"
        else
            echo -e "   ${RED}   ❌ $package 包未安装${NC}"
            MISSING_PACKAGES=$((MISSING_PACKAGES + 1))
        fi
    done
    
    if [ "$MISSING_PACKAGES" -eq 0 ]; then
        echo -e "   ${GREEN}✅ 所有Python包都已安装${NC}"
    else
        echo -e "   ${YELLOW}⚠️  缺少 $MISSING_PACKAGES 个Python包${NC}"
        echo "   安装命令: pip3 install feedparser beautifulsoup4 pyyaml"
    fi
else
    echo -e "   ${RED}❌ Python3 未安装${NC}"
fi
echo ""

# 检查5: Hugo环境
echo "5. 检查Hugo环境..."
if command -v hugo > /dev/null; then
    HUGO_VERSION=$(hugo version | head -1)
    echo -e "   ${GREEN}✅ Hugo 已安装${NC}"
    echo "   版本信息: $HUGO_VERSION"
else
    echo -e "   ${RED}❌ Hugo 未安装${NC}"
    echo "   安装命令: brew install hugo"
fi
echo ""

# 检查6: 日志目录
echo "6. 检查日志配置..."
LOG_DIR="$PROJECT_PATH/logs"
if [ -d "$LOG_DIR" ]; then
    echo -e "   ${GREEN}✅ 日志目录存在: $LOG_DIR${NC}"
    
    # 检查日志文件
    LOG_FILE="$LOG_DIR/cron.log"
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(du -h "$LOG_FILE" 2>/dev/null | cut -f1)
        LOG_LINES=$(wc -l < "$LOG_FILE" 2>/dev/null)
        echo -e "   ${GREEN}   ✅ 日志文件存在${NC}"
        echo "     文件大小: ${LOG_SIZE:-未知}"
        echo "     行数: ${LOG_LINES:-0}"
        
        # 显示最后一条记录
        LAST_LOG=$(tail -1 "$LOG_FILE" 2>/dev/null)
        if [ -n "$LAST_LOG" ]; then
            echo "     最后记录: ${LAST_LOG:0:60}..."
        fi
    else
        echo -e "   ${YELLOW}⚠️  日志文件不存在，Cron任务运行后会创建${NC}"
    fi
else
    echo -e "   ${YELLOW}⚠️  日志目录不存在，正在创建...${NC}"
    mkdir -p "$LOG_DIR"
    if [ $? -eq 0 ]; then
        echo -e "   ${GREEN}✅ 日志目录已创建${NC}"
    else
        echo -e "   ${RED}❌ 无法创建日志目录${NC}"
    fi
fi
echo ""

# 检查7: 下一次运行时间
echo "7. 下一次Cron任务运行时间..."
echo "   根据配置，任务将在以下时间运行："
echo "   • 每天 08:00 (早上8点)"
echo "   • 每天 20:00 (晚上8点)"
echo ""
echo "   下一次运行:"
CURRENT_HOUR=$(date +%H)
if [ "$CURRENT_HOUR" -lt 8 ]; then
    echo "   ✅ 今天 08:00 (约 $((8 - CURRENT_HOUR)) 小时后)"
elif [ "$CURRENT_HOUR" -lt 20 ]; then
    echo "   ✅ 今天 20:00 (约 $((20 - CURRENT_HOUR)) 小时后)"
else
    echo "   ✅ 明天 08:00 (约 $((32 - CURRENT_HOUR)) 小时后)"
fi
echo ""

# 总结
echo "=========================================="
echo "验证结果总结"
echo "=========================================="

# 计算通过的项目
PASS_COUNT=0
TOTAL_COUNT=7

if pgrep -x "cron" > /dev/null || pgrep -x "crond" > /dev/null; then PASS_COUNT=$((PASS_COUNT + 1)); fi
if [ "$CRON_JOBS" -gt 0 ]; then PASS_COUNT=$((PASS_COUNT + 1)); fi
if [ -d "$PROJECT_PATH" ]; then PASS_COUNT=$((PASS_COUNT + 1)); fi
if command -v python3 > /dev/null; then PASS_COUNT=$((PASS_COUNT + 1)); fi
if command -v hugo > /dev/null; then PASS_COUNT=$((PASS_COUNT + 1)); fi
if [ -d "$LOG_DIR" ]; then PASS_COUNT=$((PASS_COUNT + 1)); fi
# 第7项是信息性检查，不算入通过计数

PASS_RATE=$((PASS_COUNT * 100 / TOTAL_COUNT))

if [ "$PASS_RATE" -ge 90 ]; then
    echo -e "${GREEN}✅ 优秀! $PASS_COUNT/$TOTAL_COUNT 项检查通过 ($PASS_RATE%)${NC}"
    echo "Cron任务配置完整，系统准备就绪！"
elif [ "$PASS_RATE" -ge 70 ]; then
    echo -e "${YELLOW}⚠️  良好! $PASS_COUNT/$TOTAL_COUNT 项检查通过 ($PASS_RATE%)${NC}"
    echo "Cron任务基本配置完成，但有一些小问题需要关注。"
else
    echo -e "${RED}❌ 需要改进! $PASS_COUNT/$TOTAL_COUNT 项检查通过 ($PASS_RATE%)${NC}"
    echo "Cron任务配置存在问题，请根据上面的检查结果进行修复。"
fi
echo ""

echo "=========================================="
echo "后续操作建议"
echo "=========================================="
echo "1. 监控日志: tail -f $PROJECT_PATH/logs/cron.log"
echo "2. 手动测试: cd $PROJECT_PATH && python3 scripts/publish.py --all"
echo "3. 管理任务: ./manage-cron.sh"
echo "4. 查看网站: https://durtime.github.io/news-blog/"
echo "=========================================="