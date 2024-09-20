import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models.ldamodel import LdaModel

# Download NLTK data files (one-time setup)
nltk.download('punkt')
nltk.download('stopwords')

# Load stopwords
stop_words = set(stopwords.words('english'))


def preprocess(text):
    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove punctuation and convert to lower case
    tokens = [word.lower() for word in tokens if word.isalpha()]

    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    return tokens


# Example: Preprocess a single article
article = """
[Shipping and logistics](https://www.tradefinanceglobal.com/freight-forwarding/) managers are responsible for abiding by business ESG standards for greener, more ethical shipping practices on land, water and air. It encompasses brick-and-mortar outfits and e-commerce as global shopping rises in every corporate corner.

ESG focuses on disclosing transparent data for B2B and B2C accountability, which catalyses attentive adherence to up-and-coming regulatory frameworks and legislation. Its effects on the shipping sector are revolutionary for eco-conscious and socially aware operations and communications.

## Environmental impacts

As of 2023, the shipping industry is not on track to meet carbon emission reduction targets. It is due to entities like the International Maritime Organization having independently assigned metrics.. However, the objectives, which previously deviated from the recommendations of the Paris Agreement and the Net Zero Emissions by 2050 Scenario, are now aligned.

ESG forces international and domestic shipping to prioritize collaboration with regulators for cohesion. Otherwise, logistics managers generate aspirations not informed by global experts. ESG implementation continues to make numbers match to [achieve a 15% reduction](https://www.iea.org/energy-system/transport/international-shipping) goal. Shipping and logistics accomplish the [eco-friendly](https://www.tradefinanceglobal.com/export-finance/green-bonds-renewables/) shift in several ways:

  * Analysing why GHGs rose from a previous trend of decline
  * Reducing well-to-wake impact by collecting data about all carbon emission scopes
  * Phasing out fossil fuels, and focusing on renewables and electrification
  * Investing finances in impact investing, and time into research and development
  * Lobbying for more holistic and specific standardisation and auditing procedures
  * Supporting infrastructure overhauls and retrofits

Genuine environmental attention provides numerous benefits. Greenwashing is rampant in every sector and shipping is no exception. Diminishing the [possibility of greenwashing claims](https://environment.co/greenwashing-claims/) relies on honesty in ESG development.

For example, shippers must not claim a commitment to shift to biofuels if they are only in trial stages. Using fossil [fuels](https://www.tradefinanceglobal.com/finance-products/fuels/) still pollutes waters and harms biodiversity. Publicising spontaneous or poorly worded intentions without evidence destroys loyalty and confuses customers.

## Social Shifts

Too often, the “S” in ESG is ignored. But instilling ethical working conditions and removing labor inequality are the focuses of social shifts in ESG. Advocacy involves:

  * Increasing physical health and safety access via more comprehensive benefits.
  * Protecting employees’ digital records with data minimisation and security.
  * Prioritising mental health, rest and vacations.
  * Incorporating adequate safety training.
  * Advocating for workers’ rights and welfare.
  * Solidifying colleague relationships with a strong workplace culture.
  * Aligning corporate priorities to staff values.
  * Eliminating discrimination by enforcing diversity, equity and inclusion frameworks.

Shippers’ quality of life can be low due to unsustainable scheduling, poor benefits and wages that do not support mental resilience. Shipping and logistics managers are in charge of improving conditions. Doing so requires enhancing technical proficiency in data management and collection for growth monitoring.

Shippers need to distinguish between what is lawful and what is ethical, as these two may not always align. Investigations into shipping conditions have exposed dangerous cost-saving measures and a lack of essential maintenance for vessels. Within many shipping organisations, human rights violations are prevalent, and training is often minimal. There is a clear need for more workers to carry out various tasks, and the practices within ship-breaking operations have been found to be abusive towards labour. However, the integration of ESG considerations is starting to influence budget decisions, helping to ensure that welfare is not compromised.

ESG shapes shipping by increasing diversity in the ranks. Organisations like the Women’s International Shipping and Trading Association collaborate with companies to bolster the Sustainable Development Goal of gender equality. Currently, only [20% of national maritime authorities](https://wistainternational.com/our-work/women-in-maritime-imo-wista-international-survey-2021/) in the industry are women, but proper ESG actions can help increase these numbers, while still supporting other diversity initaitves.

## Governance changes

Fair governance structures are essential for value-driven ESG execution. Organisations like the United Nations-supported Principles for Responsible Investing reveal how [$100 trillion in assets](https://www.unpri.org/news-and-press/principles-for-responsible-investment-releases-new-framework-for-signatories-to-take-action-on-the-sustainable-development-goals/5924.article) and thousands of worldwide signatories dedicated themselves to intentional action. It guides boards of directors, shareholders and management partners.

The plan underscores the pivotal role that governance and reporting play in shaping the environmental and social components of ESG. Decisions in each category stem from administrative choices, leading to internal shifts that can spark broader systemic reform. ESG-led shipping and logistics leaders are also entrusted with the responsibility of initiating these transformative changes.

The executive transformation alters how related departments like procurement and cybersecurity reinforce and promote ESG discourse. It eliminates unnecessary favouritism and corrupt dealings by encouraging greater accountability from top influencers of shipping and logistics.

Governance is the most complexly layered challenge in authentic ESG efforts. Compliance exists to monitor these activities. However, geopolitical tensions, personal biases and financial motivations litter the landscape.

Proper [sanction adherence is crucial](https://www.jdsupra.com/legalnews/economic-sanctions-in-the-shipping-1243874/) but cannot abate governance influences outside their control. ESG shifts come from mindset adjustments to remove malintent and bribery. Additionally, shippers must fix working conditions to incentivise ethical oversight and leadership.

## ESG frameworks change shipping for the better

Logistics and shipping are on their way to becoming better for people and the planet. Banning corrupt activity that exploits shipping workers and the Earth is vital. ESG determines relationships and bottom lines, which enterprises may realise only when they commit to the framework.

Addressing resource scarcity for the environment, emotional and financial security for workers, and risk management in governance carry equal gravity in changing the shipping sector toward a more positive reputation and impact.
"""

processed_article = preprocess(article)
print(processed_article)

# Assume 'processed_articles' is a list of pre-processed articles
processed_articles = [preprocess(article) for article in [article]]  # Replace with more articles as needed

# Create a dictionary representation of the documents
dictionary = corpora.Dictionary(processed_articles)

# Convert documents to Bag of Words format
corpus = [dictionary.doc2bow(article) for article in processed_articles]

print(corpus[0])  # Example output for the first article

# Set the number of topics
num_topics = 3  # Adjust as needed

# Train the LDA model using Gibbs Sampling
lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15, random_state=42)

# Print the topics
for i, topic in lda_model.print_topics(num_topics=num_topics, num_words=10):
    print(f"Topic {i}: {topic}")

# Get the topic distribution for a specific document
doc_topics = lda_model.get_document_topics(corpus[0])
print(doc_topics)

# Get the topic distribution across the entire corpus
corpus_topics = [lda_model.get_document_topics(doc) for doc in corpus]
