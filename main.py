
import face_landmark

def main():
    face = face_landmark.FaceMark()
    # Se toma la posición inicial, la referencia es el punto 4
    pos_inicial = face.FaceLandMark(True)
    Juego = face.FaceLandMark(coordenadasIniciales=pos_inicial)

main()
