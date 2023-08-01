import pygame

red = (255, 0, 0)
green = (0, 255, 0)

class HealthBar():

    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.owner = owner
        #self.hp = hp
        #self.max_hp = max_hp
    
    def draw(self, screen):
        


        #update with new health
        #calculate the ration
        ratio = self.owner.hp / self.owner.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 13)) 
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 13)) 