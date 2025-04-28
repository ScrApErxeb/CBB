# app/sources/internet/ddg.py

import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://duckduckgo.com/'
}

def search_duckduckgo(query, region='fr-fr', max_retries=3):
    base_url = "https://html.duckduckgo.com/html/"
    params = {
        'q': query,
        'kl': region,
        's': '0',
    }
    for attempt in range(max_retries):
        try:
            response = requests.post(
                base_url,
                data=params,
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()
            if "DuckDuckGo" in response.text:
                return response.text
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(random.uniform(2, 5))
    return None

def parse_ddg_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    result_blocks = soup.find_all('div', class_='result')

    for block in result_blocks:
        try:
            title_elem = block.find('a', class_='result__a')
            link_elem = block.find('a', class_='result__url')
            desc_elem = block.find('a', class_='result__snippet')

            if not title_elem or not link_elem:
                continue

            raw_link = link_elem['href']
            clean_link = raw_link.split('uddg=')[-1] if 'uddg=' in raw_link else raw_link

            results.append({
                'title': title_elem.get_text(strip=True),
                'url': clean_link,
                'description': desc_elem.get_text(strip=True) if desc_elem else "",
                'domain': link_elem.get_text(strip=True)
            })
        except Exception:
            continue

    return results

def ddg_search(query, region='fr-fr', max_results=10, delay=1.5):
    time.sleep(random.uniform(delay, delay + 1))
    html = search_duckduckgo(query, region=region)
    if not html:
        return []
    results = parse_ddg_results(html)
    return results[:max_results]
