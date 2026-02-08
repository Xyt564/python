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

## Recommended: Delete all the other projects

#### This clones the entire repo
```bash
git clone https://github.com/Xyt564/python.git
```

#### This command gets you into the repo directory

```bash
cd python
```

#### This moves the yt-tui folder to the Downloads folder

```bash
mv yt-tui ~/Downloads/
```

#### This take you back to the directory you cloned the repo originally

```bash
cd ..
```

#### This gets rid of the entire python repo folder and all the unnecessary files
**(warning: This will get rid of all the files in this python repo so if you wish to keep any move them beforehand using mv or ur file manager)**
```bash
rm -rf ~/python/
```

#### Takes you directly to the yt-tui folder

```bash
cd Downloads/yt-tui/
```

---

#### 3️⃣ Install Python dependencies

```bash
pip install -r requirements.txt
```

#### If your distro complains (looking at you, Ubuntu / Pop os):

```bash
pip install -r requirements.txt --break-system-packages
```

---

### 4️⃣ Run it

```bash
python3 main.py
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
~/Downloads/yt-tui/downloads/
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


## 🛠️ Maintenance Status

This project is **not actively maintained**.

I’ll likely only update or fix it if:

* I personally run into issues while using it, or
* A request or bug report is opened

Feel free to submit pull requests if you want any improvements or for me to extend it.

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 Xyt564

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---
