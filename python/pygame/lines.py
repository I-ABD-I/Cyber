from math import cos, pi, sin
import pygame


WIDTH = 720
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lines and Circle")

clock = pygame.time.Clock()

img = pygame.image.load("img.jpg")
screen.blit(img, (0, 0))


alpha = 0
mid = (WIDTH // 2, HEIGHT // 2)
for i in range(50):
    pygame.draw.line(
        screen,
        (255, 0, 0),
        (mid[0] - 350 * cos(alpha), mid[1] - 350 * sin(alpha)),
        (mid[0] + 350 * cos(alpha), mid[1] + 350 * sin(alpha)),
    )
    alpha += 2 * pi / 100

pygame.draw.circle(screen, (0, 0, 0), mid, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
