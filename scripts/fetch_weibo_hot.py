import requests
import json
from datetime import datetime
import os
import random
import time
from bs4 import BeautifulSoup

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    ]
    return random.choice(user_agents)

def fetch_weibo_hot():
    url = "https://weibo.com/ajax/statuses/hot_band"
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://weibo.com/hot/search',
    }
    
    try:
        # Add a random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        topics = []
        
        # Get first 20 topics
        for item in data.get('data', {}).get('band_list', [])[:20]:
            try:
                title = item.get('word', '')
                hot_score = item.get('raw_hot', 0)
                link = f"https://s.weibo.com/weibo?q={requests.utils.quote(title)}"
                
                topics.append({
                    'title': title,
                    'url': link,
                    'hot_score': hot_score
                })
                
            except Exception as e:
                print(f"Error processing topic: {e}")
                continue
        
        return topics
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def save_topics(topics):
    if not topics:
        print("No topics to save")
        return
        
    # Create output directory if it doesn't exist
    base_dir = 'daily_hot'
    output_dir = os.path.join(base_dir, 'weibo')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/weibo_hot_{today}.txt"
    
    try:
        # Write topics to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"微博热搜榜 Top 20 - {today}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, topic in enumerate(topics, 1):
                f.write(f"{i}. {topic['title']}\n")
                f.write(f"   热度: {topic['hot_score']}\n")
                f.write(f"   链接: {topic['url']}\n")
                f.write("\n")
        print(f"Successfully saved topics to {filename}")
    except Exception as e:
        print(f"Error saving topics to file: {e}")

def main():
    print("Fetching Weibo hot topics...")
    topics = fetch_weibo_hot()
    if topics:
        print(f"Successfully fetched {len(topics)} topics")
        save_topics(topics)
        print("Successfully saved Weibo hot topics")
    else:
        print("Failed to fetch Weibo hot topics")

if __name__ == "__main__":
    main()