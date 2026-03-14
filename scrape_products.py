import requests
from bs4 import BeautifulSoup
import json
import time
import re

BASE_URL = "https://colophotoshop.com"
COLLECTION_URL = f"{BASE_URL}/collections/all"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_all_product_urls():
    product_urls = set()
    page = 1
    while True:
        url = f"{COLLECTION_URL}?page={page}"
        print(f"Finding products on page {page}...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # More robust selector: any <a> with /products/ in href
            links = soup.find_all('a', href=re.compile(r'/products/'))
            
            if not links:
                print(f"  No product links found on page {page}. Stopping.")
                break
                
            found_on_page = 0
            for a in links:
                href = a.get('href')
                if href:
                    # Remove query params like ?variant=...
                    clean_href = href.split('?')[0]
                    full_url = BASE_URL + clean_href if clean_href.startswith('/') else clean_href
                    if '/products/' in full_url and full_url not in product_urls:
                        product_urls.add(full_url)
                        found_on_page += 1
            
            print(f"  Found {found_on_page} new products (Total so far: {len(product_urls)})")
            
            if found_on_page == 0:
                print(f"  No NEW products found on page {page}. Stopping.")
                break
                
            # Check for next page
            # Shopify usually has a pagination element
            next_page = soup.find('a', class_=re.compile(r'pagination__item--next')) or \
                        soup.find('a', string=re.compile(r'Next'))
            
            if not next_page:
                # Fallback check: if we found products, try next page anyway until we find 0
                if found_on_page > 0:
                    page += 1
                    time.sleep(1)
                    continue
                else:
                    break
            
            page += 1
            time.sleep(1)
        except Exception as e:
            print(f"Error finding products on page {page}: {e}")
            break
        
    return list(product_urls)

def scrape_product(url):
    print(f"Scraping {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        name_tag = soup.find('h1')
        name = name_tag.text.strip() if name_tag else ""
        
        # Price
        # Shopify often has price in a specific schema or meta tag
        price_tag = soup.find('meta', property='og:price:amount') or \
                    soup.find('span', class_=re.compile(r'price-item--sale')) or \
                    soup.find('span', class_=re.compile(r'price-item--regular'))
        
        if price_tag and price_tag.name == 'meta':
            price = price_tag.get('content', '')
        else:
            price = price_tag.text.strip() if price_tag else ""
        
        # Image
        img_tag = soup.find('meta', property='og:image')
        img_url = img_tag['content'] if img_tag else ""
        
        # Description
        desc_tag = soup.find('meta', property='og:description')
        desc = desc_tag['content'] if desc_tag else ""
        
        # Fallback for description if meta is empty or too short
        if not desc or len(desc) < 20:
            desc_div = soup.find('div', class_=re.compile(r'product__description'))
            if desc_div:
                desc = desc_div.text.strip()
        
        return {
            "name": name,
            "price": price,
            "image_url": img_url,
            "description": desc,
            "url": url
        }
    except Exception as e:
        print(f"  Error scraping {url}: {e}")
        return None

def main():
    urls = get_all_product_urls()
    print(f"Discovered {len(urls)} products. Starting scrape...")
    
    products = []
    for url in urls:
        data = scrape_product(url)
        if data:
            products.append(data)
        time.sleep(0.5)
        
    with open('products_data.json', 'w') as f:
        json.dump(products, f, indent=4)
    
    print(f"Done. Saved {len(products)} products to products_data.json")

if __name__ == '__main__':
    main()
