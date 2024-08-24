import sys
import random

import pygame

pygame.init()

width, height = 1280, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pong Game")

# Controls the FPS of the game
clock = pygame.time.Clock()

ball = pygame.Rect(0, 0, 30, 30)
ball.center = (width / 2, height / 2)

cpu = pygame.Rect(0, 0, 20, 100)
cpu.centery = (height / 2)

player = pygame.Rect(0, 0, 20, 100)
player.midright = (width, height / 2)

ball_speed_x = 6
ball_speed_y = 6
player_speed = 0
cpu_speed = 5

cpu_points, player_points = 0, 0

score_font = pygame.font.Font(None, 100)


def animate_ball():
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0:
        points_won("Player")

    if ball.right >= width:
        points_won("CPU")

    if (ball.bottom >= height or ball.top <= 0):
        ball_speed_y *= -1

    if (ball.colliderect(cpu) or ball.colliderect(player)):
        ball_speed_x *= -1


def points_won(winner):
    global cpu_points
    global player_points

    if winner == "CPU":
        cpu_points += 1

    if winner == "Player":
        player_points += 1

    reset_ball()


def animate_player():
    player.y += player_speed

    if player.top <= 0:
        player.top = 0

    if player.bottom >= height:
        player.bottom = height


def animate_cpu():
    global cpu_speed
    cpu.y += cpu_speed

    if (ball.centery <= cpu.centery):
        cpu_speed = -5

    if (ball.centery >= cpu.centery):
        cpu_speed = 5

    if cpu.top <= 0:
        cpu.top = 0

    if cpu.bottom >= height:
        cpu.bottom = height


def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.x = width / 2
    ball.y = random.randint(10, 100)

    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed = -6
            if event.key == pygame.K_DOWN:
                player_speed = 6
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed = 0
            if event.key == pygame.K_DOWN:
                player_speed = 0

    # Update ball speed
    animate_ball()
    animate_player()
    animate_cpu()

    # Draw the graw objects
    screen.fill("black")

    cpu_score_surface = score_font.render(str(cpu_points), True, "white")
    player_score_surface = score_font.render(str(player_points), True, "white")

    screen.blit(cpu_score_surface, (width / 4, 20))
    screen.blit(player_score_surface, (3 * width / 4, 20))

    pygame.draw.aaline(screen, "white", (width/2, 0), (width/2, height))
    pygame.draw.ellipse(screen, "white", ball)
    pygame.draw.rect(screen, "white", cpu)
    pygame.draw.rect(screen, "white", player)

    # Update the display
    pygame.display.update()
    clock.tick(120)