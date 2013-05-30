from serial import Serial
import os
import time

class Imprimante:
    """
    Classe implÃ©mentant une communication sÃ©rie avec l'imprimante.
    Elle permet d'envoyer une trame sur un pÃ©riphÃ©rique et d'en recevoir une en retour.
    """

    #constantes de classe pour la liaison sÃ©rie
    baudrate = 9600
    ping = '#'
    newLine = "\n"

    #Ã©cart entre le recalage du bloc moteur et l'origine 0 (en mm)
    origine = 5.2

    def __init__(self):

        #pÃ©riphÃ©rique sÃ©rie de l'imprimante (une fois la carte trouvÃ©e)
        self.serie = None

        #les threads attendent la serie
        self.prete = False

        #recherche du port sÃ©rie
        self.attribuer()

        #sauvegarde des coordonnÃ©es
        self.x = 0 #position atteinte par le moteur pas Ã  pas (position du poinÃ§on)
        self.y = 0 #position atteinte par les rouleaux (position du carton)

    def attribuer(self):
        """
        Cette mÃ©thode invoquÃ©e au lancement du service sÃ©rie permet de dÃ©tecter et stocker le chemin pour communiquer avec la carte.
        """

        #liste les pÃ©riphÃ©riques prÃ©sents sur les ports COM
        sources = []
        for location in ["com"+str(i) for i in range(22)]:
            try:
                serialport = Serial(location, 9600, timeout = 0)
                sources.append(location)
                serialport.close()
            except Exception as e:
                #aucun pÃ©riphÃ©rique
                pass

        #pÃ©riphÃ©riques usb : en gÃ©nÃ©ral en fin de liste, donc on gagne du temps
        sources.reverse()

        for source in sources:
            try:
                instanceSerie = Serial(source, Imprimante.baudrate, timeout=0.1)

                #vide le buffer sÃ©rie cotÃ© pc
                instanceSerie.flushInput()

                #initialisation de l'arduino (quit recoit un reset Ã  l'instanciation de la sÃ©rie)
                time.sleep(2)

                #Ã©vacuation du message de fin d'initialisation (gardÃ© pour le debug)
                instanceSerie.readline()

                #envoi d'une demande d'identifiant (ping)
                instanceSerie.write(bytes("?"+Imprimante.newLine,"utf-8"))

                #Ã©vacuation de la trame d'acquittement
                instanceSerie.readline()

                #rÃ©ception de l'id de la carte
                rep = self._clean_string(str(instanceSerie.readline(),"utf-8"))

                #lecture de l'identifiant
                if rep == Imprimante.ping:
                    print("imprimante trouvÃ©e sur "+source)
                    self.serie = instanceSerie
                    break
                else:
                    #fermeture du pÃ©riphÃ©rique
                    instanceSerie.close()
            except Exception as e:
                print("exception durant la dÃ©tection des pÃ©riphÃ©riques sÃ©rie: {0}".format(e))

        if not self.serie:
            raise Exception("Imprimante non trouvÃ©e ! Est-elle bien branchÃ©e ?")
        self.prete = True

    def _clean_string(self, chaine):
        """
        supprime des caractÃ¨res spÃ©ciaux sur la chaine
        """
        return chaine.replace("\n","").replace("\r","").replace("\0","")

    def communiquer(self, messages, nb_lignes_reponse):
        """
        MÃ©thode de communication via la sÃ©rie.
        Envoie d'abord au destinataire une liste de trames au pÃ©riphÃ©riques
        (celles ci sont toutes acquittÃ©es une par une pour Ã©viter le flood),
        puis rÃ©cupÃ¨re nb_lignes_reponse trames sous forme de liste.

        Une liste messages d'un seul Ã©lÃ©ment : ["chaine"] peut Ã©ventuellement Ãªtre remplacÃ©e par l'Ã©lÃ©ment simple : "chaine".  #userFriendly
        """
        if not type(messages) is list:
            #permet l'envoi d'un seul message, sans structure de liste
            messages = [messages]

        #parcourt la liste des messages envoyÃ©s
        for message in messages:
            #print("message : >"+str(message)+"<")#DEBUG
            try:
                self.serie.write(bytes(str(message) + Imprimante.newLine,"utf-8"))
            except Exception as e:
                print("Exception levÃ©e lors de l'envoi de la trame : "+e)
                return None

            #chaque envoi est acquitÃ© par le destinataire, pour permettre d'Ã©mettre en continu sans flooder la sÃ©rie
            try:
                acquittement = ""
                while acquittement != "_":
                    acquittement = self._clean_string(str(self.serie.readline(),"utf-8"))
                    #print("\t acquittement de "+destinataire+" : >"+acquittement+"<")#DEBUG

                    if acquittement == "":
                        #renvoi de la trame
                        self.serie.write(bytes(str(message) + Imprimante.newLine,"utf-8"))

            except Exception as e:
                print("Exception levÃ©e lors de l'acquittement : "+e)
                return None

        #liste des rÃ©ponses
        reponses = []
        for i in range(nb_lignes_reponse):
            reponse = "_"
            while reponse == "_":
                reponse = self._clean_string(str(self.serie.readline(),"utf-8"))
                #print("\t r>"+destinataire+reponse)
            reponses.append(reponse)
        return reponses

    def serie_prete(self):
        return self.prete

#########################################################
###       TRAMES SPÃ‰CIFIQUES Ã€ L'IMPRIMANTE           ###
#########################################################

    def _pap_aller_a(self, position):
        self.communiquer(["go_pap",position*1000],0)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)
        self.x = position

    def initialise(self):
        """
        DÃ©finit la position courante du carton comme 0,
        et alimente les moteurs des rouleaux pour asservir en position le carton.
        """

        self.communiquer(["set_mot",0],0)
        self.y = 0
        self.communiquer("asserv_on",0)

    def recalage_x(self):
        """
        Recale le moteur pas Ã  pas sur une butÃ©e pour palier aux glissements.
        """

        self._pap_aller_a(-20)
        self.communiquer("reset_pap",0)
        self._pap_aller_a(Imprimante.origine)
        self.communiquer("reset_pap",0)
        self.x = 0

    def poinconne(self, x, y):
        """
        x correspond Ã  une position atteinte par le moteur pas Ã  pas (position du poinÃ§on)
        y correspond Ã  une position atteinte par les rouleaux (position du carton)
        L'imprimante s'y dÃ©place, poinÃ§onne, et rend la main au programme.
        Les coordonnÃ©es sont indiquÃ©es en mm (avec ou sans virgule) et sont envoyÃ©es en microns entiers.
        """

        #envoi des consignes (n'attend pas de rÃ©ponse)
        self.communiquer(["aller_a", int(1000*x), int(1000*y)],0)

        #acquittement d'arrivÃ©e par l'imprimante (boolÃ©en dans le 1er Ã©lÃ©ment de la liste)
        while not int(self.communiquer("acq?",1)[0]):
            time.sleep(0.1)

        self.x = x
        self.y = y

        #ordre de poinÃ§onnage (l'attente se fait grÃ¢ce Ã  une trame renvoyÃ©e en fin de poinÃ§onnage)
        self.communiquer("poinconne",1)

    #TODO
    def lit_pistes(self):
        """
        Renvoit une liste des id des trous lus Ã  la position courante.
        Renvoit [] si aucun trou dÃ©tectÃ©.
        """

        #lit les pistes et renvoit le nombre de trous
        nb_trous = int(self.communiquer("lecture",1)[0])

        if nb_trous:
            #rÃ©cupÃ¨re les id des trous et retourne la liste d'entiers
            liste_id = list(map(lambda x: int(x), self.communiquer("get_ids",nb_trous)))
            return liste_id
        else:
            return []

    def debut_rentrer_poincon(self):
        """
        DÃ©cale le bloc poinÃ§onneur vers la gauche.
        Doit etre stoppÃ© par l'utilisateur.
        """

        self.communiquer(["go_pap",-999999999],0)

    def fin_rentrer_poincon(self):
        """
        Stoppe le moteur lorsque l'utilisateur a vÃ©rifiÃ© la butÃ©e du bloc poinÃ§onneur.
        """

        self.communiquer("reset_pap",0)
        self._pap_aller_a(Imprimante.origine)
        self.communiquer("reset_pap",0)
        self.x = 0

    def debut_sortir_carton(self):
        """
        Evacue le carton de l'imprimante en fin d'impression.
        Doit etre stoppÃ© par l'utilisateur.
        """

        self.communiquer(["go_mot",999999999],0)

    def fin_sortir_carton(self):
        """
        Stoppe le moteur lorsque l'utilisateur a vÃ©rifiÃ© la sortie du carton.
        """

        self.communiquer(["set_mot",0],0)
        self.communiquer("asserv_off",0)