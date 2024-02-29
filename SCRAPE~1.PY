from bs4 import BeautifulSoup
import requests

# CONSTANTS:
LIMIT_OF_MAXIMUM_ARTICLES_TO_DATA_SCRAPE = 32
print(f"Generating {LIMIT_OF_MAXIMUM_ARTICLES_TO_DATA_SCRAPE} Articles... \n")

response = requests.get("https://news.ycombinator.com/news")
html_doc = response.text

soup = BeautifulSoup(html_doc, 'html.parser')

# initialize an empty list to store article information
articles_info = []

title1 = ""
url1 = ""
upvotes1 = ""

# finds the article rows by their unique class 'athing'
article_rows = soup.find_all('tr', class_='athing', limit=LIMIT_OF_MAXIMUM_ARTICLES_TO_DATA_SCRAPE)

for article_row in article_rows:
    # navigates to the title within each article row
    title_span = article_row.find('span', class_='titleline')
    if title_span:
        title_link = title_span.find('a')
        if title_link:
            title = title_link.text
            url = title_link['href']  # extract the URL

            # finds the next sibling of the article row which is a 'tr' containing the upvote information
            upvote_info = article_row.find_next_sibling('tr')
            upvote_span = upvote_info.find('span', class_='score') if upvote_info else None
            upvotes = int(upvote_span.text.split()[0]) if upvote_span else 0  # Defaults to 0 if no upvotes

            # appends a dictionary of the article's details to the list
            articles_info.append({'title': title, 'url': url, 'upvotes': upvotes})
        else:
            print("Title link not found.")
    else:
        print("Title span not found.")

# sort the articles by upvotes from highest to lowest
articles_info.sort(key=lambda x: x['upvotes'], reverse=True)

# print the sorted articles:
for i, article in enumerate(articles_info, start=1):
    print(f"Article #: {i}")
    print(f"Title of Article: {article['title']}")
    print(f"Article Link: {article['url']}")
    print(f"Upvotes Total: {article['upvotes']}\n")
    print("-" * 60)
    if i == 1:
        title1 = article['title']
        url1 = article['url']
        upvotes1 = article['upvotes']

print(f"The #1 Top article on this page with the most Upvotes (up to your Max limit) is:")
print(f"Title of Article: {title1}")
print(f"Article Link: {url1}")
print(f"Upvotes Total: {upvotes1}\n")
