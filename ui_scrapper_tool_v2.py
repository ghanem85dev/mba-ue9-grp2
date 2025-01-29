import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configure logging
logging.basicConfig(
    filename='archive_ph_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define the base URLs for media sources
base_urls = [
    "https://www.reuters.com",
    "https://www.nytimes.com",
    "https://www.washingtonpost.com",
    "https://www.statnews.com",
    "https://www.sciencenews.org",
    "https://www.fiercepharma.com",
    "https://www.theguardian.com",
    "https://www.bbc.com",
    "https://www.cnn.com",
    "https://www.aljazeera.com",
    "https://www.economist.com"
]

# Keywords for filtering relevant articles
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

# User-Agent list for rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
]

# Define the months and days for matrix
months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
days = list(range(1, 32))  # Assuming up to 31 days in a month
years = list(range(2010, 2024))  # 15 years of history

# Initialize results containers
article_counts = pd.DataFrame(0, index=pd.MultiIndex.from_product([years, months]), columns=days)
flat_results = []

# Function to fetch archived URLs with retries and delays
def fetch_archived_urls(base_url, max_pages=5, retries=5):
    archived_links = set()  # Use a set to store unique links
    for page in range(1, max_pages + 1):
        for attempt in range(retries):
            try:
                logging.info(f"Fetching archived URLs for {base_url}, page {page}, attempt {attempt + 1}/{retries}...")
                log_to_ui(f"Fetching URLs for {base_url}, page {page}, attempt {attempt + 1}/{retries}...")
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Referer": "https://archive.ph",
                    "Accept-Language": "en-US,en;q=0.9"
                }
                search_url = f"https://archive.ph/?q={base_url}&page={page}"
                response = requests.get(search_url, headers=headers, timeout=30)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    # Locate archive links
                    links = soup.find_all("a", href=True)
                    for link in links:
                        if "https://archive.ph/" in link['href']:
                            archived_links.add(link['href'])  # Add only unique links
                    logging.info(f"Found {len(links)} links on page {page}. Unique: {len(archived_links)}.")
                    log_to_ui(f"Found {len(links)} links on page {page}. Unique: {len(archived_links)}.")
                    break  # Exit retry loop on success
                elif response.status_code == 429:
                    logging.warning(f"Rate limit hit for {base_url} on page {page}. Retrying after delay...")
                    log_to_ui("Rate limit hit, retrying...")
                    time.sleep((attempt + 1) * random.uniform(5, 15))  # Exponential backoff
                else:
                    logging.warning(f"Failed to fetch archive search results for {base_url} on page {page}, status code: {response.status_code}")
                    log_to_ui(f"Failed to fetch page {page}, status code: {response.status_code}")
            except Exception as e:
                logging.error(f"Error fetching archived URLs for {base_url}, page {page}, attempt {attempt + 1}/{retries}: {e}")
                log_to_ui(f"Error: {e}")
                time.sleep((attempt + 1) * random.uniform(5, 15))  # Exponential backoff
    return list(archived_links)  # Convert back to list


# Pagination Logic for `archive.ph`
def fetch_paginated_archived_urls(base_url, start_date):
    next_page_url = f"https://archive.ph/?q={base_url}"
    archived_links = set()

    while next_page_url:
        headers = {"User-Agent": random.choice(user_agents)}
        response = requests.get(next_page_url, headers=headers, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("a", href=True)
            for article in articles:
                href = article['href']
                if "https://archive.ph/" in href:
                    date = extract_date_from_url(href)
                    if date and date >= start_date:
                        archived_links.add((href, date))
                    elif date and date < start_date:
                        logging.info("Reached date limit. Stopping pagination.")
                        return list(archived_links)

            # Find "Prior" button for pagination
            prior_button = soup.find("a", text="Prior")
            if prior_button and prior_button['href']:
                next_page_url = "https://archive.ph" + prior_button['href']
            else:
                logging.info("No more pages to paginate.")
                return list(archived_links)
        else:
            logging.warning(f"Failed to fetch page {next_page_url}")
            return list(archived_links)

    return list(archived_links)


# Function to extract date from an archived URL
def extract_date_from_url(url):
    try:
        parts = url.split('/')
        for part in parts:
            if part.isdigit() and len(part) == 8:  # YYYYMMDD format
                return f"{part[:4]}-{part[4:6]}-{part[6:]}"
    except Exception as e:
        logging.error(f"Error extracting date from URL {url}: {e}")
        log_to_ui(f"Error extracting date: {e}")
    return None

# Function to fetch article details (title, author, and keywords)
def fetch_article_details(url):
    try:
        headers = {"User-Agent": random.choice(user_agents)}
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else "No Title Found"
            author = "Unknown"
            author_tag = soup.find("meta", attrs={"name": "author"})
            if author_tag and author_tag.get("content"):
                author = author_tag.get("content")

            content = soup.get_text().lower()
            found_keywords = [kw for kw in keywords if kw in content]
            return title, author, ", ".join(found_keywords)
        else:
            return "No Title Found", "Unknown", ""
    except Exception as e:
        logging.error(f"Error fetching article details for URL {url}: {e}")
        log_to_ui(f"Error fetching details: {e}")
        return "Error Fetching Title", "Unknown", ""

# # Function to process archived URLs
# def process_archived_urls(base_url, max_pages=5):
    # archived_urls = fetch_archived_urls(base_url, max_pages=max_pages)
    # seen_urls = set()  # Track processed URLs to avoid duplicates
    # for entry in archived_urls:
        # if entry not in seen_urls:
            # title, author, found_keywords = fetch_article_details(entry)
            # flat_results.append({
                # "Base URL": base_url,
                # "Archived URL": entry,
                # "Archived Date": extract_date_from_url(entry),
                # "Article Title": title,
                # "Author": author,
                # "Keywords Found": found_keywords
            # })
            # seen_urls.add(entry)
        # else:
            # logging.info(f"Duplicate URL skipped: {entry}")
            
def process_archived_urls(base_url, start_date):
    archived_urls = fetch_paginated_archived_urls(base_url, start_date)
    seen_urls = set()  # Track processed URLs to avoid duplicates
    for url, date in archived_urls:
        if url not in seen_urls:
            title, author, found_keywords = fetch_article_details(url)
            flat_results.append({
                "Base URL": base_url,
                "Archived URL": url,
                "Archived Date": date,
                "Article Title": title,
                "Author": author,
                "Keywords Found": found_keywords
            })
            seen_urls.add(url)

            # Update the article count matrix
            year, month, day = int(date[:4]), months[int(date[5:7]) - 1], int(date[8:])
            if (year, month) in article_counts.index and day in article_counts.columns:
                article_counts.loc[(year, month), day] += 1
        else:
            logging.info(f"Duplicate URL skipped: {url}")

# Log messages to the UI
def log_to_ui(message):
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)

# Handle moving items between lists
def move_selection(source, target):
    selected = source.curselection()
    for i in selected[::-1]:
        item = source.get(i)
        source.delete(i)
        target.insert(tk.END, item)

def move_back_selection(source, target):
    selected = source.curselection()
    for i in selected[::-1]:
        item = source.get(i)
        source.delete(i)
        target.insert(tk.END, item)

# Create UI for input parameters
def start_scraper():
    max_pages = int(max_pages_entry.get())
    selected_base_urls = [chosen_base_urls_listbox.get(i) for i in range(chosen_base_urls_listbox.size())]
    selected_keywords = [chosen_keywords_listbox.get(i) for i in range(chosen_keywords_listbox.size())]
    start_year = int(start_year_entry.get())
    end_year = int(end_year_entry.get())

    # Extend keywords with synonyms
    if extend_keywords_var.get():
        selected_keywords = extend_keywords(selected_keywords)

    log_to_ui("Scraping started...")
    progress_var.set(0)
    for base_url in selected_base_urls:
        process_archived_urls(base_url, max_pages)

    # Save results to an Excel file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"archive_ph_scraper_results_{timestamp}.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        article_counts.to_excel(writer, sheet_name="Dashboard")
        pd.DataFrame(flat_results).to_excel(writer, sheet_name="Flat Results", index=False)
    log_to_ui(f"Scraping completed and results saved as {output_file}.")
    display_matrix()

# Extend keywords with synonyms
def extend_keywords(keywords):
    synonyms = {
        "pandemic": ["epidemic", "outbreak"],
        "lockdown": ["quarantine", "isolation"],
        "vaccine": ["immunization", "shot"],
    }
    extended_keywords = keywords[:]
    for keyword in keywords:
        if keyword in synonyms:
            extended_keywords.extend(synonyms[keyword])
    return extended_keywords

# Display the matrix in the UI
def display_matrix():
    matrix_window = tk.Toplevel(root)
    matrix_window.title("Matrix Results")

    text = scrolledtext.ScrolledText(matrix_window, wrap=tk.WORD, width=100, height=20)
    text.pack(expand=True, fill=tk.BOTH)

    for (year, month), row in article_counts.iterrows():
        line = f"{year} {month}: {row.sum()} articles\n"
        text.insert(tk.END, line)

# Generate and display visualizations
def generate_visualizations():
    fig, ax = plt.subplots(figsize=(10, 6))
    year_totals = article_counts.groupby(level=0).sum().sum(axis=1)
    year_totals.plot(kind="bar", ax=ax)
    ax.set_title("Total Articles per Year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Articles")

    viz_window = tk.Toplevel(root)
    viz_window.title("Visualizations")

    canvas = FigureCanvasTkAgg(fig, master=viz_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Create the main application window
root = tk.Tk()
root.title("Scraper Configuration")
root.configure(bg="#f0f8ff")

# Apply styles
def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")

    # Configure styles for widgets
    style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5, relief="raised", background="#add8e6")
    style.configure("TLabel", font=("Helvetica", 10), background="#f0f8ff")
    style.configure("TEntry", padding=5)
    style.configure("TProgressbar", thickness=10, background="#4682b4")

apply_styles()

# Frame for input parameters
frame = tk.Frame(root, padx=10, pady=10, bg="#f0f8ff")
frame.grid(row=0, column=0, sticky="nsew")

# Max pages input
tk.Label(frame, text="Max Pages:", bg="#f0f8ff", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
max_pages_entry = tk.Entry(frame, font=("Arial", 10))
max_pages_entry.grid(row=0, column=1, sticky="ew")
max_pages_entry.insert(0, "5")

# Base URLs selection
tk.Label(frame, text="Available Base URLs:", bg="#f0f8ff", font=("Arial", 10)).grid(row=1, column=0, sticky="nw")
base_urls_listbox = tk.Listbox(frame, selectmode="multiple", height=6, exportselection=False, font=("Arial", 10), bg="#ffffff")
for url in base_urls:
    base_urls_listbox.insert(tk.END, url)
base_urls_listbox.grid(row=1, column=1, sticky="ew")

chosen_base_urls_listbox = tk.Listbox(frame, selectmode="multiple", height=6, exportselection=False, font=("Arial", 10), bg="#ffffff")
chosen_base_urls_listbox.grid(row=1, column=3, sticky="ew")

add_base_url_button = ttk.Button(frame, text="Add >>", command=lambda: move_selection(base_urls_listbox, chosen_base_urls_listbox))
add_base_url_button.grid(row=1, column=2, pady=5)

remove_base_url_button = ttk.Button(frame, text="<< Remove", command=lambda: move_back_selection(chosen_base_urls_listbox, base_urls_listbox))
remove_base_url_button.grid(row=1, column=4, pady=5)

# Keywords selection
tk.Label(frame, text="Available Keywords:", bg="#f0f8ff", font=("Arial", 10)).grid(row=2, column=0, sticky="nw")
keywords_listbox = tk.Listbox(frame, selectmode="multiple", height=6, exportselection=False, font=("Arial", 10), bg="#ffffff")
for keyword in keywords:
    keywords_listbox.insert(tk.END, keyword)
keywords_listbox.grid(row=2, column=1, sticky="ew")

chosen_keywords_listbox = tk.Listbox(frame, selectmode="multiple", height=6, exportselection=False, font=("Arial", 10), bg="#ffffff")
chosen_keywords_listbox.grid(row=2, column=3, sticky="ew")

add_keyword_button = ttk.Button(frame, text="Add >>", command=lambda: move_selection(keywords_listbox, chosen_keywords_listbox))
add_keyword_button.grid(row=2, column=2, pady=5)

remove_keyword_button = ttk.Button(frame, text="<< Remove", command=lambda: move_back_selection(chosen_keywords_listbox, keywords_listbox))
remove_keyword_button.grid(row=2, column=4, pady=5)

# Extend keywords checkbox
extend_keywords_var = tk.BooleanVar()
extend_keywords_checkbox = ttk.Checkbutton(frame, text="Extend Keywords with Synonyms", variable=extend_keywords_var)
extend_keywords_checkbox.grid(row=3, column=1, sticky="w")

# Year range input
tk.Label(frame, text="Year Range:", bg="#f0f8ff", font=("Arial", 10)).grid(row=4, column=0, sticky="w")
tk.Label(frame, text="Start Year:", bg="#f0f8ff", font=("Arial", 10)).grid(row=4, column=1, sticky="w")
start_year_entry = tk.Entry(frame, font=("Arial", 10))
start_year_entry.grid(row=4, column=1, sticky="e")
start_year_entry.insert(0, "2010")
tk.Label(frame, text="End Year:", bg="#f0f8ff", font=("Arial", 10)).grid(row=5, column=1, sticky="w")
end_year_entry = tk.Entry(frame, font=("Arial", 10))
end_year_entry.grid(row=5, column=1, sticky="e")
end_year_entry.insert(0, "2023")

# Log output
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Arial", 10), bg="#ffffff", fg="#000000")
log_text.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")

# Progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

# Start button
start_button = ttk.Button(root, text="Start Scraper", command=start_scraper)
start_button.grid(row=3, column=0, pady=10)

# Visualizations button
viz_button = ttk.Button(root, text="Generate Visualizations", command=generate_visualizations)
viz_button.grid(row=4, column=0, pady=10)

# Run the application
root.mainloop()

