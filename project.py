import pygame
import math


def get_colour(x: int, y: int, dist: int, side, map):
    if side == 0:
        match map[x][y]:
            case 1:
                colour = (255 - dist * 6, 0, 0)
            case 2:
                colour = (0, 255 - dist * 6, 0)
            case 3:
                colour = (0, 0, 255 - dist * 6)
            case 4:
                colour = (255 - dist * 6, 255 - dist * 6, 255 - dist * 6)
            case _:
                colour = (255 - dist * 6, 255 - dist * 6, 0)
    else:
        match map[x][y]:
            case 1:
                colour = (200 - dist * 6, 0, 0)
            case 2:
                colour = (0, 200 - dist * 6, 0)
            case 3:
                colour = (0, 0, 200 - dist * 6)
            case 4:
                colour = (200 - dist * 6, 200 - dist * 6, 200 - dist * 6)
            case _:
                colour = (200 - dist * 6, 200 - dist * 6, 0)
    return colour


def get_dt(dt, fps, clock):
    dt = clock.tick(fps) / 1000
    move_speed = dt * 5.0
    rot_speed = dt * 3.0
    return (dt, move_speed, rot_speed)


def fix_colour(colour):
    pre = list(colour)
    if pre[0] < 0:
        pre[0] = 0
    if pre[1] < 0:
        pre[1] = 0
    if pre[2] < 0:
        pre[2] = 0
    return tuple(pre)


def main():
    win_width, win_height = (1024, 512)
    pygame.init()
    screen = pygame.display.set_mode((win_width, win_height))

    pos_x, pos_y = 22, 12
    dir_x, dir_y = -1, 0
    plane_x, plane_y = 0, 0.66
    clock = pygame.time.Clock()
    dt = 0

    # map_width = 24
    # map_height = 24
    map = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    running = True
    while running:
        pygame.display.set_caption(f"Raycaster - FPS: {clock.get_fps():.0f}")
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False

        screen.fill("black")

        rays = win_width
        for i in range(rays):
            cam_x = 2 * i / rays - 1
            ray_x = dir_x + plane_x * cam_x
            ray_y = dir_y + plane_y * cam_x

            # Coords of player in the map
            map_x = math.floor(pos_x)
            map_y = math.floor(pos_y)

            # Length of ray from x or y-side to next x or y-side
            x_off = 1e30 if ray_x == 0 else abs(1 / ray_x)
            y_off = 1e30 if ray_y == 0 else abs(1 / ray_y)

            hit = 0
            side = 0

            # Calculate step and initial side_dist
            if ray_x < 0:
                step_x = -1
                side_dist_x = (pos_x - map_x) * x_off
            else:
                step_x = 1
                side_dist_x = (map_x + 1.0 - pos_x) * x_off
            if ray_y < 0:
                step_y = -1
                side_dist_y = (pos_y - map_y) * y_off
            else:
                step_y = 1
                side_dist_y = (map_y + 1.0 - pos_y) * y_off

            # Perform DDA
            dist = 0
            while hit == 0:
                # Jump to next map square, either in x-direction, or in y-direction
                if side_dist_x < side_dist_y:
                    side_dist_x += x_off
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += y_off
                    map_y += step_y
                    side = 1
                # Check if ray has hit a wall
                if map[map_x][map_y] > 0:
                    hit = 1
                dist += 1

            if side == 0:
                perp_wall_dist = side_dist_x - x_off
            else:
                perp_wall_dist = side_dist_y - y_off

            # Calc height of line
            line_height = win_height / perp_wall_dist

            # Calc lowest and highest pixel to fill current stripe
            draw_start = -line_height / 2 + win_height / 2
            if draw_start < 0:
                draw_start = 0
            draw_end = line_height / 2 + win_height / 2
            if draw_end >= win_height:
                draw_end = win_height - 1

            # Check if colour is negative
            colour = fix_colour(get_colour(map_x, map_y, dist, side, map))

            # Draw line
            pygame.draw.line(
                screen,
                colour,
                (i, draw_start),
                (i, draw_end),
            )

        dt, move_speed, rot_speed = get_dt(dt, 60, clock)
        print(dt, move_speed, rot_speed)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if map[int(pos_x + dir_x * move_speed)][int(pos_y)] == False:
                pos_x += dir_x * move_speed
            if map[int(pos_x)][int(pos_y + dir_y * move_speed)] == False:
                pos_y += dir_y * move_speed
        if keys[pygame.K_s]:
            if map[int(pos_x - dir_x * move_speed)][int(pos_y)] == False:
                pos_x -= dir_x * move_speed
            if map[int(pos_x)][int(pos_y - dir_y * move_speed)] == False:
                pos_y -= dir_y * move_speed
        if keys[pygame.K_d]:
            old_dir_x = dir_x
            dir_x = dir_x * math.cos(-rot_speed) - dir_y * math.sin(-rot_speed)
            dir_y = old_dir_x * math.sin(-rot_speed) + dir_y * math.cos(-rot_speed)
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(-rot_speed) - plane_y * math.sin(-rot_speed)
            plane_y = old_plane_x * math.sin(-rot_speed) + plane_y * math.cos(
                -rot_speed
            )
        if keys[pygame.K_a]:
            old_dir_x = dir_x
            dir_x = dir_x * math.cos(rot_speed) - dir_y * math.sin(rot_speed)
            dir_y = old_dir_x * math.sin(rot_speed) + dir_y * math.cos(rot_speed)
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(rot_speed) - plane_y * math.sin(rot_speed)
            plane_y = old_plane_x * math.sin(rot_speed) + plane_y * math.cos(rot_speed)


        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
