#!/usr/bin/env python
# coding: utf-8

# In[1]:
"""
MODULO COPELIA
"""
import sys 
# importamos las librerías necesarias
import sim          # librería para conectar con CoppeliaSim
import numpy as np
import sympy as sp
import cv2                      # opencv
import matplotlib.pyplot as plt # pyplot
from sympy import *
from sympy.physics.vector import init_vprinting
import time
import math

# In[DefAl] --- DEFINICION ALABETO 
global theta1, theta2, theta4, d3, lc, la, lb, l4, theta, alpha, a, d 
init_vprinting(use_latex='mathjax', pretty_print=False)
from sympy.physics.mechanics import dynamicsymbols
theta1, theta2, theta4, d3, lc, la, lb, l4, theta, alpha, a, d = dynamicsymbols('theta1 theta2 theta4 d3 lc la lb l4 theta alpha a d')
# -*- coding: utf-8 -*-

def connect(port):
# Establece la conexión a VREP
# port debe coincidir con el puerto de conexión en VREP
# retorna el número de cliente o -1 si no puede establecer conexión
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID


# <h3>Control de la ventosa </h3>

# ### Establecemos la conexión con CoppeliaSim

# In[2]:
# Requerimos los handlers para los joints, la ventosa y el sensor de Cámara 
global clientID,suction,joint1,joint2,joint3, joint4,psensor
clientID = connect(19999)
retCode,suction=sim.simxGetObjectHandle(clientID,'suctionPad',sim.simx_opmode_blocking)
retCode,sensorHandle=sim.simxGetObjectHandle(clientID,'Vision_sensor',sim.simx_opmode_blocking)
retCode,joint1=sim.simxGetObjectHandle(clientID,'Joint1',sim.simx_opmode_blocking)
retCode,joint2=sim.simxGetObjectHandle(clientID,'Joint2',sim.simx_opmode_blocking)
retCode,joint3=sim.simxGetObjectHandle(clientID,'Joint3',sim.simx_opmode_blocking)
retCode,joint4=sim.simxGetObjectHandle(clientID,'Joint4',sim.simx_opmode_blocking)
retCode,psensor=sim.simxGetObjectHandle(clientID,'suctionPadSensor',sim.simx_opmode_blocking)
print(suction, sensorHandle, joint1, joint2, joint3, joint4, psensor)
print("c,",clientID)
if clientID == -1:
    sys.exit()

from Variables_Main import *
"""
#VARIABLES CONSTANTES:
global blanco; blanco = 0
global negro; negro = 1
global rojo; rojo = 2
global verde; verde = 3
global azul; azul = 4
global rotationCentro


#VARIABLES GLOBALES:
#-- fichas
global fichasTotales_Banco, fichasTotales_Jug
fichasTotales_Banco = {blanco: 8, negro: 8, rojo: 8, verde: 8, azul: 8}
fichasTotales_Jug = {blanco: 3, negro: 3, rojo: 3, verde: 3, azul: 3}


#rotationCentro = [90, 82.5, 68, 49, 28.35]
rotationCentro = [90, 82.5, 65, 43.45, 21]
#-- cartas
global cartasTotales
cartasTotales = 19
global cartasReveladas
cartasReveladas = 0
global cartasQuemadas
cartasQuemadas=0
"""

# In[3]:


def setEffector(val):
# función que acciona el efector final remotamente
# val es Int con valor 0 ó 1 para desactivar o activar el actuador final.
    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,
        "suctionPad", sim.sim_scripttype_childscript,"setEffector",[val],[],[],"", sim.simx_opmode_blocking)
    return res


# <h3> Obtenemos los controladores (handlers) de los Joints, Ventosa y Sensor de Cámara</h3>
# 
# In[51]:


def matrixFromEuler(alpha, beta, gamma):
    # theta y alpha en radianes
    # d y a en metros
    Ra = sp.Matrix([[1, 0, 0, 0],
                   [0, sp.cos(alpha), -sp.sin(alpha), 0],
                   [0, sp.sin(alpha), sp.cos(alpha), 0],
                   [0, 0, 0, 1]])
    Rb = sp.Matrix([[sp.cos(beta), 0, sp.sin(beta), 0],
                   [0, 1, 0, 0],
                   [-sp.sin(beta), 0, sp.cos(beta), 0],
                   [0, 0, 0, 1]])
    Rc = sp.Matrix([[sp.cos(gamma), -sp.sin(gamma), 0, 0],
                   [sp.sin(gamma), sp.cos(gamma), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    E = Ra*Rb*Rc
    return E

# In[77]:





# <h3> Secuencia de movimientos (pruebas) </h3>
# 
# #### En este caso se crear distintas funciones (de momento no óptimas) que permiten una gestión del robot más eficaz.
# Almacenando los datos en un vector, podemos utilizar algún factor del elemento para ordenarlo, para así, posteriormente, poder seleccionar un objeto con propiedades en concretos.
# Inicialmente, para poder operar con este sistema, utilizamos fichas de distintos tamaños (fichas de poker) y elegimos cómo manipularlas dependiendo del tamaño.
# 
# - Es necesario aplicar visión por computador (en vez de tamaño por colores o por un número que lee) para gestionar las fichas.
# - Llamar a la función de recogida de fichas mediante comandos de voz.
# 
# La función 'colocar(vector, z) nos permite colocar el manipulador encima de una posición en la mesa (en el parámetro vector se encuentra la x, y) en una altura determinada. La altura se pasa como un parametro por separado porque esta no depende solo de la altura de la mesa, sino también de la cantidad de fichas apiladas que haya en ese momento.
# 
# Para una mejor gestión de estos acontecimientos, utilizamos la función sleep() de la libreria 'time' para observar los movimientos que ejerce el robot y si se desplaza a la posición adecuada, es decir, que los cálculos de las posiciones se hacen correctamente.
# 

# In[5]:


init_vprinting(use_latex='mathjax', pretty_print=False)
from sympy.physics.mechanics import dynamicsymbols
theta1, theta2, theta4, d3, lc, la, lb, l4, theta, alpha, a, d = dynamicsymbols('theta1 theta2 theta4 d3 lc la lb l4 theta alpha a d')
theta1, theta2, theta4, d3, lc, la, lb, l4, theta, alpha, a, d 


# In[47]:


rot = sp.Matrix([[sp.cos(theta), -sp.sin(theta)*sp.cos(alpha), sp.sin(theta)*sp.sin(alpha)],
                 [sp.sin(theta), sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha)],
                 [0, sp.sin(alpha), sp.cos(alpha)]])

trans = sp.Matrix([a*sp.cos(theta),a*sp.sin(theta),d])

last_row = sp.Matrix([[0, 0, 0, 1]])

m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)

m01 = m.subs({ theta:theta1, d:lc, a:la , alpha:0})
m12 = m.subs({ theta:theta2, d:0, a:lb ,alpha:180*np.pi/180})
m12[0,2]=0
m12[1,2]=0
m12[2,1]=0
m23 = m.subs({ theta:0, d:d3, a:0 ,alpha:0*np.pi/180})
m34 = m.subs({ theta:theta4, d:l4, a:0 ,alpha:180*np.pi/180})
m34[0,2]=0
m34[1,2]=0
m34[2,1]=0
m04 = (m01*m12*m23*m34)

mbee= sp.Matrix([[sp.trigsimp(m04[0,0].simplify()), sp.trigsimp(m04[0,1].simplify()), (m04[0,2].simplify()),sp.trigsimp(m04[0,3].simplify())],
                 [sp.trigsimp(m04[1,0].simplify()), sp.trigsimp(m04[1,1].simplify()), (m04[1,2].simplify()),sp.trigsimp(m04[1,3].simplify())],
                 [sp.trigsimp(m04[2,0].simplify()), m04[2,1].simplify(), sp.trigsimp(m04[2,2].simplify()),sp.trigsimp(m04[2,3].simplify())],
                 [m04[3,0].simplify(), m04[3,1].simplify(), m04[3,2].simplify(),m04[3,3].simplify()]])

mbee=mbee.subs({ lc:0.2, la:0.2, lb:0.2, l4:0.097})
mbee



# In[49]:
def sortJugadores(arr):
    if arr[2] <= 0:
        return arr[2]
    else:
        return arr[0]

def posicionJugadores(numJugadores):
    r=0.4
    points = []
    lado = int(numJugadores/2)
    angulo = np.pi/(2*(lado + 1))
    for index in range(lado):
        points.append([round(r*math.cos((index+1)*angulo), 4), round(r*math.sin((index+1)*angulo), 4), (index+1)*angulo])
        points.append([round(r*math.cos((index+1)*angulo), 4), -round(r*math.sin((index+1)*angulo), 4), -(index+1)*angulo])
    if numJugadores%2 == 1:
        points.append([round((r)*math.cos(0), 4), round(r*math.sin(0), 4), 0])
    points.sort(reverse=True, key=sortJugadores)
    return points


# In[50]:

"""
res = posicionJugadores(4)
print(res)
x = res[0][0]
y = res[0][1]
print(np.pi/40)
print(res[0][2])
newX1= round(0.4*math.cos(res[0][2]+(np.pi/40)), 4)
newY1= round(0.4*math.sin(res[0][2]+(np.pi/40)), 4)
newX2= round(0.4*math.cos(res[0][2]-(np.pi/40)), 4)
newY2= round(0.4*math.sin(res[0][2]-(np.pi/40)), 4)
print(newX1, newY1, newX2, newY2)
print(res[1][2])
newX1= round(0.4*math.cos(res[1][2]+(np.pi/40)), 4)
newY1= round(0.4*math.sin(res[1][2]+(np.pi/40)), 4)
newX2= round(0.4*math.cos(res[1][2]-(np.pi/40)), 4)
newY2= round(0.4*math.sin(res[1][2]-(np.pi/40)), 4)
print(newX1, newY1, newX2, newY2)
print(res[2][2])
newX1= round(0.4*math.cos(res[2][2]+(np.pi/40)), 4)
newY1= round(0.4*math.sin(res[2][2]+(np.pi/40)), 4)
newX2= round(0.4*math.cos(res[2][2]-(np.pi/40)), 4)
newY2= round(0.4*math.sin(res[2][2]-(np.pi/40)), 4)
print(newX1, newY1, newX2, newY2)
print(res[3][2])
newX1= round(0.4*math.cos(res[3][2]+(np.pi/40)), 4)
newY1= round(0.4*math.sin(res[3][2]+(np.pi/40)), 4)
newX2= round(0.4*math.cos(res[3][2]-(np.pi/40)), 4)
newY2= round(0.4*math.sin(res[3][2]-(np.pi/40)), 4)
print(newX1, newY1, newX2, newY2)

"""


# In[52]:


def CogerItem(flip):
    errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,psensor, sim.simx_opmode_blocking)
    
    if detectionState==True:
        sensor_val=np.linalg.norm(detectedPoint)
        print("distacia al objeto: ",sensor_val)
        #if flip == True:
          #  return 0 
            #detectedObjectHandle#sim.simxSetObjectOrientation(clientID, detectedObjectHandle, detectedObjectHandle, [0,0,(66 + 69/4)*2], sim.simx_opmode_oneshot)
        #setEffector(1)
        if(sim.simxSetObjectParent(clientID, detectedObjectHandle, suction, True, sim.simx_opmode_oneshot)):
            print("Cogido")
        else:
            print("No se ha podido coger")
    else:
        print("No ha detectado objeto")


# In[53]:


def DejarItem():
    errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,psensor, sim.simx_opmode_blocking)
    
    if detectionState==True:
        sensor_val=np.linalg.norm(detectedPoint)
        print("distacia al objeto: ",sensor_val)
        if(sim.simxSetObjectParent(clientID, detectedObjectHandle, -1, True, sim.simx_opmode_oneshot)):
            print("Dejado")
        else:
            print("NS ha podido dejar")
    else:
        print("No ha detectado objeto")
        
    return detectedObjectHandle


# In[54]:


def Standby():
    x = -0.0895
    y = 0.0
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, -qFinal[0] - np.pi, sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, -qFinal[1], sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)   


# In[55]:


def CogerFichaAzul():
    x = -0.152
    y = 0.0
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)


# In[56]:


def CogerFichaVerde():
    x = -0.2145
    y = 0.0
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)


# In[57]:


def CogerFichaNegra():
    x = -0.277
    y = 0.0
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)


# In[58]:

def CogerFichaRoja():
    x = -0.3395
    y = 0.0
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)


# In[59]:


def CogerFichaBlanca():
    x = -0.4
    y = 0.0
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)



def CogerCarta(flip):
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0.08, sim.simx_opmode_oneshot)
    x = 0.275
    y = 0.05
    
    #z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
    #eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1.5),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0]
    
    global cartasReveladas
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, -qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0.08, sim.simx_opmode_oneshot)
    time.sleep(3)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 37*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(2)
    print(cartasReveladas)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0543 -(0.0007 * cartasReveladas), sim.simx_opmode_oneshot)
    cartasReveladas = cartasReveladas + 1
    time.sleep(2)
    CogerItem(flip)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0.08, sim.simx_opmode_oneshot)
"""
def CogerCarta(flip):
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    x = 0.275
    y = 0.05
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1.5,1),prec=5)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    global cartasReveladas
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, -qFinal[1], sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)
    time.sleep(3)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 37*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(2) 
    print(cartasReveladas)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0543 -(0.0007 * cartasReveladas)-0.0828, sim.simx_opmode_oneshot)
    cartasReveladas = cartasReveladas + 1
    time.sleep(2)
    CogerItem(flip)
    time.sleep(2) #subir 
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
"""
"""
# In[]
# COLOCAR CARTAS CENTRALES --------------- 
def Colocar3CartasCentrales():
    for numCard in range(3):
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
        CogerCarta(True)
        #x = -0.152 + (numCard*0.064)
        x = -0.152 + (numCard*0.0695)
        print(x)
        y = 0.19
        #z = 0.2
        
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
        #eq3 = 0.105 - d3 - z
        try:
            qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1),prec=5)
            if abs(qFinal[0]) > 2*np.pi:
                if qFinal[0] < 0:
                    qFinal[0] = qFinal[0] *(-1)
                    qFinal[0] = qFinal[0] % (2*np.pi)
                    qFinal[0] = qFinal[0] *(-1)
                qFinal[0] = qFinal[0] % (2*np.pi)
                print('Reajuste Realizado')
            print('Solución encontrada')
            print(qFinal)
        except:
            qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1.5,1),prec=5)
            qFinal[0] = qFinal[0] % (2*np.pi)
            print('Solución encontrada (por suerte)')
            print(qFinal)
        time.sleep(2)
        retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
        retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
        time.sleep(4)
        #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[numCard]*np.pi/180, sim.simx_opmode_oneshot)
        time.sleep(2)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0745, sim.simx_opmode_oneshot)
        time.sleep(2)
        DejarItem()
        time.sleep(3)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)


def Colocar4CartaCentral():
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    CogerCarta(True)    
    #x = -0.152 + (3*0.064)
    x = -0.152 + (3*0.0695)
    y = 0.19
    #z = 0.2
    print(x)
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    #eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1.5),prec=5)
        print('Solución encontrada')
        
        qFinal[0] = qFinal[0] % (2*np.pi)
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    qFinal[1] = qFinal[1] % (2*np.pi)
    qFinal[0] = qFinal[0] % (2*np.pi)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(5)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[3]*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(4)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0745, sim.simx_opmode_oneshot)
    time.sleep(4)
    DejarItem()
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)    




def Colocar5CartaCentral():
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    CogerCarta(True)     
    #x = -0.152 + (4*0.064)
    x = -0.152 + (4*0.0695)
    y = 0.19
    #z = 0.2
    print(x)
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    #eq3 = 0.105 - d3 - z
    try:
        #qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1),prec=5)
        qFinal=nsolve((eq1,eq2),(theta1,theta2),(2,1),prec=5)
        qFinal[1] = qFinal[1] % (2*np.pi)
        qFinal[0] = qFinal[0] % (2*np.pi)
        
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(5)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[4]*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(4)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.07, sim.simx_opmode_oneshot)
    time.sleep(4)
    DejarItem()
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)


def darCartaIzquierda(x, y):
    #x = 0.2598  
    #y = -0.3042
    z = 0.0 
     
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[1] > 6:
            eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
            eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
            try:
                print("Supera el valor de 6")
                qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1.5,1,1),prec=5)
                qFinal[0] = qFinal[0] % (2*np.pi)
                qFinal[1] = qFinal[1] % (2*np.pi)
            except:
                print("F en el chat")
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución 1')
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(10,2,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[1] > 6:
            eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
            eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
            try:
                print("Supera el valor de 6")
                qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1.5,1,1),prec=5)
                qFinal[0] = qFinal[0] % (2*np.pi)
                qFinal[1] = qFinal[1] % (2*np.pi)
            except:
                print("F en el chat")
        print(qFinal)
        #qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)


def darCartaDerecha(x, y):
    z = 0.0 
     
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[1] > 6:
            eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
            eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - x
            try:
                print("Supera el valor de 6")
                qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1.5,1,1),prec=5)
                qFinal[0] = qFinal[0] % (2*np.pi)
                qFinal[1] = qFinal[1] % (2*np.pi)
            except:
                print("F en el chat")
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución 1')
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - x
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(10,2,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[1] > 6:
            eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
            eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
            try:
                print("Supera el valor de 6")
                qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1.5,1,1),prec=5)
                qFinal[0] = qFinal[0] % (2*np.pi)
                qFinal[1] = qFinal[1] % (2*np.pi)
            except:
                print("F en el chat")
        print(qFinal)
        #qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)    

"""
def darCartaCentro(x, y):
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[0] > 6:
            print("Supera el 6")
            qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
            for i in range(2):
                if abs(qFinal[i]) > np.pi:
                    if qFinal[i] < 0:
                        qFinal[i] = qFinal[i] * (-1)
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        if qFinal[i] > np.pi:
                            qFinal[i] = qFinal[i] - (2*np.pi)
                        qFinal[i] = qFinal[i] * (-1)
                    else:
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        if qFinal[i] > np.pi:
                            qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)  

def quemarCarta():
    x = 0.1565
    y = 0.05
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    CogerCarta(False)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(3)
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 7*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(3)
    global cartasQuemadas
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0745 + (cartasQuemadas*0.0007), sim.simx_opmode_oneshot)
    cartasQuemadas = cartasQuemadas + 1
    time.sleep(3)
    DejarItem()
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    time.sleep(2) 
    
def ir_a_flipeador():
    x = 0.388#0.383
    y = -0.018#0.007
    z = 0.7926
    retCode = sim.simxSetJointTargetPosition(clientID, joint3,0.07926, sim.simx_opmode_oneshot)

    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
        
    time.sleep(4)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(4)
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, (80)*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(4)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3,0.076, sim.simx_opmode_oneshot)
    time.sleep(3)
    handle = DejarItem()
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0.08, sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, -10*np.pi/180, sim.simx_opmode_oneshot)
    #time.sleep(1)
    flip_carta(handle)
    time.sleep(2)
    #time.sleep(1)
    
    #---- ir a BANDEJA ---
    
    x = 0.383
    y = 0.082
    z = 0.6618
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
        
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, -113*np.pi/180, sim.simx_opmode_oneshot)

    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(1)
    

    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.05618, sim.simx_opmode_oneshot)
    time.sleep(2)

    CogerItem(True)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    time.sleep(2) 
    
    
def ir_a_bandeja():
    
    x = 0.383
    y = 0.082
    z = 0.6618
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
        
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, -110*np.pi/180, sim.simx_opmode_oneshot)

    time.sleep(3)
    
    #retCode = sim.simxSetJointTargetPosition(clientID, joint4, 7*np.pi/180, sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint4, -127, sim.simx_opmode_oneshot)

    time.sleep(3)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.05618, sim.simx_opmode_oneshot)
    time.sleep(3)

    CogerItem(True)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    time.sleep(2) 
    #-----
    for numCard in range(3):
   
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0.08, sim.simx_opmode_oneshot)
        
        x = -0.152 + (numCard*0.0695)
        print(x)
        y = 0.19
        #z = 0.2
        
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
        #eq3 = 0.105 - d3 - z
        try:
            qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1),prec=5)
            for i in range(2):
                if abs(qFinal[i]) > np.pi:
                    if qFinal[i] < 0:
                        qFinal[i] = qFinal[i] * (-1)
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        if qFinal[i] > np.pi:
                            qFinal[i] = qFinal[i] - (2*np.pi)
                        qFinal[i] = qFinal[i] * (-1)
                    else:
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        if qFinal[i] > np.pi:
                            qFinal[i] = qFinal[i] - (2*np.pi)
            print('Solución encontrada')
            print(qFinal)
        except:
            qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1.5,1),prec=5)
            qFinal[0] = qFinal[0] % (2*np.pi)
            print('Solución encontrada (por suerte)')
            print(qFinal)
        time.sleep(1)
        retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
        retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
        time.sleep(2)
        #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[numCard]*np.pi/180, sim.simx_opmode_oneshot)
        time.sleep(3)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0745, sim.simx_opmode_oneshot)
        time.sleep(2)
        DejarItem()
        time.sleep(1)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
        
def Colocar3CartasCentrales():
    for numCard in range(3):
        CogerCarta(True)
        #retCode = sim.simxSetJointTargetPosition(clientID, joint3, 0.08, sim.simx_opmode_oneshot)
        
        ir_a_flipeador()
        x = -0.152 + (numCard*0.0695)
        print(x)
        y = 0.19
        #z = 0.2
        
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
        #eq3 = 0.105 - d3 - z
        try:
            qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1),prec=5)
            for i in range(2):
                if abs(qFinal[i]) > np.pi:
                    if qFinal[i] < 0:
                        qFinal[i] = qFinal[i] * (-1)
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        if qFinal[i] > np.pi:
                            qFinal[i] = qFinal[i] - (2*np.pi)
                        qFinal[i] = qFinal[i] * (-1)
                    else:
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        if qFinal[i] > np.pi:
                            qFinal[i] = qFinal[i] - (2*np.pi)
            print('Solución encontrada')
            print(qFinal)
        except:
            qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1.5,1),prec=5)
            qFinal[0] = qFinal[0] % (2*np.pi)
            print('Solución encontrada (por suerte)')
            print(qFinal)
        time.sleep(1)
        retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
        retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
        time.sleep(2)
        #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[numCard]*np.pi/180, sim.simx_opmode_oneshot)
        time.sleep(3)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0725, sim.simx_opmode_oneshot)
        time.sleep(2)
        DejarItem()
        time.sleep(1)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
        retCode = sim.simxSetJointTargetPosition(clientID, joint4, 7*np.pi/180, sim.simx_opmode_oneshot)

def Colocar4CartaCentral():
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    CogerCarta(True)  
    ir_a_flipeador()
    x = -0.152 + (3*0.0695)
    y = 0.19
    #z = 0.2
    print(x)
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    #eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2),(theta1,theta2),(1,1.5),prec=5)
        print('Solución encontrada')
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[3]*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0715, sim.simx_opmode_oneshot)
    time.sleep(2)
    DejarItem()
    time.sleep(1)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot) 
# In[66]:
def Colocar5CartaCentral():
    
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    CogerCarta(True)
    ir_a_flipeador()     
    x = -0.152 + (4*0.0695)
    y = 0.19
    z = 0.2
    print(x)
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(3)
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, -rotationCentro[4]*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(3)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0725, sim.simx_opmode_oneshot)
    time.sleep(3)
    DejarItem()
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
def darCartaIzquierda(x, y):
    #x = 0.2598  
    #y = -0.3042
    z = 0.0 
     
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución 1')
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(10,2,1),prec=5)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print(qFinal)
        #qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    return qFinal

def darCartaDerecha(x, y):
    z = 0.0 
     
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución 1')
        eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
        eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - x
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(10,2,1),prec=5)
        for i in range(2):
            if abs(qFinal[i]) > np.pi:
                if qFinal[i] < 0:
                    qFinal[i] = qFinal[i] * (-1)
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
                    qFinal[i] = qFinal[i] * (-1)
                else:
                    qFinal[i] = qFinal[i] % (2*np.pi)
                    if qFinal[i] > np.pi:
                        qFinal[i] = qFinal[i] - (2*np.pi)
        print(qFinal)
        #qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0], sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    return qFinal
"""
def darCartaCentro(x, y):
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - x
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) - y
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[0] > 6:
            print("Supera el 6")
            qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
            for i in range(2):
                if abs(qFinal[i]) > 2*np.pi:
                    if qFinal[i] < 0:
                        qFinal[i] = qFinal[i] * (-1)
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        qFinal[i] = qFinal[i] * (-1)
                    else:
                        qFinal[i] = qFinal[i] % (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -qFinal[2], sim.simx_opmode_oneshot)    
"""

# In[84]:


def darCartaJugador(x, y, angulo):
    valX = [round(0.4*math.cos(angulo+(np.pi/34)), 4), round(0.4*math.cos(angulo-(np.pi/34)), 4)]
    valY = [round(0.4*math.sin(angulo+(np.pi/34)), 4), round(0.4*math.sin(angulo-(np.pi/34)), 4)]
    #z = 0.2
    for i in range(2):
        print('x' + str(i+1))
        CogerCarta(False)
        time.sleep(2)
        if angulo == 0:
            print("CENTRO")
            darCartaCentro(valX[i], valY[i])
        else:
            if y < 0:
                print("Izquierda")
                darCartaIzquierda(valX[i], valY[i])
            else:
                print("Derecha")
                darCartaDerecha(valX[i], valY[i])
        time.sleep(3)
        retCode = sim.simxSetJointTargetPosition(clientID, joint4, 0, sim.simx_opmode_oneshot)
        time.sleep(3)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0645, sim.simx_opmode_oneshot)
        time.sleep(2)
        DejarItem()
        time.sleep(2)
        retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
        time.sleep(1)


# In[]
"""
def quemarCarta():
    x = 0.1565
    y = 0.05
    z = 0.2
    
    eq1 = 0.2 * cos(theta1) + 0.2 * cos(theta1 + theta2) - y
    eq2 = 0.2 * sin(theta1) + 0.2 * sin(theta1 + theta2) + x
    eq3 = 0.105 - d3 - z
    try:
        qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
        qFinal[0] = qFinal[0] % (2*np.pi)
        qFinal[1] = qFinal[1] % (2*np.pi)
        if qFinal[0] > 6:
            print("Supera el 6")
            qFinal=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
            for i in range(2):
                if abs(qFinal[i]) > 2*np.pi:
                    if qFinal[i] < 0:
                        qFinal[i] = qFinal[i] * (-1)
                        qFinal[i] = qFinal[i] % (2*np.pi)
                        qFinal[i] = qFinal[i] * (-1)
                    else:
                        qFinal[i] = qFinal[i] % (2*np.pi)
        print('Solución encontrada')
        print(qFinal)
    except:
        print('No se encuentra solución')
        qFinal=[0,0,0]
    
    CogerCarta(False)
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, qFinal[0] , sim.simx_opmode_oneshot) 
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, qFinal[1], sim.simx_opmode_oneshot)
    time.sleep(2)
    
    retCode = sim.simxSetJointTargetPosition(clientID, joint4, 7*np.pi/180, sim.simx_opmode_oneshot)
    time.sleep(2)
    global cartasQuemadas
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0745 + (cartasQuemadas*0.0007), sim.simx_opmode_oneshot)
    cartasQuemadas = cartasQuemadas + 1
    time.sleep(3)
    DejarItem()
    time.sleep(2)
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, -0.0, sim.simx_opmode_oneshot)
    time.sleep(2)
    
"""

# In[]------------- e modulo RFJ
def get_image():
    retCode, resolution, image=sim.simxGetVisionSensorImage(clientID,sensorHandle,0,sim.simx_opmode_oneshot_wait)
    imge=np.array(image,dtype=np.uint8)
   
    imge.resize([resolution[1],resolution[0],3])

    img_Robot = cv2.cvtColor(imge,cv2.COLOR_BGR2RGB)
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')

    plt.imshow(cv2.cvtColor(imge,cv2.COLOR_BGR2RGB))
    print(resolution)

    return img_Robot

def mov_brazo(q):
    retCode = sim.simxSetJointTargetPosition(clientID, joint1, q[0], sim.simx_opmode_oneshot)
    retCode = sim.simxSetJointTargetPosition(clientID, joint2, q[1], sim.simx_opmode_oneshot)
    #retCode = sim.simxSetJointTargetPosition(clientID, joint3, q[2], sim.simx_opmode_oneshot)
def bajar_brazo(m):
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, m, sim.simx_opmode_oneshot)
    
def subir_brazo(m):
    retCode = sim.simxSetJointTargetPosition(clientID, joint3, m, sim.simx_opmode_oneshot)
def dist_object():    
    errorCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector=sim.simxReadProximitySensor(clientID,psensor, sim.simx_opmode_blocking)
    sensor_val =-1
    if detectionState==True:
        sensor_val=np.linalg.norm(detectedPoint)
        print("distacia al objeto: ",sensor_val)
    return sensor_val

def ecuaciones(x,y,z):
    eq1 = 0.2*cos(theta1) + 0.2*cos(theta1 + theta2) -y
    eq2 = 0.2*sin(theta1) + 0.2*sin(theta1 + theta2) +x
    eq3 = 0.105 - d3 - z 
    return eq1,eq2,eq3

def flip_carta(c1):
    for i in range(1,44):
        #i = 49
        ret, pos = sim.simxGetObjectPosition(clientID, c1, -1, sim.simx_opmode_blocking)
        if (i<25) or (i>=25 and i<33 and i%2==0) or (i>=35 and i<39 and i%2==0): 
            sim.simxSetObjectOrientation(clientID, c1, c1, [0,-4.8*np.pi/180,0], sim.simx_opmode_oneshot)
        if i<10 and i%2 == 0:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]-0.002,pos[2]-0.006], sim.simx_opmode_blocking)
        elif i >=10 and i<20 and i%2==0:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]-0.004,pos[2]], sim.simx_opmode_blocking)
        if i >=15 and i<20 and i%2==0:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]-0.004,pos[2]-0.008], sim.simx_opmode_blocking)
        elif i >=20 and i<25 and i%2==0:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1],pos[2]-0.008], sim.simx_opmode_blocking)
        elif i >=23 and i<25 and i%2==0:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]+0.004,pos[2]], sim.simx_opmode_blocking)
        elif i >=25 and i<35 and i%2==1:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1],pos[2]-0.0044], sim.simx_opmode_blocking)
        elif i >=25 and i<35 and i%2==0:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]+0.006,pos[2]-0.0044], sim.simx_opmode_blocking)
        #elif i >=35 and i<39 and i%2==0:
            #sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1],pos[2]-0.0044], sim.simx_opmode_blocking)
        if i >=35 and i<39:
            if i%2==0:
                sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]+0.003,pos[2]-0.0044], sim.simx_opmode_blocking)
            else:
                sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]+0.003,pos[2]], sim.simx_opmode_blocking)
        elif i >=38 and i<44:
            sim.simxSetObjectPosition(clientID, c1, -1, [pos[0],pos[1]+0.015,pos[2]-0.0028], sim.simx_opmode_blocking)
        if i>=40 and i<44:
            sim.simxSetObjectOrientation(clientID, c1, c1, [0,-9*np.pi/180,0], sim.simx_opmode_oneshot)