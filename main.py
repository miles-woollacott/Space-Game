import pygame
from pygame.locals import *
from heroes import *
from clickers import *
from enemies import *
from projectile import *
from functions import *
from path import Path
from user import User
from textbox import textBox
import os

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
ticon = TrashClicker(xy=[450, 752])
sicon = SaboteurClicker(xy=[150, 752])
seicon = SeekerClicker(xy=[200, 752])
projectiles = []
paths = [Path([[0, 400], [200, 400], [200, 100], [500, 100], [500, 600], [200, 600], [200, 700], [1000, 700]]),
         Path([[0, 400], [200, 400], [200, 100], [500, 100], [500, 600], [200, 600], [200, 700], [1000, 700]]),
         Path([[0, 300], [1000, 700]])]
level = paths[1]
difficulty_adj = {"Easy": 0.9, "Medium": 1, "Hard": 1.1}

ghost_enemies = {
    "Speeder": Speeder([0,0]),
    "Spawner": Spawner([0,0]),
    "Accelerator": Accelerator([0,0]),
    "Tanker": Tanker([0,0]),
    "Dreadnought": Dreadnought([0,0]),
    "Regenerator": Regenerator([0,0]),
    "Destroyer": Destroyer([0,0]),
    "Repairer": Repairer([0,0]),
    "Infiltrator": Infiltrator([0,0])
}
ghost_lst = list(ghost_enemies.values())
ghost_names = array([i.id for i in ghost_lst])
ghost_priorities = array([i.level for i in ghost_lst])

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

    if cooldown > 0:
        cooldown = (cooldown + 1) % (FPS // 2)

    keys = pygame.key.get_pressed()

    if inMenu:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameOn = False

            if event.type == MOUSEBUTTONDOWN and cooldown == 0:
                cooldown += 1
                if infobutton.isClicked():
                    inInfo = True
                    inMenu = False
                else:
                    for i in difficultybuttons:
                        if i.isClicked(): # Begin round
                            player = User(difficulty=i.text)
                            gicon.cost = round(gicon.cost * difficulty_adj[player.difficulty])
                            hoicon.cost = round(hoicon.cost * difficulty_adj[player.difficulty])
                            sicon.cost = round(sicon.cost * difficulty_adj[player.difficulty])
                            seicon.cost = round(seicon.cost * difficulty_adj[player.difficulty])
                            level_spawnlist = generate_level(round=player.round, difficulty=player.difficulty,
                                                             ghost_names=ghost_names, ghost_priorities=ghost_priorities)
                            if player.difficulty == "Easy":
                                maxrounds = 50
                            elif player.difficulty == "Medium":
                                maxrounds = 75
                            else:
                                maxrounds = 100
                            inLevel = True
                            inMenu = False
                            break
    
    elif inInfo:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameOn = False

            if event.type == MOUSEBUTTONDOWN and cooldown == 0:
                cooldown += 1
                if returnbutton.isClicked():
                    inInfo = False
                    inMenu = True

    elif inLevel:

        ############ Mouse Controls ############

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                gameOn = False

            if event.type == MOUSEBUTTONDOWN and cooldown == 0:
                mouseloc = list(pygame.mouse.get_pos())
                if ticon.hitBox.isClicked(mouseloc):
                    ticon.clicked = not ticon.clicked
                
                cooldown += 1
                heroes_to_remove = []

                for h in hlst:
                    canPlace = True
                    if h.hitBox.isClicked(mouseloc):
                        
                        # Sell tower
                        if ticon.clicked:
                            ticon.clicked = False
                            heroes_to_remove.append(h)
                            player.money += 3 * h.sell_value / 2
                            continue # Skip the rest of the checks for this tower
                            
                        # Check for collisions with other towers
                        for h1 in hlst:
                            if h1 != h and h.hitBox.intersects(h1.hitBox):
                                canPlace = False
                        
                        # Place tower if not yet placed
                        if h.move:
                            if player.money < h.cost:
                                if h not in heroes_to_remove:
                                    heroes_to_remove.append(h)
                            elif canPlace and mouseloc[1] < 720:
                                h.move = False
                                h.placed = True
                                player.money -= h.cost
                                
                        # Change target priority if clicked
                        else:
                            if h.target == "First":
                                h.target = "Strong"
                            elif h.target == "Strong":
                                h.target = "Unsabotaged"
                            else:
                                h.target = "First"
                
                for h in heroes_to_remove:
                    if h in hlst:
                        hlst.remove(h)
                                
                hero_purchased = False
                
                if gicon.hitBox.isClicked(mouseloc):
                    hlst.append(Gunner(mouseloc, move=True))
                    hero_purchased = True
                elif hoicon.hitBox.isClicked(mouseloc):
                    hlst.append(Howitzer(mouseloc, move=True))
                    hero_purchased = True
                elif sicon.hitBox.isClicked(mouseloc):
                    hlst.append(Saboteur(mouseloc, move=True))
                    hero_purchased = True
                elif seicon.hitBox.isClicked(mouseloc):
                    hlst.append(Seeker(mouseloc, move=True))
                    hero_purchased = True

                # Easier difficulty makes heroes cheaper
                if hero_purchased:
                    hlst[-1].cost *= difficulty_adj[player.difficulty]
                    hlst[-1].upgrades = [round(up * difficulty_adj[player.difficulty]) for up in hlst[-1].upgrades]
                    hlst[-1].super_upgrade_cost = round(hlst[-1].super_upgrade_cost * difficulty_adj[player.difficulty]) 
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE or event.key == K_ESCAPE:
                    gameOn = False
                
                elif event.key == K_p:
                    inPause = not inPause
                    inLevel = not inLevel

                if sandbox:
                    if event.key == K_q: elst.append(Speeder(level.get_start()))
                    elif event.key == K_w: elst.append(Spawner(level.get_start()))
                    elif event.key == K_e: elst.append(Accelerator(level.get_start()))
                    elif event.key == K_r: elst.append(Tanker(level.get_start()))
                    elif event.key == K_t: elst.append(Dreadnought(level.get_start()))
                    elif event.key == K_y: elst.append(Regenerator(level.get_start()))
                    elif event.key == K_u: elst.append(Destroyer(level.get_start()))
                    elif event.key == K_i: elst.append(Repairer(level.get_start()))
                    elif event.key == K_o: elst.append(Infiltrator(level.get_start()))
                    elif event.key == K_c: elst = []
                    elif event.key == K_m: player.money += 1000
                    elif event.key == K_l: player.lives += 100
                
                if event.key == K_s:
                    sandbox = not sandbox

                ############ Upgrades ############

                for h in hlst:
                    if h.hover:
                        # Super upgrade unlocked when at least 3 normal upgrades are purchased
                        if event.key == K_1 and sum(h.upgraded) >= 3 and not h.super_upgrade and player.money >= h.super_upgrade_cost:
                            h.super_upgrade = True
                            player.money -= h.super_upgrade_cost
                            h.sell_value += h.super_upgrade_cost / 2
                            if h.id == "Gunner": h.cooldown_reset = 2
                            elif h.id == "Seeker": h.cooldown_reset /= 4
                        # Standard upgrade cap logic (limits to 3 purchases max)
                        elif sum(h.upgraded) < 3:
                            if event.key == K_1 and not h.upgraded[0] and player.money >= h.upgrades[0]:
                                h.upgraded[0] = True
                                player.money -= h.upgrades[0]
                                h.sell_value += h.upgrades[0]
                                if h.id == "Gunner": h.range += 50
                                elif h.id == "Saboteur": h.range += 20
                            elif event.key == K_2 and not h.upgraded[1] and player.money >= h.upgrades[1]:
                                h.upgraded[1] = True
                                player.money -= h.upgrades[1]
                                h.sell_value += h.upgrades[1]
                                if h.id == "Gunner": h.cooldown_reset -= 10
                                elif h.id == "Howitzer": h.cooldown_reset -= 32
                            elif event.key == K_3 and not h.upgraded[2] and player.money >= h.upgrades[2]:
                                h.upgraded[2] = True
                                player.money -= h.upgrades[2]
                                h.sell_value += h.upgrades[2] / 2
                            elif event.key == K_4 and len(h.upgrades) > 3 and not h.upgraded[3] and player.money >= h.upgrades[3]:
                                h.upgraded[3] = True
                                player.money -= h.upgrades[3]
                                h.sell_value += h.upgrades[3] / 2
                            elif event.key == K_5 and len(h.upgrades) > 4 and not h.upgraded[4] and player.money >= h.upgrades[4]:
                                h.upgraded[4] = True
                                player.money -= h.upgrades[4]
                                h.sell_value += h.upgrades[4] / 2
                                if h.id == "Gunner": h.can_see_infiltrators = True
                            elif (event.key == K_6 or event.key == K_KP6) and len(h.upgrades) > 5 and not h.upgraded[5] and player.money >= h.upgrades[5]:
                                h.upgraded[5] = True
                                player.money -= h.upgrades[5]
                                h.sell_value += h.upgrades[5] / 2
                                if h.id == "Saboteur": h.can_see_infiltrators = True
                if event.key == K_SPACE and len(elst) == 0 and not sandbox:
                    player.round += 1
                    if player.round > maxrounds:
                        quit()
                    player.leveltick = 0
                    level_spawnlist = generate_level(round=player.round, difficulty=player.difficulty,
                                                     ghost_names=ghost_names, ghost_priorities=ghost_priorities)
                    
            elif event.type == QUIT:
                gameOn = False
            
            hero_to_cancel = None
            for h in hlst:
                h.hover = h.hitBox.isClicked(pygame.mouse.get_pos())
                if h.move and ticon.hitBox.isClicked(pygame.mouse.get_pos()):
                    hero_to_cancel = h
            if hero_to_cancel is not None:
                hlst.remove(hero_to_cancel)

        if player.leveltick >= player.max_ticks and not sandbox:
            player.round += 1
            if player.round > maxrounds:
                quit()
            player.leveltick = 0
            level_spawnlist = generate_level(round=player.round, difficulty=player.difficulty,
                                                ghost_names=ghost_names, ghost_priorities=ghost_priorities)

        ############ Spawning ############

        if player.leveltick < player.max_ticks and not sandbox:
            player.leveltick += 1
            if len(level_spawnlist) > 0:
                for cluster in level_spawnlist:
                    if cluster["Tick"] <= player.leveltick:
                        if cluster["ID"] == "Speeder": elst.append(Speeder(level.get_start()))
                        elif cluster["ID"] == "Spawner": elst.append(Spawner(level.get_start()))
                        elif cluster["ID"] == "Accelerator": elst.append(Accelerator(level.get_start()))
                        elif cluster["ID"] == "Tanker": elst.append(Tanker(level.get_start()))
                        elif cluster["ID"] == "Dreadnought": elst.append(Dreadnought(level.get_start()))
                        elif cluster["ID"] == "Regenerator": elst.append(Regenerator(level.get_start()))
                        elif cluster["ID"] == "Destroyer": elst.append(Destroyer(level.get_start()))
                        elif cluster["ID"] == "Repairer": elst.append(Repairer(level.get_start()))
                        elif cluster["ID"] == "Infiltrator": elst.append(Infiltrator(level.get_start()))
                        
                        elst[-1].speed *= difficulty_adj[player.difficulty]
                        elst[-1].reward /= difficulty_adj[player.difficulty]
                        cluster["n"] -= 1
                        cluster["Tick"] += cluster["Sep"]
            level_spawnlist = [i for i in level_spawnlist if i["n"] > 0]

        new_enemies = []
        for sp in elst:
            if sp.id == "Spawner" and not sp.sabotaged:
                sp.countdown = (sp.countdown + 1) % sp.countdown_reset
                if sp.countdown < 7 and sp.countdown % 2 == 0:
                    new_enemies.append(Speeder([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
            elif sp.id == "Dreadnought" and not sp.sabotaged:
                sp.countdown = (sp.countdown + 1) % sp.countdown_reset
                if sp.countdown == 1:
                    new_enemies.append(Accelerator([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
                elif sp.countdown == 6:
                    new_enemies.append(Tanker([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
                elif sp.countdown == 11:
                    new_enemies.append(Spawner([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
                elif sp.countdown == 16:
                    new_enemies.append(Regenerator([sp.center[0], sp.center[1]], index=sp.index+0, distance=sp.distance))
        elst.extend(new_enemies)

        ############ Moving ############

        for h in hlst:
            if h.move:
                mousepos = list(pygame.mouse.get_pos())
                h.center[0] = mousepos[0]
                h.center[1] = mousepos[1]
                canPlace = True
                for h1 in hlst:
                    if h1 != h and h.hitBox.intersects(h1.hitBox):
                        canPlace = False

        enemies_reached_end = []
        for e in elst:
            e.angle = level.angles[e.index]
            e.a_imp = pygame.transform.rotate(e.imp, e.angle)
            
            if e.id == "Accelerator" and not e.sabotaged:
                e.speed += 0.1
            elif e.id == "Regenerator" and not e.sabotaged:
                e.countdown = (e.countdown + 1) % e.countdown_reset
                if e.countdown == 0:
                    e.lives = min(ghost_enemies["Regenerator"].lives, e.lives)+1
            elif e.id == "Repairer":
                for e1 in elst:
                    if e1.hitBox.intersects(e.hitBox) and e1.position != e.position:
                        e1.speed = ghost_enemies[e1.id].speed
                        e1.lives = ghost_enemies[e1.id].lives
                        e1.sabotaged = False
                        e1.repaired = True
                        
            if distance(e.center, level.points[e.index+1]) < e.speed:
                e.index += 1
                if e.index >= len(level.points) - 1:
                    enemies_reached_end.append(e)
                else:
                    e.center = level.get_index(e.index)
            else:
                delta = [i * e.speed for i in anglemove(e.angle)]
                e.center[0] -= delta[0]
                e.center[1] -= delta[1]
            e.distance += e.speed

        for e in enemies_reached_end:
            if not sandbox:
                player.lives -= e.lives
            if e in elst:
                elst.remove(e)
                
        if player.lives <= 0:
            quit()
        
        dead_enemies = set()
        dead_heroes = set()

        for h in hlst:
            if h.id == "Saboteur" and len(h.upgraded) > 5 and h.upgraded[5] and not h.move:
                for e in elst:
                    if e.id == "Infiltrator" and distance(h.center, e.center) < h.range:
                        e.revealed = True

        for h in hlst:
            dist = 0
            strength = 0
            fallback_dist = 0 # Remember the furthest enemy for our fallback
            
            for e in elst:
                # Check if the tower can see it, and if the enemy is revealed
                if e.id == "Infiltrator":
                    if not e.revealed and not h.can_see_infiltrators:
                        continue

                # Notice we removed "and e.distance > dist" from this line so "Strong" works properly
                if distance(h.center, e.center) < h.range and not h.move:
                    
                    if e.distance > fallback_dist:
                        fallback_dist = e.distance # Always track the first enemy we see
                        
                    if h.target == "First" and e.distance > dist:
                        dist = e.distance
                    elif h.target == "Strong" and e.priority > strength:
                        dist = e.distance
                        strength = e.priority
                    elif h.target == "Unsabotaged" and not e.sabotaged and e.distance > dist:
                        dist = e.distance
            
            # THE FALLBACK: If we want unsabotaged, but didn't find any, default to First
            if h.target == "Unsabotaged" and dist == 0 and fallback_dist > 0:
                dist = fallback_dist
                        
            if h.id == "Saboteur" and h.super_upgrade:
                for e in elst:
                    if e.id == "Infiltrator":
                        if not e.revealed and not h.can_see_infiltrators:
                            continue
                            
                    if e.id != "Repairer" and not e.repaired and distance(h.center, e.center) < h.range and not h.move:
                        e.speed = max(0.2, e.speed*0.9)
                        e.sabotaged = True
                        
            for e in elst:
                if dist > 0 and e.distance == dist:
                    # ADDED checking for h.target == "Unsabotaged" so it actually fires!
                    if h.target == "First" or (h.target == "Strong" and e.priority == strength) or h.target == "Unsabotaged":
                        h.angle = angle(h.center, e.center)
                        h.a_imp = pygame.transform.rotate(h.imp, h.angle)
                        if h.cooldown == 0:
                            h.cooldown += 1
                            if h.id == "Gunner":
                                projectiles.append(Bullet(xy=[h.center[0], h.center[1]],
                                                    angle=h.angle + 2 * (1 - 2 * int(h.angle < 0))))
                                projectiles[-1].parent = h
                                projectiles[-1].a_imp = pygame.transform.rotate(projectiles[-1].imp, projectiles[-1].angle)
                                if h.upgraded[0]: projectiles[-1].speed *= 1.6
                                if h.upgraded[3]: projectiles[-1].pierce += 2
                                if h.super_upgrade: projectiles[-1].pierce += 1
                            elif h.id == "Howitzer":
                                projectiles.append(Blast(xy=[h.center[0], h.center[1]],
                                                    angle=h.angle + 2 * (1 - 2 * int(h.angle < 0))))
                                projectiles[-1].parent = h
                                if h.upgraded[2]:
                                    projectiles[-1].imp = pygame.transform.scale(projectiles[-1].imp, (projectiles[-1].width * 2, projectiles[-1].height * 2))
                                if h.upgraded[3]:
                                    projectiles[-1].damage *= 2
                                projectiles[-1].a_imp = pygame.transform.rotate(projectiles[-1].imp, projectiles[-1].angle)
                                if h.upgraded[0]: projectiles[-1].speed *= 1.6
                                if h.super_upgrade: projectiles[-1].pierce += 1000
                            elif h.id == "Saboteur" and e.id != "Repairer" and not e.repaired:
                                e.speed *= 0.98
                                if h.upgraded[1]: e.speed *= 0.99
                                e.speed = max(0.2, e.speed)
                                if e.id == "Accelerator" and h.upgraded[2]: e.sabotaged = True
                                elif e.id == "Regenerator" and h.upgraded[3]: e.sabotaged = True
                                elif e.id == "Spawner" and h.upgraded[4]: e.sabotaged = True
                            elif h.id == "Seeker":
                                projectiles.append(Missile(xy=[h.center[0], h.center[1]],
                                                    angle=h.angle + 2 * (1 - 2 * int(h.angle < 0))))
                                projectiles[-1].parent = h
                                projectiles[-1].target = h.target
                                if h.upgraded[0]: projectiles[-1].speed *= 2
                                if h.upgraded[1]: projectiles[-1].pierce += 4
                                if h.super_upgrade:
                                    projectiles[-1].accelerate = True
                                    projectiles[-1].speed *= 2
                                    projectiles[-1].pierce *= 3

                if e.id == "Destroyer" and e.hitBox.intersects(h.hitBox):
                    dead_enemies.add(e)
                    dead_heroes.add(h)

            if h.cooldown > 0:
                h.cooldown = (h.cooldown + 1) % h.cooldown_reset

        for e in dead_enemies:
            if e in elst: elst.remove(e)
        for h in dead_heroes:
            if h in hlst: hlst.remove(h)

        ########### Projectiles ###########

        if len(elst) == 0:
            projectiles = []

        surviving_projectiles = []

        for p in projectiles:
            d = anglemove(p.angle)
            if p.id == "Missile":
                if p.accelerate and p.speed < 40:
                    p.speed *= 1.024
                dist = 0
                strength = 0
                fallback_dist = 0 # Fallback for missiles
                
                for e in elst:
                    if e.distance > fallback_dist:
                        fallback_dist = e.distance
                        
                    if p.target == "First" and e.distance > dist:
                        dist = e.distance
                    elif p.target == "Strong" and e.priority > strength:
                        dist = e.distance
                        strength = e.priority
                    elif p.target == "Unsabotaged" and not e.sabotaged and e.distance > dist:
                        dist = e.distance
                        
                if p.target == "Unsabotaged" and dist == 0 and fallback_dist > 0:
                    dist = fallback_dist        
                        
                for e in elst:
                    if dist > 0 and e.distance == dist:
                        if p.target == "First" or (p.target == "Strong" and e.priority == strength) or p.target == "Unsabotaged":
                            p.angle = angle(p.center, e.center)
                            p.a_imp = pygame.transform.rotate(p.imp, p.angle)
                            
            p.center[0] -= p.speed * d[0]
            p.center[1] -= p.speed * d[1]
            p.lifespan += 1

            if (p.lifespan >= p.lifespan_reset or 
                p.center[1] < 0 or p.center[0] < 0 or 
                p.center[1] > 720 or p.center[0] > SCREEN_DIM[0]):
                continue

            for e in elst[:]:
                if p.hitBox.intersects(e.hitBox):
                    p.pierce -= 1
                    e.lives -= p.damage
                    
                    if e.lives <= 0:
                        player.money += e.reward
                        
                        # Award kill to the parent tower
                        if hasattr(p, 'parent') and p.parent in hlst:
                            current_kills = getattr(p.parent, 'kills', 0) 
                            p.parent.kills = current_kills + 1
                            
                        if e in elst:
                            elst.remove(e)
                            
                    if p.pierce <= 0:
                        break

            if p.pierce > 0:
                surviving_projectiles.append(p)

        projectiles = surviving_projectiles

        text = font.render(str(sandbox), True, green, blue)
        textRect = text.get_rect()
        
        level.set_position()
        for e in elst: e.update()
        for h in hlst: h.update()
        for p in projectiles: p.update()
    
    elif inPause:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_p:
                    inPause = not inPause
                    inLevel = not inLevel

    ################
    ##### Draw #####
    ################
 
    screen.fill((0, 0, 0))

    if inMenu:
        pygame.draw.rect(screen, offwhite, background.rect)
        screen.blit(font.render("Tower Defense Game ig", False, blue), (400, 200))
        for i in difficultybuttons:
            pygame.draw.rect(screen, black, i.rect)
            screen.blit(i.get_text(), (i.left + 20, i.top + 30))
        for i in pathbuttons:
            pygame.draw.rect(screen, black, i.rect)
            screen.blit(i.get_text(), (i.left + 10, i.top + 10))
        pygame.draw.rect(screen, black, infobutton.rect)
        screen.blit(infobutton.get_text(), (infobutton.left + 20, infobutton.top + 30))

    elif inInfo:
        pygame.draw.rect(screen, offwhite, background.rect)
        screen.blit(font.render("Ships n Stuff", False, blue), (440, 120))
        pygame.draw.rect(screen, black, returnbutton.rect)
        screen.blit(returnbutton.get_text(), (returnbutton.left + 20, returnbutton.top + 30))

    elif inLevel or inPause:

        # Draw grid lines
        for i in range(13):
            pygame.draw.line(screen, white, [i * 100, 0], [i * 100, 800])
        for i in range(9):
            pygame.draw.line(screen, white, [0, i * 100], [1200, i * 100])

        for i in range(len(level.points) - 1):
            pygame.draw.line(screen, (255, 0, 255), level.points[i], level.points[i + 1], width=4)

        pygame.draw.rect(screen, (0, 0, 100), (SCREEN_DIM[0] - 200, 0, 200, SCREEN_DIM[1]))
        pygame.draw.rect(screen, white, (0, SCREEN_DIM[1] - 80, SCREEN_DIM[0], 80))
        screen.blit(gicon.imp, gicon.position)
        screen.blit(ssfont.render(str(gicon.cost), False, blue), (gicon.position[0], 786))
        screen.blit(hoicon.imp, hoicon.position)
        screen.blit(ssfont.render(str(hoicon.cost), False, blue), (hoicon.position[0], 786))
        screen.blit(ticon.imp, ticon.position)
        screen.blit(sicon.imp, sicon.position)
        screen.blit(ssfont.render(str(sicon.cost), False, blue), (sicon.position[0], 786))
        screen.blit(seicon.imp, seicon.position)
        screen.blit(ssfont.render(str(seicon.cost), False, blue), (seicon.position[0], 786))
        
        for h in hlst:
            if h.move and canPlace:
                pygame.draw.circle(screen, (100, 100, 100), h.center, h.range, 3)
            elif not canPlace and h.move:
                pygame.draw.circle(screen, (200, 0, 0), h.center, h.range, 3)
            elif h.hover:
                # 1. Draw Target Circle
                if h.target == "First":
                    pygame.draw.circle(screen, (0, 200, 0), h.center, h.range, 3)
                elif h.target == "Strong":
                    pygame.draw.circle(screen, (200, 200, 0), h.center, h.range, 3)
                elif h.target == "Unsabotaged":
                    pygame.draw.circle(screen, (0, 200, 200), h.center, h.range, 3)

                # 2. Draw Tower Name and Kills
                screen.blit(font.render(h.id.upper(), False, white), (1000, 50))
                kills_str = "Target: " + str(getattr(h, 'target', 0)) + " | Kills: " + str(getattr(h, 'kills', 0))
                screen.blit(ssfont.render(kills_str, False, offwhite), (1000, 85))
                
                # Shift down slightly so upgrades don't overlap the kill count
                current_y = 115

                # 3. Determine and Draw Purchased Upgrades
                purchased_list = []
                for i in range(len(h.upgraded)):
                    if h.upgraded[i]:
                        purchased_list.append(h.upgrade_text[i])
                
                if h.super_upgrade:
                    purchased_list.append(h.super_upgrade_text)

                if len(purchased_list) == 0:
                    screen.blit(ssfont.render("Not upgraded", False, white), (1000, current_y))
                    current_y += 18
                else:
                    for text in purchased_list:
                        if text == h.super_upgrade_text:
                            screen.blit(ssfont.render(text, False, purple), (1000, current_y))
                        else:
                            screen.blit(ssfont.render(text, False, yellow), (1000, current_y))
                        current_y += 18
                
                current_y += 20
                
                # 4. Draw Available Upgrades
                if h.super_upgrade:
                    screen.blit(sfont.render("All upgrades purchased", False, green), (1000, current_y))
                elif sum(h.upgraded) >= 3:
                    screen.blit(ssfont.render("1: " + h.super_upgrade_text, False, purple), (1000, current_y))
                    screen.blit(sfont.render("Cost: " + str(h.super_upgrade_cost), False, white), (1000, current_y + 25))
                else:
                    # Show normal upgrades
                    upgrade_text = [None for i in h.upgrade_text + h.upgrades]
                    for i in range(len(h.upgrade_text)):
                        txt = str(i + 1) + ": " + h.upgrade_text[i]
                        
                        if h.upgraded[i]:
                            upgrade_text[2 * i] = ssfont.render(txt, False, yellow)
                            upgrade_text[2 * i + 1] = ssfont.render("Already purchased", False, yellow) 
                        else:
                            upgrade_text[2 * i] = ssfont.render(txt, False, white)
                            upgrade_text[2 * i + 1] = ssfont.render("Cost: " + str(h.upgrades[i]), False, white)
                    
                    for i in range(len(upgrade_text)):
                        if i % 2 == 0:
                            # Using 25 * i creates a compact 50px gap between upgrades
                            screen.blit(upgrade_text[i], (1000, current_y + 25 * i))
                        else:
                            screen.blit(upgrade_text[i], (1000, current_y + 25 * (i-1) + 18))
            
            # This line ensures the towers are actually drawn!
            screen.blit(h.a_imp, h.position)
        for e in elst:
            screen.blit(e.a_imp, e.position)
        for p in projectiles:
            screen.blit(p.a_imp, p.position)

        player.money = int(player.money)
        player.lives = int(player.lives)
        player.round = int(player.round)
        money_surface = sfont.render('Money: ' + str(player.money), False, purple)
        lives_surface = sfont.render("Lives: " + str(player.lives), False, purple)
        round_surface = sfont.render("Round " + str(player.round) + "/" + str(maxrounds), False, purple)
        time_surface = sfont.render("Time to next round: " + str(player.max_ticks - player.leveltick), False, purple)
        
        screen.blit(money_surface, (700, 730))
        screen.blit(lives_surface, (700, 770))
        screen.blit(round_surface, (900, 730))
        screen.blit(time_surface, (900, 770))

    pygame.display.flip()
    fpsClock.tick(FPS)

pygame.quit()