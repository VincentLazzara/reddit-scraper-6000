# Reddit Scraper 6000

This project scrapes posts from a given subreddit, preprocesses the text data, and performs topic modeling and object identification to uncover common themes and frequently mentioned items.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd reddit-scraper-6000
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Reddit API credentials:**
    - Create a new application on the [Reddit apps page](https://www.reddit.com/prefs/apps).
    - Select "script" as the application type.
    - Set the following environment variables with your credentials:
      ```bash
      export REDDIT_CLIENT_ID="YOUR_CLIENT_ID"
      export REDDIT_CLIENT_SECRET="YOUR_CLIENT_SECRET"
      export REDDIT_USER_AGENT="YOUR_USER_AGENT"
      ```

## Usage

1.  **Scrape the data:**
    ```bash
    python scripts/scraper.py
    ```
    This will scrape the top 500 posts from r/InteriorDesign and save them to `data/InteriorDesign_posts.csv`.

2.  **Preprocess the data:**
    ```bash
    python scripts/preprocess.py
    ```
    This will clean the text data and save it to `data/InteriorDesign_posts_processed.csv`.

3.  **Run the analysis:**
    - First, you'll need to generate the analysis notebook:
      ```bash
      python scripts/create_notebook.py
      ```
    - Then, you can run the notebook and generate the HTML report:
      ```bash
      jupyter nbconvert --to html --execute notebooks/analysis.ipynb
      ```
    - The final report will be available at `notebooks/analysis.html`.
