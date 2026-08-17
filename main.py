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

# Background image
star_bg = pygame.image.load(os.path.join("Sprites", "Background", "stars_texture.png")).convert()
star_bg = pygame.transform.scale(star_bg, SCREEN_DIM)
galaxy_img = pygame.image.load(os.path.join("Sprites", "Background", "galaxy.png")).convert_alpha()
galaxy_rect = galaxy_img.get_rect()
galaxy_ang = 0 # Rotates galaxy in background
 
# Instantiate all objects
hlst = []
elst = []
tower_clickers = [
    (GunnerClicker(xy=[50, 752]), Gunner),
    (HowitzerClicker(xy=[100, 752]), Howitzer),
    (SaboteurClicker(xy=[150, 752]), Saboteur),
    (SeekerClicker(xy=[200, 752]), Seeker),
    (LeechClicker(xy=[250, 752]), Leech),
    (ShredderClicker(xy=[300, 752]), Shredder),
    (OrbiterClicker(xy=[350, 752]), Orbiter)
]

ticon = TrashClicker(xy=[450, 752])
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
                            for icon, _ in tower_clickers:
                                icon.cost = round(icon.cost * difficulty_adj[player.difficulty])
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
    elif inPause:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        inPause = not inPause
                        inLevel = not inLevel
                    elif event.key == K_ESCAPE:
                        gameOn = False
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
                            if h.id == "Orbiter":
                                # Count how many meteors belong to this specific Orbiter
                                meteor_count = sum(1 for p in projectiles if getattr(p, 'parent', None) == h and getattr(p, 'id', '') == "Meteor")
                                if h.target == "Cwise":
                                    h.target = "CCwise"
                                elif h.target == "CCwise" and meteor_count > 1:
                                    h.target = "Mixed"
                                else:
                                    h.target = "Cwise"
                            else: # Standard targeting for other towers
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

                for icon, hero_class in tower_clickers:
                    if icon.hitBox.isClicked(mouseloc):
                        hlst.append(hero_class(mouseloc, move=True))
                        if hlst[-1].id == "Orbiter": # Assign orbiter special targeting and add meteor
                            hlst[-1].target = "Cwise"
                            meteor = Meteor([mouseloc[0]+50, mouseloc[1]], 0)
                            meteor.parent = hlst[-1]
                            meteor.orbit_angle = 0
                            meteor.radius = hlst[-1].range
                            meteor.meteor_index = 0 # Helps track mixed direction
                            projectiles.append(meteor)
                            
                        hero_purchased = True
                        break

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
                    elif event.key == K_m: player.money += 10000
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
                            elif h.id == "Orbiter":
                                # Find existing meteor angle(s) to offset by 180 degrees
                                existing_meteors = [p for p in projectiles if getattr(p, 'id', '') == "Meteor" and getattr(p, 'parent', None) == h]
                                
                                if len(existing_meteors) == 1: # Add in three more
                                    base_angles = [(existing_meteors[0].orbit_angle + 90) % 360,
                                                   (existing_meteors[0].orbit_angle + 180) % 360,
                                                   (existing_meteors[0].orbit_angle + 270) % 360]
                                    meteor_indices = [1, 0, 1]
                                else:
                                    base_angles = [(existing_meteors[0].orbit_angle + 60) % 360,
                                                   (existing_meteors[0].orbit_angle + 120) % 360,
                                                   (existing_meteors[0].orbit_angle + 240) % 360,
                                                   (existing_meteors[0].orbit_angle + 300) % 360]
                                    meteor_indices = [1, 0, 0, 1]
                                for meteor in range(len(base_angles)):
                                    second_meteor = Meteor([h.center[0], h.center[1]], 0)
                                    second_meteor.parent = h
                                    second_meteor.orbit_angle = base_angles[meteor]
                                    second_meteor.radius = h.range
                                    second_meteor.meteor_index = meteor_indices[meteor]
                                    if h.upgraded[2]:
                                        scale_factor = 2
                                        new_w = int(second_meteor.imp.get_width() * scale_factor)
                                        new_h = int(second_meteor.imp.get_height() * scale_factor)
                                        
                                        second_meteor.imp = pygame.transform.scale(second_meteor.imp, (new_w, new_h))
                                        second_meteor.a_imp = pygame.transform.scale(second_meteor.a_imp, (new_w, new_h))
                                        
                                        if hasattr(second_meteor, 'hitBox') and hasattr(second_meteor.hitBox, 'scale'):
                                            second_meteor.hitBox.scale(scale_factor)
                                    projectiles.append(second_meteor)
                        # Standard upgrade cap logic (limits to 3 purchases max)
                        elif sum(h.upgraded) < 3:
                            if event.key == K_1 and not h.upgraded[0] and player.money >= h.upgrades[0]:
                                h.upgraded[0] = True
                                player.money -= h.upgrades[0]
                                h.sell_value += h.upgrades[0]
                                if h.id == "Gunner": h.range += 50
                                elif h.id == "Saboteur": h.range += 20
                                elif h.id == "Orbiter":
                                    # Find existing meteor angle to offset by 180 degrees
                                    existing_meteors = [p for p in projectiles if getattr(p, 'id', '') == "Meteor" and getattr(p, 'parent', None) == h]
                                    
                                    base_angle = 0
                                    if len(existing_meteors) > 0:
                                        base_angle = (existing_meteors[0].orbit_angle + 180) % 360
                                    
                                    # Spawn second meteor
                                    second_meteor = Meteor([h.center[0], h.center[1]], 0)
                                    second_meteor.parent = h
                                    second_meteor.orbit_angle = base_angle
                                    second_meteor.radius = h.range
                                    second_meteor.meteor_index = 1  # Index 1 will rotate opposite direction if target == "Mixed"
                                    second_meteor.a_imp = second_meteor.imp
                                    if h.upgraded[2]:
                                        scale_factor = 2
                                        new_w = int(second_meteor.imp.get_width() * scale_factor)
                                        new_h = int(second_meteor.imp.get_height() * scale_factor)
                                        
                                        second_meteor.imp = pygame.transform.scale(second_meteor.imp, (new_w, new_h))
                                        second_meteor.a_imp = pygame.transform.scale(second_meteor.a_imp, (new_w, new_h))
                                        
                                        if hasattr(second_meteor, 'hitBox') and hasattr(second_meteor.hitBox, 'scale'):
                                            second_meteor.hitBox.scale(scale_factor)
                                    projectiles.append(second_meteor)
                            elif event.key == K_2 and not h.upgraded[1] and player.money >= h.upgrades[1]:
                                h.upgraded[1] = True
                                player.money -= h.upgrades[1]
                                h.sell_value += h.upgrades[1]
                                if h.id == "Gunner": h.cooldown_reset *= 2/3
                                elif h.id == "Howitzer": h.cooldown_reset *= 3/5
                            elif event.key == K_3 and not h.upgraded[2] and player.money >= h.upgrades[2]:
                                h.upgraded[2] = True
                                player.money -= h.upgrades[2]
                                h.sell_value += h.upgrades[2] / 2
                                if h.id == "Seeker": h.cooldown_reset *= 3/5
                                elif h.id == "Orbiter":
                                    scale_factor = 1.75  # Scale size by 75%
                                    
                                    for p in projectiles:
                                        if getattr(p, 'id', '') == "Meteor" and getattr(p, 'parent', None) == h:
                                            new_width = int(p.imp.get_width() * scale_factor)
                                            new_height = int(p.imp.get_height() * scale_factor)
                                            p.imp = pygame.transform.scale(p.imp, (new_width, new_height))
                                            p.a_imp = pygame.transform.scale(p.a_imp, (new_width, new_height))
                                            if hasattr(p, 'width') and hasattr(p, 'height'):
                                                p.width = new_width
                                                p.height = new_height
                                            if hasattr(p, 'hitBox') and hasattr(p.hitBox, 'scale'):
                                                p.hitBox.scale(scale_factor)
                                            elif hasattr(p, 'hitBox') and hasattr(p.hitBox, 'width'):
                                                p.hitBox.width = new_width
                                                p.hitBox.height = new_height
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
                    sp.spawn_count += 1
                    if sp.spawn_count < 10:
                        new_enemies[-1].reward = new_enemies[-1].reward // 5
                    else:
                        new_enemies[-1].reward = 0
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
                else:
                    continue
                sp.spawn_count += 1
                if sp.spawn_count < 10:
                    new_enemies[-1].reward = new_enemies[-1].reward // 5
                else:
                    new_enemies[-1].reward = 0
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
            
            # If we want unsabotaged, but didn't find any, default to First
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
                    # Checks for h.target == "Unsabotaged" so it actually fires
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
                                if h.upgraded[3]:
                                    projectiles[-1].damage *= 2
                                if h.super_upgrade:
                                    projectiles[-1].accelerate = True
                                    projectiles[-1].speed *= 2
                                    projectiles[-1].pierce *= 3
                            elif h.id == "Shredder":
                                angle_central = h.angle + 2 * (1 - 2 * int(h.angle < 0))
                                if h.upgraded[0]:
                                    angles = [angle_central-45, angle_central-22.5, angle_central, angle_central+22.5, angle_central+45]
                                else:
                                    angles = [angle_central-30, angle_central, angle_central+30]
                                for a in angles:
                                    projectiles.append(Shrapnel(xy=[h.center[0], h.center[1]], angle=a))
                                    if h.upgraded[1]:
                                        projectiles[-1].speed *= 2.5
                                    if h.upgraded[4]:
                                        projectiles[-1].pierce += 1
                                    if h.upgraded[5]:
                                        projectiles[-1].damage *= 2
                                    projectiles[-1].parent = h
                                    projectiles[-1].a_imp = pygame.transform.rotate(projectiles[-1].imp, projectiles[-1].angle)
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
            projectiles = [p for p in projectiles if getattr(p, 'id', '') == "Meteor"]

        surviving_projectiles = []

        for p in projectiles:

            if getattr(p, 'id', '') == "Meteor": # Meteor Orbital Movement
                if not hasattr(p, 'parent') or p.parent not in hlst:
                    continue
                
                direction = 1
                if p.parent.target == "CCwise":
                    direction = -1
                elif p.parent.target == "Mixed":
                    direction = 1 if getattr(p, 'meteor_index', 0) % 2 == 0 else -1
                base_speed = getattr(p, 'speed', 5)
                if len(p.parent.upgraded) > 1 and p.parent.upgraded[1]:
                    base_speed *= 2.5
                
                p.orbit_angle = (getattr(p, 'orbit_angle', 0) + direction * base_speed) % 360
                d = anglemove(p.orbit_angle) 
                
                orbit_radius = getattr(p.parent, 'range', getattr(p, 'radius', 50))
                
                p.center[0] = p.parent.center[0] + orbit_radius * d[0]
                p.center[1] = p.parent.center[1] + orbit_radius * d[1]
                
                p.position = [p.center[0] - p.imp.get_width() // 2, p.center[1] - p.imp.get_height() // 2]
                p.lifespan = 0
            else:
                d = anglemove(p.angle)
                if p.id == "Missile":
                    if p.accelerate and p.speed < 40:
                        p.speed *= 1.024
                    dist = 0
                    strength = 0
                    fallback_dist = 0
                    
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

            # Despawning bounds (Bypass for Meteor)
            if p.id != "Meteor" and (p.lifespan >= p.lifespan_reset or 
                p.center[1] < 0 or p.center[0] < 0 or 
                p.center[1] > 720 or p.center[0] > SCREEN_DIM[0]):
                continue

            # Collision Logic
            for e in elst[:]:
                if p.hitBox.intersects(e.hitBox):
                    if p.id != "Meteor":
                        p.pierce -= 1
                        
                    e.lives -= p.damage
                    
                    if e.lives <= 0:
                        player.money += e.reward
                        
                        if hasattr(p, 'parent') and p.parent in hlst:
                            current_kills = getattr(p.parent, 'kills', 0) 
                            p.parent.kills = current_kills + 1
                            if p.parent.id == "Shredder" and p.parent.upgraded[3]:
                                if p.parent.kills % 50 == 0 and p.parent.cooldown_reset > 1:
                                    p.parent.cooldown_reset -= 1
                            
                        if e in elst:
                            elst.remove(e)
                            
                    if p.pierce <= 0 and p.id != "Meteor":
                        break

            # Keep meteors alive always, keep standard projectiles alive if they have pierce remaining
            if p.pierce > 0 or getattr(p, 'id', '') == "Meteor":
                surviving_projectiles.append(p)

        projectiles = surviving_projectiles

        text = font.render(str(sandbox), True, green, blue)
        textRect = text.get_rect()
        
        level.set_position()
        for e in elst: e.update()
        for h in hlst: h.update()
        for p in projectiles: p.update()

    ################
    ##### Draw #####
    ################
 
    screen.blit(star_bg, (0, 0))
    galaxy_ang = (galaxy_ang+0.04)%360
    galaxy_rimg = pygame.transform.rotate(galaxy_img, galaxy_ang)
    galaxy_rect = galaxy_rimg.get_rect(center=(SCREEN_DIM[0] // 2, SCREEN_DIM[1] // 2))
    screen.blit(galaxy_rimg, galaxy_rect)

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
        '''
        for i in range(13):
            pygame.draw.line(screen, white, [i * 100, 0], [i * 100, 800])
        for i in range(9):
            pygame.draw.line(screen, white, [0, i * 100], [1200, i * 100])
        '''
        for i in range(len(level.points) - 1):
            pygame.draw.line(screen, (10, 10, 10), level.points[i], level.points[i + 1], width=4)
        pygame.draw.rect(screen, (0, 0, 100), (SCREEN_DIM[0] - 200, 0, 200, SCREEN_DIM[1]))
        pygame.draw.rect(screen, white, (0, SCREEN_DIM[1] - 80, SCREEN_DIM[0], 80))
        # Draw buyable tower icons & costs
        for icon, _ in tower_clickers:
            screen.blit(icon.imp, icon.position)
            screen.blit(ssfont.render(str(icon.cost), False, blue), (icon.position[0], 786))

        # Draw utility icons
        screen.blit(ticon.imp, ticon.position)
        screen.blit(ssfont.render(str("Sell"), False, blue), (ticon.position[0]-10, 770))
        
        for h in hlst:
            if h.move and canPlace:
                pygame.draw.circle(screen, (100, 100, 100), h.center, h.range, 3)
            elif not canPlace and h.move:
                pygame.draw.circle(screen, (200, 0, 0), h.center, h.range, 3)
            elif h.hover:
                # Draw targeting circle
                if h.target == "First":
                    pygame.draw.circle(screen, (0, 200, 0), h.center, h.range, 3)
                elif h.target == "Strong":
                    pygame.draw.circle(screen, (200, 200, 0), h.center, h.range, 3)
                elif h.target == "Unsabotaged":
                    pygame.draw.circle(screen, (0, 200, 200), h.center, h.range, 3)

                # Draw tower name and kills
                screen.blit(font.render(h.id.upper(), False, white), (1000, 50))
                kills_str = "Target: " + str(getattr(h, 'target', 0)) + " | Kills: " + str(getattr(h, 'kills', 0))
                screen.blit(ssfont.render(kills_str, False, offwhite), (1000, 85))
                
                # Shift down slightly so upgrades don't overlap the kill count
                current_y = 115

                # Determine and draw purchased upgrades
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
                
                # Draw available upgrades
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