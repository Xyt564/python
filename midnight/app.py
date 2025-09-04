import customtkinter as ctk
from datetime import datetime, timedelta

def update_time():
    now = datetime.now()
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    diff = midnight - now

    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    countdown_label.configure(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    app.after(1000, update_time)  # refresh every second


# App setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Midnight Countdown")

# Window size
width, height = 400, 200

# Center the window
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

app.geometry(f"{width}x{height}+{x}+{y}")
app.resizable(False, False)  # lock size

# Title
title_label = ctk.CTkLabel(app, text="Time Until Midnight", font=("Arial", 22, "bold"))
title_label.pack(pady=(30, 10))

# Countdown
countdown_label = ctk.CTkLabel(app, text="", font=("Arial", 40, "bold"))
countdown_label.pack(pady=10)

update_time()
app.mainloop()