
import cv2
import mediapipe as mp
import numpy as np

import juego


class FaceMark():   

    def __init__(self) -> None:
        self.numero_opcion = 1
        self.primera_opcion = 1
        self.seleccion = 1
        self.confirmar = 0
        self.inicio_juego = False
        self.Opcion = False

        
    def FaceLandMark(self, posicionInicial=False, coordenadasIniciales=False):
        
        mp_face_mesh = mp.solutions.face_mesh
        mp_drawing = mp.solutions.drawing_utils

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # Opciones que se le da al detectar
        with mp_face_mesh.FaceMesh(
        
            # Determina si la imagen es estatica
            static_image_mode=False,
            # Máximo número de caras que va a detectar
            max_num_faces=1,

            min_detection_confidence=0.5) as face_mesh:

                while True:

                    # Lee la imagen 
                    ret, frame = cap.read()

                    # Tamaño de la imagen
                    height,width,_ = frame.shape 
                    
                    # Si no hay imagen termina el ciclo
                    if ret == False:
                        break

                    frame = cv2.flip(frame,1)
                    # cv2 lee los colores por defecto se leen en BGR se deben cambiar a RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    # El resultado al cambiar los colores de la imagen a RGB
                    # Retorna un objeto
                    results = face_mesh.process(frame_rgb)

                    # Se miran los 468 puntos de referecia encontrados por el face landmark 
                    if results.multi_face_landmarks:
                        # Se mira la posicón de cada punto
                        for face_landmarks in results.multi_face_landmarks:

                            mp_drawing.draw_landmarks(frame, face_landmarks,
                                mp_face_mesh.FACEMESH_CONTOURS,
                                mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1),
                                mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1))
                            

                        if coordenadasIniciales:

                            # Punto que se va a tomar como referencia para determinar la dirección del movivmiento de la cabeza
                            self.PuntoInicial(frame,int(coordenadasIniciales[0]),int(coordenadasIniciales[1]))
                            
                            #si mueve la cabeza hacia la derecha o izquierda
                            self.movimiento_lateral= self.movimiento_derecha_izquierda(frame, 4, coordenadasIniciales[0],width,results.multi_face_landmarks[0])

                            # Si se determina que se mueve en hacia arriba suma , hacia abajo resta
                            self.numero_opcion+= self.movimiento_arriba_abajo(frame, 4, coordenadasIniciales[0],coordenadasIniciales[1],height,results.multi_face_landmarks[0],width)
                            
                            # Muestra el punto de referencia donde el jugador debe de posicionar nuevamente la cabeza 
                            # Se controla que no baje mas de 0 y se dibuja en la pantalla el número de la opción 
                            self.dibujar_numero_opcion(frame)

                            # Si abre la boca se suma el contador y cuando llegue a 6 se cuenta como una confirmación para enviar el número de opción
                            self.confirmar += self.abrir_boca(results.multi_face_landmarks[0],frame,height,width)


                            # Si aún no se ha iniciado el juego 
                            if not self.inicio_juego :
                                cv2.putText(frame,f"Abra la boca para iniciar",(100,90),1,2,(255,255,255),2)
                                if self.confirmar > 6:
                                    self.numero_opcion = round(self.numero_opcion)
                                    game = self.iniciar_juego(self.numero_opcion)
                                    print(self.numero_opcion)
                                    # game.min_size()
                                    self.confirmar = 0
                                    self.numero_opcion = 0
                                    
                            else:
                                # Se envia las opciones q se ahn seleccionado
                                self.confirmar_opcion(game)
                            
                        # Si se va a determinar la posicion en x, y de la cara del jugador
                        else:

                            cv2.putText(frame,"Posicione su cara y luego presione esc o enter para continuar",(0,30),1,1,(255,255,255),1)
                            cv2.putText(frame,"el punto coloreado verde es el punto de referencia para determinar ",(0,45),1,1,(255,255,255),1)
                            cv2.putText(frame,"la dirección de sus movimientos para determinar la direccion de sus movimientos",(0,60),1,1,(255,255,255),1)
                            #Se toma como referencia el punto #4
                            x = results.multi_face_landmarks[0].landmark[4].x * width
                            y= results.multi_face_landmarks[0].landmark[4].y * height
                            cv2.circle(frame,(int(x),int(y)),2,(77, 243, 10),2)
                            if self.abrir_boca(results.multi_face_landmarks[0],frame,height,width):
                                return (x,y,)


                    # Se muestra la imagen/video
                    cv2.imshow("Frame", frame)
                    
                    # Si ya se inicio el juego y la vida del jugador o del mosntruo son menores o iguales que cero
                    # Se termina el flujo
                    if self.inicio_juego:
                        if game.Jugador.Vida <= 0 or game.Monstruo.Vida <= 0:
                                break
                    
                    # Si pulsa las teclas designadas para finalizar 
                    if self.Finalizar(cv2.waitKey(22)) :
                        break

                cap.release()
                cv2.destroyAllWindows()  

    
    def Finalizar(self, key):
        return key == 13 or key == 27
    
    def PuntoInicial(self,frame,x,y):
        cv2.circle(frame,(x,y),2,(255,0,6),2)
    
    def dibujar_tipo_movimiento(self, frame, nombre):
        cv2.putText(frame,nombre,(300,30),1,2,(255,255,255),2)


    def dibujar_numero_opcion(self,frame):
        # Va mirando el número de la opción
        if self.numero_opcion <= 0:
            self.numero_opcion = 1

        cv2.putText(frame,f"Opcion #",(15,35),1,2,(255,255,255),2)
        cv2.rectangle(frame,(55,55),(105,105),(125,220,0),-1)
        cv2.putText(frame,f"{round(self.numero_opcion)}",(70,90),1,2,(255,255,255),2)

    def confirmar_opcion(self, game:juego.Juego):

        # Se usa el número 6 para controlar que se active despues de un tiempo
        # Ya que los frames se reproducen muy rápido no encontre la frorma de que sea solo una función de true o false
        if self.confirmar>6:

            self.confirmar = 0
            
            # Ya que se suman decimales se debe redondear el número
            self.numero_opcion = round(self.numero_opcion)
            
            # Si aún no ha hecho la elección de la primera opción a realizar
            # El número de opción escogido se va para la opción
            if self.numero_opcion !=0 or self.numero_opcion<=4:

                game.MostrarJuego()

                # Si aun no se ha escogido la primera acción
                if not self.Opcion :

                    # Se le asigna el número que va sumando con el movivmiento de la cabeza
                    self.primera_opcion = self.numero_opcion

                    print(self.numero_opcion)

                    # Se envia como parametro la primera opción y con mostrar_sub_opciones no ejecuta ninguna 
                    # función que altere el juego, solo muestra las acciones disponibles con esa primera opción
                    game.Opciones(self.primera_opcion,mostrar_sub_opciones=True)
                    
                    # Si la opción es uno, ahora necesita un segundo número para la dirección del movimiento
                    # Por lo que se pone Opcion True para dar paso a la siguiente opción 
                    if self.numero_opcion == 1:
                        self.Opcion = True
                    elif self.numero_opcion == 4 :
                        game.Menu()
                    elif self.numero_opcion == 3 or self.numero_opcion == 2:
                        
                        if self.numero_opcion == 3: 
                            busqueda = "comida"
                        else:
                            busqueda = "arma"
                        
                        inventario_jugador = list(filter(lambda x: x.TipoObjeto == busqueda, game.Jugador.Inventario))
                        # Si no hay objetos de la acción q se quiere realizar vuelve a buscar otra opción 
                        # y se muestra el inventario
                        if  len(inventario_jugador) == 0:
                            print("No tiene objetos de tipo",busqueda)
                            game.Menu()

                        # Necesita otro número dependiendo de si tiene de ese objeto o no para seleccionar
                        self.Opcion = len(inventario_jugador) != 0
           
                # Si ya escogio la opción el número que ahora estaría escogiendo 
                # la seleccion dentro de la primera opción
                else:
                    self.seleccion = self.numero_opcion
                    # Se envia la primera opción y la seleccion dentro de la primera opción
                    game.Opciones(self.primera_opcion,self.seleccion)                                            
                    # Se vuelve a activar la elección de la primera opción
                    self.Opcion = False
                    # Se reinician los contadores
                    self.primera_opcion=1
                    self.seleccion = 1

                    game.Menu()
                
                self.numero_opcion =1

            else:
                print(f"el {self.numero_opcion} no es una opción válida ")

    # Se toman los puntos 14 labio inferior, 13 labio superior
    def abrir_boca(self,lista_landmark,frame,height, width):
        x = int(lista_landmark.landmark[13].x *width)
        y = int(lista_landmark.landmark[13].y *height)


        # Segundo punto 
        x2 = int(lista_landmark.landmark[14].x *width)
        y2 = int(lista_landmark.landmark[14].y *height)
        if self.calcular_distancia(x,y,x2,y2,frame) > 20:
            return 0.5

        return 0
    
    def iniciar_juego(self, nxn):

        ListArmas = [juego.Arma(30,9999,"chancla","👞"),juego.Arma(3,1,"palo","🏏")]
        ListComidas = [ juego.Comida(30,"fresa","🍓"), juego.Comida(-10,"changua","🍽")]

        game = juego.Juego(ListArmas,ListComidas)
    
        if nxn >= game.min_size():
            game.Iniciar(nxn)  
            self.inicio_juego = True
            
        return game

    def movimiento_arriba_abajo(self,frame,punto_referencia,posicion_inicial_x,posicion_inicial_y,height,lista_landmark, width):

        posicion_actual_x = lista_landmark.landmark[4].x * width
        posicion_actual_y = lista_landmark.landmark[4].y * height

        
        cv2.line(frame,(int(posicion_inicial_x),int(posicion_inicial_y)),(int(posicion_actual_x),int(posicion_actual_y)),(100,0,6),2)
        cv2.circle(frame,(int(posicion_actual_x),int(posicion_actual_y)),2,(255,0,6),2)
        cv2.circle(frame,(int(posicion_inicial_x),int(posicion_inicial_y)),2,(255,0,6),2)

        posicion_actual_y = lista_landmark.landmark[punto_referencia].y * height
   
        if (posicion_inicial_y - posicion_actual_y > 30):
            self.dibujar_tipo_movimiento(frame,"Arriba")
            return 0.09
        elif (posicion_inicial_y - posicion_actual_y < -30):
            self.dibujar_tipo_movimiento(frame,"Abajo")
            return -0.09
        else:  
            return 0

    
    def movimiento_derecha_izquierda(self,frame,punto_referencia,posicion_inicial_x,width,lista_landmark):
        
        posicion_actual_x = lista_landmark.landmark[punto_referencia].x * width

        if (posicion_inicial_x - posicion_actual_x > 60):
            self.dibujar_tipo_movimiento(frame,"Izquierda")
            return -0.07
        elif (posicion_inicial_x - posicion_actual_x < -60):
            self.dibujar_tipo_movimiento(frame,"Derecha")
            return 0.07 
        else:
            return 0 



    def calcular_distancia(self,x1,y1, x2,y2,frame):
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        cv2.line(frame,(x1,y1),(x2,y2),(100,0,6),2)
        cv2.circle(frame,(x1,y1),2,(255,0,6),2)
        cv2.circle(frame,(x2,y2),2,(255,0,6),2)

        # Se convierten las posiciones en un array
        p1 = np.array([x1,y1])
        p2 = np.array([x2,y2])

        # Se restan para saber la distancia entre ambas posiciones
        return np.linalg.norm(p1-p2)
