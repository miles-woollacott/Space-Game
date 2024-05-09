import math
from pandas import DataFrame

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

def get_all_ticks(df):
    newdf = []
    for i in range(df.shape[0]):
        row = df.iloc[i,]
        if row.Count > 0:
            for j in range(row.Count):
                newdf.append([row.ID, row.Tick + j*row.Sep])
    return DataFrame(newdf, columns=["ID", "Tick"])