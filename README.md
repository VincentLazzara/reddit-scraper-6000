# Reddit Scraper 6000

This project provides a powerful and resilient pipeline to scrape all historical posts from a subreddit, preprocess the text data, and perform NLP analysis to uncover common themes and discussion topics.

The scraper is designed for long-term, exhaustive data collection. It is:
- **Historical**: Uses the Pushshift API to fetch every post since the subreddit's creation.
- **Resumable**: Automatically saves its progress. If the script is stopped, it will resume exactly where it left off, ensuring no data is lost.
- **Robust**: Handles API rate limits and temporary network issues gracefully.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd reddit-scraper-6000
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```
    *Note: The spaCy model is required for the data preprocessing step.*

## Usage

The data pipeline is designed to be run in sequence.

### 1. Scrape the Data (Historical)

The scraper is designed to fetch posts in batches, making it ideal for running over a long period.

-   **To run a single batch:**
    ```bash
    python scripts/scraper.py
    ```
    The script will fetch up to 1000 posts, append them to `data/InteriorDesign_posts.csv`, and save its progress in `data/scraper_state.json`.

-   **To run continuously for full historical scraping:**
    You can run the script in a loop from your shell. This will continuously fetch batches until the entire history of the subreddit has been scraped.
    ```bash
    while true; do
      python scripts/scraper.py
      echo "Batch complete. Waiting 10 seconds before next run..."
      sleep 10
    done
    ```
    You can leave this running overnight or for as long as needed to collect all the data. The script will automatically pick up where it left off each time.

### 2. Preprocess the Data

Once you have collected a sufficient amount of data, you can preprocess it.

```bash
python scripts/preprocess.py
```
This will read the raw data from `data/InteriorDesign_posts.csv`, clean the text, and save the result to `data/InteriorDesign_posts_processed.csv`.

### 3. Analyze and Visualize the Results

Finally, you can generate the analysis notebook and create a visual report.

1.  **Generate the notebook:**
    ```bash
    python scripts/create_notebook.py
    ```
2.  **Run the analysis and create the HTML report:**
    ```bash
    jupyter nbconvert --to html --execute notebooks/analysis.ipynb
    ```
The final, shareable report will be available at `notebooks/analysis.html`.
