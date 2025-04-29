from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_match_score(profile_text, title):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([profile_text, title])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0]
