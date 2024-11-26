# so much code has become redudant because ive changed the idea after a game jam its in the txt file. im sorry ˊᴖˋ 

import pygame as p
import subprocess
import os

p.init()
screen = p.display.set_mode((1850, 900))
p.display.set_caption("Two Games in One")
clock = p.time.Clock()
running = True
background = p.image.load('images\\background hemophobia.png')
npc = p.image.load('images\\Witch(Bigger).gif')
interaction_radius = 50
interaction_active = False
#Player Things
player_width = 20
player_height = 20
adventurer_pos_x = 450
adventurer_pos_y = 700

#Buttons
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

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        if p.key.get_pressed()[p.K_ESCAPE]:
            running = False
        elif event.type == p.KEYDOWN:
            # Interactions
            if event.key == p.K_e:
                if interaction_active_1:
                    print("Interaction triggered with object 1!")
                elif interaction_active_2:
                    running = False
                elif interaction_active_3:
                    subprocess.run(['python', 'credit.py'])
            #Actual Movement Keys
            if event.key == p.K_a: #left
                move(-475, 0)
            if event.key == p.K_d: #right
                move(475, 0)
        if adventurer_pos_x < 450:
                adventurer_pos_x = 450
        elif adventurer_pos_x > 1400:
                adventurer_pos_x = 1400
    

    #Proximity Code
    interaction_active_1 = check_proximity(object_rect_1, p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height), interaction_radius)
    interaction_active_2 = check_proximity(object_rect_2, p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height), interaction_radius)
    interaction_active_3 = check_proximity(object_rect_3, p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height), interaction_radius)


    # Interactive object as rectangle
    p.draw.rect(screen, red, object_rect_1)  
    p.draw.rect(screen, red, object_rect_2) 
    p.draw.rect(screen, red, object_rect_3)  

    player_rect = p.Rect(adventurer_pos_x, adventurer_pos_y, player_width, player_height)
    p.draw.rect(screen, blue, player_rect)
    # screen.blit(frames[current_frame], (adventurer.pos_x+450, adventurer.pos_y+700))  # Player animation (not for this part)    

    # #Screen Things
    # screen.fill((255, 255, 255))  # Clear with white background
    screen.blit(background, (125, 0))  # Background
    screen.blit(button_1, (200,580))
    screen.blit(button_2, (700,580))
    screen.blit(button_3, (1200,580))

    #Animation
    frame_count += 1
    if frame_count >= frame_delay:
        frame_count = 0
        current_frame = (current_frame + 1) % len(frames)


    #Interaction Result
    if interaction_active_1 or interaction_active_2 or interaction_active_3:
        font = p.font.Font(None, 24)
        text = font.render("Press 'E' to interact", True, blue)
        text_x = adventurer_pos_x + 40
        text_y = adventurer_pos_y
        text_x = max(0, min(text_x, screen.get_width() - text.get_width()))
        text_y = max(0, min(text_y, screen.get_height() - text.get_height()))
        screen.blit(text, (text_x, text_y))
        
    # flip() the display to put your work on screen
    p.display.flip()

    clock.tick(60)

p.quit()