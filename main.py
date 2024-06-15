import pygame
import json
import math

with open("systems.json", "r") as file:
    systems = json.load(file)
    for i in systems:
        i["x"] *= 100
        i["y"] *= 100


pos = [-10000000, -10000000, 20000000, 20000000]

default_color = (5, 5, 30)
colors = {'RED_STAR': (255, 0, 0), 'UNSTABLE': (255, 0, 255), 'ORANGE_STAR': (255, 128, 0), 'WHITE_DWARF': (255, 255, 255), 'YOUNG_STAR': (255, 255, 0), 'NEUTRON_STAR': (0, 255, 255), 'BLUE_STAR': (0, 0, 255), 'HYPERGIANT': (255, 128, 0), 'BLACK_HOLE': (0, 0, 0)}
system_size = 3
pygame.font.init()
font = pygame.font.SysFont("Monospace", 24)
planet_color = (190, 190, 190)

def update(pos, mouse, systems):
    pointed = None, float("inf"), True

    window.fill(default_color)
    for sys in systems:
        if pos[0] <= sys["x"] < pos[0]+pos[2] and pos[1] <= sys["y"] < pos[1]+pos[3]:
            if system_size-math.log2(pos[2]/window.get_width()/1000) >= 4:
                for i in sys["waypoints"]:
                    point = {"symbol" : i["symbol"], "type" : i["type"], "x" : sys["x"]+i["x"]*2, "y" : sys["y"]+i["y"]*2}

                    coord = ((point["x"]-pos[0])*window.get_width()//pos[2], (point["y"]-pos[1])*window.get_height()//pos[3])
                    
                    point_dist = math.sqrt(((point["x"]-pos[0])*window.get_width()/pos[2]-mouse[0])**2 + ((point["y"]-pos[1])*window.get_height()/pos[3]-mouse[1])**2)
                    if point_dist < 5-math.log2(pos[2]/window.get_width()/1000) and point_dist < pointed[1]:
                        pointed = point, point_dist, True

                    if 0 <= coord[0] < window.get_width() and 0 <= coord[1] < window.get_height() and window.get_at(coord) == default_color:
                        if (system_size-math.log2(pos[2]/window.get_width()/1000))/4 >= 1:
                            pygame.draw.circle(window, planet_color, coord, (system_size-math.log2(pos[2]/window.get_width()/1000))//4)
                        else :
                            pygame.draw.line(window, planet_color, coord, coord)
            
            coord = ((sys["x"]-pos[0])*window.get_width()//pos[2], (sys["y"]-pos[1])*window.get_height()//pos[3])
            
            point_dist = math.sqrt(((sys["x"]-pos[0])*window.get_width()/pos[2]-mouse[0])**2 + ((sys["y"]-pos[1])*window.get_height()/pos[3]-mouse[1])**2)
            if point_dist < 12-math.log2(pos[2]/window.get_width()/1000) and (point_dist < pointed[1] or pointed[2]):
                pointed = sys, point_dist, False

            if system_size-math.log2(pos[2]/window.get_width()/1000) >= 1:
                pygame.draw.circle(window, colors[sys["type"]] if window.get_at(coord) in (default_color, planet_color) else "white", coord, system_size-math.log2(pos[2]/window.get_width()/1000))
            else :
                pygame.draw.line(window, colors[sys["type"]] if window.get_at(coord) in (default_color, planet_color) else "white", coord, coord)
    
    if pointed[0] != None:
        coord = ((pointed[0]["x"]-pos[0])*window.get_width()//pos[2], (pointed[0]["y"]-pos[1])*window.get_height()//pos[3])
        if "waypoints" in pointed[0]:
            pygame.draw.circle(window, "white", coord, system_size-math.log2(pos[2]/window.get_width()/1000)+3, 1)
        else :
            pygame.draw.circle(window, "white", coord, (system_size-math.log2(pos[2]/window.get_width()/1000))//4+3, 1)

    if pointed[0] != None:
        symbol = font.render(f"Symbol : {pointed[0]['symbol']}", True, "white")
        type = font.render(f"Type : {pointed[0]['type']}", True, "white")
        text = pygame.Surface((max(symbol.get_width(),type.get_width())+10, symbol.get_height()+type.get_height()), pygame.SRCALPHA)

        text.set_alpha(200)
        text.blit(symbol, (5, 0))
        text.blit(type, (5, symbol.get_height()))
        window.blit(text, (0, 0))

    pygame.display.flip()

pygame.init()
win_size = (800, 800)
window = pygame.display.set_mode(win_size, pygame.RESIZABLE)

clock = pygame.time.Clock()
quit = False
click = (0, 0), False
mouse = (0, 0)
update(pos, mouse, systems)
while not quit:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            mouse = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            click = event.pos, True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if click[1]:
                pos = [pos[0]+(click[0][0]-mouse[0])*pos[2]//window.get_width(), pos[1]+(click[0][1]-mouse[1])*pos[3]//window.get_height(), pos[2], pos[3]]
                click = mouse, False
        if event.type == pygame.WINDOWRESIZED:
            pos[2] = int(pos[2] * event.x / win_size[0])
            pos[3] = int(pos[3] * event.y / win_size[1])
            win_size = (event.x, event.y)
        if event.type == pygame.MOUSEWHEEL:
            if click[1]:
                pos = [pos[0]+(click[0][0]-mouse[0])*pos[2]//window.get_width(), pos[1]+(click[0][1]-mouse[1])*pos[3]//window.get_height(), pos[2], pos[3]]
            ratio = 1.1**event.y
            pos[2:4] = [int(pos[2] / ratio), int(pos[3] / ratio)]
            pos[0] -= int(mouse[0]*(pos[2]/window.get_width())*(1-ratio))
            pos[1] -= int(mouse[1]*(pos[3]/window.get_height())*(1-ratio))
            if click[1]:
                click = mouse, True

        
    if click[1]:
        update([pos[0]+(click[0][0]-mouse[0])*pos[2]//window.get_width(), pos[1]+(click[0][1]-mouse[1])*pos[3]//window.get_height(), pos[2], pos[3]], mouse, systems)
    else :
        update(pos, mouse, systems)
