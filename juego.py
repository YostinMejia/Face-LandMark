from jugador import * 
from monstruo import *
from herramienta import *
import random

class Juego:
    def __init__(self, armas:list, comida:list ) -> None:
        self.Matriz = []
        self.Monstruo:Monstruo
        self.Jugador:Jugador 
        self.ArmasDisponibles=armas
        self.ComidaDisponibles=comida

    def MostrarJuego(self):
        for i in self.Matriz:
            print (i)

    
    def AgregarElemento(self, Comida=False, Arma=False):

        # Se mueve el monstruo 
        while True:
            # Se Cambia la posicion
            PosicionY = (random.randint(0,len(self.Matriz)-1))
            PosicionX =(random.randint(0,len(self.Matriz)-1))
                                 
            # Se corrobora si en la posicion no hay un objeto
            if self.Matriz[PosicionX][PosicionY] == 0:
                # Si es la primera vez no hay que eliminar ningún monstruo de la matriz
                
                if(Comida):
                    # Se selecciona aleatoriamente la posicion del elemento 
                    posicionObjeto = random.randint(0,len(self.ComidaDisponibles)-1)
                    # Se agrega el elemento a la matriz
                    self.Matriz[PosicionX][PosicionY] = self.ComidaDisponibles[posicionObjeto]
                    # Se elimina el objeto de la lista
                    self.ComidaDisponibles.pop(posicionObjeto)
                    
                elif Arma:
                    # Se selecciona aleatoriamente la posicion del elemento 
                    posicionObjeto = random.randint(0,len(self.ArmasDisponibles)-1)
                    # Se agrega el elemento a la matriz
                    self.Matriz[PosicionX][PosicionY] = self.ArmasDisponibles[posicionObjeto]
                    # Se elimina el objeto de la lista
                    self.ArmasDisponibles.pop(posicionObjeto)
                break
            

    def min_size(self):
        nxn = 0
        # Se mira cual es el tamaño mínimo de la matriz para poder poner la cantidad de comida y armas ingresadas
        for i in range(2,(len(self.ArmasDisponibles)+len(self.ComidaDisponibles)) +2):
            # Si hay sificientes cuadrados para ingresar las armas , la comida, el mosntruo y el jugador
            if i*i > (len(self.ArmasDisponibles)+len(self.ComidaDisponibles)) +2:
                nxn = i
                break
        print(f"El tamaño de la matriz debe ser igual o mayor a {nxn}")
        return nxn

    def Iniciar(self, nxn):
    
        self.Matriz = [[0]*nxn for x in range (nxn) ]

        # Se le da una posicion al jugador 
        n=len(self.Matriz)-1
        self.Jugador = Jugador(random.randint(0,n,), random.randint(0,n))
        
        self.Matriz[self.Jugador.PosicionX][self.Jugador.PosicionY] = self.Jugador
        
        # Se posiciona el monstruo 
        self.Monstruo=Monstruo()
        self.Monstruo.Moverse(self.Matriz,True)
        


        while len(self.ArmasDisponibles) >0 or len(self.ComidaDisponibles) >0:
            
            if (len(self.ArmasDisponibles)>0):
                self.AgregarElemento(Arma=True)

            if (len(self.ComidaDisponibles)>0):
                self.AgregarElemento(Comida=True)

        self.MostrarJuego()
        self.Menu()

    def Menu(self):
        print("Suba la cabeza para aumentar el número de opción, bajela para disminuir el número de opción\nPara seleccionar el número de la opción abra la boca")
        print("Las opciones disponibles son:")
        print("\n1)Moverse\n2)Atacar\n3)Comer\n4)Inventario")

    def Opciones(self, accion, sub_opcion=None,mostrar_sub_opciones=False):  
        
        # Si se quiere solamente mostrar las sub_opciones pero no realizar ninguna accion ,
        #  mostrar_sub_opciones = true y no se toma en cuenta la sub opcion enviada            
        # accion = input("Ingrese el número de la acción que desea realizar:\n1)Moverse\n2)Atacar\n3)Comer\n4)Inventario\n-->")
        if accion == 1:
            print(self.Jugador.Moverse(self.Matriz, sub_opcion,mostrar_opciones=mostrar_sub_opciones))
        elif accion ==2:
            if mostrar_sub_opciones:
                self.Jugador.Atacar(self.Monstruo.PosicionX,self.Monstruo.PosicionY,sub_opcion,mostrar_sub_opciones)
            else:
                self.Monstruo.Atacado(self.Jugador.Atacar(self.Monstruo.PosicionX,self.Monstruo.PosicionY,sub_opcion))
        elif accion ==3 :
            self.Jugador.Comer(sub_opcion,mostrar_sub_opciones)
        elif accion == 4:
            print(self.Jugador.MostrarInventario())
        else:
            print("el jugador no hace nichi")
        # Se termina el flujo antes de que el monstruo realice algún movivmiento
        if mostrar_sub_opciones:
            return
        
        self.Monstruo.Moverse(self.Matriz)            
        self.MostrarJuego()
        print("------------------------------------------------------------")
        
