## Importing all the necessary libraries and components
import csv
import ssl
import requests
import sched, time, datetime

# Adding this to skip the SSL certificate check
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.exceptions import HTTPError
from urllib.robotparser import RobotFileParser
from InvertedIndex import inverted_index


## Checks whether a given URL is allowed to be crawled by a web crawler, based on the rules specified in the robots.txt file for the domain.
def check_allowed_robots(url) -> bool:
    robot_parser = RobotFileParser()
    robot_parser.set_url(urljoin(url, "/robots.txt"))
    try:
        robot_parser.read()
        print("Provided URL can be crawled as it adheres to the rules mentioned in robots.txt.")
        return robot_parser.can_fetch("*", url)
    except HTTPError:
        return False


## Crawls the given link and stores records in a csv file
def crawler(pub_url, prof_url):
    # Initializing variables
    publication_results = []
    profile_results = []

    print("Crawling Started.")
    print("Publications link which will be crawled -> ", pub_url)
    print("Profiles link which will be crawled -> ", prof_url)

    if check_allowed_robots(website_url):
        profiles = requests.get(prof_url)
        profiles_soup = BeautifulSoup(profiles.content, 'html.parser')
        profiles_lists = profiles_soup.find_all('div', class_="result-container")
        # Extracting all the profile links of the members of the profiles_url passed
        print("Fetching all the profile details.")
        for lists in profiles_lists:
            for profile in lists.find_all("a", class_="link person"):
                profile_results.append(profile.get('href'))
        print("All the profile details are now retrieved.")

    while True:
        if check_allowed_robots(website_url):
            publications = requests.get(pub_url)
            publications_soup = BeautifulSoup(publications.content, 'html.parser')
            publications_lists = publications_soup.find_all('div', class_="result-container")

            # Extracting all the information from articles fetched from the publications page
            print("Fetching all the article details.")
            for paper in publications_lists:
                author_names = []
                author_profile_links = []
                dictionary = {}

                title = paper.find("h3", class_="title")
                paper_link = paper.find("a", class_="link")
                published_date = paper.find("span", class_="date")

                #################################################################################################################################################################################
                # I attempted to extract the publisher information, but since the property class/tag is not consistent, I am disregarding this information.
                #################################################################################################################################################################################
                # publisher = paper.find("a", class_="link", attrs={"rel": ["Publisher", "Journal"]}).find("span").text
                # print(publisher)

                #################################################################################################################################################################################
                # I made an attempt to retrieve the names of authors who did not have a profile, but I was unable to do so because their names were only declared within <span> tags without any specific class. Since pulling all <span> tags returns unnecessary values, I have decided to skip the process of fetching the names of authors without a profile.
                #################################################################################################################################################################################
                # authors_span = paper.find("div", class_="rendering rendering_researchoutput rendering_researchoutput_portal-short rendering_contributiontobookanthology rendering_portal-short rendering_contributiontobookanthology_portal-short").find_all("span")
                # for author in authors_span:
                #     if author.has_attr('class'):
                #         continue
                #     author_names.append(author.string.strip())
                #     print(author.string.strip())

                for author in paper.find_all("a", class_="link person"):
                    author_names.append(author.string)
                    author_profile_links.append(author.get('href'))

                #################################################################################################################################################################################
                # Uncomment the below section to print details of individual articles.
                #################################################################################################################################################################################
                # print("--------------------------------------------------------------------------------")
                # print("Title of the research paper: ", title.text)
                # print("Link to the research paper: ", paper_link.get('href'))
                # print("Published date: ", published_date.text)
                # print("Authors of the research paper: ", ', '.join(author_names))
                # print("Profile links to the author profiles: ", ', '.join(author_profile_links))

                # Refining the article selection by filtering for pieces authored by members of the Research Centre for Computational Science and Mathematical Modelling (CSM) at Coventry University.
                for link in author_profile_links:
                    if link in profile_results:
                        # Storing all the retrieved information regarding each publication in a dictionary
                        dictionary['Title of the Research Paper'] = title.text
                        dictionary['Link to the Research Paper'] = paper_link.get('href')
                        dictionary['Published Date'] = published_date.text
                        dictionary['Authors'] = author_names
                        dictionary['Pureportal Profile Link'] = author_profile_links

                        # Adding all rows to a list
                        publication_results.append(dictionary)
                        break

            next_link = publications_soup.find("a", class_="nextLink")
            if not next_link:
                break
            print("There are additional articles to browse through, crawling next page contents.")
            pub_url = "https://pureportal.coventry.ac.uk" + next_link["href"]

    print("Crawling Completed.")

    print("Creating a CSV file to store all the records.")
    with open('records.csv', 'w', newline='', encoding="utf-8") as csv_file:
        field_names = ['Title of the Research Paper', 'Link to the Research Paper', 'Published Date', 'Authors',
                       'Pureportal Profile Link']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_writer.writeheader()
        for record in publication_results:
            csv_writer.writerow(record)
        csv_file.close()
    print("A file named records.csv has been generated.")


## Calling the Crawler function

publications_url = 'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/publications/'
profiles_url = 'https://pureportal.coventry.ac.uk/en/organisations/research-centre-for-computational-science-and-mathematical-modell/persons/'
website_url = 'https://pureportal.coventry.ac.uk'

# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)

while True:
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------------")
    user_input = input(
        "Below are your options to run the crawler. \n a. Run the crawler manually.(This will crawl the data now and create a csv file) \n b. Start the scheduler.(This will run every Sunday and will update the csv file with new entries. No manual input needed.)\n\n Make a your choice a or b and provide the same as input.\n").lower()
    if user_input == 'a':
        print("You selected to run the crawler manually.")
        crawler(publications_url, profiles_url)
        break
    elif user_input == 'b':
        print("You selected to schedule the crawler run.")
        while True:
            # Calculate the delay until the next Sunday
            now = datetime.datetime.now()
            delay = (7 - now.weekday()) % 7  # delay until next Sunday

            # Schedule the function to be called on the next Sunday
            scheduler.enter(delay * 24 * 60 * 60, 1, crawler, (publications_url, profiles_url))
            # Uncomment the below code for testing the scheduler. This executes after 20 seconds
            # scheduler.enter(20, 1, crawler, (publications_url, profiles_url))

            # Starting the scheduler
            scheduler.run()
            # Updating the Inverted Index with new data
            inverted_index()

            # Wait for the next event to be scheduled
            time.sleep(60)  # specified in seconds
    else:
        print("You gave an Invalid Input. \nPlease choose either (a) or (b).\n")
