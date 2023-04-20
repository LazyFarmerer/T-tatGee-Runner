import pygame, random, os
from save import Save
from TtatGee import TtatGee
from Alpaca import Alpaca, Mayreel_Respawn
from game_sys import Game
from Background import Floor, Cloud

class Image:
    path = os.path.dirname(__file__)
    # 배경, 캐릭터 이미지
    floor = pygame.image.load(os.path.join(path, "resoure", "images", "floor.png"))
    cloud = pygame.image.load(os.path.join(path, "resoure", "images", "cloud.png"))
    nari = pygame.image.load(os.path.join(path, "resoure", "images", "fox_mouse_nari.png"))
    nari_s = pygame.image.load(os.path.join(path, "resoure", "images", "nari_side.png"))
    mayreel = pygame.image.load(os.path.join(path, "resoure", "images", "bari_mayreel.png"))
    mayreel = pygame.transform.flip(mayreel, True, False)

class Music:
    def __init__(self):
        pygame.mixer.init()
        self.path = os.path.dirname(__file__)
        self.__bgm = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "rana-tema-guardian-tales-bgm.mp3"))
        self.__bgm.set_volume(0.4)
        self.__this_why = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "this_why.mp3"))
        self.__this_why.set_volume(0.6)
        self.__mario_jump = pygame.mixer.Sound(os.path.join(self.path, "resoure", "music", "mario_jump.mp3"))
        self.__mario_jump.set_volume(0.2)
    def bgm_play(self):
        self.__bgm.play(-1)
    def bgm_stop(self):
        self.__bgm.stop()
    def this_why_play(self):
        self.__this_why.play(maxtime=4200)
    def this_why_stop(self):
        self.__this_why.stop()
    def mario_jump_play(self):
        self.__mario_jump.play()
    def mario_jump_stop(self):
        self.__mario_jump.stop()

def start_wait(win, clock):
    wait_run = True

    for idx, mayreel in enumerate(Alpaca.li):
        mayreel.active(True)
        mayreel.x = Game.game_size[0] / len(Alpaca.li) * (idx+1)

    while wait_run:
        FPS = clock.tick(60)
        # 창 끄거나 키 & 마우스 눌러 다시 시작
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.run = False
                Game.re_run = False
                wait_run = False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                wait_run = False

        win.fill((247,247,247))
        for f in Floor.li:
            f.update(win, FPS)
        for c in Cloud.li:
            c.update(win, FPS)
        for mayreel in Alpaca.li:
            if mayreel.is_active is False:
                mayreel.active(True)
            mayreel.update(win, FPS)

        pygame.display.update()
    
    for mayreel in Alpaca.li:
        mayreel.active(False)

def game_over(win, big_font, small_font, music):
    # 창 끄거나 스페이스바 눌러 다시 시작
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.run = False
            Game.re_run = False
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN or event.key == pygame.K_r:
                Game.run = True
                Game.re_run = False
                reset(music)

    black = (0,0,0)
    win.blit(big_font.render("게임 오버", True, black), (Game.game_size[0]*0.4, Game.game_size[1]*0.4))
    win.blit(small_font.render("다시 시작은 r 버튼 또는 마우스 클릭", True, black), (Game.game_size[0]*0.4, Game.game_size[1]*0.55))

def reset(music):
    Game.score = 0
    for may in Alpaca.li:
        may.active(False)

    music.this_why_stop()
    music.bgm_play()

def text_render(win, big_font, small_font, clock):
    black = (0,0,0)
    win.blit(small_font.render(f"fps:{clock.get_fps():.2f}", True, black), (Game.game_size[0]*0.92, Game.game_size[1]*0.9))

    win.blit(small_font.render(f"점수 : {Game.score}", True, black), (Game.game_size[0]*0.9, Game.game_size[1]*0.03))
    win.blit(small_font.render(f"최고점수 : {Game.high_score}", True, black), (Game.game_size[0]*0.8, Game.game_size[1]*0.03))

def key_event(save):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save.save(Game.high_score)
            Game.run = False
            Game.re_run = False
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEBUTTONDOWN or event.key == pygame.K_SPACE:
                Game.k_space = True

def game_event(player, music, FPS):
    # 점프 여부
    if Game.k_space is True:
            player.jump(FPS, active=True, music=music)
            Game.k_space = False
    # 최고점수 기록
    if Game.high_score < Game.score:
        Game.high_score = Game.score

def main():
    pygame.init()
    pygame.display.set_icon(Image.nari)
    win = pygame.display.set_mode(Game.game_size)
    pygame.display.set_caption("T-tatGee Runner")

    # 기본 변수
    clock = pygame.time.Clock()
    big_font = pygame.font.Font(os.path.join(Image.path, "resoure", "MaruBuriTTF", "MaruBuri-Regular.ttf"), 50)
    small_font = pygame.font.Font(os.path.join(Image.path, "resoure", "MaruBuriTTF", "MaruBuri-Regular.ttf"), 20)

    # 게임 변수
    save = Save()
    Game.high_score = save.road()
    music = Music()
    mayreel_respawn = Mayreel_Respawn()
    player = TtatGee(Image.nari_s.convert_alpha())
    for idx in range(10):
        mayreel = Alpaca(Image.mayreel.convert_alpha())
    floor_width = Image.floor.get_width()
    for idx in range(Game.game_size[0] // floor_width + 2):
        Floor(Image.floor.convert_alpha(), position=(floor_width * idx, Game.game_size[1]*0.9))
    for idx in range(3):
        Cloud(Image.cloud.convert_alpha(), position=(Game.game_size[0] / 3 * idx, Game.game_size[1]*0.5))

    # 불필요한 변수 삭제
    del floor_width, idx

    start_wait(win, clock) # 게임 시작 전 대기 장면

    music.bgm_play()
    while Game.run:
        FPS = clock.tick(60)

        key_event(save)
        game_event(player, music, FPS)

        # 메이릴 리스폰 관리
        mayreel_respawn.update(FPS)
        # background & 바닥
        win.fill((247,247,247))
        for f in Floor.li:
            f.update(win, FPS)
        for c in Cloud.li:
            c.update(win, FPS)
        # 메이릴 리스트 업데이트
        for mayreel in Alpaca.li:
            mayreel.update(win, FPS)
            # 플레이어 - 메이릴 충돌검사
            if pygame.sprite.collide_mask(player, mayreel):
                Game.run = False
                Game.re_run = True
        # 플레이어 업데이트
        player.update(win, FPS)
        # 텍스트 표시
        text_render(win, big_font, small_font, clock)

        pygame.display.update()

        # 게임 종료
        if Game.re_run is True:
            music.bgm_stop()
            music.this_why_play()
            save.save(Game.high_score)

            while Game.re_run:
                FPS = clock.tick(60)
                game_over(win, big_font, small_font, music)
                pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
