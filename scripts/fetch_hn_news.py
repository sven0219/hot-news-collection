import requests
import json
from datetime import datetime
import os

def fetch_top_stories():
    # Get list of top story IDs
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    response = requests.get(top_stories_url)
    story_ids = response.json()[:10]  # Only get top 10 stories
    
    stories = []
    # Get details for each story
    for story_id in story_ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = requests.get(story_url)
        story = story_response.json()
        stories.append({
            'title': story.get('title'),
            'url': story.get('url', 'No URL'),
            'score': story.get('score'),
            'by': story.get('by')
        })
    
    return stories

def save_stories(stories):
    # Create output directory if it doesn't exist
    output_dir = 'news'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with date
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{output_dir}/hn_news_{today}.txt"
    
    # Write stories to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Hacker News Top Stories - {today}\n")
        f.write("=" * 50 + "\n\n")
        
        for i, story in enumerate(stories, 1):
            f.write(f"{i}. {story['title']}\n")
            f.write(f"   URL: {story['url']}\n")
            f.write(f"   Score: {story['score']}\n")
            f.write(f"   By: {story['by']}\n")
            f.write("\n")

def main():
    stories = fetch_top_stories()
    save_stories(stories)

if __name__ == "__main__":
    main()