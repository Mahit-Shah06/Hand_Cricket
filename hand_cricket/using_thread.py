import pygame
import sys
import tkinter as tk
from tkinter import messagebox
import random
import threading
import toss
import time

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

# Variables
running_pygame = True
current1 = None
current2 = None

# Score Variables
total_runs_inning1 = 0
total_runs_inning2 = 0
wickets_inning1 = 0
wickets_inning2 = 0
current_inning = 1

# Toss Variables (Player or Computer)
tossWin = tk.Tk()
app = toss.CoinTossApp(tossWin)
tossWin.mainloop()
batting = app.user_choice

# Number of Wickets per innings
max_wickets = 1

# Game Screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Animation")

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
            const = f"Player wins by {score_diff} runs."
        else:
            const = f"Computer wins by {score_diff} runs."

    elif total_runs_inning1 < total_runs_inning2:
        wicket_diff = max_wickets - wickets_inning2
        if batting == "Player":
            const = f"Computer wins by {wicket_diff} wickets."
        else:
            const = f"Player wins by {wicket_diff} wickets."

    else:
        const = "It's a draw!"

    if is_game_over():
        messagebox.showinfo("End of Innings 2", const)

        # reset
        total_runs_inning1 = 0
        total_runs_inning2 = 0
        wickets_inning1 = 0
        wickets_inning2 = 0
        current_inning = 1

        # toss
        tossWin = tk.Tk()
        app = toss.CoinTossApp(tossWin)
        tossWin.mainloop()
        batting = app.user_choice

        showinfo()


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
window.title('Press Buttons :)')
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
