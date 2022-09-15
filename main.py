import pygame,os,time,random
from pygame import mixer


pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Shooter Tutorial")
messagefont = pygame.font.SysFont("comicsans", 50)

pygame.mixer.music.load(os.path.join("assets", "music.mp3"))
pygame.mixer.music.play(-1)

ENEMY1 = pygame.image.load(os.path.join("assets", "enemy1.png"))
ENEMY2 = pygame.image.load(os.path.join("assets", "enemy2.png"))
ENEMY3 = pygame.image.load(os.path.join("assets", "enemy3.png"))
PLAYER = pygame.image.load(os.path.join("assets", "player.png"))

LASER1 = pygame.image.load(os.path.join("assets", "laser1.png"))
LASER2 = pygame.image.load(os.path.join("assets", "laser2.png"))
LASER3 = pygame.image.load(os.path.join("assets", "laser3.png"))
LASER4 = pygame.image.load(os.path.join("assets", "laser4.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

FPS = 60
lives = 10

class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self,v = -10):
        self.y += v

    def out_of_bounds(self, height):
        if self.y <= height and self.y >= 0:
            return False 
        else: 
            return True




class Player:
    TIMER = 10
    def __init__(self, x, y, health=100, v = 5):
        self.x = x
        self.y = y
        self.v = v
        self.health = health
        self.lasers = []
        self.timer = 0
        self.ship_img = PLAYER
        self.laser_img = LASER4
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
  
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_a] and self.x - self.v > 0: 
            self.x -= self.v
        if keys[pygame.K_d] and self.x + self.v + self.ship_img.get_width() < WIDTH: 
            self.x += self.v
        if keys[pygame.K_w] and self.y - self.v > 0:
            self.y -= self.v
        if keys[pygame.K_s] and self.y + self.v + self.ship_img.get_height() + 15 < HEIGHT: 
            self.y += self.v

    def move_lasers(self,objs):
        if self.timer >= self.TIMER:
            self.timer = 0
        elif self.timer > 0:
            self.timer += 1
        for laser in self.lasers:
            laser.move()
            if laser.out_of_bounds(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if collide(laser,obj):
                        objs.remove(obj)
                        if obj.ship_img == ENEMY1:
                          if self.health+20 <= 200:
                           self.health +=20
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                    else:
                        for laserenemy in obj.lasers:
                            if collide(laser,laserenemy):
                                obj.lasers.remove(laserenemy)
                                self.lasers.remove(laser)

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def shoot(self):
        if self.timer == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.timer = 1

class Enemy:
    TIMER = 30
    def __init__(self, x, y, enemytype, health=100, v = 1):
        self.x = x
        self.y = y
        self.v = v
        self.health = health
        self.lasers = []
        self.timer = 0
        if enemytype == "enemy1":
            self.ship_img = ENEMY1 
            self.laser_img = LASER1 
        elif enemytype == "enemy2":
            self.ship_img = ENEMY2 
            self.laser_img = LASER2 
        else:
            self.ship_img = ENEMY3 
            self.laser_img = LASER3                         
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self):
        self.y += self.v

    def shoot(self):
        if self.timer == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.timer = 1

    def move_lasers(self, obj):
        if self.timer >= self.TIMER:
            self.timer = 0
        elif self.timer > 0:
            self.timer += 1
        for laser in self.lasers:
            laser.move(10)
            if laser.out_of_bounds(HEIGHT):
                self.lasers.remove(laser)
            elif collide(laser,obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)


def collide(obj1, obj2):
    return obj1.mask.overlap(obj2.mask, (obj2.x - obj1.x, obj2.y - obj1.y)) != None

player = Player(300, 630)
enemies = []
def move_objects():
        global lives
        player.move()
        for enemy in enemies:
            enemy.move()
            enemy.move_lasers( player)
            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.ship_img.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        player.move_lasers(enemies)

def main():
    run = True
    enemywave = 5
    clock = pygame.time.Clock()
    level = 0
    lost = False
    lost_count = 0
    while run:
        clock.tick(FPS)
        WINDOW.blit(BG, (0,0))
        lives_label = messagefont.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = messagefont.render(f"Level: {level}", 1, (255,255,255))
        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        player.draw(WINDOW)
        for enemy in enemies:
            enemy.draw(WINDOW)
        if lost:
            lost_label = messagefont.render("Better Luck Next Time!", 1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.display.update()
            time.sleep(3)
            break
        pygame.display.update()
        if lives <= 0 or player.health <= 0:
            lost = True            
        if len(enemies) == 0:
            level += 1
            enemywave += 5
            for i in range(enemywave):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["enemy1", "enemy2", "enemy3","enemy2", "enemy3","enemy2", "enemy3"]))
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        move_objects()

def menu():
    run = True
    while run:
        WINDOW.blit(BG, (0,0))
        title_label = messagefont.render("Click to Begin", 1, (255,255,255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


menu()