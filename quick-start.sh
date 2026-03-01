#!/bin/bash
# 新闻聚合博客快速启动脚本

echo "=========================================="
echo "新闻聚合博客快速启动"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查依赖
check_dependencies() {
    echo "检查依赖..."
    
    # 检查Hugo
    if command -v hugo &> /dev/null; then
        echo -e "${GREEN}✅ Hugo 已安装${NC}"
    else
        echo -e "${RED}❌ Hugo 未安装${NC}"
        echo "安装命令: brew install hugo"
        return 1
    fi
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python3 已安装${NC}"
    else
        echo -e "${RED}❌ Python3 未安装${NC}"
        return 1
    fi
    
    # 检查Python包
    echo "检查Python包..."
    python3 -c "import feedparser, bs4, yaml" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Python依赖包已安装${NC}"
    else
        echo -e "${YELLOW}⚠️  安装Python依赖包...${NC}"
        pip3 install feedparser beautifulsoup4 pyyaml
    fi
    
    return 0
}

# 显示菜单
show_menu() {
    echo ""
    echo "请选择操作："
    echo "1. 测试新闻收集"
    echo "2. 构建网站"
    echo "3. 本地测试（启动服务器）"
    echo "4. 完整流程测试"
    echo "5. 查看网站状态"
    echo "6. 设置Cron自动化"
    echo "7. 退出"
    echo ""
    read -p "请输入选项 (1-7): " choice
}

# 测试新闻收集
test_collect() {
    echo "开始测试新闻收集..."
    python3 scripts/publish.py --collect --process
}

# 构建网站
build_site() {
    echo "构建网站..."
    hugo --minify
    echo -e "${GREEN}✅ 网站构建完成${NC}"
    echo "网站文件在: public/"
}

# 本地测试
local_test() {
    echo "启动本地测试服务器..."
    echo "访问: http://localhost:1313"
    echo "按 Ctrl+C 停止服务器"
    hugo server -D
}

# 完整测试
full_test() {
    echo "执行完整流程测试..."
    python3 scripts/publish.py --all
}

# 查看网站状态
check_status() {
    echo "检查网站状态..."
    echo "线上网站: https://durtime.github.io/news-blog/"
    
    # 检查网站可访问性
    if curl -s -o /dev/null -w "%{http_code}" https://durtime.github.io/news-blog/ | grep -q "200"; then
        echo -e "${GREEN}✅ 网站可正常访问${NC}"
    else
        echo -e "${YELLOW}⚠️  网站访问可能有问题${NC}"
    fi
    
    # 检查本地构建
    if [ -d "public" ] && [ -f "public/index.html" ]; then
        echo -e "${GREEN}✅ 本地网站已构建${NC}"
    else
        echo -e "${YELLOW}⚠️  本地网站未构建${NC}"
    fi
}

# 设置Cron
setup_cron() {
    echo "设置Cron自动化..."
    ./setup-cron.sh
}

# 主函数
main() {
    # 检查依赖
    check_dependencies
    if [ $? -ne 0 ]; then
        echo -e "${RED}依赖检查失败，请先安装必要的依赖${NC}"
        exit 1
    fi
    
    while true; do
        show_menu
        
        case $choice in
            1)
                test_collect
                ;;
            2)
                build_site
                ;;
            3)
                local_test
                ;;
            4)
                full_test
                ;;
            5)
                check_status
                ;;
            6)
                setup_cron
                ;;
            7)
                echo "再见！"
                exit 0
                ;;
            *)
                echo "无效选项，请重新选择"
                ;;
        esac
    done
}

# 运行主函数
main