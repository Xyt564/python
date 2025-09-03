import customtkinter as ctk
import tkinter as tk
import json
import os
import threading
import time

# ---------- CONFIG ----------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ---------- COLORS & TYPOGRAPHY ----------
BG = "#2b2b2b"          # soft dark background
PANEL = "#383838"       # panel background
PANEL_ALT = "#3f3f3f"   # side panel
BUTTON_BG = "#4a90e2"   # calm blue button
BUTTON_HOVER = "#357ABD" # hover color
ACCENT = "#50C878"      # subtle green accent
TEXT = "#E0E0E0"        # soft light grey text
TEXT_BORDER = "#5a5a5a" # soft grey border for text box
FONT_TITLE = ("Arial", 18, "bold")
FONT_REG = ("Arial", 15, "bold")

# ---------- WINDOW ----------
root = ctk.CTk()
root.title("Local Wiki — Sleek")
root.geometry("1000x620")
root.minsize(800, 500)
root.configure(bg=BG)

# ---------- DATA FILE ----------
data_dir = "/media/xyt564/sd_card/python/new/wiki"
os.makedirs(data_dir, exist_ok=True)
wiki_file = os.path.join(data_dir, "wiki.json")
if not os.path.exists(wiki_file):
    with open(wiki_file, "w") as f:
        json.dump({}, f)

# ---------- HELPERS ----------
def load_data():
    try:
        with open(wiki_file, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    with open(wiki_file, "w") as f:
        json.dump(data, f, indent=2)

def flash_status(msg, duration=1.6):
    export_label.configure(text=msg)
    def clear():
        time.sleep(duration)
        export_label.configure(text="")
    threading.Thread(target=clear, daemon=True).start()

# ---------- CORE FUNCTIONS ----------

def save_note():
    title = title_entry.get().strip()
    content = content_text.get("1.0", "end-1c").strip()
    tags = [t.strip() for t in tags_entry.get().split(",") if t.strip()]
    if not title or not content:
        flash_status("Title and content required")
        return
    data = load_data()
    data[title] = {"content": content, "tags": tags}
    save_data(data)
    refresh_notes()
    flash_status("Saved")

def delete_note():
    sel = listbox.curselection()
    if not sel:
        flash_status("No note selected")
        return
    key = listbox.get(sel[0])
    data = load_data()
    if key in data:
        data.pop(key)
        save_data(data)
        refresh_notes()
        clear_editor()
        flash_status("Deleted")

def clear_editor():
    title_entry.delete(0, "end")
    tags_entry.delete(0, "end")
    content_text.delete("1.0", "end")

def export_notes():
    data = load_data()
    export_file = os.path.join(data_dir, "wiki_export.json")
    with open(export_file, "w") as f:
        json.dump(data, f, indent=2)
    flash_status(f"Exported → {export_file}")

def refresh_notes(query=""):
    listbox.delete(0, "end")
    data = load_data()
    keys = sorted(data.keys(), key=lambda s: s.lower())
    for k in keys:
        v = data[k]
        if not query or query.lower() in k.lower() or any(query.lower() in t.lower() for t in v.get("tags", [])):
            listbox.insert("end", k)

def on_select(event=None):
    sel = listbox.curselection()
    if not sel:
        return
    key = listbox.get(sel[0])
    data = load_data()
    note = data.get(key, {})
    clear_editor()
    title_entry.insert(0, key)
    tags_entry.insert(0, ", ".join(note.get("tags", [])))
    content_text.insert("1.0", note.get("content", ""))

def on_search(event=None):
    q = search_entry.get().strip()
    refresh_notes(q)

# ---------- LAYOUT ----------
outer = ctk.CTkFrame(root, fg_color=BG, corner_radius=0)
outer.pack(fill="both", expand=True, padx=12, pady=12)

main = ctk.CTkFrame(outer, fg_color=PANEL, corner_radius=14)
main.pack(fill="both", expand=True, padx=6, pady=6)

# Left column
left = ctk.CTkFrame(main, fg_color=PANEL_ALT, corner_radius=12)
left.place(relx=0.02, rely=0.03, relwidth=0.28, relheight=0.84)

search_entry = ctk.CTkEntry(left, placeholder_text="Search title or tag", width=260, height=44, corner_radius=12, fg_color=PANEL_ALT, text_color=TEXT, font=FONT_REG)
search_entry.pack(padx=12, pady=(12,10), fill="x")
search_entry.bind("<KeyRelease>", on_search)

listbox_container = ctk.CTkFrame(left, fg_color=PANEL_ALT, corner_radius=12)
listbox_container.pack(fill="both", expand=True, padx=12, pady=(4,12))

listbox_scroll = tk.Scrollbar(listbox_container, orient="vertical")
listbox = tk.Listbox(listbox_container, yscrollcommand=listbox_scroll.set, bg=PANEL_ALT, fg=TEXT, selectbackground=ACCENT, bd=0, highlightthickness=0, font=("Arial", 16, "bold"), activestyle='none')
listbox_scroll.config(command=listbox.yview)
listbox.pack(side="left", fill="both", expand=True, padx=(8,0), pady=8)
listbox_scroll.pack(side="right", fill="y", padx=(0,8), pady=8)
listbox.bind("<<ListboxSelect>>", on_select)

# Right column
right = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=14)
right.place(relx=0.315, rely=0.03, relwidth=0.67, relheight=0.84)

title_entry = ctk.CTkEntry(right, placeholder_text="Title", width=560, height=46, corner_radius=12, font=FONT_TITLE, fg_color=PANEL, text_color=TEXT)
title_entry.pack(padx=14, pady=(12,8), fill="x")

tags_entry = ctk.CTkEntry(right, placeholder_text="Tags (comma-separated)", width=560, height=40, corner_radius=10, font=FONT_REG, fg_color=PANEL, text_color=TEXT)
tags_entry.pack(padx=14, pady=(0,10), fill="x")

content_container = ctk.CTkFrame(right, fg_color=PANEL, corner_radius=12)
content_container.pack(padx=14, pady=(0,10), fill="both", expand=True)

content_text = ctk.CTkTextbox(content_container, corner_radius=12, fg_color=PANEL, width=640, height=360, font=("Arial", 15, "bold"), text_color=TEXT, border_width=1, border_color=TEXT_BORDER)
content_text.pack(fill="both", expand=True, padx=10, pady=10)

# Bottom control bar
bottom = ctk.CTkFrame(outer, fg_color=BG, corner_radius=0)
bottom.pack(fill="x", side="bottom", pady=(10,0), ipady=8)

for i in range(5):
    bottom.grid_columnconfigure(i, weight=1)

save_button = ctk.CTkButton(bottom, text="Save", command=save_note, fg_color=BUTTON_BG, hover_color=ACCENT, corner_radius=12, width=160, height=44, text_color=TEXT, font=FONT_REG)
save_button.grid(row=0, column=1, padx=8, pady=8)

delete_button = ctk.CTkButton(bottom, text="Delete", command=delete_note, fg_color=BUTTON_BG, hover_color=BUTTON_HOVER, corner_radius=12, width=160, height=44, text_color=TEXT, font=FONT_REG)
delete_button.grid(row=0, column=2, padx=8, pady=8)

export_button = ctk.CTkButton(bottom, text="Export", command=export_notes, fg_color=BUTTON_BG, hover_color=BUTTON_HOVER, corner_radius=12, width=160, height=44, text_color=TEXT, font=FONT_REG)
export_button.grid(row=0, column=3, padx=8, pady=8)

export_label = ctk.CTkLabel(bottom, text="", anchor="e", font=FONT_REG, text_color=TEXT, fg_color=BG)
export_label.grid(row=0, column=4, sticky="e", padx=(4,16))

# Initialize
refresh_notes()
root.mainloop()
