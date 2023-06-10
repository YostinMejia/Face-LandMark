import random

class Jugador():

    def __init__(self, posicionX, posicionY) -> None:
        self.Nombre = "jugador"
        self.Inventario= []
        self.Vida = 100
        self.PosicionX = posicionX
        self.PosicionY = posicionY
    
    def __repr__(self) -> str:
        return "🧓🏼"
    
    def MostrarInventario(self, inventario=None,solo_mostrar =False,opcion=None)->int|object:
        
        if inventario==None or solo_mostrar:
            # Si solo se quiere mirar el inventario y no seleccionar ninguna opcion
            if not solo_mostrar:
                inventario = self.Inventario
            # Muestra todos los objetos sel inventario enviado como parametro
            pos=0
            for i in inventario:
                print(f"{pos+1})",i.Inspeccionar())
                pos+=1
            return self.Inventario
        try:
            return inventario[opcion-1]
        except:
            return 0


    def Comer(self, opcion=None,mostrar_sub_opciones=False)->None:

        # Se buscan todos los objetos de tipo comida en el inventario
        Comida = list(filter(lambda x: x.TipoObjeto == "comida", self.Inventario))
         
        if mostrar_sub_opciones:
            # Si solo se quiere mirar el inventario y no seleccionar ninguna opcion
            # Muestra todos los objetos sel inventario enviado como parametro
            self.MostrarInventario(Comida,True)

            return
        
        # Se muestran los objetos listados
        Objeto = self.MostrarInventario(Comida,opcion = opcion)
        # Se suma la vida que da el objeto
        if Objeto != 0:
            self.Vida += Objeto.Interactuar()
            print("La vida actual es de:", self.Vida)
            #Se elimina la comida del inventario
            self.Inventario.remove(Objeto)
        
    
    def AgregarObjeto(self, objeto):
        self.Inventario.append(objeto)

    # Retorna daño si está en el rango para golpear al monstruo
    def Atacar(self, monstruoPosX,monstruoPosY, opcion=None, mostrar_sub_opciones = False):
        # Se buscan todos los objetos de tipo arma en el inventario
        Armas = list(filter(lambda x: x.TipoObjeto =="arma", self.Inventario))

        if mostrar_sub_opciones:
            # Se buscan todos los objetos de tipo arma en el inventario
            self.MostrarInventario(Armas,True)
            if len(Armas)==0:
                print ("No tiene armas ")
                return 0 
            return
            
        Objeto = self.MostrarInventario(Armas,opcion = opcion)
        if Objeto != 0:
            # Si es una chancla le da desde donde sea
            if (Objeto.Nombre == "chancla"):
                return Objeto.Interactuar()
            
            #Se mira si el arma tiene rango sufiente para golpear al monstruo
            # Para golpear al monstruo
            
            #  Derecha e izquierda
            if (self.PosicionX == monstruoPosX   and (self.PosicionX + Objeto.Rango >= monstruoPosX or self.PosicionX - Objeto.Rango <= monstruoPosX  ) ):
                return Objeto.Interactuar()
    
            # Arriba y abajo
            elif (self.PosicionY == monstruoPosY and (self.PosicionY + Objeto.Rango >= monstruoPosY or self.PosicionY - Objeto.Rango <= monstruoPosY  ) ):
               return Objeto.Interactuar()
            
        # Si no tiene suficiente daño el monstruo no sufre daño
        return 0


    def Atacado(self, Damage):
        self.Vida -= Damage
        if (self.Vida<=0):
            print("Muere El jugador")
            print("Me las va a pagar en la otra vida","\n")
        else:
            print("uy me la pego monstruo care mondá")
            print("La vida actual del jugador es:", self.Vida,"\n")
        

    def Moverse(self, Matriz:list, opcion=None,mostrar_opciones = False):
        
        if mostrar_opciones :
            print("Hacia donde desea moverse \n1)Arriba\n2)Derecha\n3)Abajo\n4)Izquierda\n5)Quedarse quieto ")
            return
       
        error = "movimiento invalido"

        movimientoX=0
        movimientoY=0
        # Arriba
        if opcion == 1: 
            movimientoX-=1 
        # Derecha
        elif opcion == 2: 
            movimientoY+=1
        # Abajo
        elif opcion == 3: 
            movimientoX+=1 
        # Izquierda
        elif opcion == 4: 
            movimientoY-=1 
        else: 
            print("el jugador se quedo quieto")
            return 
    
        # Si el movimiento se pasa del limite de la matriz
        if (self.PosicionX+movimientoX >= len(Matriz) or self.PosicionY+movimientoY >= len(Matriz)  or (self.PosicionX+movimientoX < 0 or self.PosicionY+movimientoY < 0)):
                return error
        
        # Si cae en un tipo objeto
       
        elif (Matriz[self.PosicionX+movimientoX][self.PosicionY+movimientoY] != 0):

            if (Matriz[self.PosicionX+movimientoX][self.PosicionY+movimientoY].Nombre == "monstruo"):
                return "Quiere pisar el monstruo o q?"

            
            # Si el Objeto es un arma o comida se agrega al inventario
            else:

                # Agrega el objeto al inventario 
                self.AgregarObjeto(Matriz[self.PosicionX+movimientoX][self.PosicionY+movimientoY])

            

        # Si se puede realizar el moviento 

        Matriz [self.PosicionX +movimientoX][self.PosicionY + +movimientoY] = self

        Matriz[self.PosicionX][self.PosicionY] = 0

        self.PosicionX +=movimientoX
        self.PosicionY +=movimientoY
    
           
