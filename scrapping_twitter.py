import snscrape.modules.twitter as sntwitter
import pandas as pd

# List of keywords
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

# Create a list to store all tweets
tweets = []

# Loop through each keyword
for keyword in keywords:
    print(f"Scraping tweets for keyword: {keyword}")
    # Use snscrape to collect tweets
    for tweet in sntwitter.TwitterSearchScraper(f'"{keyword}"').get_items():
        if len(tweets) >= 1000:  # Stop when 100,000 tweets are collected
            break
        tweets.append([
            tweet.date, 
            tweet.content, 
            tweet.username, 
            tweet.likeCount, 
            tweet.retweetCount, 
            tweet.replyCount, 
            keyword
        ])

# Create a DataFrame from the collected tweets
df = pd.DataFrame(tweets, columns=["Date", "Tweet", "Username", "Likes", "Retweets", "Replies", "Keyword"])

# Save the DataFrame to a CSV file
df.to_csv("twitter_keywords.csv", index=False)

print("Scraping complete. Data saved to twitter_keywords.csv.")
