---

### Terminal Banner Scroller 🖥️

A small Python script I made for fun that displays an animated ASCII banner scrolling smoothly across your terminal.
It automatically adapts to your terminal size and runs in a loop until you stop it.

Purely cosmetic. Zero productivity. Maximum vibes.

## Preview

The script animates this banner across the screen:

```
██╗  ██╗ ██╗   ██╗ ████████╗ ███████╗ ██████╗  ██╗  ██╗
╚██╗██╔╝ ╚██╗ ██╔╝ ╚══██╔══╝ ██╔════╝ ██╔════╝ ██║  ██║
 ╚███╔╝   ╚████╔╝     ██║    ███████╗ ███████╗ ███████║
 ██╔██╗    ╚██╔╝      ██║    ╚════██║ ██╔═══██╗╚════██║
██╔╝ ██╗    ██║       ██║    ███████║ ╚██████╔╝     ██║
╚═╝  ╚═╝    ╚═╝       ╚═╝    ╚══════╝  ╚═════╝      ╚═╝
```

## Features

* Smooth left-to-right scrolling animation
* Automatically centres the banner vertically
* Adjusts to your terminal size
* Hides the cursor during animation
* Clean exit with `Ctrl + C`

## Requirements

* Python 3
* A terminal that supports ANSI escape codes
  (Most Linux terminals do — works great on bash, zsh, etc.)

No external libraries required.

## Usage

Clone the repo: 

```
git clone https://github.com/Xyt564/python
```


get into the folder:

```bash
cd python
```

Then:

```
cd asci_art_banner_project
```

To run the file:

```
python3 terminal_banner_script.py
```


To stop the animation, just press:

```
Ctrl + C
```

## Notes

* This clears the terminal each frame, so don’t run it while doing anything important
* Designed mainly for Linux / Unix-like systems (not tested on windows)
* Windows may work in WSL terminals, but it’s not the main target

## Why?

Because terminal animations are fun and sometimes that’s reason enough plus why not.

## License

MIT — do whatever you want with it.

---
