import praw
import pandas as pd
import os
import sys

# --- Reddit API Credentials ---
CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
USER_AGENT = os.environ.get("REDDIT_USER_AGENT")

def scrape_reddit_posts(subreddit_name, limit=100):
    """
    Scrapes a given number of posts from a specified subreddit.

    Args:
        subreddit_name (str): The name of the subreddit to scrape.
        limit (int): The maximum number of posts to fetch.

    Returns:
        pandas.DataFrame: A DataFrame containing the scraped post data.
    """
    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    print(f"Scraping top {limit} posts from r/{subreddit_name}...")
    for post in subreddit.top(limit=limit):
        posts_data.append({
            'title': post.title,
            'selftext': post.selftext,
            'url': post.url
        })

    return pd.DataFrame(posts_data)

if __name__ == "__main__":
    if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
        print("Error: Reddit API credentials are not set. Please set the following environment variables:")
        print(" - REDDIT_CLIENT_ID")
        print(" - REDDIT_CLIENT_SECRET")
        print(" - REDDIT_USER_AGENT")
        sys.exit(1)

    SUBREDDIT = "InteriorDesign"
    POST_LIMIT = 500
    OUTPUT_FILE = f"data/{SUBREDDIT}_posts.csv"

    scraped_df = scrape_reddit_posts(SUBREDDIT, POST_LIMIT)

    if not scraped_df.empty:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        scraped_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Successfully scraped {len(scraped_df)} posts and saved to {OUTPUT_FILE}")
    else:
        print("No posts were scraped.")
