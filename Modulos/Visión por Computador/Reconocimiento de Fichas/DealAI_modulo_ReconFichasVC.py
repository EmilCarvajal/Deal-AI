"""
MODULO QUE RECOJE LAS FICHAS EN UNA ZONA, DEVUELVE SU VALOR 
"""

# -*- coding: utf-8 -*-
import sim          # librería para conectar con CoppeliaSim
import numpy as np
import sympy as sp
import cv2                      # opencv
import matplotlib.pyplot as plt # pyplot
from sympy import *
from sympy.physics.vector import init_vprinting
import time
import math


from DealAI_modulo_IK_v3D import (CogerItem,DejarItem,CogerFichaRoja,CogerFichaNegra,CogerFichaBlanca,
CogerFichaVerde,CogerFichaAzul,Standby)
from DealAI_modulo_IK_v3D import (get_image,mov_brazo,bajar_brazo,subir_brazo,dist_object,ecuaciones,darCartaDerecha)
  

#########  VC MODULO #########
def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def valorFichas(img_Robot): # devuelve los valores de la fichas que detecta  
    #--------------------------------

    #img_Robot = img_Robot[250: 410, 680 :880] #[f_inicial:f_final,c_inicial:c_final]# 70 + x  550 + y
    img= img_Robot.copy()
    img_O = img_Robot.copy()
    img =increase_brightness(img, value=80)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Eliminación del ruido
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 1)
    plt.imshow(opening)
    plt.show() 


    # Encuentra el área del fondo
    sure_bg = cv2.dilate(opening,kernel,iterations=1)
    print("dilateeeeee")
    plt.imshow(sure_bg)
    plt.show() 
    # Encuentra el área del primer
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Encuentra la región desconocida (bordes)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    print("unknow")
    plt.imshow(unknown)
    plt.show() 
    # Etiquetado
    ret, markers = cv2.connectedComponents(sure_fg)

    # Adiciona 1 a todas las etiquetas para asegurra que el fondo sea 1 en lugar de cero
    markers = markers+1
    print("markers = markers+1")
    plt.imshow(markers)
    plt.show() 


    # Ahora se marca la región desconocida con ceros
    markers[unknown==255] = 0
    """
    print("markers[unknown==255] = 0")
    plt.imshow(markers)
    plt.show() 
    """
    markers = cv2.watershed(img,markers)
    """
    print("watersher")
    plt.imshow(markers)
    plt.show() 
    """
    #img[markers == -1] = [255,0,0]
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')

    markers = markers > 1    # conevertimos manchas a blanco y negro
    markers=markers.astype(np.uint8)
    markers = cv2.dilate(markers,kernel,iterations = 1) #eliminamos ruido
    #kernel = np.ones((4,4),np.uint8)
    #markers = cv2.morphologyEx(markers,cv2.MORPH_OPEN,kernel, iterations = 2) #rellenamos

    plt.imshow(markers)
    plt.show() 

    #Buscamos los contornos de las bolas y los dibujamos en verde
    contours_o,_ = cv2.findContours(markers, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = []
    cv2.drawContours(img, contours_o, -1, (0,255,0), 2)
    if contours_o == []:
        return 0,0,0
    print(cv2.contourArea(contours_o[0]))
    for c in contours_o: # 1193.0
        if (cv2.contourArea(c)> 500  and  cv2.contourArea(c)< 2000 ):

            contours.append(c)
    cv2.drawContours(img, contours, -1, (0,255,0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX



    #Buscamos el centro de las bolas y lo pintamos en rojo
    for i in contours:
        #Calcular el centro a partir de los momentos
        momentos = cv2.moments(i)
        cx = int(momentos['m10']/momentos['m00']) 
        cy = int(momentos['m01']/momentos['m00'])

        print("cx:",cx+550," cy: ",cy+70 )
        #Dibujar el centro
        cv2.circle(img,(cx, cy), 3, (0,0,255), -1)

        #Escribimos las coordenadas del centro
        cv2.putText(img,"(x: " + str(cx) + ", y: " + str(cy) + ")",(cx+10,cy+10), font, 0.5,(255,255,255),1)
    plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    print("seleccion de contornos:")
    plt.imshow(img)
    plt.show() 

    #def bright
    # CONTOUR[0] 
    img_O = cv2.cvtColor(img_O, cv2.COLOR_BGR2RGB)
    #img_O = cv2.cvtColor(img_O, cv2.COLOR_RGB2HSV)
    img_O=increase_brightness(img_O, value=30)
    plt.imshow(img_O)
    plt.show() 
    
    if len(contours) ==0:
        return (0,0,0)
    
    for cont in range(0,len(contours)):
        print("CONTORNO", cont)
        (x,y),radius = cv2.minEnclosingCircle(contours[cont])
        center = (int(x),int(y))
        radius = int(radius)
        img_C= img_O.copy()
        img_C = cv2.circle(img_C,center,radius,(0,255,0),2)
        plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
        """
        print("Cicurlo, contorno", cont)
        plt.imshow(img_C)
        plt.show()  
        """
        #CUADRADO ------------------

        x,y,w,h = cv2.boundingRect(contours[cont])
        cv2.rectangle(img_C,(x,y),(x+w,y+h),(0,255,0),2)

        plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
        print("Cuadrado, contorno ",cont)
        plt.imshow(img_C)
        plt.show()    

        #RECORTE CUADRADO ---------------
        imR= img_O.copy()
        imRR = imR[y:y+h,x:x+w]


        train_mean =np.mean(imRR, axis=1)
        train_mean =np.mean(train_mean, axis=0)

        plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')

        plt.imshow(imRR)
        plt.show()
        print(" mitjana pixel:", train_mean)

        #color_rgb = [107, 109, 101]
        color_rgb = [int(train_mean[0]), int(train_mean[1]), int(train_mean[2])]

        black_rgb =[0, 0, 0]
        white_rgb = [255, 255, 255] 
        red_rgb = [255, 0, 0] 
        green_rgb = [0, 255, 0] 
        blue_rgb = [0, 0, 255] 


        colors_list = [black_rgb,white_rgb,red_rgb,green_rgb,blue_rgb]
        colors_names = ["black","white","red","green","blue"]
        sum_c = sum(color_rgb)
        i = 0

        dif = 10000
        itf = -1 
        for color in colors_list :
            cond = sum([abs(x1 - x2) for (x1, x2) in zip(color,color_rgb)])
            #print("sc:",cond , "dif: ",dif)
            if cond < dif:
                dif = cond
                itf = i

            i = i+1

        print("RESULT:", colors_names[itf])
    if itf!=-1:
        return (colors_names[itf],cx,cy)
