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

def fetch_douban_hot():
    # Using Douban's group hot topics
    url = "https://www.douban.com/group/explore"
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'bid=' + ''.join(random.choices('0123456789abcdef', k=11))
    }
    
    try:
        # Add a random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        topics = []
        
        # Find all topic cards
        cards = soup.select('.channel-item')[:20]  # Get first 20 items
        
        for card in cards:
            try:
                title_elem = card.select_one('h3 a')
                desc_elem = card.select_one('.desc')
                likes_elem = card.select_one('.likes')
                
                if not title_elem:
                    continue
                    
                title = title_elem.text.strip()
                link = title_elem['href']
                excerpt = desc_elem.text.strip() if desc_elem else 'No description available'
                likes = likes_elem.text.strip() if likes_elem else '0'
                
                topics.append({
                    'title': title,
                    'url': link,
                    'likes': likes,
                    'excerpt': excerpt
                })
                
            except Exception as e:
                print(f"Error processing card: {e}")
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
    output_dir = os.path.join(base_dir, 'douban')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/douban_hot_{today}.txt"
    
    try:
        # Write topics to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"豆瓣热门话题 Top 20 - {today}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, topic in enumerate(topics, 1):
                f.write(f"{i}. {topic['title']}\n")
                f.write(f"   热度: {topic['likes']}\n")
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