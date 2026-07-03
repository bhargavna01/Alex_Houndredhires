#!/usr/bin/env python3
"""
fetch_transcripts.py

A robust script to fetch, clean, and format YouTube video transcripts as Markdown.
Supports single video URL/ID processing as well as batch processing for a pre-defined list of experts.

Dependencies:
    youtube-transcript-api (pip install youtube-transcript-api)
"""

import os
import re
import sys
import argparse
import datetime
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# Define default output directory relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "research", "youtube-transcripts")

# Top 10 Selected Experts configuration with pre-resolved Channel IDs
EXPERTS = {
    "Matt Diggity": {"url": "https://www.youtube.com/MattDiggity", "channel_id": "UCP5A5lVxaT7cO_LehpxjTZg"},
    "Neil Patel": {"url": "https://youtube.com/@neilpatel", "channel_id": "UCl-Zrl0QhF66lu1aGXaTbfw"},
    "Ahrefs": {"url": "https://www.youtube.com/AhrefsCom", "channel_id": "UCWquNQV8Y0_defMKnGKrFOQ"},
    "Nico (AI Ranking)": {"url": "https://www.youtube.com/@Nico_AIRanking/", "channel_id": "UCWD0OMrAWdSUan3Hh_q9QCA"},
    "WsCube Tech": {"url": "https://youtube.com/@wscubetech", "channel_id": "UC0T6MVd3wQDB5ICAe45OxaQ"},
    "Julia McCoy": {"url": "https://www.youtube.com/juliamccoy", "channel_id": "UCqzK60-oUOEq36uU9B1MMUg"},
    "Koray Tugberk Gugur": {"url": "https://www.youtube.com/@TopicalAuthority", "channel_id": "UCXTg_CjVldLQ1RH8jxTTqiw"},
    "Mike King (iPullRank)": {"url": "https://www.youtube.com/@iPullRankSEO/", "channel_id": "UCttOymj_FLE8d7xA7rEbsTw"},
    "Simon Scrapes": {"url": "https://www.youtube.com/@simonscrapes", "channel_id": "UCdCR4-uYOg5ju-IUuDnfnQA"},
    "Leveling Up with Eric Siu": {"url": "https://www.youtube.com/@LevelingUpOfficial", "channel_id": "UC3owDdLk7HL1dyQnkoBuRew"}
}

# Standard browser headers to prevent bot-blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


def slugify(text):
    """
    Convert a string into a clean, URL-safe slug.
    """
    text = text.lower()
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text)
    # Remove leading/trailing hyphens
    text = text.strip("-")
    return text


def extract_video_id(url_or_id):
    """
    Extract the 11-character YouTube Video ID from a URL or validate a raw ID.
    """
    url_or_id = url_or_id.strip()
    if len(url_or_id) == 11 and re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id

    patterns = [
        r"(?:v=|\/v\/|embed\/|shorts\/|youtu\.be\/|\/embed\/|\/watch\?v=|\/watch\?.+&v=)([^#&?]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            vid = match.group(1)
            if len(vid) == 11:
                return vid
    return None


def fetch_video_title(video_id):
    """
    Scrape the video title from the YouTube watch page HTML.
    """
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8", errors="replace")
            # Parse title from og:title meta tag or title tag
            meta_match = re.search(r'meta property="og:title" content="([^"]+)"', html)
            if meta_match:
                return meta_match.group(1).replace(" - YouTube", "")
            
            title_match = re.search(r"<title>(.*?)</title>", html)
            if title_match:
                return title_match.group(1).replace(" - YouTube", "")
    except Exception as e:
        print(f"Warning: Failed to fetch video title for {video_id}: {e}", file=sys.stderr)
    
    return f"YouTube Video {video_id}"


def get_channel_id(channel_url):
    """
    Scrape the YouTube channel page to find the unique channel ID (UC...).
    """
    req = urllib.request.Request(channel_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode("utf-8", errors="replace")
            
            # 1. Search for RSS feed URL (very reliable)
            rss_matches = re.findall(r'href="https://www.youtube.com/feeds/videos.xml\?channel_id=(UC[a-zA-Z0-9_-]+)"', html)
            if rss_matches:
                return rss_matches[0]
            
            # 2. Search for og:url channel link
            og_url_matches = re.findall(r'meta property="og:url" content="https://www.youtube.com/channel/(UC[a-zA-Z0-9_-]+)"', html)
            if og_url_matches:
                return og_url_matches[0]
            
            # 3. Search for raw channelId in JSON structures
            json_matches = re.findall(r'"channelId":"(UC[a-zA-Z0-9_-]+)"', html)
            if json_matches:
                return json_matches[0]
                
    except Exception as e:
        print(f"Error resolving channel URL {channel_url}: {e}", file=sys.stderr)
    return None


def fetch_channel_videos(channel_id):
    """
    Fetch latest videos from a YouTube channel using its RSS feed.
    Returns a list of tuples: (title, video_id, url)
    """
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(rss_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            namespaces = {
                "atom": "http://www.w3.org/2005/Atom",
                "yt": "http://www.youtube.com/xml/schemas/2015"
            }
            
            entries = root.findall("atom:entry", namespaces)
            videos = []
            for entry in entries:
                title = entry.find("atom:title", namespaces).text
                video_id = entry.find("yt:videoId", namespaces).text
                link = entry.find("atom:link", namespaces).attrib.get("href", "")
                
                # Filter out Shorts to get high-quality content
                is_short = "/shorts/" in link or "#shorts" in title.lower()
                if not is_short:
                    videos.append((title, video_id, link))
            return videos
    except Exception as e:
        print(f"Error fetching RSS feed for channel {channel_id}: {e}", file=sys.stderr)
    return []


def remove_consecutive_duplicates(text):
    words = text.split()
    n = len(words)
    i = 0
    cleaned_words = []
    while i < n:
        found_dup = False
        for pl in range(1, min(20, (n - i) // 2 + 1)):
            pattern = words[i:i+pl]
            copies = 1
            while i + (copies + 1) * pl <= n and words[i + copies * pl : i + (copies + 1) * pl] == pattern:
                copies += 1
            if copies > 1:
                cleaned_words.extend(pattern)
                i += copies * pl
                found_dup = True
                break
        if not found_dup:
            cleaned_words.append(words[i])
            i += 1
    return " ".join(cleaned_words)


def fetch_transcript_fallback(video_id):
    """
    Fallback method to fetch and parse transcripts from a free online service
    if the local IP is blocked by YouTube.
    """
    url = f"https://youtube-transcript.ai/transcript/{video_id}.txt"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode("utf-8", errors="replace")
        
        parts = text.split("## Transcript")
        if len(parts) < 2:
            raise Exception("No transcript marker found in fallback response")
        
        raw_lines = parts[1].strip().split("\n")
        transcript_data = []
        
        for line in raw_lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r"^\[(\d+):(\d+)(?::(\d+))?\]\s*(.*)$", line)
            if match:
                h_or_m = int(match.group(1))
                m_or_s = int(match.group(2))
                s = match.group(3)
                content = match.group(4).strip()
                
                if s is not None:
                    start = h_or_m * 3600 + m_or_s * 60 + int(s)
                else:
                    start = h_or_m * 60 + m_or_s
                
                # Apply deduplication to clean up repeated phrases
                content = remove_consecutive_duplicates(content)
                
                transcript_data.append({
                    "text": content,
                    "start": start,
                    "duration": 5.0
                })
        return transcript_data
    except Exception as e:
        raise Exception(f"Fallback API failed: {e}")


def fetch_transcript_supadata(video_id, api_key):
    """
    Fetch transcript using the Supadata API.
    """
    import json
    import time
    
    url = f"https://api.supadata.ai/v1/transcript?url=https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(
        url,
        headers={
            "x-api-key": api_key,
            "User-Agent": "Mozilla/5.0"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            res_data = json.loads(r.read().decode("utf-8"))
            
        status = res_data.get("status")
        
        # Handle asynchronous jobs if returned
        job_id = res_data.get("jobId")
        if job_id and status in ("queued", "active"):
            poll_url = f"https://api.supadata.ai/v1/transcript/{job_id}"
            print(f"  Note: Supadata job is {status}. Polling for completion...")
            for attempt in range(12):  # poll for up to 36 seconds
                time.sleep(3)
                poll_req = urllib.request.Request(
                    poll_url,
                    headers={
                        "x-api-key": api_key,
                        "User-Agent": "Mozilla/5.0"
                    }
                )
                try:
                    with urllib.request.urlopen(poll_req, timeout=15) as pr:
                        res_data = json.loads(pr.read().decode("utf-8"))
                    status = res_data.get("status")
                    if status == "completed":
                        break
                    elif status == "failed":
                        raise Exception("Supadata transcript job failed")
                except Exception as poll_err:
                    print(f"    Polling attempt {attempt+1} warning: {poll_err}")
            
        if status == "completed":
            content = res_data.get("content", [])
            transcript_data = []
            for item in content:
                # offset and duration in supadata are in milliseconds, convert to seconds
                start = item.get("offset", 0) / 1000.0
                duration = item.get("duration", 0) / 1000.0
                text = item.get("text", "")
                transcript_data.append({
                    "text": text,
                    "start": start,
                    "duration": duration
                })
            return transcript_data
        else:
            raise Exception(f"Supadata job status: {status}")
            
    except Exception as e:
        raise Exception(f"Supadata API failed: {e}")


def fetch_transcript(video_id):
    """
    Download the English transcript (or fallback) using:
    1. Supadata API if SUPADATA_API_KEY environment variable is set.
    2. youtube-transcript-api (direct scraping).
    3. Fallback youtube-transcript.ai web API if rate-limited.
    """
    supadata_key = os.environ.get("SUPADATA_API_KEY")
    if supadata_key:
        print(f"  Note: Using Supadata API for video {video_id}...")
        try:
            return fetch_transcript_supadata(video_id, supadata_key)
        except Exception as e:
            print(f"  Supadata API warning: {e}. Falling back to standard methods...")

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        fetch_fn = getattr(YouTubeTranscriptApi, 'get_transcript', None)
        if fetch_fn is None:
            api_instance = YouTubeTranscriptApi()
            fetch_fn = api_instance.fetch
        
        # Try fetching English directly
        return fetch_fn(video_id, languages=["en"])
    except Exception as e:
        # Check if it was an IP block/rate limit, or transcript disabled
        e_str = str(e)
        is_ip_block = "blocking requests" in e_str or "Too Many Requests" in e_str or "IpBlocked" in e_str or "RequestBlocked" in e_str
        
        if is_ip_block:
            print(f"  Note: IP blocked by YouTube. Attempting fallback API for video {video_id}...")
            try:
                return fetch_transcript_fallback(video_id)
            except Exception as fb_err:
                print(f"  Fallback failed: {fb_err}")
        
        # If it was not an IP block or fallback failed, try to list and translate
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            list_fn = getattr(YouTubeTranscriptApi, 'list_transcripts', None)
            if list_fn is None:
                api_instance = YouTubeTranscriptApi()
                list_fn = api_instance.list
            
            transcript_list = list_fn(video_id)
            
            # Find a translatable transcript and translate to English
            for transcript in transcript_list:
                if transcript.is_translatable:
                    print(f"  Note: Translating transcript from {transcript.language} ({transcript.language_code}) to English")
                    return transcript.translate("en").fetch()
            
            # If nothing was translatable, return first available transcript
            for transcript in transcript_list:
                print(f"  Note: Falling back to original transcript in {transcript.language} ({transcript.language_code})")
                return transcript.fetch()
        except Exception as inner_e:
            # If everything else fails, try fallback API one last time as a hail mary
            if not is_ip_block:
                print(f"  Note: Standard API failed. Trying fallback API for video {video_id}...")
                try:
                    return fetch_transcript_fallback(video_id)
                except Exception as fb_err:
                    pass
            raise Exception(f"No transcripts found: {inner_e} (Original error: {e})")


def format_paragraphs(transcript_data):
    """
    Clean the transcript data and format it into readable paragraphs.
    Groups segments by time gaps, punctuation boundaries, or maximum word counts.
    """
    paragraphs = []
    current_paragraph = []
    current_word_count = 0
    prev_end = 0.0

    for entry in transcript_data:
        # Handle both dictionary (older library version) and object representations
        if isinstance(entry, dict):
            text = entry.get("text", "")
            start = entry.get("start", 0.0)
            duration = entry.get("duration", 0.0)
        else:
            text = getattr(entry, "text", "")
            start = getattr(entry, "start", 0.0)
            duration = getattr(entry, "duration", 0.0)
        
        if not text:
            continue
        
        text = text.strip()
        words = text.split()
        
        # Check if we should start a new paragraph
        time_gap = start - prev_end
        
        if current_paragraph:
            should_split = False
            # Pause in speech greater than 2 seconds
            if time_gap > 2.0:
                should_split = True
            # Accumulated word count is high (keeps paragraphs digestible)
            elif current_word_count > 100:
                should_split = True
            # End of a sentence and some progress made
            elif text[-1] in ('.', '?', '!') and current_word_count > 50:
                should_split = True
                
            if should_split:
                paragraphs.append(" ".join(current_paragraph))
                current_paragraph = []
                current_word_count = 0
        
        current_paragraph.append(text)
        current_word_count += len(words)
        prev_end = start + duration

    if current_paragraph:
        paragraphs.append(" ".join(current_paragraph))

    return "\n\n".join(paragraphs)


def save_transcript_markdown(video_title, video_id, expert_name, transcript_text):
    """
    Format and save the transcript as a Markdown file.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create filenames based on slugified expert name and video title
    expert_slug = slugify(expert_name)
    title_slug = slugify(video_title)
    filename = f"{expert_slug}-{title_slug}.md"
    file_path = os.path.join(OUTPUT_DIR, filename)
    
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    
    content = f"""# {video_title}

- **URL:** {video_url}
- **Channel/Expert:** {expert_name}
- **Date Fetched:** {date_str}

## Transcript

{transcript_text}
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Saved: {file_path}")
    return filename


def process_single_video(video_url_or_id, expert_name="YouTube Video"):
    """
    Process a single YouTube video.
    """
    video_id = extract_video_id(video_url_or_id)
    if not video_id:
        print(f"Error: Invalid YouTube video URL or ID: {video_url_or_id}", file=sys.stderr)
        return False
        
    print(f"Processing Video ID: {video_id}")
    video_title = fetch_video_title(video_id)
    print(f"Title: {video_title}")
    
    try:
        transcript_data = fetch_transcript(video_id)
        cleaned_text = format_paragraphs(transcript_data)
        filename = save_transcript_markdown(video_title, video_id, expert_name, cleaned_text)
        print(f"Success! Saved to {filename}")
        return True
    except Exception as e:
        print(f"Error processing video {video_id}: {e}", file=sys.stderr)
        return False


def run_batch_processing():
    """
    Batch process the 10 pre-defined expert channels to fetch transcripts for the 2 latest videos.
    """
    print("Starting batch processing for experts...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    summary = []
    
    for name, info in EXPERTS.items():
        channel_url = info["url"]
        channel_id = info.get("channel_id")
        
        print("=" * 60)
        print(f"Processing Expert: {name}")
        print(f"URL: {channel_url}")
        
        if not channel_id:
            channel_id = get_channel_id(channel_url)
        if not channel_id:
            print(f"  Result: Failed to resolve Channel ID for {name}")
            summary.append((name, "Failed to resolve Channel ID"))
            continue
            
        print(f"  Channel ID: {channel_id}")
        
        videos = fetch_channel_videos(channel_id)
        if not videos:
            print(f"  Result: No videos found or failed to parse feed.")
            summary.append((name, "No videos found"))
            continue
            
        print(f"  Found {len(videos)} long videos. Fetching latest 2...")
        
        successful_downloads = 0
        attempts = 0
        
        # Iterate over videos in feed until we get 2 successful transcriptions
        for title, vid, link in videos:
            if successful_downloads >= 2:
                break
                
            attempts += 1
            print(f"  [{attempts}] Fetching transcript for: {title} (ID: {vid})")
            
            try:
                transcript_data = fetch_transcript(vid)
                cleaned_text = format_paragraphs(transcript_data)
                save_transcript_markdown(title, vid, name, cleaned_text)
                successful_downloads += 1
            except Exception as e:
                print(f"    Failed: {e}")
                
        status = f"Successfully fetched {successful_downloads}/2 videos"
        print(f"  Result: {status}")
        summary.append((name, status))
        
    print("=" * 60)
    print("BATCH PROCESSING COMPLETE SUMMARY:")
    for name, status in summary:
        print(f"- {name}: {status}")


def main():
    parser = argparse.ArgumentParser(description="Fetch and format YouTube transcripts.")
    parser.add_argument("video_url_or_id", nargs="?", help="YouTube video URL or Video ID.")
    parser.add_argument("--expert", default="YouTube Video", help="Name of the expert/channel owner.")
    parser.add_argument("--batch", action="store_true", help="Batch fetch the 2 latest videos for pre-defined experts.")
    
    args = parser.parse_args()
    
    if args.batch:
        run_batch_processing()
    elif args.video_url_or_id:
        success = process_single_video(args.video_url_or_id, args.expert)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
