import pandas as pd
import spacy
from nltk.corpus import stopwords
import string
import nltk
import os

# --- Download NLTK stopwords if not already present ---
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

# --- Load spaCy model ---
nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """
    Cleans and preprocesses a given text string.

    Args:
        text (str): The text to preprocess.

    Returns:
        str: The cleaned and lemmatized text.
    """
    if not isinstance(text, str):
        return ""

    # Create a doc object
    doc = nlp(text.lower())

    # Lemmatize, remove stopwords and punctuation
    lemmatized_tokens = [
        token.lemma_ for token in doc
        if token.text not in stop_words and token.text not in string.punctuation
    ]

    return " ".join(lemmatized_tokens)

if __name__ == "__main__":
    INPUT_FILE = "data/InteriorDesign_posts.csv"
    OUTPUT_FILE = "data/InteriorDesign_posts_processed.csv"

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}")
    else:
        # Load the scraped data
        df = pd.read_csv(INPUT_FILE)

        # Combine title and selftext for a complete picture
        df['combined_text'] = df['title'] + " " + df['selftext'].fillna("")

        print("Preprocessing text data...")
        # Apply the preprocessing function
        df['processed_text'] = df['combined_text'].apply(preprocess_text)

        # Save the processed data
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Processed data saved to {OUTPUT_FILE}")
