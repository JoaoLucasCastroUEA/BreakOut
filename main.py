import pygame
import os

pygame.init()
# window config
height = 780
width = 712

# Set the screen size and create a Pygame display
size = (width, height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BreakOut - PyGame Edition - 2023-11-30")

# game loop
game_loop = True
game_clock = pygame.time.Clock()

# player
player_x = width/2
player_y = 700
player_move_left = False
player_move_right = False

# ball config
ball_speed_x = -5
ball_speed_y = 5
ball_x = 200
ball_y = 100


def visuals():
    screen.fill((0, 0, 0))
    global player
    player = pygame.draw.rect(screen, (000, 90, 137), (player_x, player_y, 70, 10))

    # walls
    upper_wall = pygame.draw.rect(screen, (255, 255, 255), (0, 0, 712, 60))
    global left_wall
    left_wall = pygame.draw.rect(screen, (255, 255, 255), (0, 0, 10, 780))
    global righ_wall
    righ_wall = pygame.draw.rect(screen, (255, 255, 255), (702, 0, 10, 780))

    # colored walls
    blue_left_wall = pygame.draw.rect(screen, (000, 90, 137), (0, 690, 10, 30))
    blue_right_wall = pygame.draw.rect(screen, (000, 90, 137), (702, 690, 10, 30))

    # ball
    global ball
    ball = pygame.draw.rect(screen, (255, 255, 0), (ball_x, ball_y, 10, 10))


def commands(event):
    global game_loop
    global player_move_right
    global player_move_left

    if event.type == pygame.QUIT:
        game_loop = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            player_move_left = True
        if event.key == pygame.K_RIGHT:
            player_move_right = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            player_move_left = False
        if event.key == pygame.K_RIGHT:
            player_move_right = False

def animations():
    # player pad animation
    global player_x
    if player_move_right and player_x < 630:
        player_x += 7
    else:
        player_x += 0

    if player_move_left and player_x > 10:
        player_x -= 7
    else:
        player_x -= 0
    #print(player,'player')
    #print(ball)

    # ball animation
    global ball_y
    global ball_x
    ball_x += ball_speed_x
    ball_y += ball_speed_y



def colliders():
    global ball
    global righ_wall
    global ball_speed_x
    global ball_speed_y
    global ball_y
    if ball.colliderect(righ_wall):
        print('colidiu com direita')
    if ball.colliderect(left_wall):
        print('colidiu com esquerda')
    if ball.colliderect(player):
        print('colidiu')
        ball_speed_y *= -1


    # collision with wall

    if ball_x > 680:
        ball_speed_x *= -1
    if ball_x < 10 :
        ball_speed_x *= -1

    if ball_y < 60:
        ball_speed_y *= -1

while game_loop == True:
    # place the visuals
    visuals()
    # search for commands
    for event in pygame.event.get():
        commands(event)

    # produce the animations
    animations()
    colliders()
    print(ball_y)
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()