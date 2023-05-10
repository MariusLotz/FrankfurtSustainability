import requests
from bs4 import BeautifulSoup


def main():
    print("starting...")
    search_query = "banks in Frankfurt"
    url = f"https://www.google.com/search?q={search_query}"

    # Send a GET request to the Google search page
    response = requests.get(url)

    # Parse the HTML content of the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the search results on the page
    search_results = soup.find_all('div', class_='g')

    # Extract relevant information from the search results
    for result in search_results:
        title = result.find('h3').text
        link = result.find('a')['href']
        print(f"Title: {title}")
        print(f"Link: {link}")
        print("---")

if __name__=="__main__":
    main()