import pygame
pygame.init()

back = (200, 255, 255)
game = True

window = pygame.display.set_mode((500, 500))
window.fill(back)

clock = pygame.time.Clock()

#класс прямоугольника
class Area():
    def __init__(self, x, y, width=10, heigth=10, color=back):
        self.rect = pygame.Rect(x, y, width, heigth)#создание прямоугольника в кординатах x и y
        self.fill_color = color#свойство с цветом прямоугольника
    #метод смены цвета карточки
    def change_color(self, new_color):
        self.fill_color = new_color
    #создание обводки у карточки(на входе принимает цвет обводки и толщину)
    def outline(self, color_line, width_line):
        pygame.draw.rect(window, color_line, self.rect, width_line)
    #метод отображения карточки на экране (pygame.draw.rect - отрисовывает именно прямоугольник)
    def fill(self):
        pygame.draw.rect(window, self.fill_color, self.rect)

class Picture(Area):
    def __init__(self, filename, x, y, width=10, heigth=10, color=back):
        super().__init__(x, y, width, heigth, color)
        self.image = pygame.image.load(filename)
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
    def set_text(self, text, size, text_color):
        font = pygame.font.SysFont('verdana', size) #создаем шрифт(начертание по умолчанию и размером size)
        self.label = font.render(text, True, text_color) #создаете надпись для отображения(текст, видимость, цвет)
    #метод для отображения текста 
    #позиция объектов фиксируется по левому верхнему углу и чтобы текст выглядел лучше добавляем отступы(shift)
    def draw(self, shift_x, shift_y):
        self.fill()#отрисовали прямоугольник
        window.blit(self.label, (self.rect.x + shift_x, self.rect.y + shift_y))#отобразили поверх прямоугольника надпись

start_x = 5
start_y = 5
count = 9
enemies = []
for line in range(3): #0, 1, 2
    y = start_y +(55*line)
    x = start_x + (27.5*line)
    for element in range(count):
        enemy = Picture('enemy.png', x, y, 50, 50)
        enemies.append(enemy)
        x += 55
    count -=1

platform_x = 200
ball = Picture('ball.png', 225, 200, 50, 50)
platform = Picture('platform.png', platform_x, 300, 100, 30)

move_right = False
move_left = False

dx = 3
dy = 3

while game:

    ball.fill()
    platform.fill()

    for enemy in enemies:
        enemy.draw()

        if enemy.rect.colliderect(ball.rect):
            enemies.remove(enemy)
            enemy.fill()
            dy *= -1.1

    ball.rect.x += dx
    ball.rect.y += dy

    if ball.rect.colliderect(platform.rect):
        dy *= -1

    if ball.rect.y <= 0:
        dy *= -1

    if ball.rect.x <= 0 or ball.rect.x >= 450:
        dx *= -1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False

    if move_right: #
        platform.rect.x += 3

    if move_left:
        platform.rect.x -= 3

    if ball.rect.y > 310:
        lose = Label(150, 170, 50, 50, back)
        lose.set_text('YOU LOSE', 60, (255,0,0))
        lose.draw(10,10)
        game = False

    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)
