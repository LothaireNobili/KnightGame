import pygame
from fighter import Fighter
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


#define game variable
current_fighter = 1
bandit_count = 3 #the hard limit is 3
total_fighter = bandit_count + 1 #amount of bandit + the player
action_cooldown = 0
action_wait_time = 40

attack = False
potion = False
potion_effect = 15
clicked = False

game_over = 0

#define fonts
font = pygame.font.SysFont("Times New Roman", 22)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

###load images
img_background = pygame.image.load("assets/img/Background/background.png").convert_alpha()
img_panel = pygame.image.load("assets/img/Icons/panel.png").convert_alpha()
#sword icon
img_sword = pygame.image.load("assets/img/Icons/sword.png").convert_alpha()
#potion icon
img_potion = pygame.image.load("assets/img/Icons/potion.png").convert_alpha()
#restart icon
img_restart = pygame.image.load("assets/img/Icons/restart.png").convert_alpha()
#win and defeat img
img_victory = pygame.image.load("assets/img/Icons/victory.png").convert_alpha()
img_defeat = pygame.image.load("assets/img/Icons/defeat.png").convert_alpha()

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


#drawing background
def draw_bg():
    screen.blit(img_background, (0, 0))

#drawing panel
def draw_panel():
    #draw panel rectangle
    screen.blit(img_panel, (0, screen_height - bottom_panel))
    #show knight stats
    draw_text(f"{knight.name} HP: {knight.hp}", font, red,
               100, screen_height - bottom_panel + 15)
    
    for count, i in enumerate(bandit_list):
        #show name and health
        draw_text(f"{i.name} HP: {i.hp} / ({i.potions})", font, red,
               550, (screen_height - bottom_panel + 15) + count*40)
    

damage_text_group = pygame.sprite.Group()


bandit_list = []
character_list = []
hud_elements = [] #basically just the healthbars for now

knight = Fighter(190, 260, "Knight", 30, 10, 3)
knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight)
character_list.append(knight)

if bandit_count>=1:
    bandit1 = Fighter(400, 270, "Bandit", 20, 6, 1)
    bandit_list.append(bandit1)
    character_list.append(bandit1)
    bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1)
    hud_elements.append(bandit1_health_bar)
if bandit_count>=2:
    bandit2 = Fighter(550, 270, "Bandit", 20, 6, 1)
    bandit_list.append(bandit2)
    character_list.append(bandit2)
    bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 80, bandit2)
    hud_elements.append(bandit2_health_bar)
if bandit_count>=3:
    bandit3 = Fighter(700, 270, "Bandit", 20, 6, 1)
    bandit_list.append(bandit3)
    character_list.append(bandit3)
    bandit3_health_bar = HealthBar(550, screen_height - bottom_panel + 120, bandit3)
    hud_elements.append(bandit3_health_bar)

#create potion button
potion_button = Button(screen, 100, screen_height-bottom_panel+70, img_potion, 64, 64)
#create potion button
restart_button = Button(screen, 330, 120, img_restart, 120, 30)


run = True
while run:

    #set the fps to 60
    clock.tick(fps)
    #draw background + panel
    draw_bg()
    draw_panel()
    for element in hud_elements:
        element.draw(screen)


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
    target = None
    pos = pygame.mouse.get_pos()
    pygame.mouse.set_visible(True)  
    
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse
            pygame.mouse.set_visible(False)
            #show sword at cursor pos
            screen.blit(img_sword, pos)
            if clicked and bandit.alive:
                attack = True
                target = bandit_list[count]
            

    if potion_button.draw():
        potion = True
    #show the amount of potions left
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)

    if game_over==0:
        #player action
        if knight.alive :
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action
                    #attack
                    if attack and target!=None:
                        knight.attack(target, damage_text_group)  #
                        current_fighter+=1
                        action_cooldown = 0
                    elif potion:
                        if knight.potions > 0 and knight.max_hp!=knight.hp:
                            
                            knight.heal(potion_effect, damage_text_group)

                            current_fighter+=1
                            action_cooldown = 0
        else:
            game_over = -1

        #bandit action
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
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
            knight.hp=1


    pygame.display.update()
pygame.quit()