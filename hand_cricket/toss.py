import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import random


class CoinTossApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Coin Toss")
        self.master.geometry("400x400")
        self.master.resizable(False, False)
        self.choice_window = None

        self.canvas = tk.Canvas(self.master, width=200, height=200)
        self.canvas.grid(row=0, column=0, columnspan=2,
                         padx=100, pady=20, sticky="ew")

        self.label = tk.Label(self.master, text="")
        self.label.grid(row=1, column=0, columnspan=2, pady=20, sticky="ew")

        self.heads_button = tk.Button(
            self.master, text="Heads", command=lambda: self.toss_coin(0)
        )
        self.heads_button.grid(row=2, column=0, padx=20, sticky="ew")

        self.tails_button = tk.Button(
            self.master, text="Tails", command=lambda: self.toss_coin(1)
        )
        self.tails_button.grid(row=2, column=1, padx=20, sticky="ew")

        # Assuming images are named "coin-1.png" to "coin-10.png"
        self.heads_images = self.load_images((4, 21), (4, 5))
        self.tails_images = self.load_images((14, 21), (1, 15))

        # Variable to store the user's choice
        self.user_choice = None

    def load_images(self, range1, range2):
        images = []
        folder = r"gallery\sprites\ani2"
        for i in range(range1[0], range1[1]):
            path = os.path.join(folder, f"coin-{i}.png")
            img = Image.open(path)
            img = img.resize((200, 200))
            images.append(ImageTk.PhotoImage(img))
        for i in range(range2[0], range2[1]):
            path = os.path.join(folder, f"coin-{i}.png")
            img = Image.open(path)
            img = img.resize((200, 200))
            images.append(ImageTk.PhotoImage(img))
        return images

    def toss_coin(self, user_choice):
        # 0 represents 'Heads', 1 represents 'Tails'
        result = random.randint(0, 1)
        self.animate_toss(result, user_choice)

    def animate_toss(self, result, user_choice):
        self.label.config(text="")
        self.heads_button.config(state=tk.DISABLED)
        self.tails_button.config(state=tk.DISABLED)

        images = self.heads_images if result == 0 else self.tails_images

        for img in images:
            self.canvas.delete("all")
            self.canvas.create_image(100, 100, image=img, anchor=tk.CENTER)
            self.master.update_idletasks()
            self.master.after(50)

        if result == user_choice:
            messagebox.showinfo("Result","You won, choose bat or bowl")
            self.label.config(text="You win!")
            self.prompt_user_for_choice()
        else:
            messagebox.showinfo("Result",f"You lost, computer chose to {self.random_choice()}")
            self.label.config(text="You lose!")


    def prompt_user_for_choice(self):
        self.choice_window = tk.Toplevel(self.master)
        self.choice_window.title("Choose Bat or Bowl")
        self.choice_window.geometry(
            f"400x100+{self.master.winfo_x()}+{self.master.winfo_y()+200}"
        )
        self.choice_window.resizable(False, False)

        bat_button = tk.Button(
            self.choice_window, text="Bat",
            command=lambda: self.set_user_choice("Bat", "user"),
            width=50
        )
        bat_button.place(x=20, y=20, width=150, height=50)

        bowl_button = tk.Button(
            self.choice_window, text="Bowl",
            command=lambda: self.set_user_choice("Bowl", "user"),
            width=50
        )
        bowl_button.place(x=230, y=20, width=150, height=50)

    def random_choice(self):
        result = random.choice(["Bat", "Bowl"])
        self.set_user_choice(result, "random")
        return result

    def set_user_choice(self, choice, src):

        if self.choice_window:
            self.choice_window.destroy()

        if src == "user":
            txt = "You chose to "
            if choice == "Bat":
                self.user_choice = "Player"
            else:
                self.user_choice = "Computer"
        else:
            txt = "Computer chose to "
            if choice == "Bat":
                self.user_choice = "Computer"
            else:
                self.user_choice = "Player"

        self.display_result(txt+choice)
        self.close()

    def display_result(self, choice):
        self.label.config(text=choice)
        self.heads_button.config(state=tk.NORMAL)
        self.tails_button.config(state=tk.NORMAL)

    def close(self):
        self.master.destroy()


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = CoinTossApp(root)
    root.mainloop()

    # Access user's choice after main loop
    user_choice = app.user_choice