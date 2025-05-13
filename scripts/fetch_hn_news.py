import requests
import json
from datetime import datetime
import os
from newspaper import Article
import nltk
import traceback

def get_article_summary(url):
    """
    Get summary of the article from the given URL
    Returns a tuple of (summary, error_message)
    """
    try:
        if not url or url == 'No URL':
            return None, "No URL available"
            
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()  # This will generate summary
        
        # Get the first 3 sentences of the summary or the entire summary if shorter
        summary = '. '.join(article.summary.split('. ')[:3]) + '.'
        return summary, None
        
    except Exception as e:
        error_msg = str(e)
        return None, f"Error fetching summary: {error_msg}"

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
        
        url = story.get('url', 'No URL')
        summary, error = get_article_summary(url)
        
        stories.append({
            'title': story.get('title'),
            'url': url,
            'score': story.get('score'),
            'by': story.get('by'),
            'summary': summary if summary else "No summary available",
            'summary_error': error if error else None
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
            f.write(f"   Summary: {story['summary']}\n")
            if story['summary_error']:
                f.write(f"   Note: {story['summary_error']}\n")
            f.write("\n")

def main():
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    stories = fetch_top_stories()
    save_stories(stories)

if __name__ == "__main__":
    main()