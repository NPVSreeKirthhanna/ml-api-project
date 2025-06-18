import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the scraped data
df = pd.read_csv("discourse_posts.csv")
titles = df['title'].fillna("").tolist()  # handle missing values

# Convert titles to vectors
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(titles)

# Function to get top matching links
def get_top_links(query, top_n=2):
    query_vec = vectorizer.transform([query])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarity.argsort()[-top_n:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            "url": df.iloc[idx]['url'],
            "text": df.iloc[idx]['title']
        })
    return results



