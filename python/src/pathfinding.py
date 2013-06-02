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
        self.vitesseX = 6.6 # mm/sec
        self.vitesseY = 45.6 # mm/sec
        self.longueurSegment = 400 # distance de segmentation (en mm).
        self.points = points
        self.lastSegmentPret = -1
        #print ("Avant traitement :")
        #self.afficherPoints(self.points)
        self.pointsTries = self.points
        self.segments = self.segmentePoints()
        self.segmentsTries = []

    """
    Calcule tous les segments en une fois.
    """
    def calculSegments(self):
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
                print("Optimisation du temps de poinçonnage : "+"%.2f"%avancement+"%")
        print("Distance totale : "+str(self.distanceTotaleParcoursSegmente()))
        return self.segmentsTries


    """
    Calcule un segment donné. Utilisé par les threads.
    """
    def calculSegment(self, id_segment):
        segment = self.segments[id_segment]
        if len(segment) > 0 :
            self.points = list(segment)
            print("segment de "+str(self.longueurSegment)+"mm contenant "+str(len(segment))+" pts")
            #print ("Algo plus proche voisin en cours sur "+str(len(segment))+"points")
            self.pointsTries = self.plusProcheVoisin()
            #print ("Apres calcul plus proche voisin :")
            #self.afficherPoints(self.pointsTries)   #décommenter pour avoir l'affichage de la liste des points.
            print(" PPV : longueur : "+str(self.distanceTotaleParcours()))

            #Choix de 2-opt ou 3-opt :
            derniereDistanceTotale = self.distanceTotaleParcours()
            if len(self.pointsTries) > 150 :
                nb3opt = 0
            elif len(self.pointsTries) > 80 :
                nb3opt = 1
            else :
                nb3opt = 2
            for i in range(nb3opt):
                self.calcule_parcours_3opt()
                print(" 3-opt : longueur : " + str(self.distanceTotaleParcours()))
                for j in range(5):
                    self.calcule_parcours_2opt()
                    print(" 2-opt : longueur : " + str(self.distanceTotaleParcours()))
                    if self.distanceTotaleParcours() == derniereDistanceTotale :
                        break
                    else:
                        derniereDistanceTotale = self.distanceTotaleParcours()
            if nb3opt == 0 :
                for j in range(5):
                    self.calcule_parcours_2opt()
                    print(" 2-opt : longueur : " + str(self.distanceTotaleParcours()))
                    if self.distanceTotaleParcours() == derniereDistanceTotale :
                        break
                    else:
                        derniereDistanceTotale = self.distanceTotaleParcours()

            self.segmentsTries.append(self.pointsTries)
            #print(self.distanceTotaleParcoursSegmente())
            print("Optimisation du temps de poinçonnage du segment n°"+str(id_segment)+": OK ("+str(self.distanceTotaleParcours())+")")
        self.lastSegmentPret = id_segment

    def segmentePoints(self):
        segments = [ [] for i in range(int(self.maxY(self.pointsTries)/self.longueurSegment + 1))]
        for pt in self.pointsTries:
            segments[int(pt.getY()/self.longueurSegment)].append(pt)
        self.nbSegments = len(segments)
        print("Après segmentation : "+str(self.nbSegments)+" segments")
        return segments

    def getNbSegments(self):
        return self.nbSegments

    def getDernierSegmentCalcule(self):
        return self.pointsTries

    def getLastSegmentPret(self):
        return self.lastSegmentPret

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

    """
    Calcule le parcours optimal selon la méthode du plus proche voisin : après chaque
    """
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

    """
    Permet d'échanger 2 points dans self.pointsTries
    """
    def echangerPoints(self, id1, id2):
        temp=self.pointsTries[id2];
        self.pointsTries[id2]=self.pointsTries[id1];
        self.pointsTries[id1]=temp;

    """
    Renverse le parcours entre deux points. Utilisé dans les 2-opt et 3-opt.
    """
    def renverserParcours(self, i, j):
        a = min(i,j)
        b = max(i,j)
        while a < b:
            self.echangerPoints(a, b);
            a+=1
            b-=1

    """
    Echange deux portions de parcours. Utilisé notamment lors des parcours 3-opt
    """
    #Attention : échange seulement des portions adjacentes :
    def echangerPortions(self, debutPortion1, finPortion1, debutPortion2, finPortion2):
        if debutPortion2 == finPortion1 + 1:
            i = 0
            portion1 = []
            portion1Points = []
			#Stockage en mémoire des 2 portions à échanger
            while debutPortion1 + i <= finPortion1:
                portion1.append(debutPortion1 + i)
                portion1Points.append(self.pointsTries[debutPortion1 + i])
                i+=1
            i = 0
            portion2 = []
            portion2Points = []
            while debutPortion2 + i <= finPortion2:
                portion2.append(debutPortion2 + i)
                portion2Points.append(self.pointsTries[debutPortion2 + i])
                i+=1
			#échange de ces deux portions :
            inversion = portion2+portion1
            inversionPoints = portion2Points + portion1Points
            i=0
            while debutPortion1 + i <= finPortion2:
                self.pointsTries[debutPortion1 + i] = inversionPoints[i]
                i+=1
        else:
            print("ERREUR : les portions à échanger ne sont pas consécutives !")

    """
    différence de cout du parcours si on renverse le parcours entre les trous i et j
    """
    def difference_cout(self, i, j):
        if j<len(self.pointsTries)-1:
            return self.distance(self.pointsTries[i], self.pointsTries[j+1]) + self.distance(self.pointsTries[i-1], self.pointsTries[j]) - self.distance(self.pointsTries[i-1], self.pointsTries[i]) - self.distance(self.pointsTries[j], self.pointsTries[j+1])
        else:
            return self.distance(self.pointsTries[i-1], self.pointsTries[j]) - self.distance(self.pointsTries[i-1], self.pointsTries[i])


    """
     calcule un parcours 2-opt
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
                    debug = self.distanceTotaleParcours()
                    if surplusDistACBEDF < 0:
                        print("A", end="")
                        self.renverserParcours(indexC, indexB)
                        self.renverserParcours(indexE, indexD)
                        #print("A "+str(self.distanceTotaleParcours() - debug), end="")
                    elif surplusDistADEBCF < 0:
                        print("B", end="")
                        self.echangerPortions(indexB, indexC, indexD, indexE)
                    elif surplusDistADECBF < 0:
                        print("C", end="")
                        self.renverserParcours(indexB, indexC)
                        self.echangerPortions(indexB, indexC, indexD, indexE)
                    elif surplusDistAEDBCF < 0:
                        print("D", end="")
                        self.renverserParcours(indexE, indexD)
                        self.echangerPortions(indexB, indexC, indexD, indexE)

"""
points = []
nbPoints = 100
for i in range(nbPoints):
    x = random.randint(1,1000)
    y = random.randint(1,1000)
    points.append(Point(x, y))
print ("Génération aléatoire des "+str(nbPoints)+" points : OK")

l=LinKernighan(points)
liste = []
liste = l.calculSegments()
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