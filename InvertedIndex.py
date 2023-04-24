## Importing all the necessary libraries and components
import ssl
import os
import re
import nltk
import pandas as pd
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer

# Adding this to skip the SSL certificate check to download stopwords from the nltk package
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

## Function to create an inverted index by fetching the data from records.csv
def inverted_index():
    print("\nStarting to create an Inverted Index.")
    ## Reading the data from csv file and creating a dataframe
    if os.path.isfile('records.csv'):
        dataframe = pd.read_csv("records.csv")
        ## Exploring the dataframe
        print(
            "----------------------------------------------------------------------------------------------------------------------------------------------")
        print("No of research papers found: ", len(dataframe))
        print(
            "----------------------------------------------------------------------------------------------------------------------------------------------")
        print(dataframe.count())
        print(
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        print(dataframe.head())
        print(
            "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        ## Pre-processing data

        clean_titles = []
        stemmer = PorterStemmer()
        title_tokens = []
        for title in dataframe['Title of the Research Paper']:
            # Removing non-ASCII characters
            title = re.sub(r'[^\x00-\x7F]+', '', title)
            # Removing mentions (starting with '@')
            title = re.sub(r'@\w+', '', title)
            # Converting to lowercase
            title = title.lower()
            # Removing punctuation marks
            title = re.sub(r'[^\w\s]', '', title)
            # Removing stop words
            stop_words = set(stopwords.words('english'))
            title = ' '.join(word for word in title.split() if word not in stop_words)
            clean_titles.append(title)

        for title in clean_titles:
            # Creating word tokens
            tokenized_title = word_tokenize(title)
            # Stemming the word tokens
            stemmed_title = [stemmer.stem(word) for word in tokenized_title if word.isalpha()]
            processed_title = ' '.join(stemmed_title)
            title_tokens.append(processed_title)

        # Uncomment the below section to print the titles of the article after pre-processing
        # for title in title_tokens:
        #     print(title)

        ## Creating an Inverted Index

        # Creating an empty dictionary to hold the inverted index
        inverted_index = {}

        # iterate through each title and tokenize it
        for i, title in enumerate(title_tokens):
            tokens = title.split()
            # iterate through each token and update the inverted index
            for token in tokens:
                if token in inverted_index:
                    inverted_index[token].append(i)
                else:
                    inverted_index[token] = [i]

        # Uncomment the below section to print the inverted index
        # for token in inverted_index:
        #     print(token + ":", inverted_index[token])

        print("Inverted Index is created.\n")
        return inverted_index
    else:
        print(
            "The records.csv file is not present at the moment. Run the crawler to generate the file and then execute this program.")

# Uncomment the below section to call the inverted index manually
# inverted_index()