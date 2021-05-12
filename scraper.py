import requests
from bs4 import BeautifulSoup
import string
import os


url = 'https://www.nature.com/nature/articles'
r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
os.chdir('C:\\Users\\Admin\\PycharmProjects\\Web Scraper\\Web Scraper\\task')

def get_requests(num_of_pages=1, type_of_articles="News"):
    global url
    global r

    def find_the_article(num_of_pages, type_of_articles):
        soup = BeautifulSoup(r.content, 'html.parser')
        # Article here refers to the article tag
        find_article = soup.find_all('article')
        # For every <article> tag that soup finds
        for article in find_article:
            # Find a tag span inside the article tag
            article_type = article.find('span', class_="c-meta__type").text
    # If bare text between the <span> tags is the same as the article type passed by user
            if article_type == type_of_articles:
                # Execute this code
                h3 = article.find("h3")
                variable = h3.find('a')
                # Getting text from <a> tags
                article_name = variable.text
                article_body_url = variable.get('href')
# Changing the .txt file names to be titles of articles without spaces
                article_name = article_name.translate(str.maketrans('', '', string.punctuation))
                article_name = article_name.replace(" ", "_")

                url_to_write = 'https://www.nature.com' + article_body_url
                print(url_to_write)
                c = requests.get(url_to_write, headers={'Accept-Language': 'en-US,en;q=0.5'})
                soupp = BeautifulSoup(c.content, 'html.parser')
                try:
                    article_body = soupp.find("div", attrs={"class" : "article-item__body"}).text
                except AttributeError:
                    article_body = soupp.find("div", attrs={"class" : "article__body cleared"}).text
                    article_body_text_bytes = bytes(article_body, encoding='utf-8')
                else:
                    article_body_text_bytes = bytes(article_body, encoding='utf-8')
                with open(f'{article_name}.txt', 'wb') as file:
                    file.write(article_body_text_bytes)

                file.close()

    if num_of_pages > 1:
        # find_the_article(num_of_pages, type_of_articles)
        for page in range(1, num_of_pages + 1):
            additional_url = f'?searchType=journalSearch&sort=PubDate&page={page}'
            os.chdir('C:\\Users\\Admin\\PycharmProjects\\Web Scraper\\Web Scraper\\task')
            os.mkdir(f'Page_{page}')
            os.chdir('C:\\Users\\Admin\\PycharmProjects\\Web Scraper\\Web Scraper\\task' + f'\\Page_{page}')
            url = url + additional_url
            r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            find_the_article(num_of_pages, type_of_articles)

    else:
        os.mkdir('Page_1')
        os.chdir('C:\\Users\\Admin\\PycharmProjects\\Web Scraper\\Web Scraper\\task' + '\\Page_1')
        find_the_article(num_of_pages, type_of_articles)


get_requests(num_of_pages=int(input()), type_of_articles=str(input()))
print("Saved all articles.")
