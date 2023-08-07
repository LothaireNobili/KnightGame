import pygame
import random
from HUD.damagetext import DamageText

red = (255, 0, 0)
orange = (255, 75, 0)
green = (0, 255, 0)

class Fighter():

    def __init__(self, x, y, name, display_name, max_hp, strength, heal_potions):

        #fighting stats
        self.name = name
        self.display_name = display_name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_heal_potions = heal_potions 
        self.heal_potions = heal_potions
        self.alive = True

        #status effect stuff
        self.status_effect = []  #exemple : [["poison",3],["bleeding",2]]  => poisonned for 3 turns, bleeding for 2 turns
        self.turn_state = [0, 0]

        #animation values
        self.action_cooldown = 0
        self.scale = 3
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0:idle; 1:attack; 2:hurt; 3:death
        self.update_time = pygame.time.get_ticks()
        self.current_status_effect = 0 #to make sure the status effect ticks one by one

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

            if self.check_status_effect("poison"): #weakening the attack if poisoned
                damage = damage//2

            target.take_damage(damage, damage_text_group)

            #set animation to attack
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def hurt(self):
        self.action_cooldown = 0
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def take_damage(self, amount, damage_text_group, damage_type = "normal"):
        self.hp -= amount
        #run ennemy hurt animation
        self.hurt()
        #check if target died
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.death()

        damage_color = red
        if damage_type == "normal":
            damage_color = red
        elif damage_type == "poison":
            damage_color = orange


        damage_text = DamageText(self.rect.centerx, self.rect.y, str(amount), damage_color)
        damage_text_group.add(damage_text)
    
    def heal(self, amount, damage_text_group):
        
        heal_amount = amount
        if self.check_status_effect("poison"):
            heal_amount = heal_amount//2


        #check if heal_potion would overheal
        if self.max_hp - self.hp > heal_amount:
            heal_amount = heal_amount
        else:
            heal_amount = self.max_hp-self.hp

        heal_text = DamageText(self.rect.centerx, self.rect.y, str(heal_amount), green)
        damage_text_group.add(heal_text)  

        self.hp += heal_amount
        self.heal_potions-=1

    def status_effect_start_turn(self, damage_text_group):

        if self.turn_state[1] == 0 :
            if self.check_status_effect("poison"):
                poison = self.status_effect_tick("poison")
                poison_damage = 3+poison
                self.take_damage(poison_damage, damage_text_group, damage_type = "poison")
            self.turn_state[1]=1

        elif self.turn_state[1] == 1:
            if self.check_status_effect("bleed"):
                bleed = self.status_effect_tick("bleed")
                bleed_damage = 5
                self.take_damage(bleed_damage, damage_text_group, damage_type = "poison")
            self.turn_state[1]=2 #2 doesn't exist yet but it allows to break the loop
            
        else:
            self.turn_state[1]=0 #close the loop
            self.turn_state[0]=1



    def check_status_effect(self, effect_name):
        for status_effect in self.status_effect:
            if status_effect[0] == effect_name:
                return status_effect[1]
        return 0 

    def status_effect_tick(self, effect_name):
        for status_effect in self.status_effect:
            if status_effect[0] == effect_name:
                status_effect[1] -= 1  #remove a stack
                return status_effect[1]+1 #we return how much there was before removing to apply effect properly
   
   
    def apply_status_effect(self, effect_name, duration):
        # Check if the status effect is already in the list
            for status_effect in self.status_effect:
                if status_effect[0] == effect_name:
                    # If the effect is found, update its stack
                    status_effect[1] += duration
                    return

            # If the effect is not found, add it as a new entry in the list
            self.status_effect.append([effect_name, duration])


    def reset(self):
        self.alive = True
        self.hp=self.max_hp
        self.heal_potions=self.start_heal_potions

        self.status_effect = []

        self.frame_index=0
        self.action=0
        self.update_time = pygame.time.get_ticks()
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)





class Knight(Fighter):

    def __init__(self, x, y, name, display_name, max_hp, strength, heal_potions, poison_potions):
        super().__init__(x, y, name, display_name, max_hp, strength, heal_potions)
        self.start_poison_potions = poison_potions
        self.poison_potions = poison_potions
        self.poison_active = False
    
    def poison_attack(self, target, damage_text_group):
        if target.alive:  #to prevent IA attack dead, might softlock the game later
            #deal damage to ennemy
            mod = random.randint(-3, 8)
            damage = self.strength + mod
            target.hp -= damage
            target.apply_status_effect("poison", 3) 
            #run ennemy hurt animation
            target.hurt()
            self.poison_active=False
            #check if target died
            if target.hp <= 0:
                target.hp = 0
                target.alive = False
                target.death()

            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), orange)
            damage_text_group.add(damage_text)

            #set animation to attack
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def reset(self):
        super().reset()
        self.poison_potions=self.start_poison_potions