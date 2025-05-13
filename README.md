# Global Trending Hub

This project automatically collects and archives daily hot topics from Hacker News and Zhihu. The entire repository, including all code and configurations, was generated using the [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github).

## About MCP Server

This repository showcases the capabilities of Microsoft's Collaborative Protocol (MCP) server. The MCP server is an AI-powered system that can:
- Generate complete repository structures
- Create and manage GitHub workflows
- Write and maintain Python scripts
- Handle multiple API integrations
- Manage documentation and configurations

All code, workflows, and documentation in this repository were created through interactions with the MCP server, demonstrating its ability to understand and implement complex requirements.

## Features

1. **Hacker News Top Stories**
   - Automatically fetches top 10 stories from Hacker News daily
   - Captures title, URL, score, and author information
   - Runs at 00:00 UTC daily

2. **Zhihu Hot Topics**
   - Automatically fetches top 10 topics from Zhihu daily
   - Captures title, popularity, link, and topic excerpt
   - Runs at 01:00 UTC daily

## Directory Structure

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

## Automation

The project uses GitHub Actions for automation:
- Hacker News data is collected daily at 00:00 UTC
- Zhihu hot topics are collected daily at 01:00 UTC
- All data is archived by date
- Manual trigger support for data collection

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/sven0219/global-trending-hub.git
cd global-trending-hub
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scripts:
```bash
python scripts/fetch_hn_news.py  # Fetch Hacker News
python scripts/fetch_zhihu_hot.py  # Fetch Zhihu Hot Topics
```

## Data Format

### Hacker News
- File naming: `hn_news_YYYY-MM-DD.txt`
- Content: Title, URL, Score, Author

### Zhihu Hot Topics
- File naming: `zhihu_hot_YYYY-MM-DD.txt`
- Content: Title, Popularity, Link, Topic Excerpt

## Generated Content

All content in this repository was generated through interactions with the MCP server, including:
- Python scripts for data collection
- GitHub Actions workflows
- Directory structure
- Documentation and README
- Error handling and logging
- Data formatting and storage

## Contributing

Since this is an MCP-generated repository, please note that any contributions should be made through the MCP server to maintain consistency and proper integration.

## License

MIT

---
*This repository is maintained by the GitHub MCP Server. For more information about MCP and its capabilities, visit [GitHub MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github).*