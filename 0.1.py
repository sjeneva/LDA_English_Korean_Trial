import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import string

# Download NLTK data files
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

# Sample articles
articles = [
    "This is the first example article about supply chain management.",
    "This article discusses logistics and transportation in supply chain.",
    "Sustainable practices in supply chain management are becoming more important.",
]

# Preprocess articles
processed_articles = [preprocess(article) for article in articles]

# Create dictionary and corpus
dictionary = corpora.Dictionary(processed_articles)
corpus = [dictionary.doc2bow(article) for article in processed_articles]

# Train LDA model using Gibbs Sampling
lda_model = LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15, random_state=42)

# Print topics
for i, topic in lda_model.print_topics(num_topics=3, num_words=5):
    print(f"Topic {i}: {topic}")

# Example output for the first document
doc_topics = lda_model.get_document_topics(corpus[0])
print(doc_topics)
