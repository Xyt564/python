import requests
import customtkinter as ctk
from tkinter import messagebox

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# ------------------ Fetch Stories ------------------
def get_top_stories(limit=20):
    try:
        resp = requests.get(TOP_STORIES_URL)
        resp.raise_for_status()
        top_ids = resp.json()[:limit]
    except Exception as e:
        return f"Failed to fetch top stories: {e}"

    stories = []
    for story_id in top_ids:
        try:
            story_resp = requests.get(ITEM_URL.format(story_id))
            story_resp.raise_for_status()
            data = story_resp.json()
            stories.append({
                "title": data.get("title"),
                "url": data.get("url"),
                "author": data.get("by"),
                "score": data.get("score")
            })
        except Exception:
            continue
    return stories

# ------------------ GUI ------------------
class HackerNewsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hacker News Top Stories")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Bold font using CTkFont
        self.bold_font = ctk.CTkFont(family="Consolas", size=12, weight="bold")

        # Fetch button
        self.fetch_button = ctk.CTkButton(self, text="Fetch Top Stories", command=self.fetch_stories)
        self.fetch_button.pack(pady=10)

        # Scrollable text box
        self.text_box = ctk.CTkTextbox(self, width=760, height=500, wrap="word", font=self.bold_font)
        self.text_box.pack(padx=10, pady=10, fill="both", expand=True)

    def fetch_stories(self):
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", "Fetching top stories...\n\n")
        stories = get_top_stories(20)
        if isinstance(stories, str):  
            self.text_box.insert("end", stories)
            return

        for i, story in enumerate(stories, start=1):
            self.text_box.insert("end", f"{i}. {story['title']}\n", "title")
            self.text_box.insert("end", f"   by {story['author']} | {story['score']} points\n")
            if story["url"]:
                self.text_box.insert("end", f"   URL: {story['url']}\n\n")
            else:
                self.text_box.insert("end", "\n")

        
        self.text_box.tag_configure("title", font=self.bold_font)

if __name__ == "__main__":
    app = HackerNewsApp()
    app.mainloop()
