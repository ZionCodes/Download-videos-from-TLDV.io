#!/usr/bin/env python3
"""
TL;DV Video Downloader using yt-dlp

This script prompts for a TL;DV meeting URL and your auth token, fetches the
HLS/MP4 source URL, and downloads the video via yt-dlp.

Dependencies:
  - yt-dlp (https://github.com/yt-dlp/yt-dlp)
  - ffmpeg (installed and in PATH)
  - requests (pip install requests)

Usage:
  1. Clone or download this repository.
  2. Ensure you have Python 3.x installed.
  3. Install dependencies:
     ```bash
     pip install requests
     ```
  4. Make the script executable (on Unix/macOS):
     ```bash
     chmod +x tldv_downloader.py
     ```
  5. Run the script:
     ```bash
     ./tldv_downloader.py
     ```
     or
     ```bash
     python3 tldv_downloader.py
     ```
  6. When prompted, enter the TL;DV meeting URL and your JWT token.
     - Meeting URL example: https://app.tldv.io/meetings/680896fbc4011300134ad801
     - JWT token: paste the full string from your browser devtools (omit or include the "Bearer " prefix).
  7. The script will use the TL;DV API to fetch the video source and download it via yt-dlp.

The downloaded file will be named using the upload date and meeting title, e.g.
"2025-04-23_My_Meeting_Title.mp4".

Examples:
  ```bash
  $ python3 tldv_downloader.py
  Enter TL;DV meeting URL: https://app.tldv.io/meetings/680896fbc4011300134ad801
  Enter JWT token (omit 'Bearer ' prefix if desired): eyJhbGciOiJIUzI1Ni...
  Downloading video with yt-dlp...
  Download complete.
  ```

Note:
  - If you encounter HTTP errors, verify your token hasn’t expired.
  - For HLS segments issues, install ffmpeg and ensure it's in your PATH.
"""
import subprocess
import requests
import sys
import re
import json
from urllib.parse import urlparse

def extract_meeting_id(url):
    """Extract the TL;DV meeting ID from various possible URLs."""
    parsed = urlparse(url)
    match = re.search(r'/meetings/([^/\?#]+)', parsed.path)
    return match.group(1) if match else None

def main():
    try:
        meeting_url = input("Enter TL;DV meeting URL (e.g. https://app.tldv.io/meetings/<ID>): ").strip()
        raw_token = input("Enter JWT token (omit 'Bearer ' prefix if desired): ").strip()
        token = raw_token if raw_token.lower().startswith("bearer ") else f"Bearer {raw_token}"

        meeting_id = extract_meeting_id(meeting_url)
        if not meeting_id:
            print("Error: Could not extract meeting ID from URL.")
            sys.exit(1)

        api_url = f"https://gw.tldv.io/v1/meetings/{meeting_id}/watch-page?noTranscript=true"
        headers = {"Authorization": token}
        resp = requests.get(api_url, headers=headers)
        resp.raise_for_status()

        try:
            data = resp.json()
        except ValueError:
            print("Error: Received non-JSON response:")
            print(resp.text)
            sys.exit(1)

        if isinstance(data, str):
            print("Unexpected API response (string):")
            print(data)
            sys.exit(1)

        source_url = data.get("video", {}).get("source")
        if not source_url:
            print("Error: Video source URL not found in response:")
            print(json.dumps(data, indent=2))
            sys.exit(1)

        output_template = "%(upload_date>%Y-%m-%d)s_%(title)s.%(ext)s"
        cmd = [
            "yt-dlp",
            "--add-header", f"Authorization: {token}",
            "-o", output_template,
            source_url
        ]

        print("Downloading video with yt-dlp...")
        subprocess.run(cmd, check=True)
        print("Download complete.")

    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}")
    except subprocess.CalledProcessError as e:
        print(f"Error running yt-dlp: {e}")
    except Exception as e:
        print("Unexpected error:", e)

if __name__ == '__main__':
    main()
