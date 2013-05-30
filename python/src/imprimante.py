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
    newLine = "\n"
    
    def __init__(self):
        
        #périphérique série de l'imprimante (une fois la carte trouvée)
        self.serie = None
        
        #les threads attendent la serie
        self.prete = False
        
        #recherche du port série
        self.attribuer()
        
    def attribuer(self):
        """
        Cette méthode invoquée au lancement du service série permet de détecter et stocker le chemin pour communiquer avec la carte.
        """
        
        #liste les périphériques présents sur les ports COM
        sources = []
        for location in ["com"+str(i) for i in range(22)]:
            try:
                serialport = Serial(location, 9600, timeout = 0)
                sources.append(location)
                serialport.close()
            except Exception as e:
                #aucun périphérique
                pass
                
        #périphériques usb : en général en fin de liste, donc on gagne du temps
        sources.reverse()
        
        for source in sources:
            try:
                instanceSerie = Serial(source, Imprimante.baudrate, timeout=0.1)
                
                #vide le buffer série coté pc
                instanceSerie.flushInput()
                
                #initialisation de l'arduino (quit recoit un reset à l'instanciation de la série)
                time.sleep(2)
                
                #évacuation du message de fin d'initialisation (gardé pour le debug)
                instanceSerie.readline()
        
                #envoi d'une demande d'identifiant (ping)
                instanceSerie.write(bytes("?"+Imprimante.newLine,"utf-8"))
                
                #évacuation de la trame d'acquittement
                instanceSerie.readline()
                
                #réception de l'id de la carte
                rep = self._clean_string(str(instanceSerie.readline(),"utf-8"))
                
                #lecture de l'identifiant
                if rep == Imprimante.ping:
                    print("imprimante trouvée sur "+source)
                    self.serie = instanceSerie
                    break
                else:
                    #fermeture du périphérique
                    instanceSerie.close()
            except Exception as e:
                print("exception durant la détection des périphériques série: {0}".format(e))
                    
        if not self.serie:
            raise Exception("Imprimante non trouvée ! Est-elle bien branchée ?")
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
                self.serie.write(bytes(str(message) + Imprimante.newLine,"utf-8"))
            except Exception as e:
                print("Exception levée lors de l'envoi de la trame : "+e)
                return None
                
            #chaque envoi est acquité par le destinataire, pour permettre d'émettre en continu sans flooder la série
            try:
                acquittement = ""
                while acquittement != "_":
                    acquittement = self._clean_string(str(self.serie.readline(),"utf-8"))
                    #print("\t acquittement de "+destinataire+" : >"+acquittement+"<")#DEBUG
                    
                    if acquittement == "":
                        #renvoi de la trame
                        self.serie.write(bytes(str(message) + Imprimante.newLine,"utf-8"))
                        
            except Exception as e:
                print("Exception levée lors de l'acquittement : "+e)
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
     
    def _pap_aller_a(self, position):
        self.communiquer(["go_pap",position*1000],0)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)
            
    def initialise(self):
        """
        Définit la position courante du carton comme 0,
        alimente les moteurs des rouleaux pour asservir en position le carton,
        et recale le moteur pas à pas.
        """
        
        self.communiquer(["set_mot",0],0)
        self.communiquer("asserv_on",0)
        self.recalage_x()
            
    def recalage_x(self):
        """
        Recale le moteur pas à pas sur une butée pour palier aux glissements.
        """
        
        self._pap_aller_a(-20)
        self.communiquer("reset_pap",0)
        self._pap_aller_a(4.680)
        self.communiquer("reset_pap",0)
            
    def poinconne(self, x, y):
        """
        x correspond à une position atteinte par le moteur pas à pas (position du poinçon)
        y correspond à une position atteinte par les rouleaux (position du carton)
        L'imprimante s'y déplace, poinçonne, et rend la main au programme.
        Les coordonnées sont toutes deux en microns et envoyées avec un entier.
        """
        
        #envoi des consignes (n'attend pas de réponse)
        self.communiquer(["aller_a", int(1000*x), int(1000*y)],0)
        
        #acquittement d'arrivée par l'imprimante (booléen dans le 1er élément de la liste)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)
            
        #ordre de poinçonnage (l'attente se fait grâce à une trame renvoyée en fin de poinçonnage)
        self.communiquer("poinconne",1)
        
    #TODO
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
    
    def debut_sortir_carton(self):
        """
        Evacue le carton de l'imprimante en fin d'impression.
        """
        
        self.communiquer(["go_mot",999999999],0)
        
    def fin_sortir_carton(self):
        """
        Stoppe le moteur lorsque l'utilisateur a vérifié la sortie du carton.
        """
        
        self.communiquer(["set_mot",0],0)
        self.communiquer("asserv_off",0)