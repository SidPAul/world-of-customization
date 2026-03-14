import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = "https://moderngifts.in"
COLLECTION_URL = f"{BASE_URL}/collections/all"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

STATIONERY_KEYWORDS = ['pen', 'diary', 'notebook', 'pencil', 'pouch', 'stationery', 'desk', 'folder', 'clipboard', 'stamp']

def get_stationery_urls(limit=20):
    product_urls = set()
    page = 1
    while len(product_urls) < limit:
        url = f"{COLLECTION_URL}?page={page}"
        print(f"Finding stationery products on page {page}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = soup.find_all('a', href=re.compile(r'/products/'))
            
            if not links:
                break
                
            found_on_page = 0
            for a in links:
                href = a.get('href')
                name_text = a.text.lower()
                if href:
                    clean_href = href.split('?')[0]
                    full_url = BASE_URL + clean_href if clean_href.startswith('/') else clean_href
                    if '/products/' in full_url and full_url not in product_urls:
                        if any(k in clean_href.lower() or k in name_text for k in STATIONERY_KEYWORDS):
                            product_urls.add(full_url)
                            found_on_page += 1
                            if len(product_urls) >= limit:
                                break
            
            print(f"  Discovered {found_on_page} stationery products (Total: {len(product_urls)})")
            
            if page > 20: # Search deeper since stationery might be sparse
                break
            page += 1
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            break
        
    return list(product_urls)

def scrape_product(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        name_tag = soup.find('h1')
        name = name_tag.text.strip() if name_tag else ""
        
        price_tag = soup.find('meta', property='og:price:amount') or \
                    soup.find('span', class_=re.compile(r'price-item--sale')) or \
                    soup.find('span', class_=re.compile(r'price-item--regular'))
        
        if price_tag and price_tag.name == 'meta':
            price = price_tag.get('content', '')
        else:
            price = price_tag.text.strip() if price_tag else ""
        
        img_tag = soup.find('meta', property='og:image')
        img_url = img_tag['content'] if img_tag else ""
        
        desc_tag = soup.find('meta', property='og:description')
        desc = desc_tag['content'] if desc_tag else ""
        
        return {
            "name": name,
            "price": price,
            "image_url": img_url,
            "description": desc,
            "url": url
        }
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    urls = get_stationery_urls(limit=15)
    products = []
    for url in urls:
        data = scrape_product(url)
        if data:
            products.append(data)
        time.sleep(0.5)
        
    with open('stationery_products.json', 'w') as f:
        json.dump(products, f, indent=4)
    print(f"Done. Saved {len(products)} stationery products.")

if __name__ == '__main__':
    main()
