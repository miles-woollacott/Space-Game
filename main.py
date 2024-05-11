import pygame
from pygame.locals import *
from pandas import read_csv

from heroes import *
from clickers import *
from enemies import *
from projectile import *
from functions import *
from path import Path
from user import User
from textbox import textBox

import random

# Initialize pygame
pygame.init()

# Window Title
pygame.display.set_caption('Tower Defense')
 
# Define the dimensions of screen object
SCREEN_DIM = (1200, 800)
screen = pygame.display.set_mode(SCREEN_DIM)
 
# Instantiate all objects
hlst = []
elst = []
gicon = GunnerClicker(xy=[50, 752])
hoicon = HowitzerClicker(xy=[100, 752])
ticon = TrashClicker(xy=[350, 752])
sicon = SaboteurClicker(xy=[150, 752])
projectiles = []
paths = [Path([[0, 400], [200, 400], [200, 100], [500, 100], [500, 600], [200, 600], [200, 700], [1000, 700]]),
         Path([[0, 400], [200, 400], [200, 100], [500, 100], [500, 600], [200, 600], [200, 700], [1000, 700]]),
         Path([[0, 300], [1000, 700]])]
level = paths[1]
difficulty_adj = {"Easy": 0.8, "Medium": 1, "Hard": 1.2}

ghost_enemies = {
    "Speeder": Speeder([0,0]),
    "Spawner": Spawner([0,0]),
    "Accelerator": Accelerator([0,0]),
    "Tanker": Tanker([0,0]),
    "Dreadnought": Dreadnought([0,0]),
    "Regenerator": Regenerator([0,0]),
    "Destroyer": Destroyer([0,0]),
    "Repairer": Repairer([0,0])
}

# Fonts
font = pygame.font.Font('freesansbold.ttf', 32)
sfont = pygame.font.Font('freesansbold.ttf', 24)
ssfont = pygame.font.Font('freesansbold.ttf', 16)
green = (0, 255, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 128)
lightblue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
purple = (232, 0, 255)
offwhite = (220, 220, 255)

# Menu buttons
background = textBox(100, 100, 1000, 600)
difficultybuttons = [textBox(250, 300, 150, 100, "Easy", green),
                     textBox(500, 300, 150, 100, "Medium", yellow),
                     textBox(750, 300, 150, 100, "Hard", red)]
pathbuttons = [textBox(270, 420, 50, 50, "1", lightblue),
                     textBox(520, 420, 50, 50, "2", lightblue),
                     textBox(770, 420, 50, 50, "3", lightblue)]
infobutton = textBox(400, 500, 300, 100, "Towers and Enemies", purple)
returnbutton = textBox(500, 600, 120, 80, "Return", purple)

# Sample heroes and enemies (for info screen)



# Toggle mouse movement
cooldown = 0
 
# Variable to keep our game loop running
gameOn = True
inLevel = False
inMenu = True
inInfo = False
inPause = False
sandbox = False
canPlace = True

FPS = 30
fpsClock = pygame.time.Clock()
 
# Our game loop
while gameOn:

    ################
    #### Update ####
    ################

    if cooldown>0:
            cooldown = (cooldown + 1) % 20

    keys = pygame.key.get_pressed()

    if inMenu:
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameOn = False

            if event.type == MOUSEBUTTONDOWN and cooldown==0:
                cooldown += 1
                if infobutton.isClicked():
                    inInfo = True
                    inMenu = False
                else:
                    for i in difficultybuttons:
                        if i.isClicked(): # Begin round
                            player = User(difficulty=i.text)
                            leveldf = read_csv("Rounds/" + player.difficulty + ".csv")
                            current_leveldf = get_all_ticks(leveldf[leveldf.Round==player.round])
                            maxrounds = max(leveldf.Round)
                            inLevel = True
                            inMenu = False
                            break
    
    elif inInfo:

        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameOn = False

            if event.type == MOUSEBUTTONDOWN and cooldown==0:
                cooldown += 1
                if returnbutton.isClicked():
                    inInfo = False
                    inMenu = True

            

    elif inLevel:


        ############ Mouse Controls ############
            

        # for loop through the event queue
        for event in pygame.event.get():

            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameOn = False

            if event.type==MOUSEBUTTONDOWN and cooldown==0:
                mouseloc = list(pygame.mouse.get_pos())
                if ticon.hitBox.isClicked(mouseloc):
                    ticon.clicked = not ticon.clicked
                
                cooldown += 1
                ind = []
                for h in hlst:
                    canPlace = True
                    if h.hitBox.isClicked(mouseloc):
                        if ticon.clicked:
                            ticon.clicked = False
                            ind.append(hlst.index(h))
                            player.money += 3*hlst[ind[-1]].sell_value/2 # 3x since the code buys and sells at the same time
                        elif len(hlst)==1 and mouseloc[1]<720 and player.money < h.cost: # Don't need to check for collisions
                            h.move = False
                            h.placed = True
                            player.money -= h.cost
                            continue
                        for h1 in hlst:
                            if h1 != h and h.hitBox.intersects(h1.hitBox):
                                canPlace = False
                        if h.move:
                            if player.money < h.cost: # Can't afford
                                if hlst.index(h) not in ind:
                                    ind.append(hlst.index(h))
                            if canPlace and mouseloc[1]<720:
                                h.move = False
                                h.placed = True
                                player.money -= h.cost
                        elif h.hitBox.isClicked(pygame.mouse.get_pos()): # Switch targeting
                            if h.target == "First":
                                h.target = "Strong"
                            else:
                                h.target = "First"
                ind = sorted(ind, reverse=True)
                for i in ind:
                    del hlst[i]
                                
                if gicon.hitBox.isClicked(mouseloc):
                    hlst.append(Gunner(mouseloc, move=True))
                elif hoicon.hitBox.isClicked(mouseloc):
                    hlst.append(Howitzer(mouseloc, move=True))
                elif sicon.hitBox.isClicked(mouseloc):
                    hlst.append(Saboteur(mouseloc, move=True))
                        
            # Check for KEYDOWN event
            if event.type == KEYDOWN:

                if event.key == K_BACKSPACE or event.key == K_ESCAPE:
                    gameOn = False
                
                elif event.key == K_p:
                    inPause = not inPause
                    inLevel = not inLevel

                # Spawn enemies (if in sandbox mode)

                if sandbox:
                    if event.key == K_q: # Spawn speeder
                        elst.append(Speeder(level.get_start()))
                    elif event.key == K_w: # Spawn spawner
                        elst.append(Spawner(level.get_start()))
                    elif event.key == K_e: # Spawn accelerator
                        elst.append(Accelerator(level.get_start()))
                    elif event.key == K_r: # Spawn tanker
                        elst.append(Tanker(level.get_start()))
                    elif event.key == K_t: # Spawn dreadnought
                        elst.append(Dreadnought(level.get_start()))
                    elif event.key == K_y: # Spawn regenerator
                        elst.append(Regenerator(level.get_start()))
                    elif event.key == K_u: # Spawn destroyer
                        elst.append(Destroyer(level.get_start()))
                    elif event.key == K_i: # Spawn repairer
                        elst.append(Repairer(level.get_start()))
                    elif event.key == K_c:
                        elst = []
                    elif event.key == K_m:
                        player.money += 1000
                    elif event.key == K_l:
                        player.lives += 100
                
                # Toggle sandbox
                if event.key == K_s:
                    sandbox = not sandbox
                

                ############ Upgrades ############
                    
                for h in hlst:
                    if h.hover:
                        # Super upgrade
                        if event.key == K_1 and sum(h.upgraded)==len(h.upgraded) and not h.super_upgrade and player.money >= h.super_upgrade_cost:
                            h.super_upgrade = True
                            player.money -= h.super_upgrade_cost
                            h.sell_value += h.super_upgrade_cost/2
                            if h.id == "Gunner":
                                h.cooldown_reset = 2
                        # Non-super upgrades
                        if event.key == K_1 and not h.upgraded[0] and player.money >= h.upgrades[0]:
                            h.upgraded[0] = True
                            player.money -= h.upgrades[0]
                            h.sell_value += h.upgrades[0]
                            if h.id == "Gunner":
                                h.range += 50
                            elif h.id == "Saboteur":
                                h.range += 20
                        elif event.key == K_2 and not h.upgraded[1] and player.money >= h.upgrades[1]:
                            h.upgraded[1] = True
                            player.money -= h.upgrades[1]
                            h.sell_value += h.upgrades[1]
                            if h.id == "Gunner":
                                h.cooldown_reset -= 10
                            elif h.id == "Howitzer":
                                h.cooldown_reset -= 32
                        elif event.key == K_3 and not h.upgraded[2] and player.money >= h.upgrades[2]:
                            h.upgraded[2] = True
                            player.money -= h.upgrades[2]
                            h.sell_value += h.upgrades[2]/2
                        elif event.key == K_4 and len(h.upgrades)>3 and not h.upgraded[3] and player.money >= h.upgrades[3]:
                            h.upgraded[3] = True
                            player.money -= h.upgrades[3]
                            h.sell_value += h.upgrades[3]/2
                        elif event.key == K_5 and len(h.upgrades)>4 and not h.upgraded[4] and player.money >= h.upgrades[4]:
                            h.upgraded[4] = True
                            player.money -= h.upgrades[4]
                            h.sell_value += h.upgrades[4]/2
                

                if event.key == K_SPACE and len(elst)==0 and not sandbox: # Start new level
                    player.round += 1
                    if player.round>maxrounds:
                        quit()
                    player.leveltick = 0
                    current_leveldf = get_all_ticks(leveldf[leveldf.Round==player.round])
                    
            # Check for QUIT event
            elif event.type == QUIT:
                gameOn = False
            
            # Check if mouse is hovering over hero, or cancel buying new hero
            ind = None
            for h in hlst:
                if h.hitBox.isClicked(pygame.mouse.get_pos()):
                    h.hover = True
                else:
                    h.hover = False
                if h.move and ticon.hitBox.isClicked(pygame.mouse.get_pos()):
                    ind = hlst.index(h)
            if ind is not None:
                del hlst[ind]

        if player.leveltick>=player.max_ticks and not sandbox: # Auto-start level
            player.round += 1
            if player.round>maxrounds:
                quit()
            player.leveltick = 0
            current_leveldf = get_all_ticks(leveldf[leveldf.Round==player.round])


        ############ Spawning ############
                
        
        # Spawn based on level
        if player.leveltick<player.max_ticks and not sandbox:
            player.leveltick += 1
            tickdf = current_leveldf[current_leveldf.Tick == player.leveltick]
            for i in tickdf.ID:
                if i == 1: # Spawn Speeder
                    elst.append(Speeder(level.get_start()))
                elif i == 2: # Spawn Spawner
                    elst.append(Spawner(level.get_start()))
                elif i == 3: # Spawn Accelerator
                    elst.append(Accelerator(level.get_start()))
                elif i == 4: # Spawn Tanker
                    elst.append(Tanker(level.get_start()))
                elif i == 5: # Spawn Dreadnought
                    elst.append(Dreadnought(level.get_start()))
                elif i == 6: # Spawn Regenerator
                    elst.append(Regenerator(level.get_start()))
                elif i == 7: # Spawn Destroyer
                    elst.append(Destroyer(level.get_start()))
                elif i == 8: # Spawn Repairer
                    elst.append(Repairer(level.get_start()))

        # Spawner spawn new speeders
        for sp in elst:
            if sp.id == "Spawner" and not sp.sabotaged:
                sp.countdown = (sp.countdown + 1) % sp.countdown_reset
                if sp.countdown<7 and sp.countdown % 2 == 0:
                    elst.append(Speeder([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
            elif sp.id == "Dreadnought" and not sp.sabotaged:
                sp.countdown = (sp.countdown + 1) % sp.countdown_reset
                if sp.countdown == 1:
                    elst.append(Accelerator([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
                elif sp.countdown == 6:
                    elst.append(Tanker([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
                elif sp.countdown == 11:
                    elst.append(Spawner([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
                elif sp.countdown == 16:
                    elst.append(Regenerator([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))


        ############ Moving ############


        # Move heroes
        for h in hlst:
            if h.move:
                mousepos = list(pygame.mouse.get_pos())
                h.center[0] = mousepos[0]
                h.center[1] = mousepos[1]
                canPlace = True
                for h1 in hlst:
                    if h1 != h and h.hitBox.intersects(h1.hitBox):
                        canPlace = False

        # Move enemies
        rm = []
        for e in elst:
            e.angle = level.angles[e.index]
            e.a_imp = pygame.transform.rotate(e.imp, e.angle)
            # Accelerate accelerator
            if e.id == "Accelerator" and not e.sabotaged:
                e.speed += 0.24
            # Add on health to regenerator
            elif e.id == "Regenerator" and not e.sabotaged:
                e.countdown = (e.countdown + 1) % e.countdown_reset
                if e.countdown == 0:
                    e.lives += 1
            # Repairer un-sabotages enemies it touches
            elif e.id == "Repairer":
                for e1 in elst:
                    if e1.hitBox.intersects(e.hitBox) and e1.position != e.position: # Doesn't fix itself
                        e1.speed = ghost_enemies[e1.id].speed
                        e1.lives = ghost_enemies[e1.id].lives
                        e1.sabotaged = False
                        e1.repaired = True
            # Move along new line if crosses plane
            if distance(e.center, level.points[e.index+1]) < e.speed:
                e.index += 1
                if e.index >= len(level.points)-1: # Reached end of track, delete enemy
                    ind = elst.index(e)
                    if ind not in rm:
                        rm.append(ind)
                else:
                    e.center = level.get_index(e.index)
            else:
                delta = [i*e.speed for i in anglemove(e.angle)]
                e.center[0] -= delta[0]
                e.center[1] -= delta[1]
            e.distance += e.speed
        for i in reversed(rm):
            if not sandbox:
                player.lives -= elst[i].lives
            del elst[i]
        if player.lives <= 0:
            quit()
        
        # Update rotation and fire bullet if nearby
        lst = [[],[]]
        for h in hlst:
            dist = 0
            strength = 0
            for e in elst:
                if distance(h.center, e.center)<h.range and not h.move and e.distance>dist:
                    if h.target == "First":
                        dist = e.distance
                    elif h.target == "Strong" and e.priority>strength:
                        dist = e.distance
                        strength = e.priority
            # Saboteur with super upgrade
            if h.id == "Saboteur" and h.super_upgrade:
                for e in elst:
                    if e.id != "Repairer" and not e.repaired and distance(h.center, e.center)<h.range and not h.move and e.id != "Saboteur":
                        e.speed *= 0.9
                        e.sabotaged = True
            for e in elst:
                if e.distance == dist:
                    if h.target == "First" or (h.target == "Strong" and e.priority == strength):
                        h.angle = angle(h.center, e.center)
                        h.a_imp = pygame.transform.rotate(h.imp, h.angle)
                        if h.cooldown == 0:
                            h.cooldown += 1
                            if h.id == "Gunner":
                                projectiles.append(Bullet(xy=[h.center[0], h.center[1]],
                                                    angle=h.angle+2*(1-2*int(h.angle<0))))
                                projectiles[-1].a_imp = pygame.transform.rotate(projectiles[-1].imp, projectiles[-1].angle)
                                if h.upgraded[0]:
                                    projectiles[-1].speed *= 1.6
                                if h.upgraded[3]:
                                    projectiles[-1].pierce += 2
                                if h.super_upgrade:
                                    projectiles[-1].pierce += 1
                            elif h.id == "Howitzer":
                                projectiles.append(Blast(xy=[h.center[0], h.center[1]],
                                                    angle=h.angle+2*(1-2*int(h.angle<0))))
                                if h.upgraded[2]:
                                    projectiles[-1].imp = pygame.transform.scale(projectiles[-1].imp, (projectiles[-1].width*2, projectiles[-1].height*2))
                                projectiles[-1].a_imp = pygame.transform.rotate(projectiles[-1].imp, projectiles[-1].angle)
                                if h.upgraded[0]:
                                    projectiles[-1].speed *= 1.6
                                if h.super_upgrade:
                                    projectiles[-1].pierce += 1000
                            elif h.id == "Saboteur" and e.id != "Repairer" and not e.repaired:
                                e.speed *= 0.99
                                if h.upgraded[1]:
                                    e.speed *= 0.99
                                # Upgrades
                                if e.id == "Accelerator" and h.upgraded[2]:
                                    e.sabotaged = True
                                elif e.id == "Regenerator" and h.upgraded[3]:
                                    e.sabotaged = True
                                elif e.id == "Spawner" and h.upgraded[4]:
                                    e.sabotaged = True
                # Destroyers destroy heroes if collision
                if e.id == "Destroyer" and e.hitBox.intersects(h.hitBox):
                    lst[0].append(elst.index(e))
                    lst[1].append(hlst.index(h))
            # Weapon cooldown
            if h.cooldown > 0:
                h.cooldown = (h.cooldown + 1) % h.cooldown_reset
        # Delete destroyed objects
        for i in reversed(lst[0]):
                del elst[i]
        for i in reversed(lst[1]):
                del hlst[i]


        
        ########### Projectiles ###########
        

        if len(elst)==0:
            projectiles = []

        # Bullet movement/life
        lst = []
        for p in projectiles:
            d = anglemove(p.angle)
            p.center[0] -= p.speed*d[0]
            p.center[1] -= p.speed*d[1]
            p.lifespan += 1
            if p.lifespan >= p.lifespan_reset or p.center[1]<0 or p.center[0]<0 or p.center[1]>720 or p.center[0]>SCREEN_DIM[0]:
                ind = projectiles.index(p)
                if ind not in lst:
                    lst.append(ind)
                continue
            # Collision with enemy
            rm = []
            for e in elst:
                if p.hitBox.intersects(e.hitBox):
                    p.pierce -= 1
                    e.lives -= 1
                    # Delete projectile (if necessary)
                    if p.pierce == 0:
                        ind = projectiles.index(p)
                        if ind not in lst:
                            lst.append(ind)
                    if e.lives == 0:
                        ind = elst.index(e)
                        if ind not in rm:
                            rm.append(ind)
            for i in reversed(rm):
                player.money += elst[i].reward
                del elst[i]
            for i in reversed(lst):
                del projectiles[i]


        text = font.render(str(sandbox), True, green, blue)
        textRect = text.get_rect()
        
        # Update position of sprites given the center changed
        level.set_position()
        for e in elst:
            e.update()
        for h in hlst:
            h.update()
        for p in projectiles:
            p.update()
    
    elif inPause:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    inPause = not inPause
                    inLevel = not inLevel

    
    ################
    ##### Draw #####
    ################
 
    # Update the display using flip
    screen.fill((0, 0, 0))

    if inMenu:
        pygame.draw.rect(screen, offwhite, background.rect)
        screen.blit(font.render("Tower Defense Game ig", False, blue), (400, 200))
        for i in difficultybuttons:
            pygame.draw.rect(screen, black, i.rect)
            screen.blit(i.get_text(), (i.left+20, i.top+30))
        for i in pathbuttons:
            pygame.draw.rect(screen, black, i.rect)
            screen.blit(i.get_text(), (i.left+10, i.top+10))
        pygame.draw.rect(screen, black, infobutton.rect)
        screen.blit(infobutton.get_text(), (infobutton.left+20, infobutton.top+30))

    elif inInfo:
        pygame.draw.rect(screen, offwhite, background.rect)
        screen.blit(font.render("Ships n Stuff", False, blue), (440, 120))
        pygame.draw.rect(screen, black, returnbutton.rect)
        screen.blit(returnbutton.get_text(), (returnbutton.left+20, returnbutton.top+30))

    elif inLevel or inPause:

        # Draw grid lines
        for i in range(13):
            pygame.draw.line(screen, white, [i*100, 0], [i*100, 800])
        for i in range(9):
            pygame.draw.line(screen, white, [0, i*100], [1200, i*100])

        for i in range(len(level.points)-1):
            pygame.draw.line(screen, (255, 0, 255), level.points[i], level.points[i+1], width=4)

        # Use blit to draw objects on the screen surface
        pygame.draw.rect(screen, (0, 0, 100), (SCREEN_DIM[0]-200, 0, 200, SCREEN_DIM[1]))
        pygame.draw.rect(screen, white, (0, SCREEN_DIM[1]-80, SCREEN_DIM[0], 80))
        screen.blit(gicon.imp, gicon.position)
        screen.blit(ssfont.render(str(gicon.cost), False, blue), (gicon.position[0],786))
        screen.blit(hoicon.imp, hoicon.position)
        screen.blit(ssfont.render(str(hoicon.cost), False, blue), (hoicon.position[0],786))
        screen.blit(ticon.imp, ticon.position)
        screen.blit(sicon.imp, sicon.position)
        screen.blit(ssfont.render(str(sicon.cost), False, blue), (sicon.position[0],786))
        for h in hlst:
            if h.move and canPlace:
                pygame.draw.circle(screen, (100, 100, 100), 
                    h.center, h.range, 3)
            elif not canPlace and h.move:
                pygame.draw.circle(screen, (200, 0, 0), 
                    h.center, h.range, 3)
            elif h.hover and sum(h.upgraded)==len(h.upgraded) and not h.super_upgrade: # Super upgrade
                screen.blit(font.render(h.id.upper(), False, white), (1000,50))
                screen.blit(ssfont.render("1: " + h.super_upgrade_text, False, white), (1000,200))
                screen.blit(sfont.render("Cost: " + str(h.super_upgrade_cost), False, white), (1000, 250))
                # Display range and targeting
                if h.target == "First":
                    pygame.draw.circle(screen, (0, 200, 0), 
                        h.center, h.range, 3)
                elif h.target == "Strong":
                    pygame.draw.circle(screen, (200, 200, 0), 
                        h.center, h.range, 3)
            elif h.hover:
                # Display upgrades
                upgrade_text = [None for i in h.upgrade_text+h.upgrades]
                screen.blit(font.render(h.id.upper(), False, white), (1000,50))
                for i in range(len(h.upgrade_text)):
                    txt = str(i+1) + ": " + h.upgrade_text[i]
                    upgrade_text[2*i] = ssfont.render(txt, False, white)
                    upgrade_text[2*i+1] = sfont.render("Cost: " + str(h.upgrades[i]), False, white)
                for i in range(len(upgrade_text)):
                    if i%2 == 0:
                        screen.blit(upgrade_text[i], (1000,100+50*i))
                    else:
                        screen.blit(upgrade_text[i], (1000,100+50*(i-1)+20))
                
                # Display range and targeting
                if h.target == "First":
                    pygame.draw.circle(screen, (0, 200, 0), 
                        h.center, h.range, 3)
                elif h.target == "Strong":
                    pygame.draw.circle(screen, (200, 200, 0), 
                        h.center, h.range, 3)
            screen.blit(h.a_imp, h.position)
        for e in elst:
            screen.blit(e.a_imp, e.position)
        for p in projectiles:
            screen.blit(p.a_imp, p.position)

        player.money = int(player.money)
        player.lives = int(player.lives)
        player.round = int(player.round)
        money_surface = sfont.render('Money: '+str(player.money), False, purple)
        lives_surface = sfont.render("Lives: "+str(player.lives), False, purple)
        round_surface = sfont.render("Round "+str(player.round) + "/" + str(maxrounds), False, purple)
        time_surface = sfont.render("Time to next round: "+str(player.max_ticks-player.leveltick), False, purple)
        screen.blit(money_surface, (680,724))
        screen.blit(lives_surface, (680,760))
        screen.blit(round_surface, (840,724))
        screen.blit(time_surface, (840,760))

        if inPause:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    gameOn = False
            
            pygame.draw.rect(screen, white, (50, 50, SCREEN_DIM[0]-350, SCREEN_DIM[1]-250))
            screen.blit(sfont.render('Paused: Press "P" to unpause', False, blue), (350,350))

    pygame.display.flip()

    fpsClock.tick(FPS)


