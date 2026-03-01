# 新闻聚合博客部署指南

## 📋 项目概述

你已经成功搭建了一个自动化的新闻聚合博客系统！以下是完整的部署和使用指南。

## 🚀 快速部署步骤

### 步骤1：创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名: `news-blog` (或其他你喜欢的名字)
3. **不要**初始化README、.gitignore或license
4. 点击"Create repository"

### 步骤2：推送代码到GitHub
```bash
# 进入项目目录
cd news-blog

# 初始化Git（如果还没初始化）
git init

# 添加所有文件
git add .

# 提交
git commit -m "初始提交：新闻聚合博客系统"

# 添加远程仓库
git remote add origin https://github.com/durtime/news-blog.git

# 推送到GitHub
git push -u origin main
```

### 步骤3：配置GitHub Pages
1. 进入仓库页面: `https://github.com/durtime/news-blog`
2. 点击"Settings" → "Pages"
3. 在"Build and deployment"部分:
   - Source: 选择"Deploy from a branch"
   - Branch: 选择`gh-pages`，文件夹`/(root)`
4. 点击"Save"
5. 等待1-2分钟，访问: `https://durtime.github.io/news-blog/`

## ⚙️ 本地自动化设置

### 安装Cron任务（每天自动运行）
```bash
# 编辑Cron任务
crontab -e

# 添加以下内容（每天8:00和20:00运行）
0 8,20 * * * cd /Users/durtimemr/.openclaw/workspace/news-blog && python3 scripts/publish.py --collect --process --build >> logs/cron.log 2>&1

# 保存并退出（在vim中按ESC，然后输入:wq）
```

### 手动测试完整流程
```bash
cd news-blog

# 安装依赖
python3 scripts/publish.py --install

# 执行完整流程
python3 scripts/publish.py --all

# 或分步执行
python3 scripts/publish.py --collect    # 收集新闻
python3 scripts/publish.py --process    # 处理新闻
python3 scripts/publish.py --build      # 构建网站
python3 scripts/publish.py --test       # 本地测试
```

## 🌐 外网访问配置

### 自定义域名（可选）
1. 购买域名（如阿里云、腾讯云）
2. 在域名DNS设置中添加CNAME记录:
   ```
   记录类型: CNAME
   主机记录: www (或 @)
   记录值: durtime.github.io
   ```
3. 在GitHub Pages设置中添加自定义域名

### 启用HTTPS
- GitHub Pages自动提供HTTPS
- 在Settings → Pages中勾选"Enforce HTTPS"

## 🔧 自定义配置

### 修改新闻源
编辑 `scripts/news_collector.py`:
```python
NEWS_SOURCES = {
    "your_source": {
        "name": "你的新闻源",
        "url": "RSS地址",
        "category": "分类"
    }
}
```

### 修改博客外观
1. **主题**: 修改 `hugo.toml` 中的 `theme` 设置
2. **样式**: 在 `static/css/` 中添加自定义CSS
3. **布局**: 在 `layouts/` 中覆盖主题模板

### 调整发布频率
- **本地**: 修改Cron表达式
- **云端**: 修改 `.github/workflows/deploy.yml` 中的cron设置

## 📊 监控与维护

### 查看日志
```bash
# 查看Cron日志
tail -f news-blog/logs/cron.log

# 查看GitHub Actions日志
# 在GitHub仓库页面点击"Actions"选项卡
```

### 数据备份
```bash
# 备份新闻数据
cp news-blog/data/news_master.json ~/backup/news_backup_$(date +%Y%m%d).json

# 备份整个项目
tar -czf ~/backup/news-blog_$(date +%Y%m%d).tar.gz news-blog/
```

### 性能监控
1. **网站速度**: 使用 https://pagespeed.web.dev/
2. **访问统计**: 添加Google Analytics或百度统计
3. **错误监控**: 查看GitHub Actions运行状态

## 🐛 故障排除

### 常见问题

#### Q: 网站显示404错误
- 检查GitHub Pages设置是否正确
- 等待几分钟让部署完成
- 运行 `git push origin main` 重新触发部署

#### Q: 新闻收集失败
```bash
# 检查网络连接
ping 8.8.8.8

# 测试单个RSS源
cd news-blog/scripts
python3 -c "import feedparser; print(feedparser.parse('https://feeds.bbci.co.uk/zhongwen/simp/rss.xml').status)"
```

#### Q: Hugo构建失败
```bash
# 检查Hugo版本
hugo version

# 清理缓存
rm -rf public/ resources/_gen/

# 重新构建
hugo --minify
```

#### Q: 本地服务器无法启动
```bash
# 检查端口占用
lsof -i :1313

# 使用其他端口
hugo server -D --port 8080
```

## 🔄 更新与升级

### 更新项目
```bash
cd news-blog

# 拉取最新代码（如果有远程仓库）
git pull origin main

# 更新主题
git submodule update --remote --recursive

# 更新Python依赖
pip3 install -r requirements.txt --upgrade
```

### 升级Hugo
```bash
# 使用Homebrew升级
brew update
brew upgrade hugo

# 验证版本
hugo version
```

## 📞 技术支持

### 获取帮助
1. **查看文档**: `README.md` 和本指南
2. **检查日志**: `logs/` 目录下的日志文件
3. **搜索问题**: 在GitHub Issues中搜索类似问题
4. **提交Issue**: 在GitHub仓库创建新Issue

### 社区资源
- **Hugo文档**: https://gohugo.io/documentation/
- **GitHub Pages文档**: https://docs.github.com/pages
- **Python feedparser**: https://pythonhosted.org/feedparser/

## 🎯 成功指标

部署完成后，你应该能够：
- ✅ 访问 `https://durtime.github.io/news-blog/`
- ✅ 每天自动更新新闻内容
- ✅ 在本地通过Cron任务自动化运行
- ✅ 通过GitHub Actions实现云端备份自动化
- ✅ 自定义新闻源和博客外观

## 📝 最后检查清单

- [ ] GitHub仓库创建并推送代码
- [ ] GitHub Pages配置完成
- [ ] 网站可以正常访问
- [ ] 本地Cron任务配置
- [ ] 测试新闻收集功能
- [ ] 测试网站构建功能
- [ ] 备份重要数据
- [ ] 添加监控（可选）

---

**恭喜！** 你的自动化新闻聚合博客已经部署完成。🎉

*部署时间: 2026年3月1日*
*技术支持: 爱丽丝 (你的AI助手)*