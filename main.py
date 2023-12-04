import pygame

pygame.init()
# window config
HEIGHT = 780
WIDTH = 723

# Set the screen size and create a Pygame display
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BreakOut - PyGame Edition - 2023-11-30")

# game loop
game_loop = True
game_clock = pygame.time.Clock()

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets/bounce.wav')

# bricks
brick_dimension = ((WIDTH - 65) / 14, 10)
brick_list = [[[pygame.Rect((j * ((WIDTH + 5) / 14), 150 + i * 15), brick_dimension), 1] for j in range(14)]for i in range(8)]
print(brick_list)
can_break = True

# player
player_x = WIDTH/2
player_y = 700
player_move_left = False
player_move_right = False

# HUD
points = 0
lives = 3
black = (0, 0, 0)
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
font_lives = pygame.font.Font('assets/PixelGameFont.ttf', 20)
font_points = pygame.font.Font('assets/PixelGameFont.ttf', 32)



# ball config
ball_speed_x = -5
ball_speed_y = 5
ball_x = 200
ball_y = 300


def visuals():
    screen.fill((0, 0, 0))
    global player, left_wall, right_wall, ball, brick_dimension
    player = pygame.draw.rect(screen, (000, 90, 137), (player_x, player_y, 70, 10))

    #
    upper_wall = pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, 60))
    left_wall = pygame.draw.rect(screen, (255, 255, 255), (0, 0, 10, 780))
    right_wall = pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 10, 0, 10, 780))
    text_lives = font_lives.render(str(lives), True, black)
    text_points = font_points.render("%03d" % points, True, black)


# bricks
    for i in range(8):
        if i < 2:
            for j in range(14):
                if brick_list[i][j][1]:
                    pygame.draw.rect(screen, (255, 0, 0), brick_list[i][j][0])
        elif i < 4:
            for j in range(14):
                if brick_list[i][j][1]:
                    pygame.draw.rect(screen, (255, 165, 0), brick_list[i][j][0])
        elif i < 6:
            for j in range(14):
                if brick_list[i][j][1]:
                    pygame.draw.rect(screen, (0, 255, 0), brick_list[i][j][0])
        else:
            for j in range(14):
                if brick_list[i][j][1]:
                    pygame.draw.rect(screen, (255, 255, 0), brick_list[i][j][0])

    # colored walls
    for i in range(9):
        # red wall
        if i == 1 or i == 2:
            pygame.draw.rect(screen, (255, 0, 0), (WIDTH - 10, 135 + 15 * i, 10, 10))
            pygame.draw.rect(screen, (255, 0, 0), (0, 135 + 15 * i, 10, 10))

        # orange wall
        if i == 3 or i == 4:
            pygame.draw.rect(screen, (255, 165, 0), (WIDTH - 10, 135 + 15 * i, 10, 10))
            pygame.draw.rect(screen, (255, 165, 0), (0, 135 + 15 * i, 10, 10))

        # green wall
        if i == 5 or i == 6:
            pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 10, 135 + 15 * i, 10, 10))
            pygame.draw.rect(screen, (0, 255, 0), (0, 135 + 15 * i, 10, 10))

        # yellow wall
        if i == 7 or i == 8:
            pygame.draw.rect(screen, (255, 255, 0), (WIDTH - 10, 135 + 15 * i, 10, 10))
            pygame.draw.rect(screen, (255, 255, 0), (0, 135 + 15 * i, 10, 10))

    pygame.draw.rect(screen, (000, 90, 137), (WIDTH - 10, 690, 10, 30))
    pygame.draw.rect(screen, (000, 90, 137), (0, 690, 10, 30))
    display_surface.blit(text_lives, (580, 5))
    display_surface.blit(text_points, (600, 25))





    # ball
    ball = pygame.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, 10, 10))
    if 135 <= ball_y < 165:
        pygame.draw.rect(screen, (255, 0, 0), (ball_x, ball_y, 10, 10))
    elif 165 <= ball_y < 195:
        pygame.draw.rect(screen, (255, 165, 0), (ball_x, ball_y, 10, 10))
    elif 195 <= ball_y < 225:
        pygame.draw.rect(screen, (0, 255, 0), (ball_x, ball_y, 10, 10))
    elif 225 <= ball_y < 255:
        pygame.draw.rect(screen, (255, 255, 0), (ball_x, ball_y, 10, 10))


def commands(event):
    global game_loop, player_move_right, player_move_left

    if event.type == pygame.QUIT or lives == 0:
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
    global player_x, ball_y, ball_x, right_wall, left_wall
    if player_move_right and player_x < (WIDTH - player[2] - right_wall[2]):
        player_x += 7
    else:
        player_x += 0

    if player_move_left and player_x > left_wall[2]:
        player_x -= 7
    else:
        player_x -= 0

    # ball animation
    ball_x += ball_speed_x
    ball_y += ball_speed_y


def colliders():
    global ball, right_wall, ball_speed_x, ball_speed_y, ball_y, can_break, ball_x, lives, points
    if ball.colliderect(player) and ball_speed_y > 0:
        ball_y -= 10
        ball_speed_y *= -1
        bounce_sound_effect.play()

    # collision with wall
    if ball_x > 700:
        can_break = True
        ball_speed_x *= -1
        bounce_sound_effect.play()
    if ball_x < 10:
        ball_speed_x *= -1
        can_break = True
        bounce_sound_effect.play()
    if ball_y < 60:
        ball_speed_y *= -1
        can_break = True
        bounce_sound_effect.play()

    # collision with bricks
    brick_column = ball_x // 52
    if 150 < ball_y < 270:
        brick_row = ball_y // 15 - 10
        if (ball.colliderect(brick_list[brick_row][brick_column][0])
                and brick_list[brick_row][brick_column][1] and can_break):
            ball_speed_y *= -1
            if ball_speed_y < 0:
                ball_y -= ball_speed_y
            else:
                ball_y += ball_speed_y
            can_break = False
            brick_list[brick_row][brick_column][1] = 0
            bounce_sound_effect.play()
            points += 1

    # ball falling off
    if ball_y > 750:
        ball_speed_x = -5
        ball_speed_y = 5
        ball_x = 200
        ball_y = 300
        lives -= 1


while game_loop:
    # place the visuals
    visuals()
    # search for commands
    for event in pygame.event.get():
        commands(event)

    # produce the animations
    animations()
    colliders()
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
