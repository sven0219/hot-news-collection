import requests
import json
from datetime import datetime
import os

def fetch_top_stories():
    """Fetch top stories from Hacker News API"""
    try:
        # Get top story IDs
        response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
        response.raise_for_status()
        story_ids = response.json()[:20]  # Get top 20 stories
        
        stories = []
        for story_id in story_ids:
            try:
                # Get story details
                story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
                story_response = requests.get(story_url)
                story_response.raise_for_status()
                story = story_response.json()
                
                # Extract relevant information
                stories.append({
                    'title': story.get('title', ''),
                    'url': story.get('url', f'https://news.ycombinator.com/item?id={story_id}'),
                    'score': story.get('score', 0),
                    'comments': story.get('descendants', 0)
                })
                
            except requests.RequestException as e:
                print(f"Error fetching story {story_id}: {e}")
                continue
            
        return stories
    
    except requests.RequestException as e:
        print(f"Error fetching top stories: {e}")
        return []

def save_stories(stories):
    """Save stories to a text file"""
    if not stories:
        print("No stories to save")
        return
    
    # Create output directory if it doesn't exist
    base_dir = 'daily_hot'
    output_dir = os.path.join(base_dir, 'hackernews')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/hackernews_hot_{today}.txt"
    
    try:
        # Write stories to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Hacker News Top 20 Stories - {today}\n")
            f.write("=" * 50 + "\n\n")
            
            for i, story in enumerate(stories, 1):
                f.write(f"{i}. {story['title']}\n")
                f.write(f"   Points: {story['score']}\n")
                f.write(f"   Comments: {story['comments']}\n")
                f.write(f"   URL: {story['url']}\n")
                f.write("\n")
                
        print(f"Successfully saved stories to {filename}")
        
    except Exception as e:
        print(f"Error saving stories to file: {e}")

def main():
    print("Fetching Hacker News top stories...")
    stories = fetch_top_stories()
    if stories:
        print(f"Successfully fetched {len(stories)} stories")
        save_stories(stories)
        print("Successfully saved Hacker News stories")
    else:
        print("Failed to fetch Hacker News stories")

if __name__ == "__main__":
    main()