import pygame
import random

#Инициализация Pygame и создание окна
pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

#Определение цветов
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Настройки скорости, очков и шрифтов
speed = 12
speed_coin = 10
score = 0
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#Загрузка изображений
player_image = pygame.image.load("racer-elements\\Player.png")
player_image = pygame.transform.scale(player_image, (50,100))
enemy_image = pygame.image.load("racer-elements\\Enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (50,100))
coin_image = pygame.image.load("racer-elements\\coin.gif")
coin_image = pygame.transform.scale(coin_image, (30,30))
background_image = pygame.image.load("racer-elements\\Street.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

#Звуки
crash_sound = pygame.mixer.Sound("racer-elements\\crash.wav")
background_sound = pygame.mixer.Sound("racer-elements\\background.wav")
background_sound.play(-1)

# Классы машин и монет
class Car:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (50, 100))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self):
        screen.blit(self.image, self.rect)

class Player(Car):
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 50:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH - 50:
            self.rect.x += 10

class Enemy(Car):
    def update(self):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.rect.y = -100
            self.rect.x = random.choice([75, 175, 275])

class Coin:
    def __init__(self):
        self.image = pygame.transform.scale(coin_image, (30,30))
        self.radius = 15
        self.rect = pygame.Rect(random.choice([75, 175, 275]), -100, self.radius * 2, self.radius * 2)
    
    def update(self):
        self.rect.y += speed
        if self.rect.top > HEIGHT:
            self.rect.y = -100
            self.rect.x = random.choice([75, 175, 275])
            
    def update_coin(self):
        self.rect.y += speed_coin
        if self.rect.top > HEIGHT:
            self.rect.y = -100
            self.rect.x = random.choice([75, 175, 275])
    
    def draw(self):
        screen.blit(self.image, self.rect)  

#Создание объектов
player = Player(WIDTH//2 - 25, HEIGHT - 120, player_image)
enemies = [Enemy(random.choice([75, 175, 275]), -100, enemy_image)]
coins = [Coin()]

#Игровой цикл
running = True
clock = pygame.time.Clock()
while running:
    screen.blit(background_image, (0, 0))
    #Управление игроком
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    #Движение врагов
    for enemy in enemies:
        enemy.update()
        enemy.draw()
        if player.rect.colliderect(enemy.rect):
            crash_sound.play()
            pygame.time.delay(1000)
            screen.fill(RED)
            screen.blit(game_over, (30, 250))
            pygame.display.update()
            pygame.time.delay(2000)
            running = False
    
    #Движение и сбор монет
    for coin in coins:
        coin.update_coin()
        coin.draw()
        if player.rect.colliderect(coin.rect):
            score += random.randint(1, 5)
            coin.rect.y = -100
            coin.rect.x = random.choice([75, 175, 275])
    
    player.draw()
    
    score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()