  # Importamos librerías para Vision
import cv2
import numpy as np
  # Importamos librería para comunicación Serial
import serial 
  # Esta librería se ocupa para poder utilizar el retardo
from time import sleep
  # Inicializamos Puerto Serie
#ser=serial.Serial('COM6',baudrate = 9600, timeout = 10 , parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
  # Abrimos la cámara de la computadora
cap = cv2.VideoCapture(0)

  # Creamos vectores para almacenar tonos de azul
A_1 = np.array([110,100,20],np.uint8)  # El primer valor del vector es tinte
A_2 = np.array([120,255,255],np.uint8) # El segundo valor es la saturación y el tercero es el brillo

  # Inicializamos ciclo mientras sea verdadero
while True:
    # Se crean dos variables, ret para el ciclo siguiente y frame para la captura de video
  ret,frame = cap.read()
    # Mientras ret este activo seguirá el siguiente ciclo
  if ret == True:
    frame=cv2.flip(frame,1)  # Reflejamos la imagen en modo espejo
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  # Convertimos de BGR a HSV
    mascara = cv2.inRange(frameHSV,A_1,A_2)  # Se crea una mascara dentro del rango de los dos azules   
    contornos,hierarchy  = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Encontramos contornos de acuerdo a la mascara
      # Ciclo para hacer recorrido de los contornos
    for c in contornos:
      area = cv2.contourArea(c)  # Encotrar el área de cada contorno
      if area > 6000:  # Definimos los contornos dentro de una cierta área
        Momentos = cv2.moments(c)  # Momentos para calcular el centroide
        if (Momentos["m00"]==0):   # Condicional 
            Momentos["m00"]=1  #  Intercambiamos los valores del moemnto a 1 para siguiente división
          # Obtenemos coordenadas del centroide en X, Y
        x = int(Momentos["m10"]/Momentos["m00"])
        y = int(Momentos['m01']/Momentos['m00'])
        nuevoContorno = cv2.convexHull(c)  # Dibujamos contorno de cualquier área
        cv2.circle(frame,(x,y),7,(0,0,255),-1)  # Dibujamos una circulo en el centro de contorno
        font = cv2.FONT_HERSHEY_SIMPLEX  # Se declara una fuente para la escritura de te posición
        cv2.putText(frame,'{},{}'.format(x,y),(x+10,y), font , 0.75,(0,255,0),1,cv2.LINE_AA) # Escritura de coordenadas
        cv2.drawContours(frame, [nuevoContorno], 0,  [255,0,0], 3)  # Se dibija el nuevo contorno
        

          # Conforme a la división de nuestra pantalla entramos a las siguientes condiciones
          # Para las coordenadas en X
        if x <120:
          print("Mover a la izquierda") # Imprime hacia qué dirección se moverá el robot
          ser.write(bytearray("a","ascii"))  # Enviamos nuestro dato por el puerto serial para el movimiento
          sleep(0.0001)  # Retraso para no enviar datos de manera continua
        elif 240>x>=120:
          print("Mover a la izquierda")
          ser.write(bytearray("b","ascii"))
          sleep(0.0001)

        elif 240<=x<380:
          print("Mover a la centro")
          ser.write(bytearray("c","ascii"))
          sleep(0.0001)

        elif 380<=x<500:
          print("Mover a la derecha")
          ser.write(bytearray("d","ascii"))
          sleep(0.0001)

        elif x>=500:
          print("Mover a la derecha")
          ser.write(bytearray("e","ascii"))
          sleep(0.0001)
        
          # Para las coordenas en Y
        if y <100:
          print("Mover a la arriba")
          ser.write(bytearray("f","ascii"))
          sleep(0.0001)

        elif 200>y>=100:
          print("Mover a la arriba")
          ser.write(bytearray("g","ascii"))
          sleep(0.0001)

        elif 200<=y<300:
          print("Mover a la centro")
          ser.write(bytearray("h","ascii"))
          sleep(0.0001)

        elif 300<=y<400:
          print("Mover a la abajo")
          ser.write(bytearray("i","ascii"))
          sleep(0.0001)

        elif y>=400:
          print("Mover a la abajo")
          ser.write(bytearray("j","ascii"))
          sleep(0.0001)

      # Mostramos lo que está capturando la pantalla 
    cv2.imshow('Seguidor',frame)
      # Condicionamos la tecla "s" de salida para romper el bucle
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # Cerramos el puerto serie
      #ser.close()
      break
  # Realizamos el cierre de nuestra captura
cap.release()
cv2.destroyAllWindows()