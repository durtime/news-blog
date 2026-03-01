#!/bin/bash
# 手动更新和推送脚本

echo "=========================================="
echo "新闻聚合博客手动更新"
echo "开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 检查是否在项目目录
if [ ! -f "hugo.toml" ] || [ ! -d "scripts" ]; then
    echo -e "${RED}错误：请在项目根目录运行此脚本${NC}"
    echo "项目路径: /Users/durtimemr/.openclaw/workspace/news-blog"
    exit 1
fi

# 步骤1：收集和处理新闻
echo -e "${BLUE}步骤1: 收集和处理新闻...${NC}"
echo ""
python3 scripts/publish.py --collect --process --build

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 新闻处理失败，请检查错误信息${NC}"
    exit 1
fi

echo -e "${GREEN}✅ 新闻处理完成${NC}"
echo ""

# 步骤2：检查构建结果
echo -e "${BLUE}步骤2: 检查构建结果...${NC}"
if [ -d "public" ] && [ -f "public/index.html" ]; then
    FILE_COUNT=$(find public -type f | wc -l)
    INDEX_SIZE=$(du -h public/index.html | cut -f1)
    echo -e "${GREEN}✅ 网站构建成功${NC}"
    echo "  生成文件数: $FILE_COUNT"
    echo "  首页大小: $INDEX_SIZE"
else
    echo -e "${RED}❌ 网站构建失败，public目录不存在${NC}"
    exit 1
fi
echo ""

# 步骤3：Git操作
echo -e "${BLUE}步骤3: 准备Git提交...${NC}"

# 检查Git状态
GIT_STATUS=$(git status --porcelain)
if [ -z "$GIT_STATUS" ]; then
    echo -e "${YELLOW}⚠️  没有需要提交的更改${NC}"
    echo "可能是新闻内容没有变化"
    read -p "是否继续推送？ (y/N): " CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        echo "操作取消"
        exit 0
    fi
fi

# 添加所有文件
echo "添加文件到Git..."
git add .

# 提交
COMMIT_MSG="手动更新: $(date '+%Y-%m-%d %H:%M') - 新闻聚合"
echo "提交更改: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  提交失败，可能是没有实际更改${NC}"
    read -p "是否强制创建空提交？ (y/N): " FORCE_COMMIT
    if [[ $FORCE_COMMIT =~ ^[Yy]$ ]]; then
        git commit --allow-empty -m "$COMMIT_MSG"
    else
        echo "操作取消"
        exit 0
    fi
fi

echo -e "${GREEN}✅ Git提交完成${NC}"
echo ""

# 步骤4：推送到GitHub
echo -e "${BLUE}步骤4: 推送到GitHub...${NC}"
echo "推送到: origin/main"
git push origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 推送成功！${NC}"
    echo ""
    echo -e "${BLUE}网站将在几分钟内自动更新${NC}"
    echo "访问: https://durtimemr.github.io/news-blog/"
else
    echo -e "${RED}❌ 推送失败${NC}"
    echo "错误信息:"
    git push origin main 2>&1 | tail -5
    exit 1
fi

echo ""
echo "=========================================="
echo "手动更新完成！"
echo "结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""
echo "后续操作："
echo "1. 等待1-2分钟让GitHub Pages部署"
echo "2. 访问网站查看更新: https://durtimemr.github.io/news-blog/"
echo "3. 查看部署状态: https://github.com/durtimemr/news-blog/deployments"
echo "=========================================="