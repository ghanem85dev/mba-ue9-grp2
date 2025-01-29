import requests
import csv

# Clé API de News API
api_key = '57c1752cb4d24941baa7a2eac2615c03'

# Liste des mots-clés
keywords = [
    "conspiracy", "complot", "pandemic", "antiVaccine",
    "bigPharma", "covid", "lockdown", "immune system",
    "mRNA", "population control", "plandemic", "bioweapon",
    "gene therapy", "side effects", "health risks"
]

# Configuration des paramètres de requête
query_params = {
    #'language': 'en',          # Limiter à l'anglais
    'from': '2024-12-28',      # Articles à partir de cette date
    'to': '2025-01-28',        # Articles jusqu'à cette date
    'sortBy': 'relevancy'      # Trier par pertinence
}

# Fonction pour récupérer les articles
def fetch_articles(keyword):
    url = f'https://newsapi.org/v2/everything?q={keyword}&apiKey={api_key}'
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching articles for keyword '{keyword}': {response.status_code} - {response.text}")
        return None

# Fonction pour extraire les données pertinentes
def extract_article_data(article):
    return {
        'date': article['publishedAt'],
        'author': article.get('author', 'N/A'),
        'title': article['title'],
        'url': article['url'],
        'keywords': [keyword for keyword in keywords if keyword in article['title'].lower()]
    }

# Fonction principale pour récupérer et sauvegarder les articles
def main():
    all_articles = []
    for keyword in keywords:
        articles_data = fetch_articles(keyword)
        if articles_data and 'articles' in articles_data:
            for article in articles_data['articles']:
                all_articles.append(extract_article_data(article))
        else:
            print(f"No articles found for keyword '{keyword}'")

    # Sauvegarde des résultats dans un fichier CSV
    with open('articles10.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'author', 'title', 'url', 'keywords']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in all_articles:
            writer.writerow(article)

if __name__ == '__main__':
    main()
