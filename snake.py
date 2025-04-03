
import pygame
import random

#Инициализация Pygame
pygame.init()
W, H = 500, 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#Создание объектов
snake = [[100, 50], [90, 50], [80, 50]]
fruit = [random.randrange(0, W, 10), random.randrange(0, H, 10)]
direction = "RIGHT"
score = 0
speed = 5
fruits_eaten = 0  # Количество съеденных фруктов

#Загрузка фона
background = pygame.image.load("snakeback.png")
background = pygame.transform.scale(background, (W, H))

running = True

#Функции для вывода счета и завершения игры
def show_score():
    font = pygame.font.SysFont(None, 30)
    text = font.render(f" {score}", True, (128, 0, 128))
    screen.blit(text, (45, 25))

def game_over():
    font = pygame.font.SysFont(None, 40)
    text = font.render(f"Game Over! Score: {score}", True, (255, 0, 0))
    screen.blit(text, (100, 250))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    exit()

#Главный игровой цикл
while running:
    #Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
    
    #Движение змейки
    head = snake[0][:]
    if direction == "UP":
        head[1] -= 10
    elif direction == "DOWN":
        head[1] += 10
    elif direction == "LEFT":
        head[0] -= 10
    elif direction == "RIGHT":
        head[0] += 10
    
    screen.blit(background, (0, 0))

    #Проверка столкновения с фруктом
    if head == fruit:
        score += 1
        fruits_eaten += 1
        fruit = [random.randrange(0, W, 10), random.randrange(0, H, 10)]
        
        # Увеличиваем скорость каждые 5 фруктов
        if fruits_eaten % 5 == 0:
            speed += 1
    else:
        snake.pop()
    
    #Проверка столкновений
    if head in snake or head[0] < 0 or head[0] >= W or head[1] < 0 or head[1] >= H:
        game_over()
    
    #Обновление змейки
    snake.insert(0, head)

    #Отрисовка фруктов и змейки
    pygame.draw.rect(screen, (255, 0, 0), (*fruit, 10, 10))
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, 10, 10))
    
    #Отображение счета и обновление экрана
    show_score()
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()

