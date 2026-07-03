#!/usr/bin/env python3
"""
YouTube Transcript Fetcher
==========================
Fetches the last 2 uploaded video transcripts from each YouTube channel
listed in sources.md, cleans the text, and saves as Markdown files.

Dependencies (install via pip):
    pip install youtube-transcript-api yt-dlp

Usage:
    python3 fetch_transcripts.py
    python3 fetch_transcripts.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
    python3 fetch_transcripts.py --video-id VIDEO_ID
"""

import argparse
import os
import re
import sys
import textwrap
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Path to the sources.md file
SOURCES_MD_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "sources.md",
)

# Output directory for transcript files
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def slug
Dependencies (install via pip):
    pip install youtube-transcrendly    pip install youtube-transcta
Usage:
    python3 fetch_transcripts.py
   nore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("import rf extract_channel_urls_from_md(md_path: str) -> list[dict]
# --------------------md # Configuration
# ----------------------------------------------------------ists(md_path):
        print(f"[WARN] sources.md not found at: {md_path}")
        return []

    channels = []
    current_name = None

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        name_match = re.match(r"^##

# ----------------------------------   if name_match:
  # Helpers
# ------------------------------------------------------------= re.s# ------           r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/(?:@?[\w-]+|channel/[\w-]+|c/[\w-]+)",
            line,
        )
        if url_match and current_name:
            url = url_match    pp(0).rstrip("/")
            channels.append({"name": current_name, "url": url})
            current_name = None

    return channels


def extract_video_id(url_or_id: str) -> str | None:
    """Extract YouTube video ID from a URL or return the ID if already clean."""
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url_or_id):
        return url_or_id
    match = re.search(r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([a-zA-Z0-9_-]{11})", url_or_id)
    if match:
        return match.group(1)
    return None


def get_channel_videos(channel_url: str, max_results: int = 2) -> list[dict]:
    """Use yt-dlp to fetch the most recent videos from a channel."""
    try:
        import yt_dlp
    except ImportError:
        print("[ERROR] yt-dlp is required. Ins            line,
        )
        if url_match and current_name:
            url = url_match    pp(0).rstrip("/")
            channels.append({"name": current_name, "url"_e        )
      ,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            if info is None:
                print(f"  [WARN] No info returned for {channel_url}")
                return []

            entries = info.get("entries", [])
            videos = []
            for entry in entries:
                if entry is None:
                    continue
                video_id = entry.get("id")
                title = entry.get("title", "Unknown Title")
                if video_id:
                    video_url     """Use yt-dlp to fetch the most recent videos from a channel."""
    tryppend({"id": video_id, "title": title, "url": video_url})
                if len(videos) >= max_results:
                    break
            return videos

    except Exception as e:
        print(f            url = url_match    pp(0).m {channel_url}: {e}")
        return []


def get_video_title(video_id: str) -> str:
    """Fetch the video title using yt-dlp."""
                       info = ydl.extract_info(channel_ur      return "Unknown Title"
    ydl_opts = {"quiet": True, "no_warnings": True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info.get("title", "Unknown Title")
    except Exception:
        return "Unknown Title"


def fetch_transcript(video_id: str) -> str | None:
    ""                if video_id:
                    video_urlan                    video_u      tryppend({"id": video_id, "title": title, "url": video_url})
                if len(videos) cri                if len(videos) >= max_results:
                                      break
            returvail            return  except
    except Exception print        print(f          ip        return []


def get_video_title(video_id: str) -> str:
    """Fet  

def get_video_        """Fetch the video title using tApi()
                        info = ydl.extract_inua    ydl_opts = {"quiet": True, "no_warnings": True}
    try:
        with yt_dlp.Yo       try:
        with yt_dlp.YoutubeDL(ydl_opts) ascriptsDisabled:
        print(f"  [WARN] Transcripts are disabled for video {video_id}")
        return None
    except NoTranscriptFound:
        print(f"  [WARN] No transcript found for video {video_id}")
        return None
    except VideoUnavailable:
        print(f"  [WARN] Video {video_id} is unavailable")
        return None
    except Exception as e:
        print(f"  [WARN] No English transcript available for video {video_id}: {e}")
        return None


def clean_transcript(raw_text: str) -> str:
    """Clean transcript text: remove artifacts, timestamps, format into paragraphs."""
    text = re.sub(r"\[.*?\]", "", raw_text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    sentences = re.split(r"(?<=[.!?])\s+", text)
    paragraphs = []
    current_paragraph = []
    sentence_count = 0

    for sentence in sentences:
              with yt_dlp.Youtubp()
            print(f"  [WARN] Transcripts are disabled for vit_        return None
    except NoTranscriptFound:
        print(f"  [Wenc    except NoTr             print(f"  [WARN] N".jo        return None
    except VideoUnavailable:
        prin           except Vidnt = 0        print(f"  aragraph:
         return None
    except Exception as e:
        pr      except Excepti(p        print(f"  [We_trans        return None


def clean_transcript(raw_text: str) -> str:
    """Clean tranpt

def clean_transctput    """Clean transcript text: remove artife     text = re.sub(r"\[.*?\]", "", raw_text)
    text = re.sub(r"<[^>]+>", "", text)
       text = re.sub(r"<[^>]+>", "", text)
  le    text = re.sub(r"\b\d{1,2}:\d{2}(?:n(    text = re.sub(r"\s+", " ", text).strip()

    sentencesip("-")
    filename = f"{expert_slug}-{title_slug}.md"
    filepath = os.path.join(output_dir, filename)

    md_content = f"""# {video_title}

**Expert:** {expert_name}
**Source:** {video_url}
**Transcript Date:** Fetched on demand

---

## Full Transcript

{transcript_text}

---

*Transcript fetched automatically by fetch_transcripts.py*
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  [SAVED] {filepath}")
        return filepath
    except Exception as e:
        print(f"  [ERROR] Failed to save transcript: {e}")
        return None


def process_single_video(
    video_url_or_id: str, output_dir: str = OUTPUT_DIR
) -> str | None:
    """Process a single video URL or ID and save its transcript."""
    video_id = extract_video_id(video_url_or_id)
    if       text = re.sub(r"<[^>]+>", "", ] I  le    text = re.sub(r"\b\d{1,2}:\d{2}(?d}
    sentencesip("-")
    filename = f"{expert_slug}-{title_slug}.md"
    filed}")
    tit    filename = f"{le(    filepath = os.path.join(output_dir, fil   tr
    md_content = f"""# {video_title}

**Experot tr
**Expert:** {expert_name}
 [FAIL] Cou**Source:** {vranscript fo**Transcript )
        r
---

## Full Transcript

{transcranscri
#(
 
{transcriptle-video",
        title,
        f"https://www.youtube.com/watch?v={video_id}",
        transcript,
        output_dir,
    )
    return filepath


def process_channel_videos(
    channel: dict, output_dir: str = OUTPUT_DIR, videos_per_channel: int = 2
):
    """Fetch the last N videos from a channel and save their transcripts."""
    name = channel["name"]
    url = channel["url"]

    ) -> str | None:
    """Process a single video URL or      """Process     {url}")
    print(f"{'='*70}")

    videos = get_channel_videos(url, max_results=videos_per_channel)
    if not videos:
        print(f"  [WARN] No videos found for {name}")
        return []

    print(f"  Found {len(videos)} recent video(s)")

    saved_files = []
    for i, video in enumerate(videos, 1):
        print(f"\n  --- Video {i}: {video['title']} ---")
        print(f"      ID: {video['id']}")

        transcript = fetch_transcript(video["id"])
        if transcript:
            filepath = save_transcript(
                name, video["title"], video["url"], transcript, output_dir
            )
            if filepath:
                saved_files.append(filepath)
        else:
               channel: dict, outranscr):
    """Fetch the last N videos from a channel and save their transcripts    p    name = channel["name"]
    url = channel["url"]

    ) -> str | None:
 ra    url = channel["url"]
do
    ) -> str       format    """Process a e.Ra    print(f"{'='*70}")

    videos = get_channel_videos(url, ma  
    vide Examples:
        if not videos:
        print(f"  [WARN] No videos found for {naal        print(m sou        return []

    print(f"  Found {len(vpts.py --
    print(//www.yo
    saved_files = []
    for i, video in        # Pr    for i, video ino         print(f"\n  --- Video {i}: {videipts.py --video-id dQw4w9WgXcQ
                  # Process a single video by ID
        """),
    )
    parser.add_argument("--url", type=str, help="Single YouTube video URL to process")
    parser.add_argument("--video-id", type=str, help="Single YouTube video ID to process")
    parser.add_argument(
        "--output-dir",
        type=str,
        default=OUTPUT_DIR,
        help=f"Output directory for transcript files (default: {OUTPUT_DIR})",
    )
    parser.add_argument(
        "--sources",
        type=str,
        default=SOURCES_MD_PATH,
        help=f"Path to sources.md (default: {SOURCES_MD_PATH})",
    )
    parser.add_argument(
        "--videos-per-channel",
        type=int,
        default=2,
        help="Number of r        print(f"  [WA p
    print(f"  Found {len(vpts.py --
    print(//www.yo
    saved_files = []
   = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # Single video mode
    if args.url or args.video_id:
        input_val = args.url or args.video_id
        filepath = process_single_video(input_val, output_dir)
        if filepath:
            print(f"\n[SUCCESS] Transcript saved to: {filepath}")
        else:
            print(f"\n[FAILED] Could not process video: {input_val}")
            sys.exit(1)
        return

    # Batch mode: process all channels from sources.md
    sources_path = args.sources
    channels = extract_channel_urls_from_md(sources_path)

    if not channels:
        print(f"[ERROR] No YouTube channels found in {sources_path}")
        sys.exit(1)

    print(f"\n[INFO] Found {len(channels)} YouTube channels in sources.md")
    print(f"[INFO] Fetching up to {args.videos_per_channel} video(s) per channel")
    print(f"[INFO] Output directory: {output_dir}")
    print()

    all_saved = []
        print(//www.yo
    saved     saved = process_channe   = ars(channel, out    os.maargs.videos_
    # Single video mode
    if args.url ed)    if args.ary
    prin        input_val = args.url or MM        filepath = process_single_video(inpen(        if filepath:
            print(f"\n[SUCCESS] Transced)}       print(f"  Outp        else:
            print(f"\n[FAILED] Could not proces all_  ved:
                   sys.exit(1)
        return

    # Batch mode: process alnt(f"  * {os.path.basename(f)}")


if __name__ == "__main__":
    main()
