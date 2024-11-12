#importer des modules
from random import randint
from os import remove, rename


from colorama import Fore
import pygame

# Initialiser Pygame
pygame.init()

# Charger les effets sonores
correct_sound = pygame.mixer.Sound("sounds/win.mp3")  # Son pour une bonne reponse
wrong_sound = pygame.mixer.Sound("sounds/lose.mp3")      # Son pour une mauvaise reponse



# tache 2: obtenir le score de l'utilisateur
def getUserScore(name):
    s = -1  # Default score if the user is not found
    fich = open('userScores.txt', 'r')

    # Read each line in the file
    for line in fich:
        element = line.strip().split(',')

        # Check if the name matches
        if element[0] == name:
            s = int(element[1])  # Convert score to integer
            break  # Exit the loop once the user is found

    fich.close()
    return s

# tache 3: mettre à jour le score de l'utilisateur
def updateUserScore(newUser, userName, score):
    if newUser:
        fich = open('userScores.txt', 'a')
        fich.write(userName + ',' + str(score) + '\n')
        fich.close()
    else:
        fich = open('userScores.txt', 'r')
        tempfich = open('userScores.tmp', 'w')
        for line in fich:
            element = line.strip().split(',')
            if element[0] == userName:
                element[1] = str(score)
            tempfich.write(element[0] + ',' + element[1] + '\n')
        fich.close()
        tempfich.close()
        remove('userScores.txt')
        rename('userScores.tmp', 'userScores.txt')
    

# tache 4: generer une question
def generateQuestion():
    s = 0
    operandList = [0, 0, 0, 0, 0]
    operatorList = ["", "", "", ""]
    operatorDict = {1: '+', 2: '-', 3: '*', 4: '**'}

    # tache 4.1: mettre a jour d'operandList
    for i in range(4):
        operandList[i] = randint(0, 9)

    # tache 4.2: mettre a jour d'operatorList
    operatorList[0] = operatorDict[randint(1, 4)]
    for i in range(1, 3):
        operatorList[i] = operatorDict[randint(1, 4)]
        while operatorList[i - 1] == '**' and operatorList[i] == '**':
            operatorList[i] = operatorDict[randint(1, 4)]

    # tache 4.3: generer la question(expression mathematique)
    questionString = ""
    for i in range(4):
        questionString += str(operandList[i])
        if i <= 3:
           questionString += operatorList[i]
    # tache 4.4: evaluer la question
    result = eval(questionString)
    # tache 4.5: interagir avec l'utilisateur
    # etape 1: afficher la question
    print(Fore.CYAN + questionString.replace('**', '^'))
    while True:
        try:
            # etape 2: inviter l'utilisateur à repondre
            r = int(input(Fore.YELLOW + 'Entrez votre reponse: '))
           

            # etape 3: evaluer la reponse de l'utilisateur
            if r == result:
                print(Fore.GREEN + 'Bravo! Vous avez reussi!')
                correct_sound.play()
                s = 1
            else:
                print(Fore.RED + 'Desole! Vous avez echoue!\n' + Fore.MAGENTA + f"La reponse correcte est: {result}")
                wrong_sound.play()
            break
        except ValueError:
            print(Fore.RED + 'Entrez un nombre correct!')
    return s
