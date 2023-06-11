import pygame
pygame.init() # 初始化pygame
clock = pygame.time.Clock()
clock.tick(60)
screen = pygame.display.set_mode((1280,720)) # Pygame窗口
pygame.display.set_caption("文明6_低配版") # 标题
keep_going = True
Red = (255,0,0)  # 红色，使用RGB颜色
Black = (0,0,0)  # 黑色
Green = (0,255,0)  # 绿色
Blue = (0,0,255)  # 蓝色
White = (255,255,255)  # 白色
radius = 70 # 半径
pic = pygame.image.load("./image/logo.jpg")  # 加载图片

# 创建精灵
class Sprite1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(White)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# 加载音乐
pygame.mixer.music.load("./music/meun.mp3")

# 播放音乐
pygame.mixer.music.play(-1)

# 添加精灵到组中
group = pygame.sprite.Group()
sprite = Sprite1()
group.add(sprite)

collision_list = pygame.sprite.spritecollide(sprite, group, False)
if collision_list:
    print("碰撞了！")


# 游戏循环
while keep_going:
    for event in pygame.event.get():  # 遍历事件
        if event.type == pygame.QUIT:  # 退出事件
            keep_going = False
    if event.type == pygame.MOUSEBUTTONDOWN:
        print("鼠标点击")
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            sprite.rect.x -= 1
        elif event.key == pygame.K_RIGHT:
            sprite.rect.x += 1
        elif event.key == pygame.K_UP:
            sprite.rect.y -= 1
        elif event.key == pygame.K_DOWN:
            sprite.rect.y += 1
        elif event.key == pygame.K_ESCAPE:
            keep_going = False
    screen.blit(pic,(0,0))
    #pygame.draw.circle(screen, Red, player_pos, 40)
    group.draw(screen)
    #pygame.draw.circle(screen,White,(200,300),radius)
    pygame.display.flip()# 更新全部显示
    #pygame.display.update()  # 刷新屏幕



# 退出程序
pygame.quit()