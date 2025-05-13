import requests
import json
from datetime import datetime
import os
from bs4 import BeautifulSoup

def fetch_douban_hot():
    url = "https://www.douban.com/gallery/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract top 10 topics
        topics = []
        items = soup.select('.topic-item')[:10]  # Get first 10 items
        
        for item in items:
            title = item.select_one('.title').text.strip()
            link = item.select_one('a')['href']
            likes = item.select_one('.hot-num').text.strip()
            excerpt = item.select_one('.abstract').text.strip() if item.select_one('.abstract') else 'No excerpt'
            
            topics.append({
                'title': title,
                'url': link,
                'likes': likes,
                'excerpt': excerpt
            })
        
        return topics
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def save_topics(topics):
    # Create output directory if it doesn't exist
    base_dir = 'daily_hot'
    output_dir = os.path.join(base_dir, 'douban')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/douban_hot_{today}.txt"
    
    # Write topics to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"豆瓣热门话题 Top 10 - {today}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, topic in enumerate(topics, 1):
            f.write(f"{i}. {topic['title']}\n")
            f.write(f"   热度: {topic['likes']}\n")
            f.write(f"   链接: {topic['url']}\n")
            f.write(f"   简介: {topic['excerpt']}\n")
            f.write("\n")

def main():
    topics = fetch_douban_hot()
    if topics:
        save_topics(topics)
        print("Successfully fetched and saved Douban hot topics")
    else:
        print("Failed to fetch Douban hot topics")

if __name__ == "__main__":
    main()