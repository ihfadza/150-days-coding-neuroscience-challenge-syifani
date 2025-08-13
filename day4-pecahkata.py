# launcher_gui.py
# Tkinter launcher + Pygame phonics game: PecahKata

import tkinter as tk
from tkinter import messagebox
import subprocess
import json
import os
import pygame
import pyttsx3
import random
import sys

# File skor
SCORE_FILE = "score.json"

# Fungsi simpan skor
def save_score(score):
    with open(SCORE_FILE, "w") as f:
        json.dump({"score": score}, f)

# ==== PYGAME GAME ====
def run_game():
    pygame.init()
    engine = pyttsx3.init()

    WIDTH, HEIGHT = 800, 500
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    GREEN = (100, 200, 100)
    RED = (255, 100, 100)
    BLACK = (0, 0, 0)
    BLUE = (100, 100, 255)
    FONT = pygame.font.SysFont('arial', 36)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PecahKata – Game Fonik")

    words = [
        {"word": "kucing", "syllables": ["ku", "cing"], "meaning": "cat"},
        {"word": "rumah", "syllables": ["ru", "mah"], "meaning": "house"},
        {"word": "bola", "syllables": ["bo", "la"], "meaning": "ball"},
        {"word": "meja", "syllables": ["me", "ja"], "meaning": "table"},
        {"word": "topi", "syllables": ["to", "pi"], "meaning": "hat"},
    ]

    class SyllableButton:
        def __init__(self, text, x, y, w=150, h=80):
            self.text = text
            self.rect = pygame.Rect(x, y, w, h)
            self.clicked = False
            self.correct = False
            self.color = GRAY

        def draw(self, surf):
            pygame.draw.rect(surf, self.color, self.rect, border_radius=10)
            txt = FONT.render(self.text, True, BLACK)
            surf.blit(txt, (self.rect.x + 40, self.rect.y + 20))

        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)

        def update_color(self):
            if self.clicked:
                self.color = GREEN if self.correct else RED
            else:
                self.color = GRAY

    def speak(text):
        engine.say(text)
        engine.runAndWait()

    def draw_text(text, x, y, color=BLACK):
        img = FONT.render(text, True, color)
        screen.blit(img, (x, y))

    def new_round():
        nonlocal current_word, current_index, feedback, selected_output, buttons, can_click, show_next_btn
        current_word = random.choice(words)
        current_index = 0
        feedback = ""
        selected_output = []
        can_click = True
        show_next_btn = False
        create_buttons()

    def create_buttons():
        nonlocal buttons
        sylls = current_word['syllables']
        distractors = random.sample([s for w in words for s in w["syllables"] if s not in sylls], k=2)
        all_sylls = sylls + distractors
        random.shuffle(all_sylls)
        x_start = (WIDTH - (len(all_sylls) * 160)) // 2
        buttons = [SyllableButton(s, x_start + i * 160, 200) for i, s in enumerate(all_sylls)]

    # Init game state
    score = 0
    feedback = ""
    selected_output = []
    current_word = random.choice(words)
    current_index = 0
    buttons = []
    can_click = True
    show_next_btn = False
    create_buttons()

    running = True
    while running:
        screen.fill(WHITE)
        draw_text(f"Tebak: {current_word['word']}", 50, 50)
        draw_text(f"Skor: {score}", WIDTH - 180, 50)
        draw_text(f"{' '.join(selected_output)}", WIDTH // 2 - 100, 130)
        draw_text(feedback, WIDTH // 2 - 100, 320, RED if "Salah" in feedback else GREEN)

        for btn in buttons:
            btn.update_color()
            btn.draw(screen)

        if show_next_btn:
            next_btn = pygame.Rect(WIDTH//2 - 100, 370, 120, 50)
            arti_btn = pygame.Rect(WIDTH//2 + 20, 370, 120, 50)
            pygame.draw.rect(screen, BLUE, next_btn)
            pygame.draw.rect(screen, BLUE, arti_btn)
            draw_text("Next", WIDTH//2 - 85, 375, WHITE)
            draw_text("Arti", WIDTH//2 + 45, 375, WHITE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if show_next_btn:
                    if next_btn.collidepoint(pos):
                        score += 1
                        new_round()
                    elif arti_btn.collidepoint(pos):
                        speak(current_word['meaning'])
                elif can_click:
                    for btn in buttons:
                        if btn.is_clicked(pos) and not btn.clicked:
                            btn.clicked = True
                            speak(btn.text)
                            selected_output.append(btn.text)
                            if btn.text == current_word["syllables"][current_index]:
                                btn.correct = True
                                feedback = "Benar!"
                                current_index += 1
                                if current_index == len(current_word["syllables"]):
                                    can_click = False
                                    show_next_btn = True
                                    for b in buttons:
                                        b.update_color()
                            else:
                                btn.correct = False
                                feedback = "❌ Salah! Ulang ya"
                                can_click = False
                                pygame.display.flip()
                                pygame.time.delay(800)
                                current_index = 0
                                selected_output = []
                                for b in buttons:
                                    b.clicked = False
                                    b.correct = False
                                can_click = True

    save_score(score)
    pygame.quit()
    sys.exit()

# ==== TKINTER LAUNCHER ====
def start_game():
    run_game()
    update_score_label()

def update_score_label():
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            data = json.load(f)
            score = data.get("score", 0)
            label_score.config(text=f"Skor terakhir: {score}")
    else:
        label_score.config(text="Belum ada skor")

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
