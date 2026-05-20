"""
Web Scraper - Beginner Project
===============================
Scrapes headlines, links, and scores from Hacker News (news.ycombinator.com)
and saves results to a CSV file you can open in Excel or Google Sheets.

Author: You!
"""

import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime


# ─────────────────────────────────────────
# SETTINGS — change these if you want
# ─────────────────────────────────────────
TARGET_URL = "https://news.ycombinator.com"   # website to scrape
OUTPUT_FILE = "results.csv"                    # file to save results
MAX_STORIES = 30                               # how many stories to scrape


def fetch_page(url):
    """
    Downloads the HTML of a webpage and returns it.
    If something goes wrong (no internet, bad URL), it tells you clearly.
    """
    print(f"\n[1] Connecting to {url} ...")

    try:
        # Send a GET request (like visiting the page in a browser)
        # headers makes the request look like a real browser visit
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)

        # raise_for_status() will crash (on purpose) if the site returned an error
        response.raise_for_status()

        print(f"    Success! Page loaded. (Status code: {response.status_code})")
        return response.text   # returns the raw HTML as a string

    except requests.exceptions.ConnectionError:
        print("    ERROR: Could not connect. Check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("    ERROR: The website took too long to respond.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"    ERROR: Website returned an error: {e}")
        return None


def parse_stories(html):
    """
    Takes the raw HTML and extracts the story title, link, score, and rank.
    Returns a list of dictionaries, one per story.
    """
    print("\n[2] Parsing stories from the page ...")

    # BeautifulSoup reads the HTML and lets us search through it easily
    soup = BeautifulSoup(html, "html.parser")

    stories = []

    # On Hacker News, each story row has class "athing"
    story_rows = soup.select("tr.athing")

    for rank, row in enumerate(story_rows[:MAX_STORIES], start=1):

        # ── Title and link ──────────────────────────────
        title_tag = row.select_one(".titleline > a")
        if not title_tag:
            continue   # skip if we couldn't find a title

        title = title_tag.get_text(strip=True)
        link  = title_tag.get("href", "No link")

        # Some links are relative (e.g. "item?id=123"), make them absolute
        if link.startswith("item?"):
            link = TARGET_URL + "/" + link

        # ── Score (points) ──────────────────────────────
        # The score is in the NEXT table row (sibling row), not the same one
        next_row   = row.find_next_sibling("tr")
        score_tag  = next_row.select_one(".score") if next_row else None
        score      = score_tag.get_text(strip=True) if score_tag else "0 points"

        # ── Domain ─────────────────────────────────────
        site_tag   = row.select_one(".sitestr")
        domain     = site_tag.get_text(strip=True) if site_tag else "news.ycombinator.com"

        # ── Timestamp ──────────────────────────────────
        scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Build a dictionary for this story and add it to the list
        stories.append({
            "rank":       rank,
            "title":      title,
            "domain":     domain,
            "score":      score,
            "link":       link,
            "scraped_at": scraped_at,
        })

    print(f"    Found {len(stories)} stories.")
    return stories


def display_stories(stories):
    """
    Prints the scraped stories neatly in the terminal.
    """
    print("\n[3] Results:\n")
    print(f"{'#':<4} {'Score':<12} {'Title'}")
    print("-" * 80)

    for s in stories:
        # Truncate long titles so they fit on one line
        short_title = s["title"][:60] + "..." if len(s["title"]) > 60 else s["title"]
        print(f"{s['rank']:<4} {s['score']:<12} {short_title}")

    print("-" * 80)


def save_to_csv(stories, filename):
    """
    Saves the scraped stories to a CSV file.
    You can open this file in Excel, Google Sheets, or any spreadsheet app.
    """
    print(f"\n[4] Saving results to '{filename}' ...")

    # fieldnames defines the column order in the CSV
    fieldnames = ["rank", "title", "domain", "score", "link", "scraped_at"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()       # writes the column headers on the first row
        writer.writerows(stories)  # writes all story rows

    # Get absolute path so user knows exactly where the file is
    abs_path = os.path.abspath(filename)
    print(f"    Saved! File is at: {abs_path}")


def load_and_display_csv(filename):
    """
    Reads back the CSV file and prints the first 5 rows as a preview.
    This proves the file was saved correctly.
    """
    print(f"\n[5] Preview of saved CSV (first 5 rows):\n")

    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 5:
                break
            print(f"  Row {i+1}: Rank {row['rank']} | {row['score']} | {row['title'][:50]}")


# ─────────────────────────────────────────
# MAIN — this runs when you execute the file
# ─────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Hacker News Web Scraper")
    print("=" * 50)

    # Step 1: Download the HTML
    html = fetch_page(TARGET_URL)
    if html is None:
        print("\nScraping failed. Please check your internet and try again.")
        return

    # Step 2: Extract the stories from the HTML
    stories = parse_stories(html)
    if not stories:
        print("\nNo stories found. The website layout may have changed.")
        return

    # Step 3: Display results in the terminal
    display_stories(stories)

    # Step 4: Save to CSV
    save_to_csv(stories, OUTPUT_FILE)

    # Step 5: Preview the CSV
    load_and_display_csv(OUTPUT_FILE)

    print(f"\nDone! Scraped {len(stories)} stories from {TARGET_URL}")
    print(f"Open '{OUTPUT_FILE}' in Excel or Google Sheets to explore your data.\n")


if __name__ == "__main__":
    # This line means: only run main() if YOU run this file directly.
    # If another script imports this file, main() won't run automatically.
    main()
