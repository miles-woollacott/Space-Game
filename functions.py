import math
from numpy import random, array, sqrt

def distance(x, y):
    return(((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5)

def angle(x, y):
    d = [x[0]-y[0], x[1]-y[1]]
    h = (d[0]**2+d[1]**2)**0.5
    if d[0] == 0 and x[1]>y[1]:
        return 0
    elif d[0] == 0 and x[1]<y[1]:
        return 180
    elif d[0]<0:
        return -1*(90-180*math.asin(d[1]/h)/math.pi)
    return 90-180*math.asin(d[1]/h)/math.pi

def anglemove(angle):
    x = math.sin(math.pi*angle/180)
    y = math.cos(math.pi*angle/180)
    return [x,y]

def generate_level(round, difficulty, ghost_names, ghost_priorities):
    if round == 0:
        return []
    random.seed(round+1)
    ghost_priorities_p = (ghost_priorities.max() - ghost_priorities+1).astype(float)
    # Determine number of clusters and type of enemies in round
    if difficulty == "Easy":
        n = random.poisson(lam=4)+1
        if round < 20:
            ghost_priorities_p[ghost_priorities>1] = 0
        elif round < 40:
            ghost_priorities_p[ghost_priorities>2] = 0
    elif difficulty == "Medium":
        n = random.poisson(lam=6)+1
        if round < 10:
            ghost_priorities_p[ghost_priorities>1] = 0
        elif round < 20:
            ghost_priorities_p[ghost_priorities>2] = 0
        elif round < 50:
            ghost_priorities_p[ghost_priorities>3] = 0
    else:
        n = random.poisson(lam=9)+1
        if round >= 50:
            pass
        elif round < 5:
            ghost_priorities_p[ghost_priorities>1] = 0
        elif round < 10:
            ghost_priorities_p[ghost_priorities>2] = 0
        elif round < 20:
            ghost_priorities_p[ghost_priorities>3] = 0
    ghost_priorities_p = ghost_priorities_p / ghost_priorities_p.sum()
    sels = random.choice(ghost_names, size=n, p=ghost_priorities_p)
    # Determines number of items in clusters, and ticks
    ticks = random.uniform(low=1, high=500, size=n).astype(int)
    ticks -= (min(ticks)-1)
    nums = random.poisson(lam=sqrt(round), size=n)+1
    seps = random.poisson(lam=4, size=n)+1
    return [{"ID":sels[i], "Tick":ticks[i], "Sep":seps[i], "n":nums[i]} for i in range(n)]