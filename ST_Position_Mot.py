"""
Created on Wed Feb 12 10:32:31 2025

@author: Alexane Fauveau

READ ME: this code allow you to run a Stroop Test with words and positions.
2 rules are display at the same time: choose the position of the word, or 
the word itself. The color of the word will indicate which rule to follow.
The results are shown at the end. However, it is not recording your data.
You need to download 2 beep .wav (which can be find online) for the correct and 
false beep feedback. Rename them beep_correct and beep, and include them 
in the same file as your code.
"""

#%% Parameters
import pygame
import random
import time
import pandas as pd
from datetime import datetime

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer module for sound

# Load the beep sound (Make sure you have a beep sound file like 'beep.wav')
beep_sound = pygame.mixer.Sound('beep.wav')  # Replace 'beep.wav' with your sound file path
beep_correct_sound = pygame.mixer.Sound('beep_correct.wav')
# Trial data
trials = []

# Set the experiment duration in seconds (20min = 1200)
experiment_duration = 30

# Set up the screen in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Stroop Test - Positions")

# Get screen dimensions for dynamic positioning
screen_width, screen_height = screen.get_size()
center_x = screen_width // 2
center_y = screen_height // 2

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255) 

# Define fonts
small_font = pygame.font.Font(None, 140)
large_font = pygame.font.Font(None, 200)
small_font_text = pygame.font.Font(None, 50)
large_font_text = pygame.font.Font(None, 100)
small_font_text_IE = pygame.font.Font(None, 30)

direction_font = pygame.font.Font(None, 140)


# Function to display text
def display_text(text, font, color, center_x, center_y):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, rect)
    
# Function to draw a cross and place a word
font = pygame.font.Font(None, 100)
def draw_big_cross(font, rect_size, direction_name, direction_position, color):

    # Define the positions of the five squares (center + 4 sides)
    center = pygame.Rect(screen_width//2 - rect_size//2, screen_height//2 - rect_size//2, rect_size, rect_size)
    left = pygame.Rect(center.x - rect_size, center.y, rect_size, rect_size)
    right = pygame.Rect(center.x + rect_size, center.y, rect_size, rect_size)
    top = pygame.Rect(center.x, center.y - rect_size, rect_size, rect_size)
    bottom = pygame.Rect(center.x, center.y + rect_size, rect_size, rect_size)

    # Draw the squares
    pygame.draw.rect(screen, BLACK, left, 3)
    pygame.draw.rect(screen, BLACK, right, 3)
    pygame.draw.rect(screen, BLACK, top, 3)
    pygame.draw.rect(screen, BLACK, bottom, 3)

    # Determine where to place the text
    if direction_position == "GAUCHE":
        text_rect = font.render(direction_name, True, color).get_rect(center=left.center)
    elif direction_position == "DROITE":
        text_rect = font.render(direction_name, True, color).get_rect(center=right.center)
    elif direction_position == "HAUT":
        text_rect = font.render(direction_name, True, color).get_rect(center=top.center)
    elif direction_position == "BAS":
        text_rect = font.render(direction_name, True, color).get_rect(center=bottom.center)

    # Draw the textdirection_arrow
    screen.blit(font.render(direction_name, True, color), text_rect)

 
# Function to show pre-experiment instructions
def show_pre_experiment_instructions():
    screen.fill(WHITE)
    display_text("Instructions", large_font_text, BLACK, center_x, center_y - 100)
    display_text("Vous allez commencer un Stroop Test.", small_font_text, BLACK, center_x, center_y)
    display_text("Un Stroop test est un test cognitif qui permet d'évaluer", small_font_text, BLACK, center_x, center_y + 50)
    display_text("votre capacité à ignorer des informations non pertinentes.", small_font_text, BLACK, center_x, center_y + 100)
    display_text("Presser Espace pour continuer.", small_font_text, BLACK, center_x, center_y + 150)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    waiting = False 
                    
def show_instructions():
    screen.fill(WHITE)
    display_text("Instructions du Stroop Test", large_font_text, BLACK, center_x, center_y - 200)
    display_text("Un mot sera presenté avec une position différente", small_font_text, BLACK, center_x, center_y - 100)
    display_text("Vous allez devoir choisir votre réponse en fonction de la position du mot, ou du mot:", small_font_text, BLACK, center_x, center_y - 50)
    display_text("Gauche, droite, haut, bas.", small_font_text, BLACK, center_x, center_y)
    display_text("Si le mot est bleu, choissisez la position du mot.", small_font_text, BLUE, center_x, center_y + 100)
    display_text("Si le mot est rouge, choissisez le sens du mot.", small_font_text, RED, center_x, center_y + 150)
    display_text("Presser sur Espace pour continuer.", small_font_text, BLACK, center_x, center_y + 200)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False            
              
    
def show_instructions_example1():
    screen.fill(WHITE)
    display_text("Exemples", large_font_text, BLACK, center_x, center_y - 350)
    display_text("Pour commencer, si le mot est bleu, choissisez la position du mot", small_font_text, BLUE, center_x, center_y - 300)
    
    rect_size = 150  # Size of each square
    direction_name = "HAUT"
    direction_position = "BAS"
    color = BLUE
    font = pygame.font.Font(None, 75)
    draw_big_cross(font, rect_size, direction_name, direction_position, color)
    display_text("La bonne réponse est BAS", small_font_text, BLACK, center_x, center_y + 300)
    display_text("Presser sur la flèche de bas pour continuer.", small_font_text, BLACK, center_x, center_y + 350)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    waiting = False
                    beep_correct_sound.play()
           
def show_instructions_example2():
    screen.fill(WHITE)
    display_text("Exemples", large_font_text, BLACK, center_x, center_y - 350)
    display_text("Pour commencer, si le mot est rouge, choissisez le sens du mot", small_font_text, RED, center_x, center_y - 300)
    
    rect_size = 150  # Size of each square
    direction_name = "HAUT"
    direction_position = "BAS"
    color = RED
    font = pygame.font.Font(None, 75)
    draw_big_cross(font, rect_size, direction_name, direction_position, color)
    display_text("La bonne réponse est HAUT", small_font_text, BLACK, center_x, center_y + 300)
    display_text("Presser sur la flèche de haut pour continuer.", small_font_text, BLACK, center_x, center_y + 350)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    waiting = False
                    beep_correct_sound.play()



def show_instructions2():
    screen.fill(WHITE)
    display_text("Tests", large_font_text, BLACK, center_x, center_y - 220)
    display_text(f"Le test dure {experiment_duration:.2f} secondes.", small_font_text, BLACK, center_x, center_y - 150)
    display_text("Un bon score dépend de votre rapidité ET de votre précision.", small_font_text, BLACK, center_x, center_y - 100)
    display_text("Minimisez les erreurs pour obtenir le meilleur résultat possible.", small_font_text, BLACK, center_x, center_y - 50)
    display_text("Un bip sonore aura lieu si vous faites des erreurs.", small_font_text, BLACK, center_x, center_y)
    display_text("Les résultats (temps de réaction et taux d'erreur) seront indiqués à la fin.", small_font_text, BLACK, center_x, center_y + 50 )
    display_text("Quand vous êtes prêt, appuyer sur une des touches directionnelles.", small_font_text, BLACK, center_x, center_y + 100 )
    display_text("Bonne chance !", small_font_text, BLACK, center_x, center_y + 200)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    waiting = False 
                    
def show_results(error_percentage, mean_reaction_time):
    screen.fill(WHITE)
    display_text("Test Complété", large_font_text, BLACK, center_x, center_y - 150)
    display_text(f"Pourcentage d'erreur: {error_percentage:.2f}%", small_font_text, BLACK, center_x, center_y - 50)
    display_text(f"Temps de réaction moyen: {mean_reaction_time:.2f} seconds", small_font_text, BLACK, center_x, center_y )
    display_text("Presser Espace pour continuer.", small_font_text, BLACK, center_x, center_y + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                


# Show the pre-experiment instructions before starting the main test
show_pre_experiment_instructions()
# Show instructions and wait for the user to start
show_instructions()
show_instructions_example1()
show_instructions_example2()

#%% Real test
# Display instructions again before the main test
show_instructions2()  

screen.fill(WHITE)
pygame.display.flip()

# Record the start time
start_time = time.time()
type_trial = ["Test"]


rect_size = 250  # Size of each square

# Run trials until the time limit is reached or 'ESC' is pressed
while True:
    elapsed_time = time.time() - start_time
    if elapsed_time >= experiment_duration:
        break

    # Choose directions name and arrow, colors
    color = random.choice([RED, BLUE])
    
    directions = ["GAUCHE", "DROITE", "HAUT","BAS"]
    
    number_direction_name = random.randint(0, 3)
    direction_name = directions[number_direction_name]
    
    number_direction_position = random.randint(0, 3)
    direction_position = directions[number_direction_position]
    
    screen.fill(WHITE)
    font = pygame.font.Font(None, 80)
    draw_big_cross(font, rect_size, direction_name, direction_position, color)
    pygame.display.flip()
        
    
    # Record the start time for the trial
    trial_start_time = time.time()
    
    # Track the response
    response = None
    reaction_time = None
    correct = None
    
    # Record the presentation time of the numbers
    trial_start_time = time.time()
    presentation_time = trial_start_time - start_time
    
    # Wait for response
    while response is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Record reaction time
                reaction_time = time.time() - trial_start_time
    
                if event.key == pygame.K_LEFT:
                    response = 'GAUCHE'
                elif event.key == pygame.K_RIGHT:
                    response = 'DROITE'
                elif event.key == pygame.K_UP:
                    response = 'HAUT'
                elif event.key == pygame.K_DOWN:
                    response = 'BAS'
                elif event.key == pygame.K_ESCAPE:
                    # Save and exit if escape is pressed
                    pygame.quit()
                    exit()
    
    
    # Check if the response is correct
    correct = False
    if color == BLUE:
        correct = [(response == "GAUCHE" and direction_position == "GAUCHE") or (response == "DROITE" and direction_position == "DROITE") 
                   or (response == "HAUT" and direction_position == "HAUT") or (response == "BAS" and direction_position == "BAS")]
    elif color == RED:
        correct = [(response == "GAUCHE" and direction_name == "GAUCHE") or (response == "DROITE" and direction_name == "DROITE")
                   or (response == "HAUT" and direction_name == "HAUT") or (response == "BAS" and direction_name == "BAS")]
    
    # Record correctness as 0 for correct and 1 for incorrect
    correctness_value = 0 if correct == [True] else 1
    
    
    # If incorrect, play a beep sound
    if correct == [False]:
        beep_sound.play()  # Play beep sound when there is a mistake
    else:
        beep_correct_sound.play()
        
        
    #Define if it is congruent or not : 
    congruent = False
    congruent = [(direction_name == "GAUCHE" and direction_position == "GAUCHE") or (direction_name == "DROITE" and direction_position == "DROITE")
                 or (direction_name == "HAUT" and direction_position == "HAUT") or (direction_name == "BAS" and direction_position == "BAS")]
    


    # Append trial data to trials list
    trial_data = {
        'TypeSession': type_trial,
        'DirectionName': direction_name,
        'DirectionPosition': direction_position,
        'Color': color,
        'Congruent': congruent,
        'PresentationTime': presentation_time,
        'Response': response,
        'ReactionTime': reaction_time,
        'Correct': correct,
        'CorrectnessValue': correctness_value
    }
    trials.append(trial_data)
    
    # Add delay before the next trial
    pygame.time.delay(200)

# After experiment ends, calculate and display results
total_trials = len(trials)
correct_trials = sum(1 for trial in trials if trial['Correct'] == [True])
error_percentage = (1 - correct_trials / total_trials) * 100
mean_reaction_time = sum(trial['ReactionTime'] for trial in trials) / total_trials

show_results(error_percentage, mean_reaction_time)
