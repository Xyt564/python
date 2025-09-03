import tkinter as tk
from tkinter import filedialog, messagebox
from pytubefix import YouTube
from pytubefix import request

# Optional fix for large files
request.default_range_size = 1048576  # 1MB

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        download_path.set(folder)

def start_download():
    url = url_entry.get()
    path = download_path.get()
    
    if not url or not path:
        messagebox.showerror("Error", "Please enter a URL and select a folder")
        return
    
    try:
        yt = YouTube(url)
        # Automatically select the highest resolution progressive stream
        stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        
        messagebox.showinfo("Info", f"Downloading: {yt.title}")
        stream.download(output_path=path)
        messagebox.showinfo("Success", f"Downloaded: {yt.title}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Download failed:\n{e}")

# GUI setup
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x220")

download_path = tk.StringVar()

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Button(root, text="Select Download Folder", command=browse_folder).pack(pady=5)
tk.Entry(root, textvariable=download_path, width=50).pack(pady=5)

tk.Button(root, text="Start Download", command=start_download, bg="green", fg="white").pack(pady=20)

root.mainloop()
