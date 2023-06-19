
# Information-Retrieval

This repository contains code for different tasks related to Information Retrieval.

This project was created as part of the coursework for module 7071CEM Information Retrieval for [Coventry University](https://www.coventry.ac.uk/course-structure/pg/eec/data-science-and-computational-intelligence-msc/). Any use of the code needs to be cited appropriately. 

### Code Walkthrough and Demo - https://youtu.be/xF2SMsmde0Q

## Usage

The code can be executed in any Python Interpreter. I have developed this code using PyCharm.


---

## Search Engine

### Aim

This task aimed at developing a vertical search engine similar to Google Scholar but specialised to retrieve only papers/books published by a member of the [Research Centre for Computational Science and Mathematical Modelling (CSM)](https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell) at Coventry University.

There were certain factors mentioned below which were supposed to be considered while creating the system.
 - One of the co-authors should be a member of CSM.
 - The system should crawl relevant web pages and extract available data (such as authors, publication year, and title) and the links to both the publication page and the author’s profile (also called “pureportal” profile) page.
 - The crawler should be polite and preserve the robots.txt rules.
 - The crawler should have the functionality to be manually triggered and could be scheduled.
 - Every time the crawler runs it should update the Inverted Index.
 - Pre-processing tasks need to be applied to both the crawled data and the user's queries.

### Designed Solution

As a part of this solution, I have created three files below

**1. [Crawler.py](https://github.com/siddesai80/Information-Retrieval/blob/main/Crawler.py)**

This file contains the logic for Crawling the [CSM webpage](https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell) and fetching the contents from the website. The details crawled are saved in a CSV file named 'records.csv'. It also contains logic where it checks whether a given URL is allowed to be crawled by a web crawler, based on the rules specified in the robots.txt file for the domain. 

Upon execution, the Crawler will provide two execution options.
- Run the crawler manually.
- Start the scheduler. (This is programmed to run every Sunday)

**2. [InvertedIndex.py](https://github.com/siddesai80/Information-Retrieval/blob/main/InvertedIndex.py)**

This file contains the logic of creating an Inverted Index from the data which is stored in records.csv. The contents from records.csv are fetched and then different pre-processing tasks like Stemming and Tokenization are used to create an Inverted Index. 

**3. [QuerySearch.py](https://github.com/siddesai80/Information-Retrieval/blob/main/QuerySearch.py)**

This file contains logic which helps in searching and returning articles related to a particular search query. 

## Document Clustering

### Aim

To develop a document clustering system. First, collect a number of documents that belong to different categories, namely Sport, Technology and Climate. Each document should be at least one sentence (the longer is usually the better). The total number of documents is up to you but should be at least 100 (the more is usually the better). Once you have collected sufficient documents, cluster them using a standard clustering method (e.g. K-means).

Finally, use the created model to assign a new document to one of the existing clusters. That is, the user enters a document (e.g. a sentence) and your system outputs the right cluster.

### Designed Solution

[DocumentClustering.py](https://github.com/siddesai80/Information-Retrieval/blob/main/DocumentClustering.py)

As a part of this solution, there is only one file. The code implements a text clustering system using a K-means clustering algorithm on news articles fetched from multiple RSS feeds. It displays the right cluster for the new news article provided as input. 

---

## Information Paper

For more information on the above tasks refer to the document present under the [Paper](https://github.com/siddesai80/Information-Retrieval/tree/main/Paper) folder. 
