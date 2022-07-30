  # Incluimos Librerías
import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib.widgets import Slider,Button
  # Creamos ventana para la graficación de nuestra simulación
fig,ax=plt.subplots()
ax=plt.axes(projection = "3d")

  #  Funcion rotacional en X 
def matriz_rotacion_x(grados):
	rad = grados/180*np.pi  # Convertimos los grados a radianes
	  # Matriz para rotación en X
	rotacion = np.array([[1    ,0          ,           0,0],
						[0    ,np.cos(rad), -np.sin(rad),0],
						[0    ,np.sin(rad),  np.cos(rad),0],
						[0    ,          0,            0,1]])
	return rotacion  # Retorna el valor obtenido de nuestra matriz
  #  Funcion rotacional en Y 
def matriz_rotacion_y(grados):
	rad = grados/180*np.pi 
	rotacion = np.array([[np.cos(rad), 0, -np.sin(rad),0],
						 [0,           1,            0,0],
						 [np.sin(rad), 0,  np.cos(rad),0],
						 [0,           0,            0,1]])
	return rotacion
  #  Funcion rotacional en Z
def matriz_rotacion_z(grados):
	rad = grados/180*np.pi
	rotacion = np.array([[np.cos(rad),-np.sin(rad),0,0],
						[np.sin(rad), np.cos(rad),0,0],
						[		   0,           0,1,0],
						[          0,           0,0,1]])
	return rotacion

  #  Funciones de traslación
def matriz_traslacion_X(x):
	  # Creamos la matriz de traslación 
	traslacion=np.array([[1,0,0,x],
						 [0,1,0,0],
						 [0,0,1,0],
						 [0,0,0,1]])
	return traslacion

def matriz_traslacion_Y(y):
	traslacion=np.array([[1,0,0,0],
						 [0,1,0,y],
						 [0,0,1,0],
						 [0,0,0,1]])
	return traslacion

def matriz_traslacion_Z(z):
	traslacion=np.array([[1,0,0,0],
						 [0,1,0,0],
						 [0,0,1,z],
						 [0,0,0,1]])
	return traslacion
  # Configuración de nuestra gráfica
def configuracion_grafica():
	plt.title("Brazo Robótico de 3 GDL", x=-4, y=-5)
	  # Límites para cada eje
	ax.set_xlim(-7,7)  
	ax.set_ylim(-7,7)
	ax.set_zlim(-7,7)
	  # Texto para los ejes 
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	ax.set_zlabel("z")
	ax.view_init(elev=25, azim=30)

  # Creamos la función que dibujará la posición de cada eslabon

def sistema_coordenada_movil(matriz_rotacion):
	r_11 = matriz_rotacion[0,0]
	r_12 = matriz_rotacion[1,0]
	r_13 = matriz_rotacion[2,0]
	r_21 = matriz_rotacion[0,1]
	r_22 = matriz_rotacion[1,1]
	r_23 = matriz_rotacion[2,1]
	r_31 = matriz_rotacion[0,2]
	r_32 = matriz_rotacion[1,2]
	r_33 = matriz_rotacion[2,2]
	dx= matriz_rotacion[0,3]
	dy= matriz_rotacion[1,3]
	dz= matriz_rotacion[2,3]

	ax.plot3D([dx,dx+r_11],[dy,dy+r_12],[dz,dz+r_13],color='m')
	ax.plot3D([dx,dx+r_21],[dy,dy+r_22],[dz,dz+r_23],color='c')
	ax.plot3D([dx,dx+r_31],[dy,dy+r_32],[dz,dz+r_33],color='y')
  
  # Función para obtener la matriz por medio de D-H 
def denavit_hatemberg(theta_i,d_i,a_i,alpha_i):
	MT = matriz_rotacion_z(theta_i)@matriz_traslacion_Z(d_i)@matriz_traslacion_X(a_i)@matriz_rotacion_x(alpha_i)  # Multiplicación de Matrices
	return MT

  # Función para la obtención de la cinemática del robot 
def robot_RR(theta_1,d1,a1,alpha_1,theta_2,d2,a2,alpha_2,theta_3,d3,a3,alpha_3): #
	A0 = np.eye(4)  # Matriz de posicionamiento en el espacio
	  # Obtención de cinemática para cada eslabón
	A_0_1 = denavit_hatemberg(theta_1,d1,a1,alpha_1) 
	A_1_2 = denavit_hatemberg(theta_2,d2,a2,alpha_2)
	A_2_3 = denavit_hatemberg(theta_3,d2,a2,alpha_3)
	  # Multiplicacion de cada eslabón para la cinemática general
	A_0_2 = A_0_1@A_1_2
	A_0_3 = A_0_2@A_2_3
      # Movimiento para cada eslabon
	sistema_coordenada_movil(A0)
	sistema_coordenada_movil(A_0_1)
	sistema_coordenada_movil(A_0_2)
	sistema_coordenada_movil(A_0_3)
      # Dibujamos cada eslabon del robot
	ax.plot3D([A0[0,3],A_0_1[0,3]],[A0[1,3],A_0_1[1,3]],[A0[2,3],A_0_1[2,3]], color = 'red')
	ax.plot3D([A_0_1[0,3],A_0_2[0,3]],[A_0_1[1,3],A_0_2[1,3]],[A_0_1[2,3],A_0_2[2,3]], color = 'red')
	ax.plot3D([A_0_2[0,3],A_0_3[0,3]],[A_0_2[1,3],A_0_3[1,3]],[A_0_2[2,3],A_0_3[2,3]], color = 'red')
  # Funcion para dibujar el trakbar en la gráfica
def ang(valor):

		ax.cla()  # Borra la posición anterior de la gráfica
		configuracion_grafica()  # Dibujamos la gráfica
		  # Variables para realizar el cambio de angulo de cada eslabón
		theta_1=sld_angulo_1.val
		theta_1b=sld_angulo_1b.val
		theta_1c=sld_angulo_1c.val
		  # 
		robot_RR( theta_1,3,0,90,
			      theta_1b,0,3,0,
			      theta_1c,0,3,90)



ax1=plt.axes([0.2,0.95,0.1,0.03])
ax2=plt.axes([0.5,0.95,0.1,0.03])
ax3=plt.axes([0.8,0.95,0.1,0.03])

sld_angulo_1=Slider(ax1,"Teta 1P",-180,180,valinit=180)
sld_angulo_1b=Slider(ax2,"Teta 1B",-180,180,valinit=0)
sld_angulo_1c=Slider(ax3,"Teta 1C",-180,180,valinit=90)




  # Graficación de Robot en posición inicial
configuracion_grafica()

  # Valores de función del robot
robot_RR(      0,3,0,0,
			   0,0,3,0,
			   90,0,3,90)
  # Obtención de valor de cambio de posición
sld_angulo_1.on_changed(ang)
sld_angulo_1b.on_changed(ang)
sld_angulo_1c.on_changed(ang)
  # Mostramos simulción
plt.show()