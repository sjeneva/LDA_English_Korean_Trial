import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora, models
from gensim.models import CoherenceModel
import matplotlib.pyplot as plt

# Download NLTK data files (one-time setup)
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))

# Preprocess function
def preprocess(text):
    tokens = word_tokenize(text)
    tokens = [word.lower() for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stop_words]
    return tokens

# Sample articles for demonstration (replace with your data)
articles = [
    "This is the first example article about supply chain management.",
    "This article discusses logistics and transportation in supply chain.",
    "Sustainable practices in supply chain management are becoming more important.",
    # Add more articles here
]

# Preprocess articles
processed_articles = [preprocess(article) for article in articles]

# Create dictionary and corpus
dictionary = corpora.Dictionary(processed_articles)
corpus = [dictionary.doc2bow(article) for article in processed_articles]

# Compute coherence values for a range of topics
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = models.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values

# Run the model over a range of topics
model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=processed_articles, start=2, limit=50, step=6)

# Show graph
limit = 50; start = 2; step = 6
x = range(start, limit, step)
plt.plot(x, coherence_values)
plt.xlabel("Num Topics")
plt.ylabel("Coherence score")
plt.legend(["coherence_values"], loc='best')
plt.show()

# Select the model with the highest coherence score
optimal_model = model_list[coherence_values.index(max(coherence_values))]

# Print the topics of the optimal model
for i, topic in optimal_model.print_topics(num_topics=10, num_words=10):
    print(f"Topic {i}: {topic}")
