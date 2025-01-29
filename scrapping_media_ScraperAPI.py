import requests
from bs4 import BeautifulSoup
import csv
import random
import time

# Clé API de ScraperAPI
scraperapi_key = 'be38234f86bd882d23e903e99cf87c49'

# Liste des mots-clés
keywords = [
    "conspiracy", "conspiracies", "complot", "complotisme",
    "pandemic", "pandémie", "pandemi",
    "antiVaccine", "anti-vax", "antivax", "antiVaccin", "anti-vaccin", "antivaccin",
    "bigPharma", "big Pharma", "grandePharma", "grande Pharma",
    "coronavirus", "covid", "covid-19", "corona",
    "lockdown", "confinement",
    "immune system", "système immunitaire",
    "public health", "santé publique",
    "mRNA", "ARNm",
    "population control", "contrôle de la population",
    "plandemic", "plandémie",
    "bioweapon", "arme biologique",
    "gene therapy", "thérapie génique",
    "side effects", "effets secondaires",
    "health risks", "risques pour la santé"
]

# Liste des user-agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
]

# Liste des sources d'actualités
sources = [
    {'name': 'BBC News', 'url': 'https://www.bbc.com/search?q={keyword}'},
    {'name': 'The Guardian', 'url': 'https://www.theguardian.com/search?q={keyword}'},
    {'name': 'CNN', 'url': 'https://www.cnn.com/search?q={keyword}'},
    {'name': 'Reuters', 'url': 'https://www.reuters.com/search/news?blob={keyword}'},
    {'name': 'Le Monde', 'url': 'https://www.lemonde.fr/recherche/?search_keywords={keyword}'},
    {'name': 'New York Times', 'url': 'https://www.nytimes.com/search?query={keyword}'},
    {'name': 'Al Jazeera', 'url': 'https://www.aljazeera.com/search?q={keyword}'},
    {'name': 'Fox News', 'url': 'https://www.foxnews.com/search-results/search?q={keyword}'},
    {'name': 'NBC News', 'url': 'https://www.nbcnews.com/search/?q={keyword}'},
    {'name': 'Washington Post', 'url': 'https://www.washingtonpost.com/newssearch/?query={keyword}'}
]

# Fonction pour récupérer les articles avec ScraperAPI
def fetch_articles(source, keyword):
    url = source['url'].format(keyword=keyword)
    user_agent = random.choice(user_agents)
    headers = {'User-Agent': user_agent}
    scraperapi_url = f'http://api.scraperapi.com?api_key={scraperapi_key}&url={url}'
    try:
        response = requests.get(scraperapi_url, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error fetching articles for keyword '{keyword}' from {source['name']}: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request exception for keyword '{keyword}' from {source['name']}: {e}")
        return None

# Fonction pour extraire les données pertinentes
def extract_article_data(soup, source_name):
    articles = []
    if source_name == 'BBC News':
        for article in soup.find_all('div', class_='search-result'):
            title = article.find('h1').text if article.find('h1') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # BBC News n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'The Guardian':
        for article in soup.find_all('div', class_='fc-item__container'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # The Guardian n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'CNN':
        for article in soup.find_all('h3', class_='cd__headline'):
            title = article.text if article else 'N/A'
            date = 'N/A'  # CNN n'affiche pas toujours la date
            author = 'N/A'  # CNN n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'Reuters':
        for article in soup.find_all('div', class_='search-result-content'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # Reuters n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'Le Monde':
        for article in soup.find_all('article', class_='teaser'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # Le Monde n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'New York Times':
        for article in soup.find_all('li', class_='css-1l4w6pd'):
            title = article.find('h4').text if article.find('h4') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # New York Times n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'Al Jazeera':
        for article in soup.find_all('div', class_='search-result'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # Al Jazeera n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'Fox News':
        for article in soup.find_all('article', class_='article'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # Fox News n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'NBC News':
        for article in soup.find_all('div', class_='result-card'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # NBC News n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    elif source_name == 'Washington Post':
        for article in soup.find_all('div', class_='pb-feed-item'):
            title = article.find('h3').text if article.find('h3') else 'N/A'
            date = article.find('time').text if article.find('time') else 'N/A'
            author = 'N/A'  # Washington Post n'affiche pas toujours l'auteur
            url = article.find('a')['href'] if article.find('a') else 'N/A'
            keywords_found = [keyword for keyword in keywords if keyword in title.lower()]
            articles.append({
                'date': date,
                'author': author,
                'title': title,
                'url': url,
                'keywords': keywords_found
            })
    return articles

# Fonction principale pour récupérer et sauvegarder les articles
def main():
    all_articles = []
    for keyword in keywords:
        for source in sources:
            html = fetch_articles(source, keyword)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                articles = extract_article_data(soup, source['name'])
                all_articles.extend(articles)
            time.sleep(random.uniform(1, 3))  # Attendre entre 1 et 3 secondes pour éviter les blocages

    # Sauvegarde des résultats dans un fichier CSV
    with open('articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'author', 'title', 'url', 'keywords']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in all_articles:
            writer.writerow(article)

if __name__ == '__main__':
    main()
