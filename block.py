import pygame
import random
import sys

pygame.init()

pygame.mixer.music.set_volume(0.08)
pygame.mixer.music.load("beats.mp3")
pygame.mixer.music.play()

width = 800
height = 600

red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255,255,0)
#background_color = (11, 238, 207)

player_size = 50
player_pos = [width/2, height-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0, width-enemy_size), 0] #randimize the position of enemy
enemy_list = [enemy_pos]
enemy_speed = 10

screen = pygame.display.set_mode((width, height))
background_image = pygame.image.load("space.webp").convert()

game_over = False

score = 0

clock = pygame.time.Clock()
myFont = pygame.font.SysFont("monospace", 35)

def set_level(score, enemy_speed):
    if score < 20:
        enemy_speed = 5
    elif score < 40:
        enemy_speed = 8
    elif score < 60:
        enemy_speed = 12
    else:
        enemy_speed += 0.001
    return enemy_speed

def drop_enemies(enemy_list):
    delay = random.random() #adds a deplay to the append. Stagers the fall of the blocks
    if len(enemy_list) < 10 and delay < 0.3:
        x_pos = random.randint(0, width-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, blue, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for i, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < height: #determines if enemy pos is on the screen
            enemy_pos[1] += enemy_speed # This makes the cube go down.
        else:
            enemy_list.pop(i)
            score += 1
    return score

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]  #This is the vertical postition
            y = player_pos[1]  #This is the horizontal position
            if event.key == pygame.K_LEFT:
                x -= player_size

            elif event.key == pygame.K_RIGHT:
                x += player_size

            player_pos = [x, y]

    #screen.fill(background_color)  #clears the screen so the blocks update
    screen.blit(background_image, [0, 0])

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score) #int is inmutable. Can't just score += 1.
    enemy_speed = set_level(score, enemy_speed)

    text = "Score: " + str(score)
    label = myFont.render(text, 1, yellow)
    screen.blit(label, (width - 200, height - 40))

    if collision_check(enemy_list, player_pos):
        game_over = True
        break
    draw_enemies(enemy_list)

    pygame.draw.rect(screen, red, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update() #need to update the display to output stuff
