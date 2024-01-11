import tkinter as tk
from tkinter import messagebox
import csv
import os
import re
import pygame
import math
import sys
import random
import toss
import time
import threading

def load_data(file_path: str):
    """
    Load existing users from a CSV file.

    Args:
        file_path (str): The path to the CSV file.
    """

    global users

    # Check if the CSV file exists, if not, create it
    if not os.path.exists(file_path):
        with open('users.csv', 'a+', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Username', 'Password', 'W/D/L'])

    # Read existing users from the CSV file
    with open(file_path, 'r+') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        users = [row for row in csvreader]

def register(file_path: str):
    global users, wdl3
    username = username_entry.get()
    password = password_entry.get()
    wdl3 = [0, 0, 0]

    # Check if username already exists
    if username in [user[0] for user in users]:
        messagebox.showerror(
            "Error",
            "Username already exists. Please choose a different username."
        )
    elif len(username) <= 3:
        messagebox.showerror(
            "Error",
            "Username must be more than 3 characters."
        )
    elif not re.search(r"[A-Z]", password):
        messagebox.showerror(
            "Error",
            "Password must have at least 1 uppercase letter, 1 special character and must be greater than 3 characters and less than 16 characters."
        )
    elif not re.search(r"[!@#$%^&_(){};:'/\|/?<>,.]",password):
        messagebox.showerror(
            "Error",
            "Password must have at least 1 uppercase letter, 1 special character and must be greater than 3 characters and less than 16 characters."
        )
    elif len(password) <=3 and len(password) > 16:
        messagebox.showerror(
            "Error",
            "Password must have at least 1 uppercase letter, 1 special character and must be greater than 3 characters and less than 16 characters."
        )
    elif not re.search(r"[013456789]",password):
        messagebox.showerror(
            "Error",
            "Password must have at least 1 uppercase letter, 1 special character and must be greater than 3 characters and less than 16 characters."
        )
    else:
        # Add the new user to the CSV file
        with open(file_path, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([username, password, wdl3])
            messagebox.showinfo("Success", "Registration successful!")

        load_data(file_path)

# Function to log in an existing user
def login():
    """
    Log in an existing user.
    """

    global root, users, username, wdl, users2, index, wdl3
    username = username_entry.get()
    password = password_entry.get()
    users2 = []
    users_list2 = []
    wdl_list = []
    L = [username,password]
    for i in users:
        users_list2.append(i)

    if len(users_list2[0]) == 3:
        for i in users_list2:
            wdl_list.append(i[-1])
            i.pop(-1)
            users2.append(i)

    # Check if username and password match
    if L in users2:
        index = users2.index(L)
        wdl = wdl_list[index]
        wdl2 = list(wdl)
        wdl3 = []
        x = 9
        y = len(wdl2) - x
        if len(wdl2) == x:
            for i in range(1,x-1,3):
                wdl3.append(int(wdl2[i]))
        elif len(wdl2) > x:
            for i in range(1,y+1):
                wdl3.append(int(wdl2[i]))
            for i in range(y+4,len(wdl2),3):
                wdl3.append(int(wdl2[i]))
            
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()   # Destroy the login window to close the program

    else:
        load_data(file_path)
        messagebox.showerror("Error", "Invalid username or password.")

# Pygame Setup
pygame.init()
clock = pygame.time.Clock()

# Variables
file_path = 'users.csv'
running_pygame = True
current1 = None
current2 = None

# Score Variables
total_runs_inning1 = 0
total_runs_inning2 = 0
wickets_inning1 = 0
wickets_inning2 = 0
current_inning = 1

# Tkinter setup
root = tk.Tk()
root.title("Login/Register")

# root.minsize(350, 175)
# root.maxsize(350, 175)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

# Increase font size for labels
tk.Label(frame, text="Username:", font=("Helvetica", 14)).grid(row=0, column=0, pady=5)
tk.Label(frame, text="Password:", font=("Helvetica", 14)).grid(row=1, column=0, pady=5)

# Increase font size for entry widgets
username_entry = tk.Entry(frame, font=("Helvetica", 12), width=20)
username_entry.grid(row=0, column=1, pady=5)

password_entry = tk.Entry(frame, show="*", font=("Helvetica", 12), width=20)
password_entry.grid(row=1, column=1, pady=5)

# Increase font size for buttons
register_button = tk.Button(
    frame,
    text="Register",
    command=lambda: register(file_path),
    font=("Helvetica", 12)
)
register_button.grid(row=2, column=0, pady=10)

login_button = tk.Button(
    frame,
    text="Login",
    command=login,
    font=("Helvetica", 12)
)
login_button.grid(row=2, column=1, pady=10)

load_data(file_path)
root.mainloop()

def display_rules():
    rules_text = """
    Hand Cricket Rules:

    1. Toss:
       - Choose head or tails depending on your choice, where in this case dollar sign is head and yen sign is tails.
       - If you win the toss you can choose batting or bowling.
       - Else the computer will choose batting or bowling.

    3. Playing & Scoring:
       - After choosing, you have to click the buttons corresponding to your choice from 1-10.
       - There are 2 innings in first inning player is batting or bowling depending on how the toss went.
       - If you choose the same number as the computer, and supposing you are batting, than you are out.
       - With the order changed if the same number is pressed as the computer, than the computer is out
       
    4. Winnig.
       - In first inning supposing that you are batting and scored runs of 108, so for computer to win it has to score 108+1 = 109 runs.
       - To win you have to bowl out the computer before reaching 109 runs.
       - It would be the same if the batting was for computer and you had to bowl.
    """

    tk.messagebox.showinfo("Hand Cricket Rules", rules_text)

def continue_game():
    global batting
    root2.destroy()
    pygame.quit()
    # Toss Variables (Player or Computer)
    tossWin = tk.Tk()
    app = toss.CoinTossApp(tossWin)
    tossWin.mainloop()
    batting = app.user_choice
    start_game()
    sys.exit()

def exit_game():
    sys.exit()

# Create the main window
root2 = tk.Tk()
root2.title("OPTIONS")

root2.maxsize(width=300, height=150)

frame2 = tk.Frame(root2, padx = 8, pady = 2, bg = 'grey', borderwidth = '15')
frame2.pack(padx = 20, pady = 10)

# Create a button to display the rules
rules_button = tk.Button(
    frame2,
    text = "Rules",
    command = display_rules,
    font=("Helvetica", 12)
)
rules_button.grid(row = 2, column = 0, pady = 10, padx = 5)

cont_button = tk.Button(
    frame2,
    text = "Start Game",
    command = continue_game,
    font = ("Helvetica", 12)
)
cont_button.grid(row = 2, column = 1, pady = 10, padx = 5)

exit_button = tk.Button(
    frame2,
    text="Exit",
    command=exit_game,
    font=("Helvetica", 12)
)
exit_button.grid(row=2, column=2, pady = 10, padx = 5)

# Pygame Variables
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hand Cricket")

title_font = pygame.font.Font(r'gallery\fonts_py\title_chalk.otf',90)
text_font = pygame.font.Font(r'gallery\fonts_py\PRISTINA.TTF',35)

title_surface = title_font.render('Welcome to Hand Cricket', True, (100, 150, 200))
Welcome_surface = text_font.render(f'Welcome {username}', True, (255, 255, 255))
wdl_surface = text_font.render(f"WIN(S)/Draw(s)/LOSE(S)  : {wdl}", True, (255, 255, 255))
made_by_surface = text_font.render('Made by - Mahit Shah', True, (153, 153, 0))

back_surface = pygame.Surface((1280,720))
back_surface.fill('grey')

player_surface = pygame.image.load(r'gallery\sprites\player-removebg.png').convert_alpha()
computer_surface = pygame.image.load(r'gallery\sprites\computer_bg.png').convert_alpha()
classroom_surface = pygame.image.load(r"gallery\sprites\blank_board_class.png").convert_alpha()

y_pos = 389

center = [150,300]
r = 100

theta = 0


def game_loop():
    global y_pos, center, r, theta

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    y = center[1] + r * math.sin(0.1 * theta)

    screen.blit(back_surface, (0, 0))
    screen.blit(classroom_surface, (100, 0))

    screen.blit(title_surface, (206,142))
    screen.blit(Welcome_surface, (456,250))
    screen.blit(wdl_surface, (386,300))
    screen.blit(made_by_surface, (700,210))

    screen.blit(player_surface, (100, round(y) + 145))
    screen.blit(computer_surface, (725, round(y) + 145))
    theta += 0.1

    clock.tick(120)
    pygame.display.update()

    root2.after(10,game_loop)

def start_game():

    # Animation
    class AnimateP(pygame.sprite.Sprite):
        def __init__(animate, pos_x, pos_y, number):
            super().__init__()
            animate.moving_animation = False
            animate.sprites = []
            animate.number = number

            for i in range(1, 9):
                animate.sprites.append(pygame.image.load(
                    r'gallery\sprites\sprites for animation\player('+str(
                        i)+').png'
                ))
            for i in range(8, 0, -1):
                animate.sprites.append(pygame.image.load(
                    r'gallery\sprites\sprites for animation\player('+str(
                        i)+').png'
                ))
            for i in range(1, 9):
                animate.sprites.append(pygame.image.load(
                    r'gallery\sprites\sprites for animation\player('+str(
                        i)+').png'
                ))

            animate.sprites.append(pygame.image.load(
                fr'gallery\sprites\hand_sign_{animate.number}.png'
            ))

            animate.current_sprite = 0
            animate.image = animate.sprites[animate.current_sprite]

            animate.rect = animate.image.get_rect()
            animate.rect.topleft = [pos_x, pos_y]

        def start(animate):
            animate.current_sprite = 0
            animate.moving_animation = True

        def update(animate, speed):
            if animate.moving_animation:
                animate.current_sprite += speed
                if int(animate.current_sprite) >= len(animate.sprites):
                    animate.current_sprite = len(animate.sprites) - 1
                    animate.moving_animation = False

            animate.image = animate.sprites[int(animate.current_sprite)]

    class AnimateC(pygame.sprite.Sprite):
        def __init__(animate, pos_x, pos_y, number):
            super().__init__()
            animate.moving_animation = False
            animate.sprites = []
            animate.number = number

            for i in range(1, 9):
                animate.sprites.append(pygame.image.load(
                    r'gallery\sprites\sprites for comp animation\comp-'+str(
                        i)+'.png'
                ))
            for i in range(8, 0, -1):
                animate.sprites.append(pygame.image.load(
                    r'gallery\sprites\sprites for comp animation\comp-'+str(
                        i)+'.png'
                ))
            for i in range(1, 9):
                animate.sprites.append(pygame.image.load(
                    r'gallery\sprites\sprites for comp animation\comp-'+str(
                        i)+'.png'
                ))

            animate.sprites.append(pygame.image.load(
                fr'gallery\sprites\hand_sign_{animate.number}.png'
            ))

            animate.current_sprite = 0
            animate.image = animate.sprites[animate.current_sprite]

            animate.rect = animate.image.get_rect()
            animate.rect.topleft = [pos_x, pos_y]

        def start(animate):
            animate.current_sprite = 0
            animate.moving_animation = True

        def update(animate, speed):
            if animate.moving_animation:
                animate.current_sprite += speed
                if int(animate.current_sprite) >= len(animate.sprites):
                    animate.current_sprite = len(animate.sprites) - 1
                    animate.moving_animation = False

            animate.image = animate.sprites[int(animate.current_sprite)]

    # General setup
    pygame.init()
    clock = pygame.time.Clock()

    # Number of Wickets per innings
    max_wickets = 1

    # Game Screen
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Hand Cricket")

    # Creating the sprites and groups
    Player_sprites = {}
    Player = {}

    for i in range(1, 11):
        Player_sprites[i] = pygame.sprite.Group()
        Player[i] = AnimateP(-500, -0, i)
        Player_sprites[i].add(Player[i])

    Computer_sprites = {}
    Computer = {}

    for i in range(1, 11):
        Computer_sprites[i] = pygame.sprite.Group()
        Computer[i] = AnimateC(-10, -0, i)
        Computer_sprites[i].add(Computer[i])

    back_surface = pygame.Surface((1280, 720))
    back_surface.fill('grey')

    title_font = pygame.font.Font(r'gallery\fonts_py\title_chalk.otf', 90)
    text_font = pygame.font.Font(r'gallery\fonts_py\PRISTINA.TTF', 35)

    title_surface = title_font.render(
        'Welcome to Hand Cricket', True, (100, 150, 200))
    made_by_surface = text_font.render('Made by - Mahit Shah', True, (153, 153, 0))

    classroom_surface = pygame.image.load(
        r"gallery\sprites\blank_board_class.png").convert_alpha()


    # tkinter code
    def start_animation(i):
        global current1, current2, current_inning, running_pygame, \
            total_runs_inning1, total_runs_inning2, wickets_inning1, \
            wickets_inning2

        # hide window
        window.withdraw()

        random_num = random.randint(1, 10)
        # random_num = 10     # for debugging
        Computer[random_num].start()
        Player[i].start()
        current1 = i
        current2 = random_num

        if batting == "Player":
            inning1_score = i
            inning2_score = random_num
        elif batting == "Computer":
            inning1_score = random_num
            inning2_score = i

        if current_inning == 1:
            if i == random_num:
                wickets_inning1 += 1
            else:
                total_runs_inning1 += inning1_score

        elif current_inning == 2:
            if i == random_num:
                wickets_inning2 += 1
            else:
                total_runs_inning2 += inning2_score

            evaluate_score()

        if is_inning_over():
            if current_inning == 1:
                current = "Player" if batting == "Computer" else "Computer"
                messagebox.showinfo(
                    "End of Innings 1",
                    f"{current} needs {total_runs_inning1 + 1} runs to win."
                )
                current_inning = 2

        time.sleep(1.5)
        window.deiconify()

    def evaluate_score():

        global total_runs_inning1, total_runs_inning2, wickets_inning1, \
            wickets_inning2, batting, current_inning

        if total_runs_inning1 > total_runs_inning2:
            score_diff = total_runs_inning1 - total_runs_inning2
            if batting == "Player":
                wdl3[0] = int(wdl3[0]) + 1
                const = f"Player wins by {score_diff} runs."
            else:
                wdl3[2] = int(wdl3[2]) + 1
                const = f"Computer wins by {score_diff} runs."

        elif total_runs_inning1 < total_runs_inning2:
            wicket_diff = max_wickets - wickets_inning2
            if batting == "Player":
                wdl3[2] = int(wdl3[2]) + 1
                const = f"Computer wins by {wicket_diff} wickets."
            else:
                wdl3[0] = int(wdl3[0]) + 1
                const = f"Player wins by {wicket_diff} wickets."

        else:
            wdl3[1] = int(wdl3[1]) + 1
            const = "It's a draw!"

        load_data(file_path)

        users[index][-1] = wdl3

        with open(file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Username', 'Password', 'W/D/L'])
            csvwriter.writerows(users)

        if is_game_over():
            messagebox.showinfo("End of Innings 2", const)
            window.destroy()
            pygame.quit(    )
            sys.exit()


    def is_game_over():
        return (current_inning == 2 and is_inning_over()) or \
            (current_inning == 2 and total_runs_inning1 < total_runs_inning2)


    def is_inning_over():
        if current_inning == 1:
            return wickets_inning1 >= max_wickets
        else:
            return wickets_inning2 >= max_wickets


    # Tkinter window
    window = tk.Tk()
    window.title('Choose Runs')
    window.geometry("400x250")
    window.minsize(400, 250)
    window.maxsize(400, 250)
    window.configure(bg='#F0F0F0')  # Set background color

    # Frame
    frame = tk.Frame(window, padx=20, pady=20, bg='#D0D0D0',
                    borderwidth=5, relief=tk.GROOVE)
    frame.pack(padx=10, pady=10)

    # Labels
    label = tk.Label(frame, text='Choose Your Number',
                    font=('Arial', 20, 'bold'), bg='#D0D0D0')
    label.grid(row=0, column=0, columnspan=5, pady=10)

    # Button for starting the animation in Pygame
    for row in range(2):
        for i in range(1, 6):
            player_button = tk.Button(
                frame,
                text=str(i + row*5),
                command=lambda i=i+row*5: start_animation(i),
                font=('Arial', 12),
                width=4,
                height=2
            )
            player_button.grid(row=row+1, column=i-1, pady=5)


    def showinfo():
        inning_surface1 = text_font.render(
            'Inning: 1', True, (255, 255, 255)
        )
        total_runs_surface1 = text_font.render(
            f'Total Runs: {total_runs_inning1}', True, (255, 255, 255)
        )
        wickets_surface1 = text_font.render(
            f'Wickets: {wickets_inning1}', True, (255, 255, 255)
        )
        inning_surface2 = text_font.render(
            'Inning: 2', True, (255, 255, 255)
        )
        total_runs_surface2 = text_font.render(
            f'Total Runs: {total_runs_inning2}', True, (255, 255, 255)
        )
        wickets_surface2 = text_font.render(
            f'Wickets: {wickets_inning2}', True, (255, 255, 255)
        )

        screen.blit(inning_surface1, (206, 300))
        screen.blit(total_runs_surface1, (206, 350))
        screen.blit(wickets_surface1, (206, 400))

        screen.blit(inning_surface2, (650, 300))
        screen.blit(total_runs_surface2, (650, 350))
        screen.blit(wickets_surface2, (650, 400))


    # Pygame loop
    def pygame_loop():
        global current1, current2, running_pygame, current_inning, \
            total_runs_inning1, total_runs_inning2, wickets_inning1, \
            wickets_inning2

        while running_pygame:
            for event in pygame.event.get():
                # Quit pygame loop when the window is closed
                if event.type == pygame.QUIT:
                    running_pygame = False
                    window.quit()

            screen.blit(back_surface, (0, 0))
            screen.blit(classroom_surface, (100, 0))

            screen.blit(title_surface, (206, 142))
            screen.blit(made_by_surface, (700, 220))

            showinfo()

            # draws and updates player's animation
            try:
                Player_sprites[current1].draw(screen)
                Player_sprites[current1].update(0.25)
                Computer_sprites[current2].draw(screen)
                Computer_sprites[current2].update(0.25)
            except KeyError:
                Player_sprites[1].draw(screen)
                Player_sprites[1].update(0.25)
                Computer_sprites[1].draw(screen)
                Computer_sprites[1].update(0.25)
                pass

            clock.tick(120)
            pygame.display.flip()

            # Call the pygame_loop function after 10 milliseconds
            pygame.time.delay(10)


    # Callback function for closing Tkinter window
    def on_closing():
        global running_pygame
        running_pygame = False
        window.destroy()


    # Event to call the on_closing function when the tkinter window is closed
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Start Pygame loop in a separate thread
    pygame_thread = threading.Thread(target=pygame_loop)
    pygame_thread.start()

    # Start Tkinter main loop
    window.mainloop()

    # Wait for Pygame thread to finish before exiting
    pygame_thread.join()

    # Release Pygame resources before exiting
    for i in range(1, 11):
        Player_sprites[i].empty()
        Computer_sprites[i].empty()

    sys.exit()

game_loop()
root2.mainloop()