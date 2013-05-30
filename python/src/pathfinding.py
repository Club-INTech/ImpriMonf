#! /usr/bin/env python
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
        self.longueurSegment = 600 # distance de segmentation (en mm).
        self.points = points
        #print ("Avant traitement :")
        #self.afficherPoints(self.points)
        self.pointsTries = self.points
        print ("Avant tout calcul, dans l'ordre aléatoire initial : ")
        print(" longueur : "+str(self.distanceTotaleParcours()))

        print("Segmentation des points en cours...")
        self.segments = self.segmentePoints()
        print("Segmentation : done")
        self.segmentsTries = []
        nbSegmentsTraites = 0
        for segment in self.segments :
            if len(segment) > 0 :
                self.points = list(segment)
                #print ("Algo plus proche voisin en cours sur "+str(len(segment))+"points")
                self.pointsTries = self.plusProcheVoisin()
                #print ("Apres calcul plus proche voisin :")
                #self.afficherPoints(self.pointsTries)   #décommenter pour avoir l'affichage de la liste des points.
                #print(" longueur : "+str(self.distanceTotaleParcours()))

                #print ("Algo 2-opt en cours ...")
                self.calcule_parcours_2opt()
                #print (" Apres calcul 2-opt :")
                #print(" longueur : " + str(self.distanceTotaleParcours()))

                #print ("Algo 2eme 2-opt en cours ...")
                self.calcule_parcours_2opt()
                #print (" Apres calcul 2-opt :")
                #print(" longueur : " + str(self.distanceTotaleParcours()))
                """
                print ("Algo 3-opt en cours ...")
                self.calcule_parcours_3opt()
                print (" Apres calcul 3-opt :")
                print(" longueur : " + str(self.distanceTotaleParcours()))
                """
                self.segmentsTries.append(self.pointsTries)
                #print(self.distanceTotaleParcoursSegmente())
                nbSegmentsTraites+=1
                avancement = nbSegmentsTraites/self.nbSegments*100
                print("Optimisation du temps de poinçonnage : "+str(avancement)+"%")
        print("Distance totale : "+str(self.distanceTotaleParcoursSegmente()))

    def segmentePoints(self):
        segments = [ [] for i in range(int(self.maxY(self.pointsTries)/self.longueurSegment + 1))]
        for pt in self.pointsTries:
            segments[int(pt.getY()/self.longueurSegment)].append(pt)
        self.nbSegments = len(segments)
        print("Après segmentation : "+str(self.nbSegments)+" segments")
        return segments

    def maxY(self, pts):
        max = 0
        for pt in pts :
            if pt.getY() > max:
                max = pt.getY()
        return max

    def afficherPoints(self, pts):
        for pt in pts:
            pt.afficher()

    def distance(self, pt1, pt2):
        return max(abs((pt1.getX()-pt2.getX())/self.vitesseX), abs((pt1.getY()-pt2.getY())/self.vitesseY))

    def distanceTotaleParcours(self):
        d=0
        i=1
        while i < len(self.pointsTries):
            d+=self.distance(self.pointsTries[i-1], self.pointsTries[i])
            i+=1
        return round(d,2)

    def distanceTotaleParcoursSegmente(self):
        d = 0
        j = 0
        while j < len(self.segmentsTries):
            i=1
            while i < len(self.segmentsTries[j]):
                d+=self.distance(self.segmentsTries[j][i-1], self.segmentsTries[j][i])
                i+=1
            if j+1 < len(self.segmentsTries) :
                if len(self.segmentsTries[j+1]) > 0:
                    d+= self.distance(self.segmentsTries[j][i-1], self.segmentsTries[j+1][0]) # liaison entre les segments
            j+=1
        return round(d,2)

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
            pt_traite = points_restants.pop(id_pt_proche)   #correspond au point que l'on traitera dans la prochaine itération
            pointsTries.append(pt_traite)
            #print ("point enregistre : ", end="")
            #pt_traite.afficher()

        return pointsTries

    def echangerParcours(self, id1, id2):
        temp=self.pointsTries[id2];
        self.pointsTries[id2]=self.pointsTries[id1];
        self.pointsTries[id1]=temp;

    def renverserParcours(self, i, j):
        a = min(i,j)
        b = max(i,j)
        while a < b:
            self.echangerParcours(a, b);
            a+=1
            b-=1

    #Attention : échange seulement des portions adjacentes :
    def echangerPortions(self, debutPortion1, finPortion1, debutPortion2, finPortion2):
        if debutPortion2 == finPortion1 + 1:
            i = 0
            while debutPortion1 + i < finPortion2:
                self.echangerParcours((debutPortion1 + i)%len(self.pointsTries), (debutPortion2 + i)%len(self.pointsTries));
                i+=1
        else:
            print("ERREUR : les portions à échanger ne sont pas consécutives !")

    """
    différence de cout du parcours si on renversait le parcours entre les trous i et j
    on "casse" 2 liens entre 2 trous et on les remplace par 2 autres
    """
    def difference_cout(self, i, j):
        if j<len(self.pointsTries)-1:
            return self.distance(self.pointsTries[i], self.pointsTries[j+1]) + self.distance(self.pointsTries[i-1], self.pointsTries[j]) - self.distance(self.pointsTries[i-1], self.pointsTries[i]) - self.distance(self.pointsTries[j], self.pointsTries[j+1])
        else:
            return self.distance(self.pointsTries[i-1], self.pointsTries[j]) - self.distance(self.pointsTries[i-1], self.pointsTries[i])



    """
     calcule un parcours 2-opt, c'est à dire qu'aucune permutation
     de l'odre de parcours ne rend ce parcours plus court
    """
    def calcule_parcours_2opt(self):
        for i in range(1, len(self.pointsTries)):
            for j in range(i+1, len(self.pointsTries)):
                if self.difference_cout(i, j) < 0 :
                    self.renverserParcours(i, j)






    def calcule_parcours_3opt(self):
        for indexA in range(len(self.pointsTries)-6):
            indexB = indexA + 1
            for indexC in range(indexB+1, len(self.pointsTries)-4):
                indexD = indexC + 1
                for indexE in range(indexD+1, len(self.pointsTries)-2):
                    indexF = indexE + 1
                    A = self.pointsTries[indexA]
                    B = self.pointsTries[indexB]
                    C = self.pointsTries[indexC]
                    D = self.pointsTries[indexD]
                    E = self.pointsTries[indexE]
                    F = self.pointsTries[indexF]
                    distAB = self.distance(A, B)
                    distCD = self.distance(C, D)
                    distAC = self.distance(A, C)
                    distAD = self.distance(A, D)
                    distBD = self.distance(B, D)
                    distEF = self.distance(E, F)
                    distAE = self.distance(A, E)
                    distBE = self.distance(B, E)
                    distBF = self.distance(B, F)
                    distCE = self.distance(C, E)
                    distCF = self.distance(C, F)
                    distDF = self.distance(D, F)
                    surplusDistACBEDF = distAC + distBE + distDF - (distAB + distCD + distEF)
                    surplusDistADEBCF = distAD + distBE + distCF - (distAB + distCD + distEF)
                    surplusDistADECBF = distAD + distCE + distBF - (distAB + distCD + distEF)
                    surplusDistAEDBCF = distAE + distBD + distCF - (distAB + distCD + distEF)
                    if surplusDistACBEDF < 0:
                        self.renverserParcours(indexC, indexB)
                        self.renverserParcours(indexE, indexD)
                    elif surplusDistADEBCF < 0:
                        self.echangerPortions(indexB, indexC, indexD, indexE)
                        #print("ok", end="")
    #Attention : echangerPortions bug car les temps s'allongent parfois, et peut-Ãªtre que renverserParcours aussi : ÃƒÂ  tester

"""
points = []
nbPoints = 800
for i in range(nbPoints):
    x = random.randint(1,1000)
    y = random.randint(1,1000)
    points.append(Point(x, y))
print ("Génération aléatoire des "+str(nbPoints)+" points : OK")

l=LinKernighan(points)
"""
"""
print ("Algo 2-opt en cours ...")
l.calcule_parcours_2opt()
print (" Apres calcul 2-opt :")
#l.afficherPoints(l.pointsTries)
print(" longueur : " + str(l.distanceTotaleParcours()))
"""

"""
print ("Algo 3-opt en cours ...")
l.calcule_parcours_3opt()
print (" Apres calcul 3-opt :")
print(" longueur : " + str(l.distanceTotaleParcours()))
"""