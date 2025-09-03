import customtkinter as ctk
from transformers import pipeline
import threading
import time
from tkinter import filedialog

# ------------------ Model Setup ------------------
def load_model():
    global generator
    generator = pipeline(
        "text-generation",
        model="EleutherAI/gpt-neo-125M",
        device_map="cpu",
        torch_dtype="auto"
    )

print("Loading model, please wait...")
load_model()
print("Model loaded. Starting GUI...")

# ------------------ GUI Setup ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Polished AI Chat")
app.geometry("600x600")

# Chat frame (scrollable) that expands
chat_frame = ctk.CTkScrollableFrame(app)
chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Bottom frame for input and send button
bottom_frame = ctk.CTkFrame(app, fg_color="transparent")
bottom_frame.pack(fill="x", padx=10, pady=(0,10))

# Input textbox (full width minus button)
input_box = ctk.CTkTextbox(bottom_frame, height=60)
input_box.pack(side="left", fill="x", expand=True, padx=(0,5), pady=5)

send_button = ctk.CTkButton(bottom_frame, text="Send", width=80)
send_button.pack(side="right", pady=5)

# Buttons frame for Clear/Save/Load
buttons_frame = ctk.CTkFrame(app, fg_color="transparent")
buttons_frame.pack(fill="x", padx=10, pady=(0,5))

clear_button = ctk.CTkButton(buttons_frame, text="Clear Chat")
clear_button.pack(side="left", padx=5)

save_button = ctk.CTkButton(buttons_frame, text="Save Chat")
save_button.pack(side="left", padx=5)

load_button = ctk.CTkButton(buttons_frame, text="Load Chat")
load_button.pack(side="left", padx=5)

# AI typing indicator
ai_typing_label = ctk.CTkLabel(app, text="")
ai_typing_label.pack(pady=(0,5))

# Keep track of messages
messages = []

# ------------------ Functions ------------------
def add_message(speaker, message):
    # Rounded bubble effect
    if speaker == "You":
        fg_color = "#1f6aa5"
        anchor = "e"
    else:
        fg_color = "#3b3b3b"
        anchor = "w"

    bubble = ctk.CTkFrame(chat_frame, fg_color=fg_color, corner_radius=10)
    bubble.pack(fill="x", pady=5, padx=5, anchor=anchor)

    label = ctk.CTkLabel(
        bubble,
        text=f"{speaker}: {message}",
        anchor="w",
        justify="left",
        wraplength=500,
        text_color="white"
    )
    label.pack(padx=10, pady=5)

    messages.append(bubble)
    if len(messages) > 20:
        old = messages.pop(0)
        old.destroy()

    chat_frame.update_idletasks()
    # Auto-scroll removed to prevent AttributeError

def generate_text():
    prompt = input_box.get("1.0", "end").strip()
    if not prompt:
        return

    add_message("You", prompt)
    input_box.delete("1.0", "end")

    def run_model():
        try:
            ai_typing_label.configure(text="AI is typing...")
            time.sleep(0.5)
            output = generator(prompt, max_length=50, do_sample=True)[0]['generated_text']
            response = output[len(prompt):].strip()
            add_message("AI", response)
        except Exception as e:
            add_message("AI", f"[Error]: {e}")
        finally:
            ai_typing_label.configure(text="")

    threading.Thread(target=run_model, daemon=True).start()

# ------------------ Chat Management ------------------
def clear_chat():
    for msg in messages:
        msg.destroy()
    messages.clear()

def save_chat():
    if not messages:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            for msg in messages:
                text = msg.winfo_children()[0].cget("text")
                f.write(text + "\n")

def load_chat():
    file_path = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
    if file_path:
        clear_chat()
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    if line.startswith("You:"):
                        add_message("You", line[4:].strip())
                    else:
                        add_message("AI", line.split("AI:")[-1].strip())

# ------------------ Bindings ------------------
send_button.configure(command=generate_text)
clear_button.configure(command=clear_chat)
save_button.configure(command=save_chat)
load_button.configure(command=load_chat)

def on_enter(event):
    generate_text()
    return "break"

input_box.bind("<Return>", on_enter)

# ------------------ Start GUI ------------------
app.mainloop()
