import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import json

class StartupWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("300x200")
        self.name_label = tk.Label(self, text="Enter your name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        self.high_score_label = tk.Label(self, text="Last High Score:")
        self.high_score_label.pack()
        self.high_score_display = tk.Label(self, text="Name: None\nScore: 0")
        self.high_score_display.pack()
        self.load_high_score()
        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.pack()

    def load_high_score(self):
        try:
            with open("high_score.json", "r") as file:
                data = json.load(file)
                self.high_score_display.config(text="Name: {}\nScore: {}".format(data["name"], data["score"]))
        except FileNotFoundError:
            pass

    def start_game(self):
        name = self.name_entry.get()
        if name:
            game = SnakeGame(name)
            self.destroy()
            game.mainloop()
        else:
            messagebox.showerror("Error", "Please enter your name!")

class SnakeGame(tk.Tk):
    def __init__(self, player_name, width=300, height=300, scale=20, speed=200):
        super().__init__()
        self.player_name = player_name
        self.width = width
        self.height = height
        self.scale = scale
        self.speed = speed
        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.bind("<Key>", self.change_direction)
        self.score = 0
        self.game_over = False
        self.high_score = self.load_high_score()
        self.update_snake()

    def create_food(self):
        x = random.randint(0, (self.width - self.scale) // self.scale) * self.scale
        y = random.randint(0, (self.height - self.scale) // self.scale) * self.scale
        return x, y

    def update_snake(self):
        if not self.game_over:
            self.move_snake()
            self.check_collision()
            self.check_out_of_bounds()
            self.draw_snake()
            self.draw_food()
            self.after(self.speed, self.update_snake)
            self.title("Snake | Score: {}".format(self.score))
        else:
            self.canvas.create_text(self.width // 2, self.height // 2, text="Game Over! Score: {}".format(self.score), font=("Helvetica", 24))
            self.update_high_score()

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Left":
            new_head = (head[0] - self.scale, head[1])
        elif self.direction == "Right":
            new_head = (head[0] + self.scale, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - self.scale)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + self.scale)
        self.snake = [new_head] + self.snake[:-1]

    def check_collision(self):
        if self.snake[0] in self.snake[1:]:
            self.game_over = True
        if self.snake[0] == self.food:
            self.score += 1
            self.snake.append(self.snake[-1])
            self.food = self.create_food()

    def check_out_of_bounds(self):
        head = self.snake[0]
        if (
            head[0] < 0
            or head[0] >= self.width
            or head[1] < 0
            or head[1] >= self.height
        ):
            self.game_over = True

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0],
                segment[1],
                segment[0] + self.scale,
                segment[1] + self.scale,
                fill="green",
                tags="snake",
            )

    def draw_food(self):
        self.canvas.delete("food")
        self.canvas.create_oval(
            self.food[0],
            self.food[1],
            self.food[0] + self.scale,
            self.food[1] + self.scale,
            fill="red",
            tags="food",
        )

    def change_direction(self, event):
        if (
            event.keysym in ["Left", "Right", "Up", "Down"]
            and event.keysym != self.get_opposite_direction()
        ):
            self.direction = event.keysym

    def get_opposite_direction(self):
        if self.direction == "Left":
            return "Right"
        elif self.direction == "Right":
            return "Left"
        elif self.direction == "Up":
            return "Down"
        elif self.direction == "Down":
            return "Up"

    def load_high_score(self):
        try:
            with open("high_score.json", "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {"name": "None", "score": 0}

    def update_high_score(self):
        if self.score > self.high_score["score"]:
            self.high_score["name"] = self.player_name
            self.high_score["score"] = self.score
            with open("high_score.json", "w") as file:
                json.dump(self.high_score, file)
            self.high_score_display.config(text="Name: {}\nScore: {}".format(self.high_score["name"], self.high_score["score"]))

if __name__ == "__main__":
    startup_window = StartupWindow()
    startup_window.mainloop()
