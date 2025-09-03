import customtkinter as ctk
import tkinter as tk
from playsound import playsound
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CountdownApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Countdown Timer")
        self.geometry("350x200")
        self.resizable(False, False)

        self.remaining = 0
        self.running = False

        # Paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.alarm_sound = os.path.join(self.script_dir, "alarm.wav")

        self.create_input_frame()
        self.create_countdown_frame()

    def create_input_frame(self):
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label = ctk.CTkLabel(self.input_frame, text="Enter time:", font=("Arial", 16))
        self.label.pack(pady=5)

        # Minutes and Seconds entries
        self.minutes_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Minutes", width=80)
        self.minutes_entry.pack(side="left", padx=(20, 10), pady=10)
        self.seconds_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Seconds", width=80)
        self.seconds_entry.pack(side="left", padx=(10, 20), pady=10)

        self.start_button = ctk.CTkButton(self.input_frame, text="Start", command=self.start_countdown)
        self.start_button.pack(pady=10)

    def create_countdown_frame(self):
        self.countdown_frame = ctk.CTkFrame(self)

        self.countdown_label = ctk.CTkLabel(self.countdown_frame, text="", font=("Arial", 48))
        self.countdown_label.pack(pady=20)

        self.button_frame = ctk.CTkFrame(self.countdown_frame)
        self.button_frame.pack(pady=10)

        self.pause_button = ctk.CTkButton(self.button_frame, text="Pause", command=self.pause_countdown, width=80)
        self.pause_button.pack(side="left", padx=5)
        self.resume_button = ctk.CTkButton(self.button_frame, text="Resume", command=self.resume_countdown, width=80)
        self.resume_button.pack(side="left", padx=5)
        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset_countdown, width=80)
        self.reset_button.pack(side="left", padx=5)

    def start_countdown(self):
        try:
            mins = int(self.minutes_entry.get() or 0)
            secs = int(self.seconds_entry.get() or 0)
            self.remaining = mins * 60 + secs
        except ValueError:
            self.label.configure(text="Enter valid numbers!")
            return

        if self.remaining <= 0:
            self.label.configure(text="Enter a time greater than 0!")
            return

        self.running = True
        self.input_frame.pack_forget()
        self.countdown_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_countdown()

    def update_countdown(self):
        if self.running and self.remaining >= 0:
            mins, secs = divmod(self.remaining, 60)
            self.countdown_label.configure(text=f"{mins:02}:{secs:02}")
            self.remaining -= 1
            self.after(1000, self.update_countdown)
        elif self.remaining < 0:
            self.countdown_label.configure(text="Time's up!")
            self.running = False
            playsound(self.alarm_sound)

    def pause_countdown(self):
        self.running = False

    def resume_countdown(self):
        if self.remaining > 0:
            self.running = True
            self.update_countdown()

    def reset_countdown(self):
        self.running = False
        self.remaining = 0
        self.countdown_label.configure(text="")
        self.countdown_frame.pack_forget()
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.label.configure(text="Enter time:")
        self.input_frame.pack(fill="both", expand=True, padx=20, pady=20)


if __name__ == "__main__":
    app = CountdownApp()
    app.mainloop()
