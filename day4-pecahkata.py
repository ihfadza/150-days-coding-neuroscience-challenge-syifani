# launcher_gui.py
# Tkinter launcher for PecahKata game (Pygame)

import tkinter as tk
from tkinter import messagebox
import subprocess
import json
import os

# Path ke file skor (dihasilkan oleh game)
SCORE_FILE = "score.json"

def start_game():
    subprocess.run(["python", "pecahkata_game.py"])
    update_score_label()

def update_score_label():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
            score = data.get("score", 0)
            label_score.config(text=f"Skor terakhir: {score}")
    else:
        label_score.config(text="Belum ada skor")

# Tkinter GUI
root = tk.Tk()
root.title("PecahKata Launcher")
root.geometry("400x300")

label_title = tk.Label(root, text="PecahKata Game", font=("Arial", 24))
label_title.pack(pady=20)

btn_start = tk.Button(root, text="Mulai Game", command=start_game, font=("Arial", 16))
btn_start.pack(pady=10)

label_score = tk.Label(root, text="Belum ada skor", font=("Arial", 14))
label_score.pack(pady=10)

update_score_label()
root.mainloop()
