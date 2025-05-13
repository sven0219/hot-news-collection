import requests
import json
from datetime import datetime
import os
import random
import time

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    ]
    return random.choice(user_agents)

def fetch_douban_hot():
    # Using Douban's API endpoint for hot topics
    url = "https://m.douban.com/rexxar/api/v2/gallery/topic_feed"
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Origin': 'https://www.douban.com',
        'Referer': 'https://www.douban.com/',
        'Host': 'm.douban.com',
    }
    
    params = {
        'start': 0,
        'count': 20,
        'sort': 'hot'
    }
    
    try:
        # Add a random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract top 10 topics
        topics = []
        items = data.get('items', [])[:10]  # Get first 10 items
        
        for item in items:
            try:
                title = item.get('title', 'No Title')
                target = item.get('target', {})
                link = target.get('url', 'https://www.douban.com')
                likes = target.get('reaction_count', 0)
                excerpt = target.get('desc', 'No description available')
                
                topics.append({
                    'title': title,
                    'url': link,
                    'likes': likes,
                    'excerpt': excerpt
                })
            except Exception as e:
                print(f"Error processing item: {e}")
                continue
        
        return topics
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
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
    output_dir = os.path.join(base_dir, 'douban')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/douban_hot_{today}.txt"
    
    try:
        # Write topics to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"豆瓣热门话题 Top 10 - {today}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, topic in enumerate(topics, 1):
                f.write(f"{i}. {topic['title']}\n")
                f.write(f"   热度: {topic['likes']} 喜欢\n")
                f.write(f"   链接: {topic['url']}\n")
                f.write(f"   简介: {topic['excerpt']}\n")
                f.write("\n")
        print(f"Successfully saved topics to {filename}")
    except Exception as e:
        print(f"Error saving topics to file: {e}")

def main():
    print("Fetching Douban hot topics...")
    topics = fetch_douban_hot()
    if topics:
        print(f"Successfully fetched {len(topics)} topics")
        save_topics(topics)
        print("Successfully saved Douban hot topics")
    else:
        print("Failed to fetch Douban hot topics")

if __name__ == "__main__":
    main()