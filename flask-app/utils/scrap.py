import requests
def scrape(url):
    res = requests.get(url)
    return res.url

def webcrawl(url_list):
    scrap_url_list = []
    for url in url_list:
        scrap_url_list.append(scrape(url))
    return scrap_url_list