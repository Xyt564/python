import customtkinter as ctk
from PIL import Image
import os
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, "images")

CARD_WIDTH = 200
CARD_HEIGHT = 250
CARD_PADDING = 20

# ---------- God Data (all 12 Olympians) ----------
gods_info = {
    "Zeus": {
        "description": "King of the gods, ruler of Mount Olympus, god of the sky and thunder.",
        "roman_name": "Jupiter",
        "epithets": ["Lord of Thunder", "Cloud-Gatherer"],
        "symbols": ["⚡ Lightning Bolt", "🦅 Eagle", "🌳 Oak Tree"],
        "domains": ["Sky", "Thunder", "Justice"],
        "family": {
            "parents": ["Cronus", "Rhea"],
            "siblings": ["Hera", "Hades", "Poseidon", "Demeter", "Hestia"],
            "children": ["Athena", "Apollo", "Artemis", "Ares", "Hermes", "Dionysus"]
        },
        "famous_myths": ["Overthrew Cronus to become king of gods.", "Fathered many heroes and gods, including Hercules and Athena."],
        "fun_facts": ["Known for throwing thunderbolts when angry.", "Often appears with a majestic beard and eagle companion."]
    },
    "Hera": {
        "description": "Queen of the gods, goddess of marriage and family.",
        "roman_name": "Juno",
        "epithets": ["Protector of Marriage"],
        "symbols": ["🦚 Peacock", "🐄 Cow", "👑 Diadem"],
        "domains": ["Marriage", "Family"],
        "family": {"parents": ["Cronus", "Rhea"], "siblings": ["Zeus", "Hades", "Poseidon", "Demeter", "Hestia"], "children": ["Ares", "Hephaestus", "Hebe", "Eileithyia"]},
        "famous_myths": ["Often punished Zeus’ lovers and illegitimate children."],
        "fun_facts": ["Patron of married women.", "Her peacock’s tail symbolizes her beauty and pride."]
    },
    "Poseidon": {
        "description": "God of the sea, earthquakes, and horses.",
        "roman_name": "Neptune",
        "epithets": ["Earth-Shaker"],
        "symbols": ["🔱 Trident", "🐴 Horse", "🐬 Dolphin"],
        "domains": ["Sea", "Earthquakes", "Horses"],
        "family": {"parents": ["Cronus", "Rhea"], "siblings": ["Zeus", "Hera", "Hades", "Demeter", "Hestia"], "children": ["Triton", "Theseus", "Polyphemus"]},
        "famous_myths": ["Created the horse.", "Contended with Athena for Athens."],
        "fun_facts": ["Could cause storms and calm the seas.", "Brother of Zeus and Hades."]
    },
    "Athena": {
        "description": "Goddess of wisdom, warfare, and strategy.",
        "roman_name": "Minerva",
        "epithets": ["Pallas Athena"],
        "symbols": ["🦉 Owl", "🌿 Olive Tree", "🛡️ Helmet"],
        "domains": ["Wisdom", "Strategy", "Warfare"],
        "family": {"parents": ["Zeus"], "siblings": [], "children": []},
        "famous_myths": ["Born fully armored from Zeus’ head.", "Patron deity of Athens."],
        "fun_facts": ["Virgin goddess.", "Associated with crafts and weaving."]
    },
    "Apollo": {
        "description": "God of the sun, music, poetry, and healing.",
        "roman_name": "Apollo",
        "epithets": ["Phoebus"],
        "symbols": ["🎵 Lyre", "🌿 Laurel", "☀️ Sun"],
        "domains": ["Music", "Sun", "Healing"],
        "family": {"parents": ["Zeus", "Leto"], "siblings": ["Artemis"], "children": ["Asclepius"]},
        "famous_myths": ["Chased Daphne who turned into a laurel tree.", "Drove the chariot of the sun."],
        "fun_facts": ["Twin brother of Artemis.", "God of prophecy and archery."]
    },
    "Artemis": {
        "description": "Goddess of the hunt, wilderness, and the moon.",
        "roman_name": "Diana",
        "epithets": ["Mistress of Animals"],
        "symbols": ["🏹 Bow and Arrow", "🌙 Moon", "🦌 Deer"],
        "domains": ["Hunting", "Moon", "Wilderness"],
        "family": {"parents": ["Zeus", "Leto"], "siblings": ["Apollo"], "children": []},
        "famous_myths": ["Protector of young women and wildlife.", "Punished those who disrespected her."],
        "fun_facts": ["Virgin goddess.", "Often depicted with a hunting dog or deer."]
    },
    "Ares": {
        "description": "God of war, violence, and courage.",
        "roman_name": "Mars",
        "epithets": ["Bloody", "Spear-Bearer"],
        "symbols": ["⚔️ Spear", "🪖 Helmet", "🐕 Dog"],
        "domains": ["War", "Violence"],
        "family": {"parents": ["Zeus", "Hera"], "siblings": [], "children": []},
        "famous_myths": ["Fought in the Trojan War.", "Often clashed with Athena."],
        "fun_facts": ["Represents the brutal nature of war.", "Feared by mortals and gods alike."]
    },
    "Aphrodite": {
        "description": "Goddess of love, beauty, and desire.",
        "roman_name": "Venus",
        "epithets": ["Cytherea", "Golden"],
        "symbols": ["🕊️ Dove", "🌹 Rose", "🌿 Myrtle"],
        "domains": ["Love", "Beauty", "Desire"],
        "family": {"parents": ["Sea Foam"], "siblings": [], "children": ["Eros", "Aeneas"]},
        "famous_myths": ["Born from sea foam.", "Married Hephaestus but had affairs with Ares."],
        "fun_facts": ["Patron of lovers.", "Could make anyone fall in love with her."]
    },
    "Hephaestus": {
        "description": "God of fire, metalworking, and craftsmanship.",
        "roman_name": "Vulcan",
        "epithets": ["Lame God", "Smith of the Gods"],
        "symbols": ["🔨 Hammer", "⚒️ Anvil", "Tongs"],
        "domains": ["Fire", "Metalworking", "Craftsmanship"],
        "family": {"parents": ["Zeus", "Hera"], "siblings": [], "children": []},
        "famous_myths": ["Created divine weapons for gods.", "Married to Aphrodite."],
        "fun_facts": ["Known for his skill despite being lame.", "Made Zeus’ thunderbolts."]
    },
    "Hermes": {
        "description": "Messenger of the gods, god of travel, trade, and thieves.",
        "roman_name": "Mercury",
        "epithets": ["Fleet-Footed", "Trickster"],
        "symbols": ["🪄 Caduceus", "👟 Winged Sandals", "🐢 Tortoise"],
        "domains": ["Travel", "Trade", "Thieves", "Messages"],
        "family": {"parents": ["Zeus", "Maia"], "siblings": [], "children": []},
        "famous_myths": ["Stole Apollo’s cattle as a baby.", "Guided souls to Hades."],
        "fun_facts": ["Inventor of the lyre.", "Messenger between gods and mortals."]
    },
    "Demeter": {
        "description": "Goddess of the harvest, agriculture, and fertility.",
        "roman_name": "Ceres",
        "epithets": ["Corn-Mother"],
        "symbols": ["🌾 Sheaf of Wheat", "🌽 Cornucopia", "🔥 Torch"],
        "domains": ["Harvest", "Fertility", "Agriculture"],
        "family": {"parents": ["Cronus", "Rhea"], "siblings": ["Zeus", "Hades", "Poseidon", "Hera", "Hestia"], "children": ["Persephone"]},
        "famous_myths": ["Mother of Persephone, who was abducted by Hades.", "Her grief caused the seasons to change."],
        "fun_facts": ["Worshipped by farmers.", "Associated with sacred grain and fertility rituals."]
    },
    "Hestia": {
        "description": "Goddess of the hearth, home, and family.",
        "roman_name": "Vesta",
        "epithets": ["Virgin Goddess", "Keeper of the Hearth"],
        "symbols": ["🔥 Hearth", "🏠 Home", "🍵 Kettle"],
        "domains": ["Hearth", "Home", "Family"],
        "family": {"parents": ["Cronus", "Rhea"], "siblings": ["Zeus", "Hades", "Poseidon", "Hera", "Demeter"], "children": []},
        "famous_myths": ["Virgin goddess, protector of family and domestic life."],
        "fun_facts": ["Always depicted by the hearth.", "Associated with stability and domesticity."]
    },
}

# ---------- Preload CTkImages (match any extension, case-insensitive) ----------
god_images = {}
for god in gods_info:
    img_path = None
    for f in os.listdir(IMAGE_DIR):
        name, ext = os.path.splitext(f)
        if name.lower() == god.lower():
            img_path = os.path.join(IMAGE_DIR, f)
            break
    if img_path and os.path.exists(img_path):
        img = Image.open(img_path).convert("RGBA").resize((150,150))
        god_images[god] = ctk.CTkImage(light_image=img, dark_image=img, size=(150,150))
    else:
        god_images[god] = None

# ---------- Popup function ----------
def show_popup(god_name):
    data = gods_info[god_name]
    img = god_images.get(god_name)
    popup = ctk.CTkToplevel(app)
    popup.title(god_name)
    popup.geometry("500x600")
    
    scroll = ctk.CTkScrollableFrame(popup)
    scroll.pack(fill="both", expand=True)
    
    if img:
        img_label = ctk.CTkLabel(scroll, image=img, text="")
        img_label.image = img
        img_label.pack(pady=10)
    
    ctk.CTkLabel(scroll, text=god_name, font=("Arial", 20, "bold")).pack(pady=(0,5))
    ctk.CTkLabel(scroll, text=f"Roman Name: {data['roman_name']}", font=("Arial", 12, "italic")).pack(pady=(0,5))
    ctk.CTkLabel(scroll, text="Epithets: " + ", ".join(data["epithets"]), wraplength=450).pack(pady=(0,5))
    ctk.CTkLabel(scroll, text="Domains: " + ", ".join(data["domains"]), wraplength=450).pack(pady=(0,5))
    ctk.CTkLabel(scroll, text="Symbols: " + ", ".join(data["symbols"]), wraplength=450).pack(pady=(0,5))
    
    family = data["family"]
    ctk.CTkLabel(scroll, text="Family:", font=("Arial", 14, "bold")).pack(pady=(10,0))
    for rel, members in family.items():
        ctk.CTkLabel(scroll, text=f"{rel.title()}: {', '.join(members) if members else 'None'}", wraplength=450).pack(pady=(0,2))
    
    ctk.CTkLabel(scroll, text="Famous Myths:", font=("Arial", 14, "bold")).pack(pady=(10,0))
    for myth in data["famous_myths"]:
        ctk.CTkLabel(scroll, text="• " + myth, wraplength=450, justify="left").pack(anchor="w", padx=10)
    
    ctk.CTkLabel(scroll, text="Fun Facts:", font=("Arial", 14, "bold")).pack(pady=(10,0))
    for fact in data["fun_facts"]:
        ctk.CTkLabel(scroll, text="• " + fact, wraplength=450, justify="left").pack(anchor="w", padx=10)

# ---------- Main App ----------
app = ctk.CTk()
app.title("Olympus: The Twelve Gods")
app.geometry("1000x700")

scroll_frame = ctk.CTkScrollableFrame(app, corner_radius=0)
scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

cards_list = []

# Create cards
for god in gods_info:
    card = ctk.CTkFrame(scroll_frame, width=CARD_WIDTH, height=CARD_HEIGHT, corner_radius=15)
    card.grid_propagate(False)
    
    img = god_images.get(god)
    if img:
        img_label = ctk.CTkLabel(card, image=img, text="")
        img_label.image = img
        img_label.pack(pady=(10,5))
    
    ctk.CTkLabel(card, text=god, font=("Arial", 16, "bold")).pack(pady=(0,5))
    ctk.CTkLabel(card, text=gods_info[god]["description"], wraplength=180, font=("Arial", 10), fg_color="transparent", justify="center").pack(pady=(0,10))
    
    card.bind("<Button-1>", lambda e, g=god: show_popup(g))
    
    cards_list.append(card)

# ---------- Layout cards in grid ----------
def layout_cards():
    width = scroll_frame.winfo_width()
    if width == 1:
        app.after(100, layout_cards)
        return
    columns = max(1, width // (CARD_WIDTH + CARD_PADDING))
    row, col = 0, 0
    for card in cards_list:
        card.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col >= columns:
            col = 0
            row += 1

scroll_frame.bind("<Configure>", lambda e: layout_cards())
layout_cards()

app.mainloop()
