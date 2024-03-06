import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math as math

figure, axes = plt.subplots()
Wind_data = []

#Plots the windrose base
def WindRoseBase ():
    axes.set_aspect(1)
    plt.ylim(-50, 50)
    plt.xlim(-50, 50)
    angle = math.radians(22.5)
    r = [4, 15, 20, 25, 35, 45]
    Direction = ["W", "WNW", "NW", "NNW", "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW"]

    #Sets the concentric circles
    for i in range(len(r)):
        Circle = plt.Circle((0, 0), r[i], fill = False, color = "grey", linewidth = 0.5)
        axes.add_artist(Circle)
    
    #Sets the radii
    for i in range (0, 16):
        x_0 = math.cos((i*angle)+(angle/2))*4
        y_0 = math.sin((i*angle)+(angle/2))*4
        x = math.cos((i*angle)+(angle/2))*35
        y = math.sin((i*angle)+(angle/2))*35
        axes.plot([x, x_0], [y, y_0], color = "grey", linewidth = 0.5)

    #Sets the wind direction labels
    for i in range(0, 16):
        x = -math.cos(i*angle)*40
        y = math.sin(i*angle)*40
        plt.text(x, y, (Direction[i]), ha = "center", va = "center", fontsize = 9)

#Reads the datafile and places the values on the plot
def ReadData(name):
    r = [9.5, 17.5, 22.5, 30]
    angle = math.radians(22.5)
    Central_value = 0
    data = open(name)

    #Reads the data file
    for i in range (0, 16):
        line = (data.readline()).split()
        Wind_data.append(line)

        for j in range (0, 4):
            Central_value = Central_value + float(line[j])

    Central_value = 100 - Central_value
    Central_value = round(Central_value, 1)
    plt.text(0, 0, str(Central_value), ha = "center", va = "center", fontsize = 6)

    #Places the values on the plot
    for i in range(0, 16):
        for j in range(0, 4):
            x = -math.cos(i*angle + (math.pi / 2))*r[j]
            y = math.sin(i*angle + (math.pi / 2))*r[j]
            plt.text(x, y, (Wind_data[i][j]), ha = "center", va = "center", fontsize = 6)
    data.close()

#Places a certain runway with some angle and semi-width on the plot
def PlaceRunway(angle, semi_width, colour):
    angle = 90 - angle
    angle_rad = math.radians(angle)
    base = 2*semi_width 
    heigh = 2*(math.sqrt((45**2) - (semi_width**2)))
    inner_angle = math.asin(semi_width/45)
    anchor = [(-45*math.cos(inner_angle + angle_rad)), (-45*math.sin(inner_angle + angle_rad))]
    axes.add_patch(Rectangle((anchor[0], anchor[1]), heigh, base, angle, alpha = 0.3, edgecolor = colour, facecolor = colour, fill = "true"))

#Computates the usage of a certain runway
def UsageComputation(angle):
    Speeds = [15, 20, 25, 35]
    Non_use = 0

    #Computates the non usage
    for j in range (0, 4):
        for i in range (0, 16):
            angle_2 = math.radians((90 + angle) - (90 + 22.5*i))
            if (abs((Speeds[j])*math.sin(angle_2)) > 15):
                Non_use = Non_use + float(Wind_data[i][j])
    return(100 - Non_use)

#Finds the orientation with better usage
def MaximumUsageComputation():
    usage = UsageComputation(0)

    for i in range(1, 180):
        if (usage < UsageComputation(i)):
            usage = UsageComputation(i)
            angle = i
    print(angle)
    return(angle)


WindRoseBase()
ReadData("data.txt")
print(UsageComputation(30))
PlaceRunway(30, 15, "blue")
plt.show()
