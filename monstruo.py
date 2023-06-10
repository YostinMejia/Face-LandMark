import random

class Monstruo():

    def __init__(self) -> None:
        self.Vida = 100
        self.Damage = 25
        self.Nombre ="monstruo"
        self.PosicionX=0
        self.PosicionY =0

    def __repr__(self) -> str:
        return "👾"

    def Atacar(self):
        print("El monstruo ataca al jugador quitandole ",self.Damage,"de vida")
        return self.Damage


    def Moverse(self, Matriz:list, PrimeraVez=False):

        # Se mueve el monstruo 
        while True:
            # Se Cambia la posicion
            PosicionY = (random.randint(0,len(Matriz)-1))
            PosicionX =(random.randint(0,len(Matriz)-1))

            if Matriz[PosicionX][PosicionY] !=0 and not PrimeraVez:
                # Si es un objeto mira si es un jugador y lo ataca 
                try:
                    if Matriz[PosicionX][PosicionY].Nombre == "jugador":
                        Matriz[PosicionX][PosicionY].Atacado(self.Atacar())
                        break
                except:
                    pass

            # Si en la posicion no hay un objeto
            else:

                # Si es la primera vez no hay que eliminar ningún monstruo de la matriz
                if(not PrimeraVez):
                    Matriz[self.PosicionX][self.PosicionY] = 0

                Matriz[PosicionX][PosicionY] = self

                self.PosicionX = PosicionX
                self.PosicionY = PosicionY
            
                break


    def Atacado(self, damage):
        self.Vida -=damage
        if (damage>0):

            print("Ahhhhhhh me hirio care mondá")
            print(f"Al monstruo le queda {self.Vida} de vida")
            if self.Vida<=0:

                print("Nos vemos en la proxima vida.........")

        else:
            print("jajajja malo falló el disparo","\n")

