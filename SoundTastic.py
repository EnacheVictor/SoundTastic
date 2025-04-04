import tkinter as tk
import pygame
import random
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SoundGuesserGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 SoundTastic")
        self.root.geometry("680x440")
        self.root.configure(bg="#f0f8ff")

        self.sound_folder = "sounds"
        self.start_sound = "start.wav"
        self.sounds = {
            file: os.path.splitext(file)[0].lower()
            for file in os.listdir(resource_path(self.sound_folder))
            if file.endswith(".wav") and file != self.start_sound
        }
        self.sound_list = list(self.sounds.items())
        self.total_rounds = 5
        self.current_round = 0
        self.score = 0
        self.time_left = 10
        self.timer_running = False
        self.timer_id = None
        self.current_sound = None

        pygame.mixer.init()
        self.build_ui()
        self.center_window()

        self.play_again_button = tk.Button(
            self.root, text="🔄 Play Again", font=("Arial", 14), bg="#ffa07a", command=self.reset_game
        )
        self.replay_button = tk.Button(
            self.root, text="🔁 Play Sound Again", font=("Arial", 14), bg="#d3d3d3", command=self.replay_sound
        )

    def build_ui(self):
        self.title_label = tk.Label(self.root, text="🔊 Guess the Sound!", font=("Helvetica", 20, "bold"), bg="#f0f8ff")
        self.title_label.pack(pady=20)

        self.start_button = tk.Button(self.root, text="🎮 Press to Play", font=("Arial", 14), bg="#add8e6", command=self.start_game)
        self.start_button.pack(pady=20)

        self.entry = tk.Entry(self.root, font=("Arial", 14), justify="center")
        self.check_button = tk.Button(self.root, text="✔️ Check Answer", font=("Arial", 14), bg="#90ee90", command=self.check_guess)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#f0f8ff")
        self.timer_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), fg="darkred", bg="#f0f8ff")

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def start_game(self):
        self.start_button.pack_forget()
        self.result_label.config(text="🎬 Get ready!", fg="blue")
        self.result_label.pack(pady=10)
        self.play_sound(self.start_sound)
        self.root.after(2700, self.show_game_ui)

    def show_game_ui(self):
        self.entry.pack(pady=10)
        self.check_button.pack(pady=10)
        self.timer_label.pack(pady=5)
        self.replay_button.pack(pady=5)
        self.next_round()

    def next_round(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.current_round < self.total_rounds:
            self.current_sound = random.choice(self.sound_list)
            self.sound_list.remove(self.current_sound)
            self.play_sound(self.current_sound[0])
            self.result_label.config(text=f"Round {self.current_round + 1} of {self.total_rounds}", fg="black")
            self.entry.delete(0, tk.END)
            self.time_left = 15
            self.update_timer()
        else:
            self.show_final_score()

    def replay_sound(self):
        if self.current_sound:
            self.play_sound(self.current_sound[0])

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"⏳ Time left: {self.time_left}s")
            self.time_left -= 1
            self.timer_running = True
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="⏰ Time's up!")
            self.timer_running = False
            self.end_round(f"⛔ Time's up! It was: {self.current_sound[1]}", "red")

    def check_guess(self):
        if self.timer_running:
            guess = self.entry.get().strip().lower()
            correct = guess == self.current_sound[1]
            if correct:
                self.score += 1
            msg = "✅ Correct!" if correct else f"❌ Incorrect! It was: {self.current_sound[1]}"
            color = "green" if correct else "red"
            self.timer_running = False
            self.end_round(msg, color)

    def end_round(self, message, color):
        self.result_label.config(text=message, fg=color)
        self.current_round += 1
        self.root.after(1500, self.next_round)

    def show_final_score(self):
        self.entry.config(state="disabled")
        self.check_button.config(state="disabled")
        self.timer_label.config(text="")
        self.result_label.config(
            text=f"🎉 You guessed {self.score} out of {self.total_rounds} correctly!",
            fg="blue"
        )
        self.play_again_button.pack(pady=20)

    def play_sound(self, filename):
        path = resource_path(os.path.join(self.sound_folder, filename))
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

    def reset_game(self):
        self.current_round = 0
        self.score = 0
        self.time_left = 10
        self.timer_running = False
        self.timer_label.config(text="")
        self.result_label.config(text="")
        self.entry.config(state="normal")
        self.check_button.config(state="normal")
        self.play_again_button.pack_forget()
        self.sound_list = list(self.sounds.items())
        self.show_game_ui()

if __name__ == "__main__":
    root = tk.Tk()
    game = SoundGuesserGame(root)
    root.mainloop()
