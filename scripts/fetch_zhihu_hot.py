import requests
import json
from datetime import datetime
import os

def fetch_zhihu_hot():
    # API endpoint for Zhihu hot list
    url = "https://api.zhihu.com/topstory/hot-list"
    
    # Headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        # Extract top 10 topics
        topics = []
        for item in data.get('data', [])[:10]:  # Get first 10 items
            topic = {
                'title': item['target'].get('title', 'No Title'),
                'url': f"https://www.zhihu.com/question/{item['target'].get('id', '')}",
                'hot_score': item.get('detail_text', 'No Score'),
                'excerpt': item['target'].get('excerpt', 'No Excerpt')
            }
            topics.append(topic)
        
        return topics
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def save_topics(topics):
    # Create output directory if it doesn't exist
    output_dir = 'zhihu'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/zhihu_hot_{today}.txt"
    
    # Write topics to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"知乎热榜 Top 10 - {today}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, topic in enumerate(topics, 1):
            f.write(f"{i}. {topic['title']}\n")
            f.write(f"   热度: {topic['hot_score']}\n")
            f.write(f"   链接: {topic['url']}\n")
            f.write(f"   简介: {topic['excerpt']}\n")
            f.write("\n")

def main():
    topics = fetch_zhihu_hot()
    if topics:
        save_topics(topics)
        print("Successfully fetched and saved Zhihu hot topics")
    else:
        print("Failed to fetch Zhihu hot topics")

if __name__ == "__main__":
    main()