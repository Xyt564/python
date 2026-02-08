# 🎬 YouTube TUI Player

A **terminal-based YouTube browser, player, and downloader** written in Python.
Search YouTube, stream videos in **mpv**, or download videos/audio — all without leaving your terminal.

Built mainly on **Pop!_OS / Linux**, but it should work on **any system** that supports:

* Python + `pip`
* `mpv` (or another supported media player)

---

## ✨ Features

* 🔍 Search YouTube directly from the terminal
* ▶️ Stream videos in **mpv** (1080p, buffered, hardware-accelerated)
* ⬇️ Download videos (up to 1080p MP4)
* 🎵 Download audio only (MP3)
* 📁 Simple `downloads/` folder (no messy subfolders)
* 🖥️ Clean TUI powered by **rich**
* 🧠 Sensible fallbacks (VLC, browser, etc.)

---

## 📦 Requirements

### System

* Python **3.8+**
* One of the following media players:

  * **mpv** (recommended)
  * vlc
  * ffplay
  * IINA (macOS)

### Python dependencies

* `rich`
* `yt-dlp`

(Yes, it will auto-install them if missing — but don’t rely on that if your system is cursed.)

---

## 🚀 Installation (read carefully, please)

### 1️⃣ Install system dependencies

#### Pop!_OS / Ubuntu / Debian

```bash
sudo apt install mpv python3-pip
```

#### Arch

```bash
sudo pacman -S mpv python-pip
```

#### macOS (Homebrew)

```bash
brew install mpv python
```

---

### 2️⃣ Clone the repo

```bash
git clone https://github.com/Xyt564/python.git
```

```
cd yt-tui
```

(You can delete the other projects if you don’t want them)

---

### 3️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

If your distro complains (looking at you, Ubuntu):

```bash
pip install -r requirements.txt --break-system-packages
```

---

### 4️⃣ Run it

```bash
python3 youtube_tui.py
```

That’s it. If this step fails, reread steps **1–3**. Slowly.

---

## 🎮 Usage

Once running, use these commands:

| Command          | Action                         |
| ---------------- | ------------------------------ |
| `S`              | Search YouTube                 |
| `1`, `2`, `3`, … | Play video                     |
| `D#`             | Download video (example: `D1`) |
| `A#`             | Download audio only            |
| `C`              | Clear results                  |
| `Q`              | Quit                           |

Downloaded files go into:

```
./downloads/
```

---

## 🧠 Notes

* Defaults to **1080p max** for streaming and downloads
* Prefers **H.264** for smoother playback
* Falls back to browser playback if no player is found
* Uses `yt-dlp` under the hood (so yes, YouTube changes can break stuff)

---

## 🐛 Troubleshooting

**Playback doesn’t work**

* Make sure `mpv` is installed and in your `$PATH`

**Downloads fail**

```bash
pip install -U yt-dlp --break-system-packages
```

**Still broken?**

* It’s probably YouTube.
* Or your Python install.
* Or both.

---

## ⚠️ Disclaimer

This tool is for **personal use only**.
Respect YouTube’s Terms of Service and content creators.
This project is not affiliated with or endorsed by YouTube or Google.
It is intended for personal and educational use only.

---
