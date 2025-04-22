import os
import random
import sys
import time
import math
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    kk_img = pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 180, 0.9)
    kk_rct = kk_img.get_rect(center=(300, 200))

    bb_rct = pg.Rect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 20, 20)
    vx, vy = +5, +5

    bb_imgs, bb_accs = init_bb_imgs()

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        acc = bb_accs[idx]

        old_center = bb_rct.center
        bb_rct = bb_img.get_rect()
        bb_rct.center = old_center

        vx_scaled = vx * acc
        vy_scaled = vy * acc
        bb_rct.move_ip(vx_scaled, vy_scaled)

        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def game_over(screen: pg.Surface) -> None:
   
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.set_alpha(150)
    blackout.fill((0, 0, 0))
    screen.blit(blackout, (0, 0))

    sad_img = pg.image.load("fig/8.png")
    sad_img = pg.transform.rotozoom(sad_img, 0, 0.9)
    sad_rct1 = sad_img.get_rect(center=(WIDTH // 2 + 180, HEIGHT // 2))
    sad_rct2 = sad_img.get_rect(center=(WIDTH // 2 - 180, HEIGHT // 2))
    screen.blit(sad_img, sad_rct1)
    screen.blit(sad_img, sad_rct2)

    font = pg.font.SysFont(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
   
    bb_imgs: list[pg.Surface] = []
    bb_accs: list[int] = [a for a in range(1, 11)]
    for r in range(1, 11):
        size = 20 * r
        bb_img = pg.Surface((size, size))
        pg.draw.circle(bb_img, (255, 0, 0), (size // 2, size // 2), size // 2)
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    return bb_imgs, bb_accs



if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
