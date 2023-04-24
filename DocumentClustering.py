import feedparser
import nltk
from spellchecker import SpellChecker
from nltk.stem.porter import PorterStemmer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_extraction.text import CountVectorizer

# Define categories for each feed
categories = {
    'http://rss.cnn.com/rss/edition_sport.rss': 'Sports',
    'http://feeds.bbci.co.uk/news/technology/rss.xml': 'Technology',
    'http://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml': 'Entertainment',
    'http://feeds.bbci.co.uk/news/politics/rss.xml': 'Politics',
    'http://rss.cnn.com/rss/money_news_international.rss': 'Business'
}

# Define lists for each category of documents
sports_list = []
technology_list = []
entertainment_list = []
politics_list = []
business_list = []


# Define function to get text from RSS feeds
def get_text(feed_url, category):
    feed_parser = [feedparser.parse(feed_url)]
    for feeder in feed_parser:
        for entry in feeder.entries:
            if category == 'Sports':
                sports_list.append(entry.title)
            elif category == 'Technology':
                technology_list.append(entry.title)
            elif category == 'Entertainment':
                entertainment_list.append(entry.title)
            elif category == 'Politics':
                politics_list.append(entry.title)
            elif category == 'Business':
                business_list.append(entry.title)

# Define a function to tokenize and stem the text
def tokenize_and_stem(text):
    tokens = nltk.word_tokenize(text)
    stemmer = PorterStemmer()
    stems = [stemmer.stem(t) for t in tokens]
    return stems

# Define RSS feeds
feed_links = list(categories.keys())

# Get text from RSS feeds
print("\nStarting to fetch news articles from various rss feeds.")
for feed in feed_links:
    get_text(feed, categories[feed])
print("News articles fetched.")

print("------------------------------------------------------------------------")
print("Total news articles fetched from Sports category:", len(sports_list))
print("Total news articles fetched from Technology category:", len(technology_list))
print("Total news articles fetched from Entertainment category:", len(entertainment_list))
print("Total news articles fetched from Politics category:", len(politics_list))
print("Total news articles fetched from Business category:", len(business_list))

# Combine text from all feeds into one list
text_list = sports_list + technology_list + entertainment_list + politics_list + business_list
print("\nTotal news articles fetched: ", len(text_list))
print("------------------------------------------------------------------------")

# Define number of clusters
k = len(categories)

# Create bag of words
vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(text_list)

# Cluster documents using K-means
km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
km.fit(X)

# Label the clusters
labels = km.labels_
cluster_labels = {}
for i, category in enumerate(categories.values()):
    cluster_labels[i] = category
clusters = {}
for i in range(len(labels)):
    if labels[i] in clusters:
        clusters[labels[i]].append(text_list[i])
    else:
        clusters[labels[i]] = [text_list[i]]
for i in range(k):
    cluster_docs = clusters[i]
    label = cluster_labels.get(i, f"Cluster {i+1}")
    print(f'{label}: {len(cluster_docs)} documents')
    for doc in cluster_docs:
        print(doc)
    print()

# Use the model to predict a new document

while True:
    # Taking input from user
    user_input = input("\nPlease select one the options from below. \na. Search for a cluster using news headline \nb. Exit\n")

    if user_input == 'a':
        query = input("Enter a news headline to find it's cluster.\n")

        # Creating instance of SpellChecker class
        spell_checker = SpellChecker()

        # Spell-checking the search string
        corrected_search_string = ''
        for word in query.split():
            correction = spell_checker.correction(word)
            if correction is not None:
                corrected_search_string += correction + ' '
        query = corrected_search_string.strip()
        print("Query after spell check: ", query)

        vectorized_query = vectorizer.transform([query])
        prediction = km.predict(vectorized_query)[0]
        print("Inertia: ", km.inertia_)
        silhouette_avg = silhouette_score(X, labels)
        print("Silhouette Score: ", silhouette_avg)
        print(f'The new document belongs to cluster {cluster_labels[prediction]} ({cluster_labels[prediction]})')

    elif user_input == 'b':
        break
    else:
        print("You gave an Invalid Input. \nPlease choose either (a) or (b).\n")