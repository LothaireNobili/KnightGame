import pygame
import random
from HUD.damagetext import DamageText

red = (255, 0, 0)
green = (0, 255, 0)

class Fighter():

    def __init__(self, x, y, name, max_hp, strength, potions):

        #fighting stats
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions 
        self.potions = potions
        self.alive = True

        #animation values
        self.scale = 3
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0:idle; 1:attack; 2:hurt; 3:death
        self.update_time = pygame.time.get_ticks()

        #load idle/attack images
        action_images = [["Idle",8], ["Attack",8],["Hurt",3],["Death",10]] #[element],[number of sprite] (must be standardiezed for all ennemies rn)
        for action in action_images:
            temp_list = []
            for i in range(action[1]):
                img = pygame.image.load(f"assets/img/{self.name}/{action[0]}/{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has past since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #if the animation has run out, we start over again
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        

    def attack(self, target, damage_text_group):
        if target.alive:  #to prevent IA attack dead, might softlock the game later
            #deal damage to ennemy
            mod = random.randint(-5, 5)
            damage = self.strength + mod
            target.hp -= damage
            #run ennemy hurt animation
            target.hurt()
            #check if target died
            if target.hp <= 0:
                target.hp = 0
                target.alive = False
                target.death()

            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
            damage_text_group.add(damage_text)

            #set animation to attack
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def heal(self, amount, damage_text_group):
        #check if potion would overheal
        if self.max_hp - self.hp > amount:
            heal_amount = amount
        else:
            heal_amount = self.max_hp-self.hp

        heal_text = DamageText(self.rect.centerx, self.rect.y, str(amount), green)
        damage_text_group.add(heal_text)  

        self.hp += heal_amount
        self.potions-=1

    def reset(self):
        self.alive = True
        self.hp=self.max_hp
        self.potions=self.start_potions

        self.frame_index=0
        self.action=0
        self.update_time = pygame.time.get_ticks()
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

