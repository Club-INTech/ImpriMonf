class ControlZ :
    def __init__(self) :
        self.actions = []
        self.control = 0

    def annuler(self) :
        if self.control > 0 :
            self.control -= 1
            self.actions[self.control].annuler()
            return self.control > 0

    def refaire(self) :
        if self.control < len(self.actions) :
            self.actions[self.control].refaire()
            self.control += 1
            return self.control < len(self.actions)

    def addAction(self, action) :
        if self.control == len(self.actions) :
            self.actions.append(action)
            self.control += 1
        else :
            del self.actions[self.control:]
            self.actions.append(action)
            self.control += 1

class Action :
    def __init__(self, objet, properties, valeurs_initiales, valeurs_finales) :
        """
        Les attributs à rentrer doivent être des TABLEAUX
        """
        self.objet = objet
        self.properties = properties
        self.valeurs_initiales = valeurs_initiales
        self.valeurs_finales = valeurs_finales

    def annuler(self) :
        for id, p in enumerate(self.properties) :
            self.objet.__setattr__(p, self.valeurs_initiales[id])

    def refaire(self) :
        for id, p in enumerate(self.properties) :
            self.objet.__setattr__(p, self.valeurs_finales[id])

