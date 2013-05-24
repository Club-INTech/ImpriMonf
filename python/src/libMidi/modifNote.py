
class ModifNote :
    def __init__(self, note, type) :
        self.note = note
        self.type = type

    def isSizeModif(self) :
        # Retourne True si c'est une modif de taille de note
        if self.type == "BORNEIN" or self.type == "BORNEOUT" :
            return True
        return False

    def isPosModif(self) :
        # Retourne True si c'est une modif de position
        if self.type == "INSIDE" : return True
        else : return False

