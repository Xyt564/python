#!/usr/bin/env python3
import sys
import time
import shutil
import os

BANNER = """
██╗  ██╗ ██╗   ██╗ ████████╗ ███████╗ ██████╗  ██╗  ██╗
╚██╗██╔╝ ╚██╗ ██╔╝ ╚══██╔══╝ ██╔════╝ ██╔════╝ ██║  ██║
 ╚███╔╝   ╚████╔╝     ██║    ███████╗ ███████╗ ███████║
 ██╔██╗    ╚██╔╝      ██║    ╚════██║ ██╔═══██╗╚════██║
██╔╝ ██╗    ██║       ██║    ███████║ ╚██████╔╝     ██║
╚═╝  ╚═╝    ╚═╝       ╚═╝    ╚══════╝  ╚═════╝      ╚═╝
""".strip().split('\n')

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def hide_cursor():
    sys.stdout.write('\033[?25l')
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write('\033[?25h')
    sys.stdout.flush()

def get_terminal_size():
    size = shutil.get_terminal_size()
    return size.columns, size.lines

def print_at(x, y, text):
    sys.stdout.write(f'\033[{y};{x}H{text}')
    sys.stdout.flush()

def animate_banner():
    try:
        hide_cursor()
        clear_screen()
        
        term_width, term_height = get_terminal_size()
        banner_width = max(len(line) for line in BANNER)
        banner_height = len(BANNER)
        
        start_y = max(1, (term_height - banner_height) // 2)
        
        x = term_width
        
        while True:
            clear_screen()
            
            for i, line in enumerate(BANNER):
                y = start_y + i
                if 0 < y <= term_height and x < term_width:
                    visible_start = max(0, -x)
                    visible_end = min(len(line), term_width - x)
                    
                    if visible_start < visible_end:
                        visible_text = line[visible_start:visible_end]
                        print_x = max(1, x + visible_start)
                        print_at(print_x, y, visible_text)
            
            sys.stdout.flush()
            time.sleep(0.02)  
            x -= 1  
            
            if x <= -banner_width:
                x = term_width
        
    except KeyboardInterrupt:
        clear_screen()
        show_cursor()
        print("\nAnimation stopped.")
        sys.exit(0)
    finally:
        show_cursor()

if __name__ == "__main__":
    animate_banner()
