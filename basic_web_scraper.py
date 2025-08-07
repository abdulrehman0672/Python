import requests

def scrape_pages():
    for page in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successfully fetched page {page}")
            with open(f"books/page_{page}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
        else:
            print(f"Failed to fetch page {page}, status code: {response.status_code}")
        
scrape_pages()




