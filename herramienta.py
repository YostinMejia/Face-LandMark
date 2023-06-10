class IHerramienta():
    def __init__(self, nombre, tipoObjeto, img) -> None:
        self.Nombre = nombre
        self.TipoObjeto = tipoObjeto
        self.Img = img 
        
    def __repr__(self) -> str:
        return self.Img
    
    def Interactuar(self)->int:
        """Se define la forma en la que objeto va a influir con el jugador o juego"""

    def Inspeccionar(self)->str:
        """Muestra las caracteristicas del arma"""

class Comida(IHerramienta):
    def __init__(self,curacion,nombre, img) -> None:
        super().__init__(nombre,"comida", img)
        self.Curacion = curacion

    def Inspeccionar(self) -> str:
        
        return f"{super().__repr__()} Cura {self.Curacion} de vida"
        

    def Interactuar(self):
        return self.Curacion
    

class Arma(IHerramienta):
    def __init__(self, damage,rango,nombre, img) -> None:
        super().__init__(nombre,"arma", img)
        self.Damage = damage
        self.Rango = rango

    def Inspeccionar(self)->str:
         return f"{super().__repr__()} Daño {self.Damage},Golpea Arriba, Abajo, Derecha, Izquierda {self.Rango} Bloques"
         
         

    def Interactuar(self):
        return self.Damage
