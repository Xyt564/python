#!/usr/bin/env python3
import subprocess
import re
from datetime import datetime
import customtkinter as ctk
import ipaddress
import threading

# ------------------ CONFIG ------------------

LOG_FILE = "/var/log/ufw.log"

# Improved regex to match UFW entries properly
log_pattern = re.compile(
    r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+\S+\s+kernel: \[.*?\] \[UFW (\w+)\].*?SRC=([\d\.]+).*?DST=([\d\.]+)'
)

# ------------------ CTk Init ------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.title("UFW Real-Time Log Monitor")
app.geometry("900x600")

# ------------------ UI Elements ------------------

status_label = ctk.CTkLabel(app, text="🔍 Monitoring UFW logs...", text_color="gray")
status_label.pack(pady=(5, 0))

text_box = ctk.CTkTextbox(app, wrap="none", font=("Consolas", 12))
text_box.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------ IP Classification ------------------

def classify_ip(ip_str):
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if ip_obj.is_private:
            return "Private IP"
        elif ip_obj.is_loopback:
            return "Loopback"
        elif ip_obj.is_link_local:
            return "Link-local"
        elif ip_obj.is_reserved:
            return "Reserved"
        elif ip_obj.is_multicast:
            return "Multicast"
        else:
            return "Public IP"
    except ValueError:
        return "Invalid IP"

# ------------------ Timestamp Parser ------------------

def parse_timestamp(timestamp_str):
    try:
        return datetime.strptime(timestamp_str, "%b %d %H:%M:%S").strftime("%b %d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(timestamp_str.strip(), "%b %e %H:%M:%S").strftime("%b %d %H:%M:%S")
        except Exception:
            return timestamp_str

# ------------------ Log Entry Handler ------------------

def add_log_line(action, ts, src, dst):
    src_type = classify_ip(src)
    dst_type = classify_ip(dst)

    color = "#FF5555" if action.upper() == "BLOCK" else "#55FF55"
    tag_name = action.upper()

    line = f"[{action.upper()}] {ts} | {src} ({src_type}) → {dst} ({dst_type})\n"

    text_box.insert("end", line, tag_name)
    text_box.tag_config(tag_name, foreground=color)
    text_box.see("end")

def process_line(ts, action, src, dst):
    app.after(0, add_log_line, action, ts, src, dst)

# ------------------ Log Follower ------------------

def follow_logs():
    try:
        process = subprocess.Popen(["sudo", "tail", "-F", LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for line in iter(process.stdout.readline, b""):
            if not line:
                continue
            decoded_line = line.decode("utf-8", errors="ignore").strip()
            match = log_pattern.search(decoded_line)
            if match:
                timestamp, action, src, dst = match.groups()
                ts = parse_timestamp(timestamp)
                process_line(ts, action, src, dst)
            else:
                # Optional: uncomment to debug unmatched lines
                # print("Unmatched line:", decoded_line)
                pass
    except Exception as e:
        app.after(0, lambda: text_box.insert("end", f"[ERROR] {str(e)}\n"))

# ------------------ Thread Start ------------------

threading.Thread(target=follow_logs, daemon=True).start()

# ------------------ Start App ------------------

app.mainloop()
