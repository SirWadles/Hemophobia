import pygame as p
import os
import random

class Move:
    def __init__(self, name, power, cost, desc):
        self.name = name
        self.power = power
        self.cost = cost
        self.desc = desc
    
    def use(self, caster, target, all_targets):
        print(f"{caster.__class__.__name__} is using {self.name}!")
        if "all enemies" in self.desc and all_targets:
            for enemy in all_targets:
                enemy.take_damage(self.power)
                print(f"{self.name} hit {enemy.__class__.__name__} for {self.power} damage")
        else:
            target.take_damage(self.power)
            print(f"{self.name} hit {target.__class__.__name__} for {self.power} damage")
        if "Damage Self" in self.desc:
            caster.health -= 5  
            print(f"{caster.__class__.__name__} took self-damage! Health: {caster.health}")

class Enemy:
    def __init__(self, x, y, sprite_path, health, moves):
        self.original_sprite = p.image.load(sprite_path)
        self.sprite = p.transform.scale(self.original_sprite, (150, 150))
        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.health = health
        self.moves = moves
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy damage: {amount}, Enemy health: {self.health}")

    def select_move(self):
        return random.choice(self.moves)
    
class Boss(Enemy):
    def __init__(self, x, y, sprite_path, health, moves):
        super().__init__(x, y, sprite_path, health, moves)
        self.phase = 1
        self.max_health = health
        self.turn_counter = 0
        self.phase_2_moves = [
            Move("Attack 1", 15, 3, "Strong attack"),
            Move("Attack 2", 20, 4, "A stronger attack")
        ]
        self.second_sprites = 'images\\Game Sprites\\Corrupted One.png'

    def check_phase(self):
        if self.health <= self.max_health // 2:
            self.phase = 2
            self.sprite = p.transform.scale(p.image.load(self.second_sprites), (150, 150))
            self.moves = self.phase_2_moves

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.rect = p.Rect(x, y, 50, 50)

    def take_damage(self, amount):
        self.health -= amount

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class Game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((1000, 600))
        p.display.set_caption("Two Games in One")
        self.clock = p.time.Clock()
        self.running = True
        self.font = p.font.Font(None, 24)
        self.selecting_target = None
        self.selected_move = None  # Store the selected move here
        self.initialize_enemies()  # Keeping this method
        self.turn = "player"
        self.player_turn = True
        self.player_has_made_move = False  # Track whether the player has made a move

        # Sprites
        self.background = p.transform.scale(p.image.load('images\\Game Sprites\\Background.png'), (1000, 600))

        # Frames
        self.frames = self.load_frames('images\\frames\\idle\\')
        self.current_frame_index = 0
        self.frame_counter = 0  # Counter for frame rate control

        # Card Sprites
        self.card_border = p.image.load('images\\Game Sprites\\Card Border.png')
        self.card_art_paths = [
            'images\\Game Sprites\\Self Harm.png',
            'images\\Game Sprites\\Good Blood Fire.png',
            'images\\Game Sprites\\Death Grip.png',
            'images\\Game Sprites\\Abundance.png'
        ]
        self.card_arts_images = [p.image.load(path) for path in self.card_art_paths]

        # Moves
        self.moves = [
            Move("Self Harm", 8, 1, "Damage Self 5 and selected target 8"),
            Move("Blood Fire", 12, 2, "Damage Self 7 and all enemies 12"),
            Move("Death Grip", 6, 2, "If enemy is killed with this, heal 12. If not, heal 6 and damage enemy 6"),
            Move("Abundance", 15, 3, "Heals self 15, but heals random enemy 6")
        ]

        # Card Location
        self.card_rects = [
            p.Rect(100, 470, 120, 180),  # Card 1 position changed to (50, 350)
            p.Rect(280, 470, 120, 180),  # Card 2 position changed to (230, 350)
            p.Rect(490, 470, 120, 180),  # Card 3 position changed to (410, 350)
            p.Rect(640, 470, 120, 180)   # Card 4 position changed to (590, 350)
        ]
        self.player = Player(100, 100)

    def load_frames(self, folder):
        """
        Loads all PNG frames from the specified folder and returns them as a list.
        Assumes the folder contains character animation frames.
        """
        frames = []
        for file_name in sorted(os.listdir(folder)):
            if file_name.endswith(".png"):
                frame = p.image.load(os.path.join(folder, file_name))
                frames.append(p.transform.scale(frame, (130, 130)))  # Adjust size if needed
        return frames
    def run(self):
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                p.display.flip()
                self.clock.tick(60)
            p.quit()
    def update(self):
        # Only proceed with the game if the player has made a move
        if self.turn == "player" and not self.player_has_made_move:
            return  # Don't process enemy's turn if it's not the player's turn

        if self.turn == "player" and self.player_has_made_move:
            self.turn = "enemy"  # Move to enemy's turn after player's action
        elif self.turn == "enemy":
            self.enemy_turn()
        
        self.frame_counter += 1
        if self.frame_counter >= 35:
            self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
            self.frame_counter = 0

    def handle_card_click(self, pos):
        for i, rect in enumerate(self.card_rects):
            if rect.collidepoint(pos):
                self.selected_move = self.moves[i]  # Store the selected move
                print(f"Select an enemy to target for {self.selected_move.name}!")
                break

    def handle_enemy_click(self, pos):
        for enemy in self.enemies:
            if enemy.rect.collidepoint(pos):
                self.apply_selected_move(enemy)
                self.turn = "enemy"  # After player makes a move, switch to enemy turn
                self.player_has_made_move = True  # Mark that the player has finished their turn
                break

    def apply_selected_move(self, target):
        if self.selected_move:
            self.selected_move.use(self.player, target, self.enemies)
            self.check_game_end()
            self.selected_move = None  # Reset after use

    def check_game_end(self):
        # Check if player or enemies have 0 or less health
        if self.player.health <= 0:
            print("You Lose")
            self.running = False
        elif all(enemy.health <= 0 for enemy in self.enemies):
            print("You Win")
            self.running = False

    def enemy_turn(self):
        for enemy in self.enemies:
            if enemy.health > 0:
                move = enemy.select_move()
                print(f"{enemy.__class__.__name__} uses {move.name}!")
                move.use(enemy, self.player, self.enemies)  
        self.check_game_end()
        self.turn = "player"  # After enemy's turn, it's the player's turn
        self.player_has_made_move = False  # Reset for the next player's turn

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.frames[self.current_frame_index], (100, 320))  # Draw character animation frame

        for enemy in self.enemies:
            if enemy.health > 0:  # Only draw alive enemies
                self.screen.blit(enemy.sprite, enemy.rect.topleft)
                health_text = self.font.render(f"HP: {enemy.health}", True, (255, 0, 0))
                self.screen.blit(health_text, (enemy.rect.x, enemy.rect.y - 20))

        # Draw player health
        player_health_text = self.font.render(f"Player HP: {self.player.health}", True, (0, 255, 0))
        self.screen.blit(player_health_text, (20, 20))

        # Draw cards on screen
        for i, card_rect in enumerate(self.card_rects):
            self.screen.blit(self.card_border, card_rect.topleft)  # Card border
            self.screen.blit(self.card_arts_images[i], card_rect.topleft)  # Card art

        # Display turn information
        turn_text = self.font.render(f"Turn: {'Player' if self.turn == 'player' else 'Enemy'}", True, (255, 255, 255))
        self.screen.blit(turn_text, (self.screen.get_width() - turn_text.get_width() - 10, 10))

        # Display "You Lose" or "You Win" messages
        if self.player.health <= 0:
            game_over_text = self.font.render("You Lose!", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.screen.get_width() // 2 - game_over_text.get_width() // 2, self.screen.get_height() // 2))
        elif all(enemy.health <= 0 for enemy in self.enemies):
            win_text = self.font.render("You Win!", True, (0, 255, 0))
            self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2, self.screen.get_height() // 2))

    def handle_events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.running = False
            elif event.type == p.KEYDOWN:   
                if event.key == p.K_ESCAPE:
                        self.running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.selected_move:
                        self.handle_enemy_click(event.pos)
                    else:
                        self.handle_card_click(event.pos)

    def initialize_enemies(self):
        enemy_moves = [
            Move("Strike", 5, 1, "Single Strike Move"),
            Move("Harden", 0, 0, "Blocks a portion of the damage")
        ]
        boss_moves = [
            Move("Block", 0, 0, "Blocks a portion of the damage"),
            Move("Shield Bash", 10, 2, "Strikes foe with a shield")
        ]
        self.enemies = [
            Enemy(500, 312, 'images\\enemies\\Blood Slime.png', 25, enemy_moves),
            Boss(650, 312, 'images\\Game Sprites\\Holy One.png', 100, boss_moves)
        ]
