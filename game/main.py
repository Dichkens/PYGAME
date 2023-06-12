import pygame
import numpy

pygame.init()  # 初始化pygame
gameClock = pygame.time.Clock()
gameClock.tick(60)
mainScreen = pygame.display.set_mode((1280, 720))  # Pygame窗口
pygame.display.set_caption("文明6_低配版")  # 标题
ifGameGoing = True
RED = (255, 0, 0)  # 红色，使用RGB颜色
BLACK = (0, 0, 0)  # 黑色
GREEN = (0, 255, 0)  # 绿色
BLUE = (0, 0, 255)  # 蓝色
WHITE = (255, 255, 255)  # 白色
mainBackgroundPic = pygame.image.load("./image/logo.jpg")  # 加载图片
pygame.mixer.music.load("music/menu.mp3")  # 加载音乐
pygame.mixer.music.play(-1)  # 播放音乐

ifGameStarted = False
mainScreen.blit(mainBackgroundPic, (0, 0))
pygame.display.flip()
while ifGameGoing and not ifGameStarted:  # 主界面循环
    for event in pygame.event.get():  # 遍历事件
        if event.type == pygame.QUIT:  # 退出事件
            ifGameGoing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ifGameGoing = False
        if event.type == pygame.MOUSEBUTTONDOWN and not ifGameStarted:
            ifGameStarted = True
mainScreen.fill((150, 150, 150))  # 游戏开始初始化
pygame.display.update()
gameMap = numpy.random.randint(0, 4, (10, 10))
for i in range(9):
    for j in range(9):
        mapBlock = pygame.Rect(100 + i * 50, 100 + j * 50, 40, 40)
        if gameMap[i, j] == 0:
            blockColor = WHITE
        elif gameMap[i, j] == 1:
            blockColor = GREEN
        elif gameMap[i, j] == 2:
            blockColor = BLUE
        elif gameMap[i, j] == 3:
            blockColor = RED
        pygame.draw.rect(mainScreen, blockColor, mapBlock)
pygame.display.update()
while ifGameGoing:  # 游戏开始循环
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 退出事件
            ifGameGoing = False

pygame.quit()  # 退出程序
