import pygame
import numpy

pygame.init()  # 初始化pygame

RED = (255, 0, 0)  # 红色，使用RGB颜色
BLACK = (0, 0, 0)  # 黑色
GREEN = (0, 255, 0)  # 绿色
BLUE = (0, 0, 255)  # 蓝色
WHITE = (255, 255, 255)  # 白色

gameClock = pygame.time.Clock()  # test
windowSize = (1280, 720)
mainScreen = pygame.display.set_mode(windowSize)  # Pygame窗口
pygame.display.set_caption("文明6_低配版")  # 标题
ifGameGoing = True

# mainScreen.get_width() / 2
# mainScreen.get_height() / 2


mainBackgroundPic = pygame.image.load("./image/logo.jpg")  # 加载图片
nextTurnPic = pygame.image.load("./image/turn.png")
startPic = pygame.image.load("./image/start.png")
exitPic = pygame.image.load("./image/exit.png")

pygame.mixer.music.load("./music/menu.mp3")  # 加载音乐
pygame.mixer.music.play()  # 播放音乐


class Unit(pygame.sprite.Sprite):
    def __init__(self, step, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.maxMoveStep = step
        self.restMoveStep = step
        self.placeX = x
        self.placeY = y
        self.image = pygame.Surface([20, 20])
        self.image.fill(image)
        self.rect = self.image.get_rect()
        self.rect.x = 110 + self.placeX * 50
        self.rect.y = 110 + self.placeY * 50

    def move(self, xmove, ymove, block):
        if 0 <= self.placeX + xmove <= 9 and 0 <= self.placeY + ymove <= 9:
            if not block[self.placeX + xmove][self.placeY + ymove].ifArmyUnit:
                if block[self.placeX + xmove][self.placeY + ymove].moveCost <= self.restMoveStep:
                    block[self.placeX][self.placeY].ifArmyUnit = False
                    self.placeX += xmove
                    self.placeY += ymove
                    self.restMoveStep -= block[self.placeX][self.placeY].moveCost
                    block[self.placeX][self.placeY].ifArmyUnit = True
                    self.rect.x = 110 + self.placeX * 50
                    self.rect.y = 110 + self.placeY * 50


class Building(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.placeX = x
        self.placeY = y
        self.image = pygame.Surface([20, 20])
        self.image.fill(image)
        self.rect = self.image.get_rect()
        self.rect.x = 110 + self.placeX * 50
        self.rect.y = 110 + self.placeY * 50


class Block(object):
    def __init__(self):
        self.moveCost = 1
        self.mapColor = WHITE
        self.ifArmyUnit = False
        self.ifBuilding = False


def createArmyUnit(step, x, y, color, group, gamemap):
    unit = Unit(step, color, x, y)
    gamemap[x][y].ifArmyUnit = True
    group.add(unit)


def createBuilding(x, y, color, group, gamemap, buildingtype):
    building = Building(color, x, y)
    gamemap[x][y].ifBuilding = True
    group.add(building)


startArea = pygame.Rect(mainScreen.get_width() / 2 - 100, mainScreen.get_height() / 2 + 50,
                        mainScreen.get_width() / 2 + 100, mainScreen.get_height() / 2 + 50)  # 下一回合点击区域
exitArea = pygame.Rect(mainScreen.get_width() / 2 - 100, mainScreen.get_height() / 2 + 100,
                       mainScreen.get_width() / 2 + 100, mainScreen.get_height() / 2 + 100)  # 下一回合点击区域

ifGameStarted = False
font = pygame.font.SysFont('华文隶书', 40)
mainScreen.blit(mainBackgroundPic, (0, 0))
mainScreen.blit(startPic, startArea)
mainScreen.blit(exitPic, exitArea)
pygame.display.flip()

while ifGameGoing and not ifGameStarted:  # 主界面循环
    for event in pygame.event.get():  # 遍历事件
        if event.type == pygame.QUIT:  # 退出事件
            ifGameGoing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ifGameGoing = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 点击开始
            mousePos = pygame.mouse.get_pos()
            if startArea.collidepoint(mousePos):
                ifGameStarted = True
            if exitArea.collidepoint(mousePos):
                ifGameGoing = False
    pygame.display.update()
if ifGameGoing:
    pygame.mixer.music.stop()  # 停止播放音乐
    gameMap = [[Block() for i in range(10)] for j in range(10)]  # 格子类数组
    ranTemp = numpy.random.randint(0, 4, (10, 10))

    for i in range(10):
        for j in range(10):
            mapBlockDis = pygame.Rect(100 + i * 50, 100 + j * 50, 40, 40)
            if ranTemp[i, j] == 0:
                gameMap[i][j].mapColor = WHITE
                gameMap[i][j].moveCost = 1
            elif ranTemp[i, j] == 1:
                gameMap[i][j].mapColor = GREEN
                gameMap[i][j].moveCost = 2
            elif ranTemp[i, j] == 2:
                gameMap[i][j].mapColor = BLUE
                gameMap[i][j].moveCost = 3
            elif ranTemp[i, j] == 3:
                gameMap[i][j].mapColor = RED
                gameMap[i][j].moveCost = 4
            pygame.draw.rect(mainScreen, gameMap[i][j].mapColor, mapBlockDis)
    pygame.display.update()
    ifRoundEnd = False
    numOfRound = 0
    unitNum = 0
    test_group = pygame.sprite.Group()
    createArmyUnit(5, 5, 5, BLACK, test_group, gameMap)
    createArmyUnit(5, 4, 5, BLACK, test_group, gameMap)
    nowUnit = test_group.sprites()[unitNum]

    nextTurnArea = pygame.Rect((1200, 600), windowSize)  # 下一回合点击区域

    while ifGameGoing:  # 游戏开始循环
        for event in pygame.event.get():
            groupLength = len(test_group.sprites())
            if event.type == pygame.QUIT:  # 退出事件
                ifGameGoing = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                ifGameGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    nowUnit.move(-1, 0, gameMap)
                elif event.key == pygame.K_RIGHT:
                    nowUnit.move(1, 0, gameMap)
                elif event.key == pygame.K_UP:
                    nowUnit.move(0, -1, gameMap)
                elif event.key == pygame.K_DOWN:
                    nowUnit.move(0, 1, gameMap)
                elif event.key == pygame.K_RETURN:  # 回车下一回合
                    ifRoundEnd = True
                elif event.key == pygame.K_j:
                    unitNum -= 1
                    nowUnit = test_group.sprites()[unitNum % groupLength]
                elif event.key == pygame.K_k:
                    unitNum += 1
                    nowUnit = test_group.sprites()[unitNum % groupLength]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 点击下一回合
                mousePos = pygame.mouse.get_pos()
                if nextTurnArea.collidepoint(mousePos):
                    ifRoundEnd = True
            if ifRoundEnd:
                numOfRound += 1
                ifRoundEnd = False
                for a in test_group:
                    a.restMoveStep = a.maxMoveStep
                unitNum = 0

            mainScreen.fill((150, 150, 150))  # 循环的绘制部分
            textRestStep = font.render("剩余步数:" + str(nowUnit.restMoveStep), True, BLACK)
            mainScreen.blit(textRestStep, (800, 100))
            textRound = font.render("回合数:" + str(numOfRound), True, BLACK)
            mainScreen.blit(textRound, (800, 200))
            textNow = font.render("当前单位/总单位数:" + str(unitNum % groupLength + 1) + '/' + str(groupLength), True,
                                  BLACK)
            mainScreen.blit(textNow, (800, 300))
            mainScreen.blit(nextTurnPic, (1200, 600))  # 下一回合按钮

            for i in range(10):
                for j in range(10):
                    mapBlockDis = pygame.Rect(100 + i * 50, 100 + j * 50, 40, 40)
                    pygame.draw.rect(mainScreen, gameMap[i][j].mapColor, mapBlockDis)
            test_group.draw(mainScreen)
            renderNow = pygame.Rect(120 + nowUnit.placeX * 50, 120 + nowUnit.placeY * 50, 10, 10)
            pygame.draw.rect(mainScreen, WHITE, renderNow)
            pygame.display.update()
            gameClock.tick(60)

pygame.quit()  # 退出程序
