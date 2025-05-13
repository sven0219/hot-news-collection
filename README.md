# Daily Hot Topics Collector

这个项目自动收集和保存每日热门话题，包括 Hacker News 和知乎热榜。

## 功能

1. **Hacker News Top Stories**
   - 每天自动获取 Hacker News 排名前 10 的故事
   - 保存标题、URL、分数和作者信息
   - UTC 00:00 自动运行

2. **知乎热榜**
   - 每天自动获取知乎热榜前 10 的话题
   - 保存标题、热度、链接和简介
   - UTC 01:00 自动运行

## 目录结构

```
.
├── daily_hot/
│   ├── hackernews/
│   │   └── hn_news_YYYY-MM-DD.txt
│   └── zhihu/
│       └── zhihu_hot_YYYY-MM-DD.txt
├── scripts/
│   ├── fetch_hn_news.py
│   └── fetch_zhihu_hot.py
└── .github/
    └── workflows/
        ├── fetch_news.yml
        └── fetch_zhihu.yml
```

## 自动化

项目使用 GitHub Actions 实现自动化：
- Hacker News 数据在每天 UTC 00:00 收集
- 知乎热榜在每天 UTC 01:00 收集
- 所有数据按日期存档
- 支持手动触发数据收集

## 本地运行

1. 克隆仓库：
```bash
git clone https://github.com/sven0219/MCP-Test.git
cd MCP-Test
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行脚本：
```bash
python scripts/fetch_hn_news.py  # 获取 Hacker News
python scripts/fetch_zhihu_hot.py  # 获取知乎热榜
```

## 数据格式

### Hacker News
- 文件名格式：`hn_news_YYYY-MM-DD.txt`
- 包含内容：标题、URL、分数、作者

### 知乎热榜
- 文件名格式：`zhihu_hot_YYYY-MM-DD.txt`
- 包含内容：标题、热度、链接、话题简介

## License

MIT