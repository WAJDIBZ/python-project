#importation des modules
import myPythonFunctions as myPy 

import sys
from colorama import Fore, init
import time
from time import sleep
import pygame
from rich.console import Console
from rich.text import Text
from PIL import Image, ImageTk
import tkinter as tk
from rich.table import Table

# Utilisation

console = Console()

def blinking_text(message, blink_times=5, delay=0.5):
    for i in range(blink_times):
        console.clear()  # Effacer l'écran
        console.print(Text(message, style="bold red"))  # Afficher le message
        time.sleep(delay)
        console.clear()  # Effacer l'écran
        time.sleep(delay)




def get_sorted_scores():
    players = []
    f = open('userScores.txt', 'r')
    for line in f:
        name, score = line.strip().split(',')
        players.append((name, int(score)))
    #tri a bulle
    n = len(players)
    while True:
        permut = False
        for i in range(n - 1):
            if players[i][1] < players[i + 1][1]:
                players[i], players[i + 1] = players[i + 1], players[i]
                permut = True
        if not permut:
            break
    return players


def display_leaderboard():
    players = get_sorted_scores()
    table = Table(title="Leaderboard", show_header=True, header_style="bold magenta")
    table.add_column("Rank", justify="center")
    table.add_column("Player", justify="center")
    table.add_column("Score", justify="center")

    #top 10 players
    for i, (name, score) in enumerate(players[:10], start=1):
        table.add_row(str(i), name, str(score))

    console.print(table)

def get_user_rank(user_name):
    players = get_sorted_scores()
    for rank, (name, score) in enumerate(players, start=1):
        if name == user_name:
            return rank
    return None

def display_congratulations(user_name):
    rank = get_user_rank(user_name)
    if rank is None:
        print("User not found in the leaderboard.")
        return

    if rank == 1:
        image_path = "gold_prize.png"
        message = f"Bravo {user_name}! Vous êtes au rang {rank} et avez gagné l'or!"
    elif rank == 2:
        image_path = "silver_prize.png"
        message = f"Bravo {user_name}! Vous êtes au rang {rank} et avez gagné l'argent!"
    elif rank == 3:
        image_path = "bronze_prize.png"
        message = f"Bravo {user_name}! Vous êtes au rang {rank} et avez gagné le bronze!"
    else:
        image_path = None
        message = f"Bravo {user_name}! Vous êtes au rang {rank}."


    root = tk.Tk()
    root.title("Congratulations")
    root.geometry("300x400")

    label_message = tk.Label(root, text=message, font=("Helvetica", 14), wraplength=250, justify="center")
    label_message.pack(pady=20)

    if image_path:
        image = Image.open(image_path)
        image = image.resize((150, 150), Image.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(root, image=photo)
        label_image.image = photo 
        label_image.pack(pady=10)

    root.mainloop()


# Initialize colorama
init(autoreset=True)
delays = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.05, 0.01, 0.02, 0.1, 0.2]
def welcome_message():
    message = [
        "Bienvenue dans le Jeu Mathématique!",
        "Un projet pour pratiquer la programmation en Python.",
        "Préparez-vous à résoudre des questions mathématiques.",
        "qui teste notre compréhension",
        "de la règle de calcul arithmétique BODMAS (",
        "B Brackets first",
        "O Orders (i.e. Powers and Square Roots, etc.)",
        "DM Division and Multiplication (left-to-right)",
        "AS Addition and Subtraction (left-to-right)",
        ")"
    ]

    
    for i, (line, char_delay) in enumerate(zip(message, delays), 1):
        for char in line:
            print(Fore.YELLOW + char, end="")
            sys.stdout.flush()
            sleep(char_delay)
        time.sleep(delays[i])
        print('')

def ascii_logo():
    logo_lines = [
        "I",
        "           *****     *****",
        "         *******   *******",
        "       ********* *********",
        "       *******************",
        "        *****************",
        "          *************",
        "            *********",
        "              *****",
        "               ***",
        "                *",
        "PYTHON",
        "*" * 30,
        "      Let the Math Game Begin!      ",
        "*" * 30
    ]
    
    for i, line in enumerate(logo_lines, 1):
        for char in line:
            if i == 1:
                print(Fore.RED + char, end="")
            elif 2 <= i <= 11:
                print(Fore.RED + char, end="")
            elif i == 12:
                print(Fore.GREEN + char, end="")
            elif i == 13:
                print(Fore.BLUE + char, end="")
            elif i == 14:
                print(Fore.MAGENTA + char, end="")
            elif i == 15:
                print(Fore.BLUE + char, end="")
            sys.stdout.flush()
            sleep(0.01)
        time.sleep(0.01)
        print('')
def title_screen():
    console.print(Text("Math Game Challenge", style="bold cyan"))
    console.print(Text("Are you ready to test your math skills?", style="bold magenta"))
    time.sleep(2)
def animate_final_score(score):
    console.print(f"[bold green]Votre score final est : {score}[/bold green]", style="reverse blink")




pygame.init()
title_screen()
welcome_message()
console.clear()
blinking_text("think before respond!", blink_times=5, delay=0.5)
ascii_logo()

# Game logic
try:
    userName = input(Fore.CYAN + 'Entrez votre nom : ')
    userScore = myPy.getUserScore(userName)
    newUser = (userScore == -1)
    if newUser:
        userScore = 0

    while True:
        userChoice = input(Fore.YELLOW + "Tapez '-1' pour quitter ou 'Enter' pour continuer : ")
        if userChoice == '-1':
            break

        # Générer et évaluer la question
        score_increment = myPy.generateQuestion()
        userScore += score_increment

        # Demander à l'utilisateur s'il souhaite une nouvelle question
        repeat = input(Fore.YELLOW + "Voulez-vous une nouvelle question (o/n) ? ").strip().lower()
        if repeat != 'o':
            break

    # Mettre à jour le score dans le fichier
    myPy.updateUserScore(newUser, userName, userScore)
    animate_final_score(userScore)

except Exception as e:
    print(Fore.RED + f"Une erreur est survenue : {e}")
display_leaderboard()
display_congratulations(userName)