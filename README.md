# 每日新闻聚合博客

一个自动化的新闻聚合博客系统，每天从各大新闻源收集、汇总并发布新闻内容。

## 功能特点

- 📰 **自动收集**：每日从多个新闻源自动获取最新内容
- 🤖 **智能处理**：自动分类、去重、生成摘要
- ⏰ **定时发布**：每天固定时间自动更新网站
- 🌐 **外网访问**：通过GitHub Pages免费部署
- 🔄 **完全自动化**：本地Cron + 云端GitHub Actions双保险

## 快速开始

### 1. 环境准备
```bash
# 安装Hugo
brew install hugo

# 安装Python依赖
pip3 install feedparser beautifulsoup4 python-frontmatter markdown
```

### 2. 本地测试
```bash
# 进入项目目录
cd news-blog

# 安装依赖
python3 scripts/publish.py --install

# 收集新闻
python3 scripts/publish.py --collect

# 处理新闻
python3 scripts/publish.py --process

# 构建网站
python3 scripts/publish.py --build

# 本地测试
python3 scripts/publish.py --test
```

### 3. 部署到GitHub Pages

1. **创建GitHub仓库**
   - 在GitHub上创建新仓库，例如 `news-blog`
   - 不要初始化README、.gitignore等文件

2. **推送代码到GitHub**
   ```bash
   git remote add origin https://github.com/durtime/news-blog.git
   git add .
   git commit -m "初始提交"
   git push -u origin main
   ```

3. **配置GitHub Pages**
   - 进入仓库设置 → Pages
   - 选择 `gh-pages` 分支作为源
   - 保存设置

4. **访问你的网站**
   - 等待几分钟，访问：`https://durtime.github.io/news-blog/`

## 项目结构

```
news-blog/
├── content/              # Hugo文章内容
│   └── posts/           # 自动生成的新闻文章
├── data/                # 新闻数据（JSON格式）
├── scripts/             # Python脚本
│   ├── news_collector.py   # 新闻收集
│   ├── news_processor.py   # 新闻处理
│   └── publish.py          # 发布脚本
├── themes/              # Hugo主题
├── static/              # 静态资源
├── .github/workflows/   # GitHub Actions工作流
├── hugo.toml           # Hugo配置
└── README.md           # 项目文档
```

## 自动化配置

### 本地自动化（Cron）
```bash
# 安装Cron任务
crontab -e

# 添加以下内容（每天8:00和20:00运行）
0 8,20 * * * cd /path/to/news-blog && python3 scripts/publish.py --collect --process --build >> logs/cron.log 2>&1
```

### 云端自动化（GitHub Actions）
- 代码推送到GitHub后自动触发
- 每天UTC时间0:00和12:00自动运行（对应北京时间8:00和20:00）
- 自动部署到GitHub Pages

## 自定义配置

### 修改新闻源
编辑 `scripts/news_collector.py` 中的 `NEWS_SOURCES` 字典：
```python
NEWS_SOURCES = {
    "source_name": {
        "name": "新闻源名称",
        "url": "RSS地址",
        "category": "分类"
    },
    # 添加更多新闻源...
}
```

### 修改博客配置
编辑 `hugo.toml`：
```toml
baseURL = 'https://durtime.github.io/news-blog/'
title = '你的博客标题'
theme = 'paper'

[params]
  subtitle = "你的副标题"
  name = "你的名字"
```

### 修改主题
1. 浏览 [Hugo主题库](https://themes.gohugo.io/)
2. 安装新主题：`git submodule add 主题地址 themes/主题名`
3. 修改 `hugo.toml` 中的 `theme` 设置

## 新闻源列表

当前支持的新闻源：
- 新华社 (国内新闻)
- 人民网 (政治新闻)
- 央视新闻 (综合新闻)
- 36氪 (科技新闻)
- 虎嗅 (科技评论)
- BBC中文 (国际新闻)
- 路透社 (国际新闻)

## 常见问题

### Q: 网站无法访问？
- 检查GitHub Pages设置是否正确
- 等待几分钟让部署完成
- 查看GitHub Actions运行状态

### Q: 新闻收集失败？
- 检查网络连接
- 验证RSS地址是否有效
- 查看日志文件：`logs/cron.log`

### Q: 如何添加自定义新闻源？
1. 在 `news_collector.py` 中添加新的RSS源
2. 测试收集：`python3 scripts/news_collector.py`
3. 重新部署

### Q: 如何修改发布频率？
- 本地：修改Cron表达式
- 云端：修改 `.github/workflows/deploy.yml` 中的cron设置

## 技术栈

- **前端**: Hugo (静态网站生成器)
- **后端**: Python (新闻收集处理)
- **部署**: GitHub Pages
- **自动化**: Cron + GitHub Actions
- **主题**: Hugo Paper Theme

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 支持

如有问题，请：
1. 查看 [常见问题](#常见问题)
2. 提交 [Issue](https://github.com/durtime/news-blog/issues)
3. 查看日志文件

---

*最后更新: 2026年3月1日*