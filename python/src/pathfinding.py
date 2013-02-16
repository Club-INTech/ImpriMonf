#! /usr/bin/env python
# -*- coding: utf8 -*-
import math
import random

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
	
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def afficher(self):
        print ("("+str(self.getX())+","+str(self.getY())+"), ")

class LinKernighan():
    def __init__(self, points):
        self.INF = 99999
        self.vitesseX = 1.
        self.vitesseY = 5.
        self.points = points
        #print ("Avant traitement :")
        #self.afficherPoints(self.points)
        self.pointsTries = self.plusProcheVoisin()
        print ("Apres traitement :")
        self.afficherPoints(self.pointsTries)
        print("Calcul : OK")
	
    
    def afficherPoints(self, pts):
        for pt in pts:
            pt.afficher()
            
    def distance(self, pt1, pt2):
        return math.sqrt(((pt1.getX()-pt2.getX())/self.vitesseX)**2+((pt1.getY()-pt2.getY())/self.vitesseY)**2)

    def distanceTotaleParcours(self):
        d=0
        i=1
        while i < len(self.pointsTries):
            d+=self.distance(self.pointsTries[i-1], self.pointsTries[i])
            i+=1
        return d
    
    def plusProcheVoisin(self):
        pointsTries = [self.points[0]]
        points_restants = self.points
        pt_traite = points_restants.pop(0)
        #pt_traite.afficher()
        while len(points_restants) > 0:
            distance_min = self.INF
            #i=0
            id_pt_proche = -1
            for i in range(len(points_restants)):
                pt = points_restants[i]
                #print ("   pt = ", end="")
                #pt.afficher()
                #print (str(self.distance(pt, pt_traite))+" < "+str(distance_min)+" ")
                if pt != pt_traite and self.distance(pt, pt_traite) < distance_min:
                    distance_min = self.distance(pt, pt_traite)
                    id_pt_proche = i
                    #print ("retenu", end="")
                #print ("")
            if(id_pt_proche < 0):
                print ("Erreur : id_pt_proche < 0 ("+str(id_pt_proche)+"), i = "+str(i))
            pt_traite = points_restants.pop(id_pt_proche)	#correspond au point que l'on traitera dans la prochaine itération
            pointsTries.append(pt_traite)
            #print ("point enregistre : ", end="")
            #pt_traite.afficher()
        
        return pointsTries
        
    def echangerParcours(self, id1, id2):
        inter=points[id2];
        points[id2]=points[id1];
        points[id1]=inter;

    def renverserParcours(self, i, j):
        a = math.min(i,j)
        b = math.max(i,j)
        while a < b:
            echangeParcours(a, b);
            a+=1
            b-=1

        
        
points = []
for i in range(10):
    x = random.randint(1,1000)
    y = random.randint(1,1000)
    points.append(Point(x, y))
print ("Génération aléatoire des points : OK")

l=LinKernighan(points)
print (l.distanceTotaleParcours())
