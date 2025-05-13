# MCP-Test Repository

This repository is entirely created and managed by GitHub MCP (Managed Copilot for Prometheus). You can try MCP at [https://mcp.dev](https://mcp.dev).

## Features

- Issue templates for bug reports and feature requests
- Daily Hacker News top stories collector
- Automated GitHub Actions workflow

## Hacker News Collector

This repository includes a Python script that automatically fetches the top 10 stories from Hacker News daily and saves them to text files.

### How It Works

The script:
- Fetches the top 10 stories from Hacker News API
- Extracts title, URL, score, and author information
- Saves the data to a dated text file in the `news/` directory
- Runs automatically every day at 00:00 UTC through GitHub Actions

### Running the Script Locally

1. Clone the repository:
```bash
git clone https://github.com/sven0219/MCP-Test.git
cd MCP-Test
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the script:
```bash
python scripts/fetch_hn_news.py
```

The script will create a new file in the `news/` directory with today's date (format: `hn_news_YYYY-MM-DD.txt`).

### GitHub Actions Workflow

The repository includes a GitHub Actions workflow that:
- Runs automatically every day at 00:00 UTC
- Can be triggered manually from the Actions tab
- Commits and pushes the new news file to the repository

To manually trigger the workflow:
1. Go to the "Actions" tab
2. Select "Fetch Daily Hacker News"
3. Click "Run workflow"

## Project Structure

```
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── fetch_news.yml
├── scripts/
│   └── fetch_hn_news.py
├── news/
│   └── (daily news files)
├── requirements.txt
└── README.md
```

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or find any bugs.

## License

This project is open source and available under the MIT License.