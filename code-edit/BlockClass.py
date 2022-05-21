import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, item_type = 'none', cloud_speep_ = 1, uron = 0, pow = 2, is_collected = False, gnd = 900):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect(x=x, y=y)
        self.item = item_type
        self.cloud_speed = cloud_speep_
        self.uron = uron
        self.pow_i = pow
        self.GND = gnd
        self.grav = 0
        self.max_jamp = 15
        self.is_collected = is_collected
    def updata(self, sc):
        sc.blit(self.image, self.rect)

    def anim(self,filename):
        self.image = pygame.image.load(filename).convert_alpha()

    def cloud_update(self, screen_max_X):
        self.rect.x += self.cloud_speed
        if self.rect.left > screen_max_X:
            self.rect.right = 5

    def move(self):
        if self.rect.bottom > self.GND:
            self.rect.bottom = self.GND

        if self.rect.bottom < self.GND:
            self.rect.y += self.grav
            if self.grav < self.max_jamp:
                self.grav+=1