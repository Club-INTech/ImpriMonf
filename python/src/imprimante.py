from serial import Serial
import os
import time
        
class Imprimante:
    """
    Classe implémentant une communication série avec l'imprimante.
    Elle permet d'envoyer une trame sur un périphérique et d'en recevoir une en retour.
    """
    
    baudrate = 9600
    ping = '#'
    
    def __init__(self):
        
        #périphérique série de l'imprimante (une fois la carte trouvée)
        self.serie = None
        
        #les threads attendent la serie
        self.prete = False
        
    def attribuer(self):
        """
        Cette méthode invoquée au lancement du service série permet de détecter et stocker le chemin pour communiquer avec la carte.
        """
        #liste les chemins trouvés dans /dev
        sources = os.popen('ls -1 /dev/ttyUSB* 2> /dev/null').readlines()
        sources.extend(os.popen('ls -1 /dev/ttyACM* 2> /dev/null').readlines())
        
        for k in range(len(sources)):
            sources[k] = sources[k].replace("\n","")
        
        k=0
        while k < len(sources):
            try:
                instanceSerie = Serial(sources[k], Imprimante.baudrate, timeout=0.1)
                
                #vide le buffer série coté pc
                instanceSerie.flushInput()
                
                #vide le buffer de l'avr
                instanceSerie.write(bytes(" \r","utf-8"))
                instanceSerie.readline()
                
                #envoi d'une demande d'identifiant (ping)
                instanceSerie.write(bytes("?\r","utf-8"))
                #évacuation de l'acquittement
                instanceSerie.readline()
                #réception de l'id de la carte
                rep = self._clean_string(str(instanceSerie.readline(),"utf-8"))
                
                #lecture de l'identifiant
                if rep == Imprimante.ping:
                    print("imprimante trouvée sur "+sources[k])
                    self.serie = instanceSerie
                    break
                else:
                    #fermeture du périphérique
                    instanceSerie.close()
            except Exception as e:
                print("exception durant la détection des périphériques série: {0}".format(e))
            k += 1
                    
        if not self.serie:
            print("imprimante non trouvée !")
        time.sleep(1)
        self.prete = True
        
    def _clean_string(self, chaine):
        """
        supprime des caractères spéciaux sur la chaine
        """
        return chaine.replace("\n","").replace("\r","").replace("\0","")         
        
    def communiquer(self, messages, nb_lignes_reponse):
        """
        Méthode de communication via la série.
        Envoie d'abord au destinataire une liste de trames au périphériques 
        (celles ci sont toutes acquittées une par une pour éviter le flood),
        puis récupère nb_lignes_reponse trames sous forme de liste.
        
        Une liste messages d'un seul élément : ["chaine"] peut éventuellement être remplacée par l'élément simple : "chaine".  #userFriendly
        """
        if not type(messages) is list:
            #permet l'envoi d'un seul message, sans structure de liste
            messages = [messages]
        
        #parcourt la liste des messages envoyés
        for message in messages:
            #print("message : >"+str(message)+"<")#DEBUG
            try:
                self.serie.write(bytes(str(message) + '\r',"utf-8"))
            except Exception as e:
                print(e)
                return None
                
            #chaque envoi est acquité par le destinataire, pour permettre d'émettre en continu sans flooder la série
            try:
                acquittement = ""
                while acquittement != "_":
                    acquittement = self._clean_string(str(self.serie.readline(),"utf-8"))
                    #print("\t acquittement de "+destinataire+" : >"+acquittement+"<")#DEBUG
                    
                    if acquittement == "":
                        #renvoi de la trame
                        self.serie.write(bytes(str(message) + '\r',"utf-8"))
                        
            except Exception as e:
                print(e)
                return None
                
        #liste des réponses
        reponses = []
        for i in range(nb_lignes_reponse):
            reponse = str(self.serie.readline(),"utf-8")
            #print("\t r>"+destinataire+reponse)
            reponses.append(self._clean_string(reponse))
        return reponses

    def serie_prete(self):
        return self.prete
    
#########################################################
###       TRAMES SPÉCIFIQUES À L'IMPRIMANTE           ###
#########################################################
     
    def initialise(self):
        """
        Définit la position courante du carton comme 0,
        alimente les moteurs des rouleaux pour asservir en position le carton,
        et recale le moteur pas à pas.
        """
        
        self.communiquer(["set_y",0.0],0)
        self.communiquer("asserv_on",0)
        self.communiquer("recal_x",0)
        
        #acquittement d'arrivée par l'imprimante (booléen dans le 1er élément de la liste)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)
            
    def recalage_x(self):
        """
        Recale le moteur pas à pas sur une butée pour palier aux glissements.
        """
        
        self.communiquer("recal_x",0)
        
        #acquittement d'arrivée par l'imprimante (booléen dans le 1er élément de la liste)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)
            
    def poinconne(self, x, y):
        """
        x correspond à une position atteinte par le moteur pas à pas (position du poinçon)
        y correspond à une position atteinte par les rouleaux (position du carton)
        L'imprimante s'y déplace, poinçonne, et rend la main au programme.
        """
        
        #envoi des consignes (n'attend pas de réponse)
        self.communiquer(["aller_a",x,y],0)
        
        #acquittement d'arrivée par l'imprimante (booléen dans le 1er élément de la liste)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)
            
        #ordre de poinçonnage (l'attente se fait grâce à une trame renvoyée en fin de poinçonnage)
        self.communiquer("poinconne",1)
        
    def lit_pistes(self):
        """
        Renvoit une liste des id des trous lus à la position courante.
        Renvoit [] si aucun trou détecté.
        """
        
        #lit les pistes et renvoit le nombre de trous
        nb_trous = int(self.communiquer("lecture",1)[0])
        
        if nb_trous:
            #récupère les id des trous et retourne la liste d'entiers
            liste_id = list(map(lambda x: int(x), self.communiquer("get_ids",nb_trous)))
            return liste_id
        else:
            return []
    
    def sortir_carton(self):
        """
        Evacue le carton de l'imprimante en fin d'impression.
        """
        
        self.communiquer("sortir",0)
