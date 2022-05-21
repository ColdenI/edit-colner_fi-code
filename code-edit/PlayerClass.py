import pygame, keyboard, Button_name, math

ANIMA_PLAYER = {'L1':'gamedata/texture/player/l_1.png',
                'L2':'gamedata/texture/player/l_2.png',
                'L3':'gamedata/texture/player/l_3.png',
                'L4':'gamedata/texture/player/l_2.png',
                'R1':'gamedata/texture/player/r_1.png',
                'R2':'gamedata/texture/player/r_2.png',
                'R3':'gamedata/texture/player/r_3.png',
                'R4':'gamedata/texture/player/r_2.png',
                'F':'gamedata/texture/player/f.png',
                'D':'gamedata/texture/player/d.png'
                }

class Player(pygame.sprite.Sprite):
    speed = None
    live = None
    money = None
    speed_max = None
    grav = 0
    max_jamp = None
    im_stat = 'F'
    is_jamp = False
    GND = None
    stamina = 100
    screen_res = (None,None)

    def __init__(self, x, y, filename, speed, speed_max):
        self.speed = speed
        self.speed_max = speed_max
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def anim(self,filename):
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(center=self.rect.center)

    def jamp(self):
        if  self.is_jamp and self.rect.bottom <= self.GND:
            self.rect.bottom -= self.grav
            if self.grav <= self.max_jamp:
                self.grav-=1
            if self.grav <= 0:
                self.is_jamp = False

    def move(self):
        if keyboard.is_pressed(Button_name.P_boost):
            if keyboard.is_pressed(Button_name.P_right) and self.stamina > 10:
                self.rect.x += self.speed_max
            if keyboard.is_pressed(Button_name.P_left) and self.stamina > 10:
                self.rect.x -= self.speed_max
        else:
            if keyboard.is_pressed(Button_name.P_right) and self.stamina > 0:
                self.rect.x += self.speed
            if keyboard.is_pressed(Button_name.P_left) and self.stamina > 0:
                self.rect.x -= self.speed

        if (keyboard.is_pressed(Button_name.P_up) or keyboard.is_pressed(Button_name.P_up_alt))  and not self.is_jamp and self.rect.bottom == self.GND:
            self.is_jamp=True
            self.grav = self.max_jamp

        self.jamp()

        if self.rect.bottom > self.GND:
            self.rect.bottom = self.GND

        if self.rect.bottom < self.GND and not self.is_jamp:
            self.rect.y += self.grav
            if self.grav < self.max_jamp:
                self.grav+=1

    def update(self, sc):
        sc.blit(self.image, self.rect)
        self.move()

    def update_(self, sc):
        sc.blit(self.image, self.rect)


    def telep(self, boo):
        if boo:
            if self.rect.left > self.screen_res[0]:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = self.screen_res[0]
        else:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.screen_res[0]:
                self.rect.right = self.screen_res[0]
