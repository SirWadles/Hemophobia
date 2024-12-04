import asyncio
import pygame as p
import subprocess
import os
from game import Game


p.init()
screen = p.display.set_mode((1850, 900))
p.display.set_caption("Two Games in One")
clock = p.time.Clock()
running = True
background = p.image.load('images\\background hemophobia.png')
npc = p.image.load('images\\Witch(Bigger).gif')
interaction_radius = 50
interaction_active = False
cred_pressed = False
game_begin = True
#Player Things
player_width = 20
player_height = 20
adventurer_pos_x = 450
adventurer_pos_y = 700

#Buttons
border = p.image.load('images\\selected.png')
x_change = 0
button_1 = p.image.load('images\\FuckAssButton1.png')
button_2 = p.image.load('images\\FuckAssButton2.png')
button_3 = p.image.load('images\\FuckAssButton3.png')

# player = p.Rect(2, 4, 20, 20)  # Player's rectangle (x, y, width, height)

# Interactive object's rectangle
object_rect_1 = p.Rect(450, 700, 30, 30)  
object_rect_2 = p.Rect(925, 700, 30, 30)
object_rect_3 = p.Rect(1400, 700, 30, 30) 

#Frames
frame_folder = "images\\frames\\idle"
frames = [p.image.load(os.path.join(frame_folder, f)) for f in sorted(os.listdir(frame_folder))]
current_frame = 0
frame_delay = 50
frame_count = 0

#Colors
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

class Player():
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        
adventurer = Player()

def move(dx, dy):
    global adventurer_pos_x, adventurer_pos_y
    adventurer_pos_x += dx
    adventurer_pos_y += dy

#Proximity Check
def check_proximity(object_rect, player, radius):
    distance = (player.centerx - object_rect.centerx) ** 2 + (player.centery - object_rect.centery) ** 2
    return distance <= radius ** 2

game_instance = Game()
game_instance.running = False

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.KEYDOWN:   
            if event.key == p.K_ESCAPE:
                    running = False
            # Interactions
            if event.key == p.K_e:
                if interaction_active_1:
                    game_begin = False
                    game_instance.running = True
                    game_instance.run()
                elif interaction_active_2:
                    running = False
                elif interaction_active_3:
                    # subprocess.run(['python', 'credit.py']) Wont work fore demo part
                    #Probably a way to simplify the credit code but eh
                    cred_pressed = True
            #Button Movement Keys
            if event.key == p.K_a: #left
                move(-475, 0)
                if x_change < 300:
                    x_change = 0
                else:
                    x_change -= 300
            if event.key == p.K_d: #right
                move(475, 0)
                if x_change > 300:
                    x_change = 700
                else:
                    x_change += 300
        if adventurer_pos_x < 450:
                adventurer_pos_x = 450
        elif adventurer_pos_x > 1400:
                adventurer_pos_x = 1400
        
        
    
    #Menu Code
    if game_begin:
        #Proximity Code
        interaction_active_1 = check_proximity(object_rect_1, p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height), interaction_radius)
        interaction_active_2 = check_proximity(object_rect_2, p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height), interaction_radius)
        interaction_active_3 = check_proximity(object_rect_3, p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height), interaction_radius)


        # Interactive object as rectangle
        player_rect = p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height)
        p.draw.rect(screen, white, player_rect)
        p.draw.rect(screen, red, object_rect_1)  
        p.draw.rect(screen, red, object_rect_2) 
        p.draw.rect(screen, red, object_rect_3)  

        
        # screen.blit(frames[current_frame], (adventurer.pos_x+450, adventurer.pos_y+700))  # Player animation (not for this part)    

        # #Screen Things
        screen.blit(background, (-280, 0))  # Background
        screen.blit(border, (98+x_change, 348))
        screen.blit(button_1, (100,350))
        screen.blit(button_2, (400,350))
        screen.blit(button_3, (700,350))



    #Animation
    frame_count += 1
    if frame_count >= frame_delay:
        frame_count = 0
        current_frame = (current_frame + 1) % len(frames)

    #Credit Code
    if cred_pressed:
        screen.fill((150, 150, 150))
        main = p.font.Font("fonts\\Bokor-Regular.ttf", 50)
        title = main.render("Credits", True, black)
        screen.blit(title, (410, 25))

        norm = p.font.Font("fonts\\Bokor-Regular.ttf", 30)
        text1 = norm.render("Adrian - Artist(Made All Graphics)", True, black)
        text2 = norm.render("Aiden - Coder(Created Cards' System)", True, black)
        text3 = norm.render("Saman - Coder(Created the Enemy System)", True, black)
        text4 = norm.render("Andrew - Musician(Created Every Sound)", True, black)
        text5 = norm.render("Press F to exit credits", True, black)
        screen.blit(text1, (290, 130))
        screen.blit(text2, (250, 185))
        screen.blit(text4, (240, 235))
        screen.blit(text3, (236, 285))
        screen.blit(text5, (336, 385))
        if p.key.get_pressed()[p.K_f]:
            cred_pressed = False
            
    # flip() the display to put your work on screen
    p.display.flip()
    
    clock.tick(60)

p.quit()