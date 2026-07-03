#!/usr/bin/env python3
"""
fetch_linkedin_posts.py

A robust script to fetch, clean, and save the latest LinkedIn post for a given expert as Markdown.
"""

import os
import re
import sys
import argparse
import datetime
import html
import urllib.request

# Configuration of 10 Selected Experts (excluding Nico who has no LinkedIn)
EXPERTS = {
    "Matt Diggity": {"url": "https://www.linkedin.com/in/mattdiggityseo", "handle": "mattdiggityseo"},
    "Neil Patel": {"url": "https://www.linkedin.com/in/neilkpatel", "handle": "neilkpatel"},
    "Sam Oh": {"url": "https://www.linkedin.com/in/sam-o-84593014", "handle": "sam-o-84593014"},
    "Ryan Law": {"url": "https://www.linkedin.com/in/thinkingslow", "handle": "thinkingslow"},
    "WsCube Tech": {"url": "https://www.linkedin.com/company/wscubetechindia", "handle": "wscubetechindia"},
    "Julia McCoy": {"url": "https://www.linkedin.com/in/juliaemccoy", "handle": "juliaemccoy"},
    "Koray Tugberk GUBUR": {"url": "https://www.linkedin.com/in/koray-tugberk-gubur", "handle": "koray-tugberk-gubur"},
    "Mike King": {"url": "https://www.linkedin.com/in/michaelkingphilly", "handle": "michaelkingphilly"},
    "Simon Scrapes": {"url": "https://www.linkedin.com/in/simon-coton-81608b98", "handle": "simon-coton-81608b98"},
    "Eric Siu": {"url": "https://www.linkedin.com/in/ericosiu", "handle": "ericosiu"}
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "research", "linkedin-posts")


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def get_activity_id(url):
    match = re.search(r"activity-(\d+)", url)
    return int(match.group(1)) if match else 0


def fetch_latest_post(name):
    if name not in EXPERTS:
        print(f"Error: Unknown expert '{name}'", file=sys.stderr)
        return False
        
    info = EXPERTS[name]
    profile_url = info["url"]
    handle = info["handle"]
    expert_slug = slugify(name)
    
    print(f"Fetching profile for {name} ({profile_url})...")
    req = urllib.request.Request(profile_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            profile_html = r.read().decode("utf-8", errors="replace")
            
        # Find all post URLs on the page
        all_posts = re.findall(r"href=\"(https://www\.linkedin\.com/posts/[^\"]+)\"", profile_html)
        
        # Filter posts belonging to this handle
        filtered_posts = [u for u in all_posts if handle.lower() in u.lower()]
        unique_posts = list(set(filtered_posts))
        
        if not unique_posts:
            # Fall back to any unique post URL on the page just in case handle is spelled differently in post paths
            filtered_posts = [u for u in all_posts if "activity-" in u]
            unique_posts = list(set(filtered_posts))
            
        if not unique_posts:
            print(f"  Error: No posts found on profile for {name}", file=sys.stderr)
            return False
            
        # Sort by activity ID (largest is newest)
        unique_posts.sort(key=get_activity_id, reverse=True)
        latest_post_url = unique_posts[0]
        
        print(f"  Latest post URL: {latest_post_url}")
        
        # Fetch the latest post page
        post_req = urllib.request.Request(latest_post_url, headers=HEADERS)
        with urllib.request.urlopen(post_req, timeout=15) as pr:
            post_html = pr.read().decode("utf-8", errors="replace")
            
        # Extract post text from attributed-text-segment-list__content tag
        segments = re.findall(r"<p[^>]*class=\"[^\"]*attributed-text-segment-list__content[^\"]*\"[^>]*>(.*?)</p>", post_html, re.DOTALL)
        
        # Fallback to general meta or title tag if segment extraction fails
        if not segments:
            # Look inside <span class="sr-only">
            segments = re.findall(r"<span[^>]*class=\"[^\"]*sr-only[^\"]*\"[^>]*>(.*?)</span>", post_html, re.DOTALL)
            
        if not segments:
            print(f"  Error: Failed to parse post text for {name}", file=sys.stderr)
            return False
            
        # Clean HTML tags and unescape entities
        post_text = html.unescape(re.sub(r"<[^>]+>", "", segments[0])).strip()
        
        # Save to markdown file
        expert_dir = os.path.join(OUTPUT_DIR, expert_slug)
        os.makedirs(expert_dir, exist_ok=True)
        
        file_path = os.path.join(expert_dir, "post1.md")
        date_str = datetime.date.today().strftime("%Y-%m-%d")
        
        content = f"""# LinkedIn Post by {name}

- **Profile URL:** {profile_url}
- **Post URL:** {latest_post_url}
- **Date Scraped:** {date_str}

## Content

{post_text}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"  Saved to: {file_path}")
        return True
        
    except Exception as e:
        print(f"  Error processing {name}: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Fetch latest LinkedIn posts for experts.")
    parser.add_argument("--expert", required=True, help="Name of the expert to fetch.")
    args = parser.parse_args()
    
    success = fetch_latest_post(args.expert)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
