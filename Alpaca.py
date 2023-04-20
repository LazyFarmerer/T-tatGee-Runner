import pygame, os, random
from game_sys import Game

class Alpaca:
    li = []
    def __init__(self, image):
        self.image = image
        self.image = pygame.transform.scale(self.image, Game.alpaca_size)
        self.img_width, self.img_height = Game.alpaca_size

        self.rect = self.image.get_rect()
        self.reset()

        # 게임 변수
        self.is_active = False
        self.speed = 200
        self.score = 0 # Mayreel_Respawn 클래스에서 점수 부여

        Alpaca.li.append(self)
    
    def reset(self):
        self.x, self.y = Game.game_size[0], Game.game_size[1] - self.img_height

        self.rect.left = self.x
        self.rect.top = self.y

        # 게임 변수
        self.speed = 200 + (Game.score*30)
        self.score = 0
        self.first_update_No_FPS = True

    def active(self, is_bool):
        if is_bool is True:
            self.is_active = True
            self.reset()
        elif is_bool is False:
            self.is_active = False
            self.x, self.y = Game.game_size[0], Game.game_size[1] - self.img_height

            self.rect.left = self.x
            self.rect.top = self.y
    
    def add_score(self, num):
        self.score += num

    def move(self, FPS):
        self.x -= self.speed * (FPS/1000)
        self.rect.left = self.x
        self.rect.top = self.y

        # 메이릴이 끝에 도착시 비활성화 및 점수 반영
        if self.x <= 0:
            Game.score += self.score
            self.active(False)

    def update(self, win, FPS):
        # 액티브 변수 비활성화 시 작동 안함
        if self.is_active is False:
            return

        self.move(FPS)
        win.blit(self.image, (self.x,self.y))

class Mayreel_Respawn:
    # 이 클래스 역할 :
    # 시간이 지날 때 마다 메이릴 활성화
    def __init__(self):
        self.timer = 0
        self.score_level = 0

    def reset(self):
        ran = random.random()
        self.timer = 0
        self.score_level = 5 + (ran*3) - (Game.score/3)
        self.score_level = max(ran*2, self.score_level)

    def active(self, may_type):
        # A - 메이릴 지상, B - 메이릴 공중
        # C - 메이릴 둘
        for may in Alpaca.li:
            # 비활성화 되어있는 메이릴이라면
            if may.is_active is False:
                self.reset()
                may.active(True)
                may.add_score(1)
                if may_type == "A":
                    break
                elif may_type == "B":
                    may.y = Game.game_size[1] - (may.img_height * 2.5)
                    break
                else: # 한마리 더 활성화
                    may_type = random.choice(["C_1", "C_2"])
                    for may_2nd in Alpaca.li:
                        if may_2nd.is_active is False:
                            may_2nd.active(True)
                            if may_type == "C_1":
                                may_2nd.x = Game.game_size[0] + may_2nd.img_width
                                break
                            elif may_type == "C_2":
                                may_2nd.y = Game.game_size[1] - (may_2nd.img_height * 2)
                                break
                    break


    def update(self, FPS):
        self.timer += FPS / 1000
        # print(f"\r점수 : {Game.score} 다음 메이릴 {self.score_level - self.timer:.2f}", end="")

        if self.timer >= self.score_level:
            # A - 메이릴 지상, B - 메이릴 공중
            # C - 메이릴 둘
            may_type = random.choice(["A","B","C"])
            self.active(may_type)

if __name__ == "__main__":
    os.startfile("C:/code/가디언테일즈/T-tatGee Runner/main.py")