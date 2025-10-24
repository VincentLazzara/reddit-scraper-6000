import nbformat as nbf

# Create a new notebook object
nb = nbf.v4.new_notebook()

# --- Markdown Cell: Title ---
nb['cells'].append(nbf.v4.new_markdown_cell(
    "# Analysis of r/InteriorDesign Posts"
))

# --- Code Cell: Imports and Data Loading ---
nb['cells'].append(nbf.v4.new_code_cell(
    """
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os

# --- Load the processed data ---
INPUT_FILE = "../data/InteriorDesign_posts_processed.csv"
if not os.path.exists(INPUT_FILE):
    print(f"Error: Input file not found at {INPUT_FILE}")
else:
    df = pd.read_csv(INPUT_FILE)
    print("Data loaded successfully.")
"""
))

# --- Markdown Cell: Object Identification ---
nb['cells'].append(nbf.v4.new_markdown_cell(
    "## Object Identification Analysis"
))

# --- Code Cell: Object Identification ---
nb['cells'].append(nbf.v4.new_code_cell(
    """
DECOR_OBJECTS = [
    "sofa", "couch", "chair", "table", "desk", "bed", "dresser", "cabinet",
    "bookshelf", "rug", "carpet", "curtain", "drape", "lamp", "light",
    "mirror", "art", "painting", "poster", "plant", "vase", "cushion",
    "pillow", "shelf", "fireplace", "tv", "window", "door", "floor", "wall"
]

def identify_decor_objects(text, decor_list):
    if not isinstance(text, str):
        return []
    identified_objects = [word for word in text.split() if word in decor_list]
    return identified_objects

if 'processed_text' in df.columns:
    df['decor_objects'] = df['processed_text'].dropna().apply(lambda text: identify_decor_objects(text, DECOR_OBJECTS))
    all_objects = [obj for sublist in df['decor_objects'] for obj in sublist]
    object_counts = Counter(all_objects)

    # --- Visualize the most common objects ---
    if object_counts:
        most_common_objects = object_counts.most_common(10)
        objects, counts = zip(*most_common_objects)

        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(objects), y=list(counts))
        plt.title('Top 10 Most Common Decor Objects')
        plt.xlabel('Object')
        plt.ylabel('Frequency')
        plt.show()
    else:
        print("No decor objects identified.")
"""
))

# --- Markdown Cell: Topic Modeling ---
nb['cells'].append(nbf.v4.new_markdown_cell(
    "## Topic Modeling Analysis"
))

# --- Code Cell: Topic Modeling ---
nb['cells'].append(nbf.v4.new_code_cell(
    """
def display_topics(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic #{topic_idx + 1}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))

if 'processed_text' in df.columns and not df['processed_text'].dropna().empty:
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    doc_term_matrix = vectorizer.fit_transform(df['processed_text'].dropna())

    lda = LatentDirichletAllocation(n_components=5, random_state=42)
    lda.fit(doc_term_matrix)

    # --- Display the topics ---
    feature_names = vectorizer.get_feature_names_out()
    display_topics(lda, feature_names, 10)

    # --- Visualize topics with word clouds ---
    for topic_idx, topic in enumerate(lda.components_):
        topic_frequencies = {feature_names[i]: topic[i] for i in topic.argsort()[:-50 - 1:-1]}
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(topic_frequencies)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(f'Topic #{topic_idx + 1}')
        plt.show()
else:
    print("No processed text found to analyze.")
"""
))

# --- Write the notebook to a file ---
with open('notebooks/analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook created successfully.")
