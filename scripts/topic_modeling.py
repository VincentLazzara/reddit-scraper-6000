import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os

def perform_topic_modeling(data, n_topics=5, n_top_words=10):
    """
    Performs LDA topic modeling on the given data.

    Args:
        data (pandas.Series): A series of processed text documents.
        n_topics (int): The number of topics to discover.
        n_top_words (int): The number of top words to display for each topic.

    Returns:
        None
    """
    # Create a document-term matrix
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(data)

    # Apply LDA
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(doc_term_matrix)

    # Display the topics
    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic #{topic_idx + 1}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

    return lda, vectorizer

if __name__ == "__main__":
    INPUT_FILE = "data/InteriorDesign_posts_processed.csv"

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}")
    else:
        df = pd.read_csv(INPUT_FILE)

        # Ensure the processed_text column exists and is not empty
        if 'processed_text' in df.columns and not df['processed_text'].dropna().empty:
            print("Performing topic modeling...")
            perform_topic_modeling(df['processed_text'].dropna())
        else:
            print("No processed text found to analyze.")
