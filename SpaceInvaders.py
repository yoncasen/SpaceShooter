import random

sounds.alien1963ramzoid.set_volume(0.2)
sounds.alien1963ramzoid.play(loops=-1)


WIDTH = 1280
HEIGHT = 720

TITLE = "Space Journey"
FPS = 30

font_name = "pressstart2p-regular"
background_image = "darkpurple"
explosion_frames = [
    "fragmentation_frame_1",
    "fragmentation_frame_2",
    "fragmentation_frame_3",
    "fragmentation_frame_4",
    "fragmentation_frame_5",
    "fragmentation_frame_6",
]


class Ship(Actor):
    def __init__(self, image, position):
        super().__init__(image, position)

    def move(self, pos):
        self.x = max(0, min(WIDTH, pos[0]))
        self.y = max(0, min(HEIGHT, pos[1]))


class Enemy(Actor):
    def __init__(self, image, position, speed):
        super().__init__(image, position)
        self.speed = speed

    def move(self):
        if self.y < HEIGHT:
            self.y += self.speed
        else:
            self.reset_position()

    def reset_position(self):
        self.y = random.randint(-450, -50)
        self.x = random.randint(0, WIDTH)
        self.speed = random.randint(2, 8)


class Meteor(Actor):
    def __init__(self, image, position, speed):
        super().__init__(image, position)
        self.speed = speed

    def move(self):
        if self.y < HEIGHT:
            self.y += self.speed
        else:
            self.x = random.randint(0, WIDTH)
            self.y = -20
            self.speed = random.randint(2, 10)


class Missile(Actor):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.image = image
        self.pos = position

    def move(self):
        if self.y > 0:
            self.y -= 10
        else:
            return False
        return True


class Explosion(Actor):
    def __init__(self, position):
        super().__init__("fragmentation_frame_0", position)
        self.frame = 0
        self.animation_speed = 0.6

    def update(self):
        self.frame += self.animation_speed
        if self.frame >= len(explosion_frames):
            self.frame = 0
            explosions.remove(self)
        self.image = explosion_frames[int(self.frame)]


mode = "menu"
score = 0
lives = 3
money = 100
ship = Ship("playership2_orange", (300, 400))
space = Actor("darkpurple")

ship1 = Actor("playership1_orange", center=(WIDTH / 4, HEIGHT / 3 * 2))
ship2 = Actor("playership2_orange", center=(WIDTH / 4 * 2, HEIGHT / 3 * 2))
ship3 = Actor("playership3_orange", center=(WIDTH / 4 * 3, HEIGHT / 3 * 2))
ship_prices = {
    "playership1_orange": 50,
    "playership2_orange": 75,
    "playership3_orange": 100,
}

enemies = []
meteors = []
missiles = []
explosions = []

menu_options = ["Start Game", "Shop", "Instructions", "Exit"]
selected_option = 0


def create_enemies(count):
    for _ in range(count):
        x = random.randint(0, WIDTH)
        y = random.randint(-450, -50)
        speed = random.randint(2, 8)
        enemies.append(Enemy("enemyblue2", (x, y), speed))


def create_meteors(count):
    for _ in range(count):
        x = random.randint(0, WIDTH)
        y = random.randint(-450, -50)
        speed = random.randint(2, 10)
        meteors.append(Meteor("meteorbrown_small2", (x, y), speed))


def collisions():
    global mode, score, lives, money
    for enemy in enemies[:]:
        if ship.colliderect(enemy): 
            lives -= 1
            enemies.remove(enemy)
            create_enemies(1)
            if lives <= 0:
                sounds.gameover.set_volume(0.3)
                sounds.gameover.play()
                mode = "gameover"

        for missile in missiles[:]:
            if missile.colliderect(enemy):
                score += 1

                if random.random() < 0.2:
                    money += 50
                enemies.remove(enemy)
                missiles.remove(missile)
                create_enemies(1)

                explosion = Explosion(enemy.pos)
                explosions.append(explosion)

                sounds.explosion.set_volume(0.4)
                sounds.explosion.play()

                break


def move_enemy_ships():
    for enemy in enemies[:]:
        enemy.move()


def move_meteors():
    for meteor in meteors:
        meteor.move()


def move_missiles():
    for missile in missiles[:]:
        if not missile.move():
            missiles.remove(missile)


def buy_ship(selected_ship):
    global money
    price = ship_prices[selected_ship]
    if money >= price:
        money -= price
        ship.image = selected_ship
        sounds.purchase.set_volume(0.5)
        sounds.purchase.play()
        return True
    else:
        sounds.error.set_volume(0.5)
        sounds.error.play()
        return False


def draw():
    global lives

    for x in range(0, WIDTH, images.darkpurple.get_width()):
        for y in range(0, HEIGHT, images.darkpurple.get_height()):
            screen.blit("darkpurple", (x, y))

    if mode == "menu":
        screen.draw.text(
            "SPACE JOURNEY",
            center=(WIDTH // 2, HEIGHT // 3),
            fontsize=60,
            color="white",
            fontname=font_name,
        )
        for index, option in enumerate(menu_options):
            color = "yellow" if index == selected_option else "white"
            screen.draw.text(
                option,
                center=(WIDTH // 2, HEIGHT // 2 + index * 50),
                fontsize=40,
                color=color,
                fontname=font_name,
            )

    elif mode == "shop":
        screen.draw.text(
            "Select Your Ship",
            center=(WIDTH // 2, HEIGHT // 4),
            fontsize=50,
            color="white",
            fontname=font_name,
        )

        ship1.draw()
        screen.draw.text(
            f"{ship_prices['playership1_orange']}",
            center=(WIDTH // 4, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

        ship2.draw()
        screen.draw.text(
            f"{ship_prices['playership2_orange']}",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

        ship3.draw()
        screen.draw.text(
            f"{ship_prices['playership3_orange']}",
            center=(WIDTH // 4 * 3, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

        screen.draw.text(
            f"Money: {money}",
            center=(WIDTH // 2, HEIGHT // 4 + 100),
            fontsize=30,
            color="white",
            fontname=font_name,
        )
        screen.draw.text(
            "Press 'Enter' to return to menu.",
            center=(WIDTH // 2, HEIGHT - 50),
            fontsize=24,
            color="white",
            fontname=font_name,
        )

    elif mode == "instructions":
        screen.draw.text(
            "Instructions",
            center=(WIDTH // 2, HEIGHT // 3),
            fontsize=60,
            color="white",
            fontname=font_name,
        )
        screen.draw.text(
            "Use the mouse to move the ship.",
            center=(WIDTH // 2, HEIGHT // 2 - 50),
            fontsize=30,
            color="white",
            fontname=font_name,
        )
        screen.draw.text(
            "Click to shoot missiles.",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )
        screen.draw.text(
            "Press 'Enter' to return to the menu.",
            center=(WIDTH // 2, HEIGHT // 2 + 50),
            fontsize=30,
            color="white",
            fontname=font_name,
        )

    elif mode == "game":
        for meteor in meteors:
            meteor.draw()
        ship.draw()
        for enemy in enemies:
            enemy.draw()
        for missile in missiles:
            missile.draw()
        for explosion in explosions:
            explosion.draw()

        screen.draw.text(
            f"{score}",
            topright=(WIDTH - 50, 20),
            color="white",
            fontname=font_name,
            fontsize=24,
        )
        for i in range(lives):
            heart_image_actor = Actor("playerlife2_orange", (30 + i * 40, 20))
            heart_image_actor.draw()  

    elif mode == "gameover":
        screen.draw.text(
            "GAME OVER!",
            center=(WIDTH / 2, HEIGHT / 3),
            color="white",
            fontsize=36,
            fontname=font_name,
        )
        screen.draw.text(
            f"Final Score: {score}",
            center=(WIDTH / 2, HEIGHT / 3 + 50),
            color="white",
            fontsize=24,
            fontname=font_name,
        )
        screen.draw.text(
            "Press 'Enter' to return to the menu.",
            center=(WIDTH // 2, HEIGHT // 2),
            fontsize=30,
            color="white",
            fontname=font_name,
        )


def on_mouse_move(pos):
    ship.move(pos)


def update(dt):
    global mode
    if mode == "game":
        move_enemy_ships()
        collisions()
        move_meteors()
        move_missiles()

        for explosion in explosions:
            explosion.update()


def on_mouse_down(button, pos):
    global mode, ship, money
    if mode == "shop":
        if ship1.collidepoint(pos):
            if buy_ship("playership1_orange"):
                pass
        elif ship2.collidepoint(pos):
            if buy_ship("playership2_orange"):
                pass
        elif ship3.collidepoint(pos):
            if buy_ship("playership3_orange"):
                pass
        sounds.alien1963ramzoid.set_volume(0.05)
    elif mode == "game" and button == mouse.LEFT:
        missile = Missile("laserred01", ship.pos)
        sounds.lasergun.set_volume(0.3)
        sounds.lasergun.play()
        missiles.append(missile)


def on_key_down(key):
    global selected_option, mode, lives, enemies, meteors, missiles

    if mode == "menu":
        if key == keys.UP:
            selected_option = (selected_option - 1) % len(menu_options)
        elif key == keys.DOWN:
            selected_option = (selected_option + 1) % len(menu_options)
        elif key == keys.RETURN:
            if menu_options[selected_option] == "Start Game":
                mode = "game"
            elif menu_options[selected_option] == "Shop":
                mode = "shop"
            elif menu_options[selected_option] == "Instructions":
                mode = "instructions"
            elif menu_options[selected_option] == "Exit":
                exit()
    elif mode == "gameover" and keyboard.RETURN:
        mode = "menu"
        score = 0
        lives = 3
        enemies = []
        meteors = []
        missiles = []
        create_enemies(5)
        create_meteors(5)
    elif mode in ["instructions", "shop"]:
        if key == keys.RETURN:
            mode = "menu"


create_enemies(5)
create_meteors(5)
