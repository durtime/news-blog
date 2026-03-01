#!/bin/bash
# Cron任务管理脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目路径
PROJECT_PATH="/Users/durtimemr/.openclaw/workspace/news-blog"
LOG_PATH="$PROJECT_PATH/logs/cron.log"

# 显示标题
show_header() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}  新闻聚合博客Cron任务管理${NC}"
    echo -e "${BLUE}==========================================${NC}"
    echo ""
}

# 显示当前Cron任务
show_cron_jobs() {
    echo -e "${YELLOW}📋 当前Cron任务：${NC}"
    echo ""
    crontab -l | grep -A 2 -B 2 "新闻聚合博客" || echo -e "${RED}未找到新闻聚合博客的Cron任务${NC}"
    echo ""
}

# 显示Cron任务状态
show_status() {
    echo -e "${YELLOW}📊 Cron任务状态：${NC}"
    echo ""
    
    # 检查Cron服务状态
    if pgrep -x "cron" > /dev/null; then
        echo -e "${GREEN}✅ Cron服务正在运行${NC}"
    else
        echo -e "${RED}❌ Cron服务未运行${NC}"
        echo "启动命令: sudo service cron start"
    fi
    
    # 检查日志文件
    if [ -f "$LOG_PATH" ]; then
        LOG_SIZE=$(du -h "$LOG_PATH" | cut -f1)
        LOG_LINES=$(wc -l < "$LOG_PATH")
        LOG_LAST=$(tail -1 "$LOG_PATH" 2>/dev/null | cut -c1-80)
        
        echo -e "${GREEN}✅ 日志文件存在${NC}"
        echo "  文件大小: $LOG_SIZE"
        echo "  行数: $LOG_LINES"
        
        if [ -n "$LOG_LAST" ]; then
            echo "  最后记录: $LOG_LAST..."
        fi
    else
        echo -e "${YELLOW}⚠️  日志文件不存在${NC}"
    fi
    
    echo ""
}

# 查看日志
view_log() {
    echo -e "${YELLOW}📝 查看Cron日志：${NC}"
    echo ""
    
    if [ -f "$LOG_PATH" ]; then
        echo "选择查看方式："
        echo "1. 查看最后10行"
        echo "2. 查看最后50行"
        echo "3. 查看完整日志"
        echo "4. 实时监控日志"
        echo "5. 返回"
        echo ""
        read -p "请输入选项 (1-5): " choice
        
        case $choice in
            1)
                echo -e "${BLUE}最后10行日志：${NC}"
                tail -10 "$LOG_PATH"
                ;;
            2)
                echo -e "${BLUE}最后50行日志：${NC}"
                tail -50 "$LOG_PATH"
                ;;
            3)
                echo -e "${BLUE}完整日志：${NC}"
                cat "$LOG_PATH"
                ;;
            4)
                echo -e "${BLUE}实时监控日志（按Ctrl+C退出）：${NC}"
                tail -f "$LOG_PATH"
                ;;
            5)
                return
                ;;
            *)
                echo -e "${RED}无效选项${NC}"
                ;;
        esac
    else
        echo -e "${RED}日志文件不存在${NC}"
    fi
    
    echo ""
}

# 手动运行任务
run_manual() {
    echo -e "${YELLOW}🚀 手动运行新闻收集任务：${NC}"
    echo ""
    
    echo "选择运行模式："
    echo "1. 只收集新闻"
    echo "2. 收集并处理新闻"
    echo "3. 完整流程（收集+处理+构建）"
    echo "4. 测试运行（不实际执行）"
    echo "5. 返回"
    echo ""
    read -p "请输入选项 (1-5): " choice
    
    case $choice in
        1)
            echo -e "${BLUE}开始收集新闻...${NC}"
            cd "$PROJECT_PATH" && python3 scripts/publish.py --collect
            ;;
        2)
            echo -e "${BLUE}开始收集并处理新闻...${NC}"
            cd "$PROJECT_PATH" && python3 scripts/publish.py --collect --process
            ;;
        3)
            echo -e "${BLUE}开始完整流程...${NC}"
            cd "$PROJECT_PATH" && python3 scripts/publish.py --collect --process --build
            ;;
        4)
            echo -e "${BLUE}测试运行（显示命令但不执行）...${NC}"
            echo "cd $PROJECT_PATH"
            echo "python3 scripts/publish.py --collect --process --build"
            ;;
        5)
            return
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            ;;
    esac
    
    echo ""
}

# 管理Cron任务
manage_cron() {
    echo -e "${YELLOW}⚙️  Cron任务管理：${NC}"
    echo ""
    
    echo "选择操作："
    echo "1. 重新安装Cron任务"
    echo "2. 移除Cron任务"
    echo "3. 编辑Cron任务"
    echo "4. 查看Cron服务状态"
    echo "5. 返回"
    echo ""
    read -p "请输入选项 (1-5): " choice
    
    case $choice in
        1)
            echo -e "${BLUE}重新安装Cron任务...${NC}"
            # 先移除现有任务
            crontab -l | grep -v "新闻聚合博客" | crontab -
            # 添加新任务
            (crontab -l 2>/dev/null; echo ""; echo "# 新闻聚合博客自动化任务"; echo "0 8,20 * * * cd $PROJECT_PATH && /usr/bin/python3 scripts/publish.py --collect --process --build >> $LOG_PATH 2>&1"; echo "0 7 * * 1 find $PROJECT_PATH/logs -name \"*.log\" -mtime +7 -delete") | crontab -
            echo -e "${GREEN}✅ Cron任务已重新安装${NC}"
            ;;
        2)
            echo -e "${YELLOW}⚠️  确认移除新闻聚合博客的Cron任务？ (y/N): ${NC}"
            read -p "" confirm
            if [[ $confirm == "y" || $confirm == "Y" ]]; then
                crontab -l | grep -v "新闻聚合博客" | crontab -
                echo -e "${GREEN}✅ Cron任务已移除${NC}"
            else
                echo -e "${BLUE}操作已取消${NC}"
            fi
            ;;
        3)
            echo -e "${BLUE}编辑Cron任务...${NC}"
            crontab -e
            ;;
        4)
            echo -e "${BLUE}Cron服务状态：${NC}"
            if pgrep -x "cron" > /dev/null; then
                echo -e "${GREEN}✅ Cron服务正在运行${NC}"
            else
                echo -e "${RED}❌ Cron服务未运行${NC}"
                echo "启动命令: sudo service cron start"
            fi
            ;;
        5)
            return
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            ;;
    esac
    
    echo ""
}

# 显示帮助
show_help() {
    echo -e "${YELLOW}📖 使用说明：${NC}"
    echo ""
    echo "Cron任务配置："
    echo "  • 每天 8:00 和 20:00（北京时间）自动运行"
    echo "  • 执行新闻收集、处理和网站构建"
    echo "  • 日志保存到: $LOG_PATH"
    echo ""
    echo "手动运行命令："
    echo "  cd $PROJECT_PATH"
    echo "  python3 scripts/publish.py --collect --process --build"
    echo ""
    echo "查看日志命令："
    echo "  tail -f $LOG_PATH"
    echo ""
}

# 主菜单
main_menu() {
    while true; do
        show_header
        show_cron_jobs
        show_status
        
        echo -e "${YELLOW}请选择操作：${NC}"
        echo "1. 查看日志"
        echo "2. 手动运行任务"
        echo "3. 管理Cron任务"
        echo "4. 显示帮助"
        echo "5. 退出"
        echo ""
        read -p "请输入选项 (1-5): " main_choice
        
        case $main_choice in
            1)
                view_log
                ;;
            2)
                run_manual
                ;;
            3)
                manage_cron
                ;;
            4)
                show_help
                read -p "按Enter键继续..."
                ;;
            5)
                echo -e "${GREEN}再见！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选项，请重新选择${NC}"
                sleep 1
                ;;
        esac
    done
}

# 运行主菜单
main_menu