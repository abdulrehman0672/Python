from bs4 import BeautifulSoup
import os

def extract_links(file_path):
    links = []
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    soup = BeautifulSoup(content, "html.parser")
    for product in soup.find_all('article', class_='product_pod'):
        h3 = product.find('h3')
        if h3:
            link = h3.find('a')
            if link and 'href' in link.attrs:
                links.append(link['href'])
    return links

file_path = "books/page_1.html"
book_links = extract_links(file_path)
print(book_links)