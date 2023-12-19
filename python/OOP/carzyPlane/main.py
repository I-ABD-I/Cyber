from pygame import Surface, Rect
from pygame.draw import rect
import pygame
from crazy_plane import CrazyPlane, Position

clock = pygame.time.Clock()


def draw_squares(surf: Surface):
    width = surf.get_width()
    height = surf.get_height()
    for x in range(0, width, width // 10):
        for y in range(0, height, height // 10):
            rect(
                surf,
                (255, 255, 255),
                Rect(x, y, width // 10, height // 10),
                1,
            )


def check_collison(planes: list[CrazyPlane], plane: CrazyPlane):
    for p in [p for p in planes if p is not plane]:
        if plane.distance(p) < 2:
            plane.turn(p)
            if plane.should_destroy():
                planes.remove(plane)
                break


def main():
    pygame.init()
    canvas = pygame.display.set_mode((1000, 750))

    planes = [CrazyPlane(i * 2, i * 2) for i in range(6)]

    while len(planes) > 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        for plane in planes:
            plane.erase(canvas)
            plane.update()

            check_collison(planes, plane)

            print(plane, len(planes))

        for plane in planes:
            plane.draw(canvas)

        draw_squares(canvas)
        clock.tick(1)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    main()
