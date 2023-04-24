import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from nltk.stem.porter import PorterStemmer
from InvertedIndex import inverted_index

# Taking the user input
while True:
    print("----------------------------------------------------------------------------------------------------------------------------------------------")
    user_input = input("\nPlease select one the options from below. \n a. Search for article published under \"Research Centre for Computational Science and Mathematical Modelling\" \n b. Exit\n")
    if user_input == 'a':
        # Variable initializations
        porter_stemmer = PorterStemmer()
        stop_words = set(stopwords.words('english'))
        matched_words = []
        corrected_search_string = []

        # Creating instance of SpellChecker class
        spell_checker = SpellChecker()

        # Getting the inverted index and reading the csv file in dataframe
        document_index = inverted_index()
        dataframe = pd.read_csv("records.csv")

        search_string = input("Enter the article name you are looking for: ")

        # Spell-checking the search string
        corrected_search_string = ''
        for word in search_string.split():
            corrected_search_string += spell_checker.correction(word) + ' '
        search_string = corrected_search_string.strip()
        print("Query after spell check: ", search_string)

        ## Pre-processing the input data
        # Tokenize the search string
        tokenized_words = word_tokenize(search_string.lower())
        # Stem and remove stop words and non-alphabetic words
        stemmed_words = [porter_stemmer.stem(word) for word in tokenized_words if word not in stop_words and word.isalpha()]
        # Join the stemmed words and split into a list
        processed_query = ' '.join(stemmed_words).split()
        # Print the pre-processed query
        print("Processed Query tokens:", processed_query)

        # Searching for the query in the document index
        for word in processed_query:
            if word in document_index:
                matched_words.append(word)

        # Finding the documents that match the query
        matched_docs = set()
        for word in matched_words:
            for doc_id in document_index[word]:
                matched_docs.add(doc_id)

        # Displaying the matched documents
        if len(matched_docs) > 0:
            print("Found", len(matched_docs), "documents matching the search query:")
            for doc_id in matched_docs:
                print("------------------------------------------------------------------------------------------")
                print("Title:", dataframe.iloc[doc_id]['Title of the Research Paper'])
                print("Link:", dataframe.iloc[doc_id]['Link to the Research Paper'])
                print("Published Date:", dataframe.iloc[doc_id]['Published Date'])
                print("Authors:", dataframe.iloc[doc_id]['Authors'])
                print("Authors Profile Link:", dataframe.iloc[doc_id]['Pureportal Profile Link'])
        else:
            print("No documents found matching the search query.")
    elif user_input == 'b':
        break
    else:
        print("You gave an Invalid Input. \nPlease choose either (a) or (b).\n")
