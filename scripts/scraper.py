import pandas as pd
import os
import sys
import json
import time
import random
from pmaw import PushshiftAPI

# --- State Management ---
STATE_FILE = "data/scraper_state.json"
OUTPUT_FILE = "data/InteriorDesign_posts.csv"

def load_state():
    """Loads the last scraped timestamp from the state file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: State file is corrupted. Starting from scratch.")
                return {"last_timestamp": None}
    return {"last_timestamp": None}

def save_state(timestamp):
    """Saves the last scraped timestamp to the state file."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({"last_timestamp": int(timestamp) if timestamp else None}, f)

def scrape_historical_posts(subreddit_name):
    """
    Scrapes a batch of historical posts from a subreddit, with resumable state.

    Args:
        subreddit_name (str): The name of the subreddit to scrape.

    Returns:
        bool: True if new posts were scraped, False otherwise.
    """
    # Initialize the API
    api = PushshiftAPI()

    # Load the last known timestamp
    state = load_state()
    start_epoch = state.get('last_timestamp')

    # Ensure state file exists from the start
    if not os.path.exists(STATE_FILE):
        save_state(None)

    print(f"Searching for posts in r/{subreddit_name} after timestamp: {start_epoch or 'the beginning'}")

    # Fetch posts from Pushshift
    posts = api.search_submissions(
        subreddit=subreddit_name,
        after=start_epoch,
        sort='asc',
        sort_type='created_utc',
        limit=1000  # Fetch in batches of 1000
    )

    post_list = list(posts)

    if not post_list:
        print("No new posts found.")
        return False

    posts_df = pd.DataFrame(post_list)

    # --- Data Processing and Saving ---
    posts_df = posts_df[['created_utc', 'title', 'selftext', 'url']].copy()
    posts_df.rename(columns={'created_utc': 'timestamp'}, inplace=True)

    file_exists = os.path.exists(OUTPUT_FILE)

    print(f"Appending {len(posts_df)} new posts to {OUTPUT_FILE}...")
    posts_df.to_csv(OUTPUT_FILE, mode='a', header=not file_exists, index=False)

    # --- State Update ---
    last_timestamp = posts_df['timestamp'].iloc[-1]
    save_state(last_timestamp)

    print(f"Scrape successful. Next run will start after timestamp: {last_timestamp}")

    return True

if __name__ == "__main__":
    SUBREDDIT = "InteriorDesign"

    try:
        new_posts_found = scrape_historical_posts(SUBREDDIT)
        if new_posts_found:
            sleep_time = random.uniform(5, 15)
            print(f"Sleeping for {sleep_time:.2f} seconds before finishing.")
            time.sleep(sleep_time)
        else:
            print("Process finished. No new posts to scrape.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
