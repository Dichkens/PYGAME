import os
import sys
import pygame
import numpy
import random
os.chdir(os.path.dirname(sys.argv[0]))
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


# mainScreen.get_width() / 2
# mainScreen.get_height() / 2

##图片
mainBackgroundPic = pygame.image.load("./image/logo.jpg")  # 加载封面
nextTurnPic = pygame.image.load("./image/turn.png")# 加载下一回合
startPic = pygame.image.load("./image/start.png")# 加载开始按钮
exitPic = pygame.image.load("./image/exit.png")# 加载离开按钮
GoingtoStartPic = pygame.image.load("./image/GoingtoStart.png")# 加载GoingtoStartPic
GoingtoExitPic = pygame.image.load("./image/GoingtoExit.png")# 加载GoingtoExitPic
braverPic = pygame.image.load("./image/braver1.png")# 加载勇士
swordsManPic = pygame.image.load("./image/swordsMan1.png")# 加载剑士
tribePic = pygame.image.load("./image/tribe.png")# 加载部落
musicPausePic = pygame.image.load("./image/musicPause.png")# 加载暂停音乐按钮
musicSkipPic = pygame.image.load("./image/musicSkip.png")# 加载跳过音乐按钮
settlerInBuildingPic = pygame.image.load("./image/settlerInBuilding.png")# 加载建造中的移民
settlerPic = pygame.image.load("./image/settler.png")# 加载移民

##音乐
musicList = ['China', 'BGM1', 'BGM2', 'BGM3', 'BGM4', 'BGM5', 'BGM6', 'Russia' ]
pygame.mixer.music.load("./music/menu.mp3")  # 加载音乐
pygame.mixer.music.play()  # 播放音乐

##点 or 坐标
startArea1 = (mainScreen.get_width() / 2 - 140, mainScreen.get_height() / 2 + 50)
startArea2 = (280,50)
exitArea1 = (mainScreen.get_width() / 2 - 140, mainScreen.get_height() / 2 + 100)
exitArea2 = (280,50)

##区域
startArea = pygame.Rect(startArea1, startArea2)  # 下一回合点击区域
exitArea = pygame.Rect(exitArea1, exitArea2)  # 下一回合点击区域
nextTurnArea = pygame.Rect((1200, 600), windowSize)  # 下一回合点击区域
musicPauseArea = pygame.Rect((1205, 0), (75, 75))  # 音乐暂停点击区域
musicSkipArea = pygame.Rect((1130, 0), (75, 75))  # 音乐跳过点击区域
settlerInBuildingArea = pygame.Rect((40, 60), (280, 300))  # 建造中的移民点击区域

##tag
ifGameStarted = False
ifGameGoing = True
ifGoingtoStart = False
ifGoingtoExit = False
ifMusicPause = False
ifRoundEnd = False
ifBuildingWindow = False

font = pygame.font.SysFont('华文隶书', 40) # 字体

class Unit(pygame.sprite.Sprite):
    def __init__(self, step, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.maxMoveStep = step
        self.restMoveStep = step
        self.placeX = x
        self.placeY = y
        self.image = pygame.Surface([32, 32])
        self.image.fill(image)
        self.rect = self.image.get_rect()
        self.rect.x = 36 + self.placeX * 70
        self.rect.y = 36 + self.placeY * 70
        self.attack = 0
        self.life = 0

    def dead(self):
        self.remove(unit_group)

    def move(self, xmove, ymove, block):
        if 0 <= self.placeX + xmove <= 9 and 0 <= self.placeY + ymove <= 9:  # 移动是否越界
            if not block[self.placeX + xmove][self.placeY + ymove].ifArmyUnit:  # 如果移动位置没人 执行移动
                if block[self.placeX + xmove][self.placeY + ymove].moveCost <= self.restMoveStep:
                    block[self.placeX][self.placeY].ifArmyUnit = False
                    self.placeX += xmove
                    self.placeY += ymove
                    self.restMoveStep -= block[self.placeX][self.placeY].moveCost
                    block[self.placeX][self.placeY].ifArmyUnit = True
                    self.rect.x = 36 + self.placeX * 70
                    self.rect.y = 36 + self.placeY * 70
            elif self.restMoveStep != 0:  # 如果移动位置有人且剩余步数不为0
                for unit in unit_group.sprites():  # 遍历组中的成员判断攻击对象
                    if unit.placeX == self.placeX + xmove and unit.placeY == self.placeY + ymove:
                        break
                self.restMoveStep = 0
                unit.life -= self.attack
                if unit.life <= 0:
                    block[unit.placeX][unit.placeY].ifArmyUnit = False
                    unit.dead()
                    self.move(xmove, ymove, block)
                self.life -= unit.attack + 1
                if self.life <= 0:
                    block[self.placeX][self.placeY].ifArmyUnit = False
                    self.dead()


class Building(pygame.sprite.Sprite):#建筑类
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.placeX = x
        self.placeY = y
        self.image = pygame.Surface([60, 40])
        self.image.fill(image)
        self.rect = self.image.get_rect()
        self.rect.x = 22 + self.placeX * 70
        self.rect.y = 32 + self.placeY * 70


class Block(object):
    def __init__(self):
        self.moveCost = 1
        self.mapColor = WHITE
        self.ifArmyUnit = False
        self.ifBuilding = False


def createArmyUnit(step, x, y, color, group, gamemap, armytype):#创建军队单位
    unit = Unit(step, color, x, y)
    gamemap[x][y].ifArmyUnit = True
    group.add(unit)
    if armytype == "braver":
        unit.image.blit(braverPic, (0, 0))
        unit.life = 10
        unit.attack = 3
    elif armytype == "swordsMan":
        unit.image.blit(swordsManPic, (0, 0))
        unit.life = 20
        unit.attack = 5


def createBuilding(x, y, color, group, gamemap, buildingtype):#创建城市
    building = Building(color, x, y)
    gamemap[x][y].ifBuilding = True
    group.add(building)
    if buildingtype == "tribe":
        building.type = "tribe"
        building.image.blit(tribePic, (0, 0))
        building.life = 25
        building.attack = 3



def buildingWindow(building):#建筑窗口
    ifSwordsMan = False
    ifBuildingWindow = True
    while ifBuildingWindow:
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                ifGameGoing = False
                ifBuildingWindow = False  
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if settlerInBuildingArea.collidepoint(mousePos):
                    
                    ifBuildingWindow = False 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ifBuildingWindow = False
            
        if building.type == "county":
            ifSwordsMan = True
        mainScreen.fill(WHITE)
        mainScreen.blit(settlerInBuildingPic, settlerInBuildingArea)
        if ifSwordsMan:
            mainScreen.blit(swordsManPic, (40, 60))
        textRestStep = font.render("剩余步数:" + str(nowUnit.restMoveStep), True, BLACK)
        mainScreen.blit(textRestStep, (800, 100))
        pygame.display.update()

while ifGameGoing and not ifGameStarted:  # 主界面循环
    for event in pygame.event.get():  # 遍历事件
        if event.type == pygame.QUIT:  # 退出事件
            ifGameGoing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                ifGameGoing = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 点击开始
            mousePos = pygame.mouse.get_pos()
            print(mousePos)                           # 打印鼠标位置
            if startArea.collidepoint(mousePos):
                ifGameStarted = True
            if exitArea.collidepoint(mousePos):
                ifGameGoing = False
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            if startArea.collidepoint(mousePos):
                ifGoingtoStart = True
            else:
                ifGoingtoStart = False
            if exitArea.collidepoint(mousePos):
                ifGoingtoExit = True
            else:
                ifGoingtoExit = False
    mainScreen.blit(mainBackgroundPic, (0, 0)) # 封面
    mainScreen.blit(startPic, startArea1) # 开始按钮
    mainScreen.blit(exitPic, exitArea1) # 离开按钮
    if ifGoingtoStart:
        mainScreen.blit(GoingtoStartPic, startArea)
    if ifGoingtoExit:
        mainScreen.blit(GoingtoExitPic, exitArea)
    pygame.display.update()
if ifGameGoing:
    pygame.mixer.music.load("./music/China.mp3")  # 加载游戏内音乐
    pygame.mixer.music.play()  # 播放音乐
    gameMap = [[Block() for i in range(10)] for j in range(10)]  # 格子类数组
    ranTemp = numpy.random.randint(0, 4, (10, 10))  # 随机数生成

    for i in range(10):
        for j in range(10):  # 根据随机数生成地形
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
    numOfRound = 0
    unitNum = 0
    unit_group = pygame.sprite.Group()
    building_group = pygame.sprite.Group()
    createArmyUnit(5, 5, 5, BLACK, unit_group, gameMap, "braver")
    createArmyUnit(5, 4, 5, BLACK, unit_group, gameMap, "braver")
    createArmyUnit(5, 3, 5, BLACK, unit_group, gameMap, "swordsMan")
    createBuilding(5, 7, BLACK, building_group, gameMap, "tribe")
    nowUnit = unit_group.sprites()[unitNum]

    while ifGameGoing:  # 游戏开始循环
        for event in pygame.event.get():
            groupLength = len(unit_group.sprites())
            mousePos = pygame.mouse.get_pos()
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
                    nowUnit = unit_group.sprites()[unitNum % groupLength]
                elif event.key == pygame.K_k:
                    unitNum += 1
                    nowUnit = unit_group.sprites()[unitNum % groupLength]
                elif event.key == pygame.K_a:
                    createArmyUnit(5, 3, 3, BLACK, unit_group, gameMap, "braver")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 点击下一回合
                print(mousePos)                    # 打印鼠标位置
                if nextTurnArea.collidepoint(mousePos):
                    ifRoundEnd = True
                elif musicPauseArea.collidepoint(mousePos):#音乐暂停
                    ifMusicPause = not ifMusicPause
                    if ifMusicPause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif musicSkipArea.collidepoint(mousePos):#下一首音乐
                    next = random.choice(musicList)
                    pygame.mixer.music.load(r"./music/%s.mp3" % next)
                    pygame.mixer.music.play()
                else:
                    for unit in building_group.sprites():
                        if unit.rect.collidepoint(mousePos):
                            buildingWindow(unit)
                            break
            if ifRoundEnd:
                numOfRound += 1
                ifRoundEnd = False
                for a in unit_group:
                    if a is nowUnit:
                        a.restMoveStep = a.maxMoveStep
                unitNum = 0
            groupLength = len(unit_group.sprites())
            mainScreen.fill((150, 150, 150))  # 循环的绘制部分
            textRestStep = font.render("剩余步数:" + str(nowUnit.restMoveStep), True, BLACK)
            mainScreen.blit(textRestStep, (800, 100))
            textRound = font.render("回合数:" + str(numOfRound) + "/250", True, BLACK)
            mainScreen.blit(textRound, (800, 200))
            if groupLength != 0:
                nowUnit = unit_group.sprites()[unitNum % groupLength]
                textNow = font.render("当前单位/总单位数:" + str(unitNum % groupLength + 1) + '/' + str(groupLength),
                                      True, BLACK)
                textUnitHealth = font.render("生命值:" + str(nowUnit.life), True, BLACK)
            else:
                textNow = font.render("当前单位为0!,全死了", True, BLACK)
                textUnitHealth = font.render("生命值无" , True, BLACK)
            mainScreen.blit(textNow, (800, 300))
            mainScreen.blit(textUnitHealth, (800, 400))
            mainScreen.blit(nextTurnPic, (1200, 640, 80, 80))  # 下一回合按钮
            mainScreen.blit(musicPausePic, (1205, 0))  # 音乐暂停按钮
            mainScreen.blit(musicSkipPic, (1130, 0))  # 音乐跳过按钮

            for i in range(10):
                for j in range(10):
                    mapBlockDis = pygame.Rect(20 + i * 70, 20 + j * 70, 64, 64)
                    pygame.draw.rect(mainScreen, gameMap[i][j].mapColor, mapBlockDis)
            renderNow = pygame.Rect(34 + nowUnit.placeX * 70, 34 + nowUnit.placeY * 70, 36, 36)
            pygame.draw.rect(mainScreen, (255, 0, 255), renderNow)
            building_group.draw(mainScreen)
            unit_group.draw(mainScreen)
            pygame.display.update()
            gameClock.tick(60)

pygame.quit()  # 退出程序
