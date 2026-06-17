import turtle
import random
import winsound
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ENEMY_NUMBER
from renderer import Wall, Pellet, PowerPellet, UiPen
from actors import Player, Enemy

def init_screen():
    screen = turtle.Screen()
    screen.tracer(0)
    screen.title("Episode 1: PacMan in Python - setup")
    screen.setup(SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10)
    screen.bgcolor("black")
    return screen

def bind_controls(screen,player):
    screen.listen()
    screen.onkeypress(player.turn_right, "Right")
    screen.onkeypress(player.turn_left, "Left")
    screen.onkeypress(player.turn_up, "Up")
    screen.onkeypress(player.turn_down, "Down")

def game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies):
    score_pen.write_score(player.score, player.lives, pellet_pen.stamps, power_pen.stamps)
    lives_pen.write_lives(player.lives, pellet_pen.stamps, power_pen.stamps)
    for (px,py), stamp_id in list(pellet_pen.stamps.items()):
      if player.distance(px, py) < CELL_SIZE / 2 and (px, py) != (player_start_x, player_start_y):
           winsound.PlaySound("eat.wav", winsound.SND_ASYNC)
           pellet_pen.clearstamp(stamp_id)
           del pellet_pen.stamps[(px, py)]
           player.score += 2

      elif player.distance(px, py) < CELL_SIZE / 2 and (px, py) == (player_start_x, player_start_y):
        pellet_pen.clearstamp(stamp_id)
        del pellet_pen.stamps[(px, py)]

    for (px, py), stamp_id in list(power_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2:
            winsound.PlaySound("pacman_eatfruit.wav", winsound.SND_ASYNC)
            power_pen.clearstamp(stamp_id)
            del power_pen.stamps[(px, py)]
            player.score += 50

            player.move_speed += 5
            screen.ontimer(player.reset_speed, 6000)

    player.move()
    player.check_wall_collision()

    for enemy in enemies:
        enemy.move()
        enemy.check_wall_collision()
        enemy.go_after_player()

        if enemy.distance(player) < CELL_SIZE / 2:
            winsound.PlaySound("death.wav", winsound.SND_ASYNC)

            safe_spots = []
            for pellet in pellet_pen.pellets:
                if all(enemy.distance(pellet) > CELL_SIZE * 5 for enemy in enemies):

                    safe_spots.append(pellet)
            player.goto(random.choice(safe_spots))
            player.lives -= 1
    if len(power_pen.stamps) == 0 and len(pellet_pen.stamps) == 0:
        player.state = "stop"
        for enemy in enemies:
            enemy.hideturtle()
            enemy.state = "stop"
        screen.ontimer(screen.bye, 3000)

    if player.lives == 0:
        player.state = "stop"
        player.hideturtle()
        for enemy in enemies:
            enemy.state = "stop"
        screen.ontimer(screen.bye, 3000)

    screen.update()
    screen.ontimer(lambda: game_loop(
        screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies),
                   1000 // 60
                   )



def main():
    screen = init_screen()
    screen.register_shape("billo0.gif")
    screen.register_shape("left.gif")
    screen.register_shape("right.gif")
    screen.register_shape("front.gif")
    screen.register_shape("back.gif")
    screen.register_shape("aish5.gif")
    screen.register_shape("murii.gif")
    screen.register_shape("anay.gif")
    screen.register_shape("butki.gif")
    screen.register_shape("swan.gif")

    wall_pen = Wall()
    pellet_pen = Pellet()
    power_pen = PowerPellet()
    ui_pen = UiPen()
    score_pen = UiPen()
    lives_pen = UiPen()

    wall_pen.draw()
    walls = wall_pen.walls
    pellet_pen.draw()
    pellets = pellet_pen.pellets
    power_pen.draw()
    ui_pen.draw_ui_area()

    player_start_coor = random.choice(pellet_pen.pellets)
    player_start_x = player_start_coor[0]
    player_start_y = player_start_coor[1]
    player = Player(walls)
    player.goto(x= player_start_x, y=player_start_y)
    enemy_opt = ["aish5.gif", "murii.gif", "anay.gif", "butki.gif", "swan.gif"]
    enemies = []
    for _ in range(ENEMY_NUMBER):
        safe_spots = []
        for pellet in pellets:
            if player.distance(pellet) > CELL_SIZE * 5:
                safe_spots.append(pellet)
        enemy_start_x, enemy_start_y = random.choice(safe_spots)
        enemy = Enemy(enemy_start_x, enemy_start_y, walls, player)
        enemy.shape(random.choice(enemy_opt))
        enemies.append(enemy)
    winsound.PlaySound("_start_up.wav", winsound.SND_ASYNC)
    screen.ontimer(lambda : bind_controls(screen, player),2500)
    for enemy in enemies:
        screen.ontimer(enemy.start_move,2500)

    game_loop(screen, player, score_pen, lives_pen, pellet_pen,  power_pen, player_start_x, player_start_y, enemies)
    screen.mainloop()

if __name__ == "__main__":
 main()
