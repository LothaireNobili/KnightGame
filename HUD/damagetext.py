import pygame

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        font = pygame.font.SysFont("Times New Roman", 22)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        #delete text after a bit of time
        self.counter += 1
        if self.counter > 30:
            self.kill()

    