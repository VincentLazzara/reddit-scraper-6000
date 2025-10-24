import pandas as pd
import spacy
from collections import Counter
import os

# --- Predefined list of common decor objects ---
DECOR_OBJECTS = [
    "sofa", "couch", "chair", "table", "desk", "bed", "dresser", "cabinet",
    "bookshelf", "rug", "carpet", "curtain", "drape", "lamp", "light",
    "mirror", "art", "painting", "poster", "plant", "vase", "cushion",
    "pillow", "shelf", "fireplace", "tv", "window", "door", "floor", "wall"
]

def identify_decor_objects(text, decor_list):
    """
    Identifies and counts decor-related objects in a given text.

    Args:
        text (str): The text to analyze.
        decor_list (list): A list of decor-related keywords.

    Returns:
        list: A list of identified decor objects.
    """
    if not isinstance(text, str):
        return []

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text.lower())

    identified_objects = []
    for token in doc:
        if token.lemma_ in decor_list:
            identified_objects.append(token.lemma_)

    return identified_objects

if __name__ == "__main__":
    INPUT_FILE = "data/InteriorDesign_posts_processed.csv"

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file not found at {INPUT_FILE}")
    else:
        df = pd.read_csv(INPUT_FILE)

        if 'processed_text' in df.columns and not df['processed_text'].dropna().empty:
            print("Identifying decor objects...")

            # Apply the function to the processed text
            df['decor_objects'] = df['processed_text'].dropna().apply(lambda text: identify_decor_objects(text, DECOR_OBJECTS))

            # Flatten the list of lists and count the frequency of each object
            all_objects = [obj for sublist in df['decor_objects'] for obj in sublist]
            object_counts = Counter(all_objects)

            print("\n--- Top 10 Most Common Decor Objects ---")
            for obj, count in object_counts.most_common(10):
                print(f"{obj}: {count}")
        else:
            print("No processed text found to analyze.")
