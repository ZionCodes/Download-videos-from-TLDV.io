# TL;DV Video Downloader

This is a simple Python script that allows you to download TL;DV meeting recordings using [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

It authenticates using your JWT token, fetches the video source from the TL;DV API, and downloads it using `yt-dlp` (with optional HLS/MP4 stream support via `ffmpeg`).

---

## 🚀 Features

- 🔒 Authenticated downloads using your JWT token  
- 🎥 Supports both MP4 and HLS video formats  
- 📝 Automatically names downloads based on upload date and meeting title  
- 💻 Works on macOS, Linux, and Windows (via WSL or native Python)

---

## 📦 Requirements

- Python 3.x  
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)  
- [`ffmpeg`](https://ffmpeg.org/) (must be in your system PATH for HLS video)  
- `requests` module (`pip install requests`)

---

## 🛠 Installation

```bash
git clone https://github.com/yourusername/tldv-downloader.git
cd tldv-downloader
pip install requests
