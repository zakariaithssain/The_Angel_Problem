# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:29:27 2024

@author: zakaria
"""

import random as rd
import pygame as pg
import time as t
import sys
from math import sqrt
import mysql.connector



def sql(simula, coups, Type):
    try:
        
        connection = mysql.connector.connect(
            host="localhost",
            user="zeco",  
            password="5311692",   
            database="simulations"    
        )

        cursor = connection.cursor()


        insert_query = """
        INSERT INTO simulations (simulation, coups, type)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_query, (simula, coups, Type))

       
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


simul=1
def simulation(simul):
    pg.init()
    long, larg, carr = 700, 700, 10
    coup, Type = 1, ""
    screen = pg.display.set_mode((long, larg))
    
    positions = [(x, y) for x in range(0, larg, carr) for y in range(0, long, carr)]
    corners = [[(x, y) for x in range(0, larg - 5 * carr + 1, 5 * carr)] for y in range(0, long - 5 * carr + 1, 5 * carr)]
    blocs = [[(corners[i][j][0], corners[i][j][1] + 5 * carr), corners[i][j], (corners[i][j][0] + 5 * carr, corners[i][j][1])]
             for i in range(len(corners)) for j in range(len(corners[0]))]

    def grill():
        screen.fill((255, 255, 255))
        for x in range(0, larg, carr):
            pg.draw.line(screen, (224, 224, 224), (x, 0), (x, long))
        for y in range(0, long, carr):
            pg.draw.line(screen, (224, 224, 224), (0, y), (larg, y))
            
    def subd():
        for x in range(0, larg, 5 * carr):
            pg.draw.line(screen, (128, 128, 128), (x, 0), (x, long), 2)
        for y in range(0, long, 5 * carr):
            pg.draw.line(screen, (128, 128, 128), (0, y), (larg, y), 2)
            
    def distance(pt1, pt2):
        return sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def tri(pt):
        dist = distance(pt, (ange.x, ange.y))
        return (dist, pt[0])  

    class Demon:
        def __init__(self):
            self.arete = carr
            self.color = (0, 0, 0)
            self.ptvisite = set()
            self.x, self.y = long // 2, larg // 2
         
        def contrestrat(self, ange):
            actuel = ange.blocactuel()
            Abloquer = []
            for pos in positions:
                if actuel[1][0] - 3 * carr < pos[0] < actuel[1][0] + 7 * carr and actuel[1][1] - 3 * carr < pos[1] < actuel[1][1] +7 * carr:
                    if pos not in [pt for pt in positions if actuel[1][0] <= pt[0] < actuel[2][0] and actuel[1][1] <= pt[1] < actuel[0][1]]:
                        Abloquer.append(pos)
            if (self.x, self.y) in Abloquer:
                Abloquer.remove((self.x, self.y))
            Abloquer = list(set(Abloquer) - self.ptvisite - {(ange.x, ange.y)})
            Abloquer.sort(key=tri)
            return Abloquer
        
        def mvt(self, ange):
            if self.contrestrat(ange):
                self.x, self.y = self.contrestrat(ange).pop(0)
                self.ptvisite.add((self.x, self.y))
           
        
        
        def drawvstdpts(self):
            for pt in self.ptvisite:
                pg.draw.rect(screen, self.color, (pt[0], pt[1], carr, carr))

    class Ange:
        def __init__(self, demon):
            self.pui = 2
            self.arete = carr
            self.color = (0, 128, 255)
            self.x = larg // 2 + 2 * carr
            self.y = long // 2 + 2 * carr
            self.demon = demon
           
        def mvt(self):
            interdit = self.demon.ptvisite
            access = [pt for pt in positions if max(abs(self.x - pt[0]), abs(self.y - pt[1])) <= self.pui * carr]
            valable = list(set(access) - interdit)
            if (self.x, self.y) in valable:
                valable.remove((self.x, self.y))
         
            if not valable: return False
               
            self.x, self.y = valable[rd.randint(0, len(valable) - 1)]
            return True
           
        def draw(self):
                pg.draw.rect(screen, self.color, (self.x, self.y, carr, carr))
         
        def blocactuel(self):
            for bloc in blocs:
                if bloc[1][0] <= self.x < bloc[2][0] and bloc[1][1] <= self.y < bloc[0][1]:
                    return bloc
       
        def touchefrontiere(self):
            if self.x == 0 or self.x == larg - carr or self.y == 0 or self.y == long - carr:
                return True
            return False

    demon = Demon()       
    ange = Ange(demon)

    def game(temps):
        nonlocal coup
        nonlocal Type
        grill() 
        subd()
        
        if not (ange.mvt() and demon.contrestrat(ange)):
            t.sleep(2)
            print(f"{simul}e simulation: L'Ange est borné après {coup} coups.")
            Type="Ange Borné"
         
            return False
        if ange.touchefrontiere():
            t.sleep(2)
            print(f"{simul}e simulation: L'Ange a touché les frontières après {coup} coups")
            Type="Frontière touchée "
           
            return False
        
        ange.draw()
        demon.mvt(ange)
        demon.drawvstdpts()
        pg.display.flip()
        t.sleep(temps)
        coup += 1
        return True
                   
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT: running = False
        if not game(0.000000001): running = False
        
    pg.quit()
    return (simul, coup, Type)


while simul < 1000:
    
    resultat=simulation(simul)
    sql(resultat[0], resultat[1], resultat[2])
    simul += 1
    
    
sys.exit()