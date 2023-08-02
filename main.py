import pygame
from fighter import Fighter, Knight
from HUD.healthbar import HealthBar
from HUD.button import Button
from HUD.damagetext import DamageText

pygame.init()

clock = pygame.time.Clock()
fps = 60

###game window infos
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#define game rules and variable
current_fighter = 1
bandit_count = 1
total_fighter = bandit_count + 1 #amount of bandit + the player
action_cooldown = 0
action_wait_time = 40
potion_effect = 15

#define convenient graphical values
character_shift = 200/2**bandit_count - (bandit_count//5)*70
ennemy_spread = 90/2**bandit_count
start_bottom_panel = screen_height - bottom_panel

#define input logic values
attack = False
potion = False
clicked = False

#define game logic value
game_over = 0

#define fonts
font = pygame.font.SysFont("Times New Roman", 22)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

#######load images
img_background = pygame.image.load("assets/img/Background/background.png").convert_alpha()
img_panel = pygame.image.load("assets/img/Icons/panel.png").convert_alpha()
#sword icon
img_sword = pygame.image.load("assets/img/Icons/sword.png").convert_alpha()
#potion icon
img_potion = pygame.image.load("assets/img/Icons/potion.png").convert_alpha()
img_poison = pygame.image.load("assets/img/Icons/poison.png").convert_alpha()
#restart icon
img_restart = pygame.image.load("assets/img/Icons/restart.png").convert_alpha()
#win and defeat img
img_victory = pygame.image.load("assets/img/Icons/victory.png").convert_alpha()
img_defeat = pygame.image.load("assets/img/Icons/defeat.png").convert_alpha()


#to draw text mor easily
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


#drawing background
def draw_bg():
    screen.blit(img_background, (0, 0))


def draw_panel_knight():
    #draw panel rectangle
    screen.blit(img_panel, (0, start_bottom_panel))
    #show knight stats
    draw_text(f"{knight.display_name} HP: {knight.hp}", font, red,
               100, start_bottom_panel + 10)
    knight_health_bar.draw(screen)
    

def draw_panel_bandit(bandit):
    for count, i in enumerate(bandit_list):
        if i==bandit:
            #show name and health
            draw_text(f"{i.display_name} HP: {i.hp}", font, red,
                550, start_bottom_panel + 10)
            draw_text(f"{i.potions} Potion", font, red,
                550, start_bottom_panel + 55)
    for element in bandits_healthbars:
        if element.owner==bandit:
            element.draw(screen)


damage_text_group = pygame.sprite.Group()


bandit_list = []
character_list = []
bandits_healthbars = [] 

knight = Knight(190 + (character_shift), 260, "Knight", "Knight", 30, 10, 3, 3)
knight_health_bar = HealthBar(100, start_bottom_panel + 40, knight)
bandits_healthbars.append(knight_health_bar)
character_list.append(knight)

for i in range(bandit_count):
    bandit_list.append(Fighter(350 + i*(80+ennemy_spread) + (character_shift),
                                270, "Bandit", "Bandit "+str(i+1), 200, 6, 1))
    character_list.append(bandit_list[i])
    bandits_healthbars.append(HealthBar(550, start_bottom_panel + 40, bandit_list[i]))

#create potion button
potion_button = Button(screen, 100, start_bottom_panel+70, img_potion, 64, 64)
poison_button = Button(screen, 164, start_bottom_panel+70, img_poison, 64, 64)
#create restart button
restart_button = Button(screen, 330, 120, img_restart, 120, 30)

#prepare some temporary value for each loop
attack = False
potion = False
poison = False
target = None


run = True
while run:

    #set the fps to 60
    clock.tick(fps)
    #draw background + panel
    draw_bg()

    #draw_panel()
    draw_panel_knight()
    draw_panel_bandit(target)
    

    


    for character in character_list:
        character.update()
        character.draw(screen)

    #draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player action
    #reset action variable
    attack = False
    potion = False
    poison = False
    target = None
    pos = pygame.mouse.get_pos()
    pygame.mouse.set_visible(True)  
    
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword at cursor pos
            screen.blit(img_sword, pos)
            target = bandit_list[count]
            if clicked and bandit.alive:
                attack = True
               
            
            

    if potion_button.draw():
        potion = True
    if poison_button.draw():
        poison = True
    #show the amount of potions left
    draw_text(str(knight.potions), font, red, 150, start_bottom_panel + 70)
    #show the amount of poison potions left
    draw_text(str(knight.poison_potions), font, red, 214, start_bottom_panel + 70)

    if game_over==0:
        #player action
        if knight.alive :
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack and target!=None:
                        if knight.poison_active:
                            knight.poison_attack(target, damage_text_group)  #poison attack
                        else:
                            knight.attack(target, damage_text_group)         #normal attack
                        current_fighter+=1
                        action_cooldown = 0
                    elif potion:
                        if knight.potions > 0 and knight.max_hp!=knight.hp:
                            
                            knight.heal(potion_effect, damage_text_group)

                            current_fighter+=1
                            action_cooldown = 0
                    elif poison:
                        if not knight.poison_active:
                            knight.poison_potions -= 1
                            knight.poison_active = True

        else:
            game_over = -1

        #bandit action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive:    
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        print('poke')
                        bandit.status_effect_start_turn(damage_text_group)
                        if bandit.alive:  #we must check if the target is still alive after the damage of the effects
                            #check if needs to heal
                            if (bandit.hp/bandit.max_hp) < 0.5 and bandit.potions > 0 :
                                #check if potion would overheal
                                bandit.heal(potion_effect, damage_text_group)
                                current_fighter+=1
                                action_cooldown = 0
                            else:
                                #attack
                                bandit.attack(knight, damage_text_group)
                                current_fighter+=1                                
                                action_cooldown = 0
                else:
                    current_fighter += 1


        #reset the turn after all played
        if current_fighter > total_fighter:
            current_fighter=1
    
    
    
    #check if all ennemies are dead
    alive_bandits = 0
    for bandit in bandit_list:
        if bandit.alive:
            alive_bandits+=1
    if alive_bandits==0:
        game_over=1

    if game_over!=0:
        if game_over==1:
            screen.blit(img_victory, (250, 50))
        elif game_over==-1:
            screen.blit(img_defeat, (290, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter=1
            action_cooldown=0
            game_over=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False
        if event.type==pygame.KEYDOWN and event.key==pygame.K_m:
            knight.strength=40
        if event.type==pygame.KEYDOWN and event.key==pygame.K_n:
            knight.hp=30


    pygame.display.update()
pygame.quit()