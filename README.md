Hacker News Web Scraper
A beginner-friendly yet fully functional Python web scraper that autonomously extracts real-time data from Hacker News — one of the most widely read technology news aggregators on the internet. Built using industry-standard Python libraries, this project demonstrates core concepts in HTTP communication, HTML parsing, data extraction, error handling, and structured data export.

📌 Project Overview
This project was developed as a hands-on introduction to web scraping with Python. It programmatically visits Hacker News, downloads the page's HTML content, navigates the document structure to locate relevant data, and extracts up to 30 stories per run — including the story title, source domain, community score, and direct URL. All results are automatically saved to a .csv file that can be opened and analysed in Excel, Google Sheets, or any data tool of your choice.
The scraper is designed with absolute beginners in mind — every function is clearly named, every step is commented, and the output is immediate and visible both in the terminal and as a saved file.

⚙️ Features
1. Scrapes live data from Hacker News on every run — always fresh results.
2. Extracts 5 data points per story: rank, title, domain, score, and URL
3. Auto-exports to CSV — open directly in Excel or Google Sheets
4. Robust error handling — gracefully handles connection errors, timeouts, and HTTP failures
5. Beginner-readable code — every function and step is documented with comments
6. Timestamps every scrape — each row records exactly when it was scraped
7. Zero configuration needed — runs immediately after installing two libraries


🛠️ Tech Stack
Tool                Purpose
Python              Core programming language
requests            Sending HTTP requests to fetch web pages
BeautifulSoup4      Parsing and navigating HTML content
csv (built-in)      Writing structured data to CSV files
datetime (built-in) Timestamping each scraped record
os (built-in)       File path handling

📁 Project Structure
web-scraper/
│
├── web_scraper.py      # Main scraper script
├── results.csv         # Output file (auto-generated on run, not tracked by git)
├── .gitignore          # Excludes results.csv from version control
└── README.md           # Project documentation

🚀 Getting Started
Prerequisites
Make sure you have Python 3.x installed. You can verify by running:
                   bashpython --version
If Python is not installed, download it from python.org and ensure you tick "Add Python to PATH" during installation.
  ** Installation:**
1. Clone the repository:
         bashgit clone https://github.com/adiithi0510-alt/web-scraper.git
         cd web-scraper
2. Install the required libraries:
         bashpip install requests beautifulsoup4
3. Run the scraper:
         bashpython web_scraper.py

📊 Sample Output
Terminal:
==================================================
  Hacker News Web Scraper
==================================================

[1] Connecting to https://news.ycombinator.com ...
    Success! Page loaded. (Status code: 200)

[2] Parsing stories from the page ...
    Found 30 stories.

[3] Results:

#    Score        Title
--------------------------------------------------------------------------------
1    512 points   Someone built a solar-powered server that's been online for...
2    389 points   Why I stopped using Docker for local development...
3    301 points   A 25-year-old bug in the Linux kernel was finally fixed...
...

[4] Saving results to 'results.csv' ...
    Saved! File is at: C:\Users\YourName\web-scraper\results.csv
CSV file (results.csv):
ranktitledomainscorelinkscraped_at1Someone built a solar-powered...example.com512 pointshttps://...2026-05-20 10:30:002Why I stopped using Docker...blog.example.com389 pointshttps://...2026-05-20 10:30:00

🔧 Configuration
You can customise the scraper by editing these three variables at the top of web_scraper.py:
      pythonTARGET_URL  = "https://news.ycombinator.com"   # Website to scrape
      OUTPUT_FILE = "results.csv"                     # Output filename
      MAX_STORIES = 30                                # Number of stories to extract
To scrape page 2 of Hacker News, change TARGET_URL to:
      pythonTARGET_URL = "https://news.ycombinator.com?p=2"

🧩 How It Works
1. fetch_page(url) — Sends an HTTP GET request to the target URL with browser-like headers to avoid being blocked. Returns the raw HTML string, or None on failure.
2. parse_stories(html) — Feeds the HTML into BeautifulSoup. Locates every story row using the CSS selector tr.athing, then extracts the title, link, domain, and score from each row and its sibling row.
3. display_stories(stories) — Formats and prints the results as a clean table in the terminal.

🚧 Known Limitations
1. Only scrapes static HTML — websites that load content via JavaScript require additional tools like Selenium or Playwright.
2. Limited to one page per run by default (30 stories). Can be extended to loop through multiple pages.
3. If Hacker News updates their HTML structure, the CSS selectors in parse_stories() may need updating.
   
save_to_csv(stories, filename) — Writes all extracted data to a .csv file using Python's built-in csv.DictWriter.
load_and_display_csv(filename) — Reads back the saved CSV and prints a 5-row preview to confirm the file was written correctly.
main() — Orchestrates all the above steps in sequence, with clear numbered output at each stage.
