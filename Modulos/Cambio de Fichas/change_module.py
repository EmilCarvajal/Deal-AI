# -*- coding: utf-8 -*-
"""
MODULO QUE RECOGE FICHAS DE LA BANCA Y DEVUELVE EL CAMBIO
"""

from DealAI_modulo_IK_v3D import (CogerItem,DejarItem,CogerFichaRoja,CogerFichaNegra,CogerFichaBlanca,
CogerFichaVerde,CogerFichaAzul)
from DealAI_modulo_IK_v3D import (get_image,mov_brazo,bajar_brazo,subir_brazo,dist_object,ecuaciones,darCartaDerecha)
from Variables_Main import *

#from DealAI_modulo_IK_v3D import  fichasTotales_Banco
def solucio(sol, fitxa):
    return sum(sol) == fitxa
import time 
      
def cambiar_fichas_greedy(fitxa,mode): #esquema greedy
    Candidats = [5,10,25,50,100]
    Sol = []
       
    if mode == 0 and fitxa !=5:
        if fitxa in Candidats:
          Candidats.remove(fitxa)  
        #Candidats.remove(max(Candidats))
    
    while (not solucio(Sol,fitxa) and Candidats!=[]):
        x = max(Candidats)
        if sum(Sol)+x <= fitxa:
            Sol.append(x)
        else:
            Candidats.remove(x)
    if solucio(Sol,fitxa) == True:
        print(Sol,sum(Sol))
        return Sol
    else:
        print("No hi ha solucio")
           
#canvi = change_chips(50)   
def dar_Cambio(cambio, q): # q es matriz con posiciones donde deja el robot
    global fichasTotales_Banco
    monton = 3 #valor 0 mas bajo para dejar fichas
    for num in cambio:
        if num == 50:
            CogerFichaRoja()

            fichasTotales_Banco[2]-=1
        elif num == 25:
            CogerFichaVerde()
    
            fichasTotales_Banco[3]-=1
        elif num == 10:
            CogerFichaAzul()

            fichasTotales_Banco[4]-=1
        elif num == 100:
            CogerFichaNegra()
      
            fichasTotales_Banco[1]-=1
        elif num == 5:
            CogerFichaBlanca()
            
            fichasTotales_Banco[0]-=1
        #coge ficha
        subir_brazo(0.13)
        time.sleep(2)
        bajar_brazo(-dist_object())
        time.sleep(3)
        CogerItem(False)
        time.sleep(2)
        
        #deja ficha
        subir_brazo(0.13) 
        time.sleep(1)
        mov_brazo(q)
        subir_brazo(0.13)
        time.sleep(1)
        f = (monton) * 0.005
        time.sleep(1)
        bajar_brazo(-(0.089-f))
        bajar_brazo(-(0.089-f))
        time.sleep(2)
        DejarItem()
        time.sleep(1)
        subir_brazo(0.13)
        
        monton+=1
    