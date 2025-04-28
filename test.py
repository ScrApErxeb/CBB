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
    """
    Effectue une recherche sur DuckDuckGo et retourne les résultats HTML
    Args:
        query (str): Terme de recherche
        region (str): Région pour les résultats (ex: 'fr-fr')
        max_retries (int): Nombre maximal de tentatives
    Returns:
        str: Code HTML de la page de résultats
    """
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
            
            # Vérification du contenu retourné
            if "Aucun résultat" in response.text:
                return None
            if "DuckDuckGo" in response.text:  # Vérifie que c'est bien une page DDG
                return response.text
                
        except requests.exceptions.RequestException as e:
            print(f"Tentative {attempt + 1} échouée: {e}")
            if attempt < max_retries - 1:
                wait_time = random.uniform(2, 5)
                time.sleep(wait_time)
    
    return None

def parse_ddg_results(html):
    """
    Parse les résultats de recherche DuckDuckGo
    Args:
        html (str): Code HTML de la page de résultats
    Returns:
        list: Liste de dictionnaires contenant les résultats
    """
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    # Les résultats principaux
    result_blocks = soup.find_all('div', class_='result')
    
    for block in result_blocks:
        try:
            title_elem = block.find('a', class_='result__a')
            link_elem = block.find('a', class_='result__url')
            desc_elem = block.find('a', class_='result__snippet')
            
            if not title_elem or not link_elem:
                continue
                
            # Nettoyage des liens (DDG ajoute souvent des préfixes)
            raw_link = link_elem['href']
            clean_link = raw_link.split('uddg=')[-1] if 'uddg=' in raw_link else raw_link
            
            results.append({
                'title': title_elem.get_text(strip=True),
                'url': clean_link,
                'description': desc_elem.get_text(strip=True) if desc_elem else "",
                'domain': link_elem.get_text(strip=True)
            })
        except Exception as e:
            print(f"Erreur lors du parsing d'un résultat: {e}")
            continue
    
    return results

def ddg_search(query, region='fr-fr', max_results=10, delay=2):
    """
    Fonction principale pour effectuer une recherche complète
    Args:
        query (str): Terme de recherche
        region (str): Région pour les résultats
        max_results (int): Nombre maximal de résultats à retourner
        delay (int): Délai minimum entre les requêtes
    Returns:
        list: Résultats formatés
    """
    time.sleep(delay)  # Respect du délai entre requêtes
    
    html = search_duckduckgo(query, region=region)
    if not html:
        return []
    
    results = parse_ddg_results(html)
    return results[:max_results]

# Exemple d'utilisation
if __name__ == "__main__":
    search_query = "python web scraping"
    print(f"Recherche DuckDuckGo pour: '{search_query}'\n")
    
    search_results = ddg_search(search_query)
    
    if not search_results:
        print("Aucun résultat trouvé ou erreur lors de la recherche.")
    else:
        for i, result in enumerate(search_results, 1):
            print(f"{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   Description: {result['description']}")
            print(f"   Domaine: {result['domain']}\n")