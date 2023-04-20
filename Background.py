import pygame, os
from game_sys import Game

class Background: # 상속 용 클래스
    li = []
    def __init__(self):
        self.li.append(self)
    
    def move(self, FPS):
        self.x -=  self.speed * (FPS/1000)

        if self.x <= -self.img_width:
            self.x += self.img_width * len(self.li)

    def update(self, win, FPS):
        self.move(FPS)
        win.blit(self.image, (self.x,self.y))

class Floor(Background):
    li = []
    def __init__(self, image, position):
        self.image = image
        self.img_width, self.img_height = self.image.get_size()

        self.x, self.y = position

        # 게임 변수
        self.speed = 300
        super().__init__()
        # Floor.li.append(self)

class Cloud(Background):
    li = []
    def __init__(self, image, position):
        self.image = image
        self.img_width, self.img_height = self.image.get_size()

        self.x, self.y = position

        # 게임 변수
        self.speed = 300
        super().__init__()
    
    def move(self, FPS):
        self.x -=  self.speed * (FPS/1000)

        if self.x <= -self.img_width:
            self.x += Game.game_size[0] + self.img_width

if __name__ == "__main__":
    os.startfile("C:/code/가디언테일즈/T-tatGee Runner/main.py")