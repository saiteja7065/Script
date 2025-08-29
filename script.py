import requests
from bs4 import BeautifulSoup
import json
import csv
import time

def scrape_olx_car_covers():
    url = 'https://www.olx.in/items/q-car-cover'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = []
        listings = soup.find_all('div', class_='_1m8bBz')
        
        for listing in listings:
            try:
                title = listing.find('span', class_='_3vEEm').text.strip() if listing.find('span', class_='_3vEEm') else 'N/A'
                price = listing.find('span', class_='_1YYK_').text.strip() if listing.find('span', class_='_1YYK_') else 'N/A'
                location = listing.find('span', class_='_3hJWx').text.strip() if listing.find('span', class_='_3hJWx') else 'N/A'
                link_elem = listing.find('a', href=True)
                link = 'https://www.olx.in' + link_elem['href'] if link_elem else 'N/A'
                
                results.append({
                    'title': title,
                    'price': price,
                    'location': location,
                    'link': link
                })
            except Exception as e:
                continue
        
        # Save to CSV file
        with open('olx_car_covers.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'location', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        
        print(f'Scraped {len(results)} car cover listings and saved to olx_car_covers.csv')
        return results
        
    except Exception as e:
        print(f'Error scraping OLX: {e}')
        return []

if __name__ == '__main__':
    scrape_olx_car_covers()
```


