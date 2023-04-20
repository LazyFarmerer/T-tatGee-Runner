import pygame, os
from game_sys import Game


class TtatGee:
    def __init__(self, images):
        # 이미지 처리
        self.image = images
        self.img_len = round(self.image.get_width() / self.image.get_height()) # 8
        self.img_num = 0 # 이미지 번호 0 ~ 8
        self.img_timer = 0 # 이미지 변경을 위한 시간 받음
        self.image = pygame.transform.scale(self.image, (Game.ttatGee_size[0] * self.img_len, Game.ttatGee_size[1]))
        self.img_width, self.img_height = Game.ttatGee_size

        self.x, self.y = Game.game_size[0]*0.1, Game.game_size[1] - self.img_height

        self.rect = self.image.get_rect()
        self.rect.width = self.img_width
        self.rect.left = self.x
        self.rect.top = self.y

        # 게임 변수
        self.is_jumping = False
        self.jump_power = 450
        self.gravity_vector = 0
    
    def jump(self, FPS, active=False, music=None):
        # 점프키 입력 받고 and 점프중이 아니라면
        if active is True and self.is_jumping is False:
            music.mario_jump_play()
            self.is_jumping = True
            self.gravity_vector -= self.jump_power * (FPS/1000)
            return

        self.gravity_vector += Game.gravity * (FPS/1000)
        self.y += self.gravity_vector

        if self.y >= Game.game_size[1] - self.img_height:
            self.y = Game.game_size[1] - self.img_height
            self.is_jumping = False
            self.gravity_vector = 0

        self.rect.left = self.x
        self.rect.top = self.y

    def img_show(self, FPS):
        # 이미지 선택
        self.img_timer += FPS / 100
        self.img_num = round(self.img_timer) % (self.img_len - 1) if self.is_jumping is False else (self.img_len - 1)

        # 이미지 자르고 마스크(충돌감지) 새로고침
        self.img_subsurf = self.image.subsurface(self.img_num * Game.ttatGee_size[0],0, Game.ttatGee_size[0], Game.ttatGee_size[1])
        self.mask = pygame.mask.from_surface(self.img_subsurf)

    def update(self, win, FPS):
        self.jump(FPS)
        self.img_show(FPS)

        win.blit(self.img_subsurf, (self.x,self.y))

if __name__ == "__main__":
    os.startfile("C:/code/가디언테일즈/T-tatGee Runner/main.py")