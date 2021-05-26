# -*- coding: utf-8 -*-

import numpy as np
import eval7 #instalar :  pip install eval7
from pokereval.card import Card# install pip install pokereval
from pokereval.hand_evaluator import HandEvaluator 
#--
import cv2  
import matplotlib.pyplot as plt # pyplot
from PIL import Image
import glob
import os
import math

from DealAI_modulo_IK_v3D import get_image

#------ CARREGUEM DATASET
#carreguem dataset ranks cartes i tipus
imgsRanks=[] #A, 1, 2, ... , J, Q, K
imgsTipus=[] #cors, piques, trebol, rombes

for nomImgR in glob.glob('dataset/ranks/*.jpg'): #assuming gif
    card = cv2.imread(nomImgR, cv2.IMREAD_GRAYSCALE)
    imgsRanks.append([card,os.path.splitext(os.path.basename(nomImgR))[0]])

for nomImgT in glob.glob('dataset/tipus/*.jpg'): #assuming gif
    card = cv2.imread(nomImgT, cv2.IMREAD_GRAYSCALE)
    imgsTipus.append([card, os.path.splitext(os.path.basename(nomImgT))[0]])

#---- VAR GLOABLES
#RETALLJUGADORS = [[870,1100,300,630],[780,1100,1150,1500],[970,1200,1550,2000],[]] #[filaIni,FilaFi,colIni,colFi]
f_inicial = 325   #100 margen
f_final = 425
c_inicial = 700  #150 margen
c_final = 850
#RETALLJUGADORS = [[250,500,300,500],[120,250,500,800],[150,350,50,380],[0,150,250,500],[250,450,500,800],[150,350,350,700]] #[filaIni,FilaFi,colIni,colFi]
#CORNERW = 32
#CORNERH = 50
widthCantonada = 24 #15
heigthCantonada = 25
CARD_THRESH = 30
ZOOMW_RANK = 70
ZOOMH_RANK = 125
ZOOMW_TIPUS = 70
ZOOMH_TIPUS = 100

#AREAS DONDE SE VEN LAS CARTAS DE CADA: 5JUGADORES (PARA JOFRE)

areas5jugC =[
        [175, 410, 780 , 1012],
        [20 , 250 , 630,860 ],
        [20,200, 400,640],
        [20 , 250 , 180,420 ],
        [175, 394, 30 , 258], [240,380,350,720]   #pos 5 es cartas centrales
]

#areaCartasCentrales = [123,4,3,4]

def decirGanador(players_p):
    img_Robot = get_image()
    #im_central = img_Robot[]
    respostaEv7_maq, respostaHandEv_maq = valorsCartesImg(img_Robot, 5, 5)
    #puntuacio, nomCombo = comboJugador(np.array(eval7_jug, dtype=object), np.array(eval7_Maqu, dtype=object), hanEv_player,handEv_Maqu)
    
    m_puntuaciones =0
    ganador = -1
    combo_ganador = -1
    for p in players_p:    
        eval7_jug, respostaHandEv = valorsCartesImg(img_Robot, p-1, 2)
        puntuacio, nomCombo = comboJugador(np.array(eval7_jug, dtype=object), np.array(respostaEv7_maq, dtype=object), respostaHandEv,respostaHandEv_maq)
        puntuacio = round(puntuacio,10)
        if puntuacio > m_puntuaciones:
            m_puntuaciones = puntuacio #double
            ganador = p
            combo_ganador = nomCombo # string
    print("ganador ", p)
    print("combo_ganador: ", nomCombo )
    return ganador, combo_ganador




#----------------------- 
def comboJugador(cPlayer, cBoard , hand, board):
    
    valorsConcat = np.concatenate((board,hand))  
    print("hand: ",hand,"board: " ,board,"cPLayer", cPlayer, "cboard",cBoard)
    print("valorsConcat--------")
    print(valorsConcat)
    allCards = [eval7.Card(s) for s in valorsConcat.tolist()]
    
    cP = [Card(r,t) for r, t in cPlayer]
    cB = [Card(r,t) for r, t in cBoard]
    
    return HandEvaluator.evaluate_hand(cP, cB), eval7.handtype(eval7.evaluate(allCards))
    

"""        
cPlayer = [[4,1],[4,2]]
cBoard = [[6,1],[5,1],[7,1],[4,3],[8,1]]
cartesJug = ["4s","4h"]
cartesMaq = ["Ks","Qs","4c","4d","9s"]
#cartesJug = [Card(10,1),Card(11,1)]
#cartesMaq = [Card(7,1),Card(8,1),Card(9,1),Card(14,2),Card(14,3)]

puntuacio, nomCombo = comboJugador(np.array(cartesJug, dtype=object), np.array(cartesMaq, dtype=object), cPlayer,cBoard)
#comb = comboJugador(cartesJug, cartesMaq)
print(nomCombo)
print('{0:.50f}'.format(puntuacio))
#--------------------
"""



#funcio per canviar de dimensions una matriu en concret (funcio auxiliar)
def rectificar(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)
    
    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]
   
    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew

#funcio on detectem les cartesi els seus respectius ranks i tipus
def detectarCartes(thresh, img, numcards=2):
    
    #trobem contorns cartes
    contorn, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contorn = sorted(contorn, key=cv2.contourArea,reverse=True)[:numcards]  
    
    cartes = []
    ranks = []
    tipus = []
    
    #bucle per cada carta trobada
    for carta in contorn:
        #obtenim perimetre, al pasarli True li estem dient que es un area tancada
        perimetre = cv2.arcLength(carta,True)
        
        #aproximem una forma de contorn amb minim vertexs depenent de la presicio especificada
        epsilon = 0.1*perimetre #con 0.02 mejor?
        approx = cv2.approxPolyDP(carta,epsilon,True)
        pts = np.float32(approx)
        approxRect = rectificar(pts)
        
        #obtenim tamany carta
        xArr = np.int0(approxRect)[:,0]
        yArr = np.int0(approxRect)[:,1]
        
        x = np.amax(xArr, axis=0) - np.amin(xArr, axis=0)
        y = np.amax(yArr, axis=0) - np.amin(yArr, axis=0)
        
        
        
        #definir tamany final carta
        h = np.array([ [0,0],[x-1,0],[x-1,y-1],[0,y-1] ],np.float32)
                
        #Retallar carta en la imatge i despres aplicar transformacions per deixarla recta
        transf = cv2.getPerspectiveTransform(approxRect,h)
        cartaColor = cv2.warpPerspective(img,transf,(x,y))
        cartaGris = cv2.cvtColor(cartaColor,cv2.COLOR_RGB2GRAY)
        h,w,canal =  cartaColor.shape
        if w > h: 
            cartaGris = cv2.rotate(cartaGris, cv2.cv2.ROTATE_90_CLOCKWISE)
            cartaColor = cv2.rotate(cartaColor, cv2.cv2.ROTATE_90_CLOCKWISE)
        plt.imshow(cartaGris, cmap='gray', vmin=0,vmax=255)
        plt.show()
        
        plt.imshow(cartaColor)
        plt.show()
        
        #retallar cantonada ja que alla trobem el rank i el tipus
        retallCantonada = cartaGris[0:int(heigthCantonada*y/100), 0:int(widthCantonada*x/100)]
        #ampliem el tamany del retall per a tenir major zona a comparar
        zoomRetall = cv2.resize(retallCantonada, (0,0), fx=4, fy=4)
        
        #plt.imshow(retallCantonada, cmap='gray', vmin=0,vmax=255)
        #plt.show()
        
        #plt.imshow(zoomRetall, cmap='gray', vmin=0,vmax=255)
        #plt.show()
        
        #Mostrem la intensitat de píxels blancs que hi han per a determinar un bon nivell de llindar
        nivellBlancs = zoomRetall[15,int((widthCantonada*4*x/100)/2)]
        nivellThresh = nivellBlancs - CARD_THRESH
        if (nivellThresh <= 0):
            nivellThresh = 1
        retval, retallThresh = cv2.threshold(zoomRetall, nivellThresh, 255, cv2.THRESH_BINARY_INV)
        
        plt.imshow(retallThresh, cmap='gray', vmin=0,vmax=255)
        plt.show()
        
        #retallRank = retallThresh[20:125, 20:100]
        #retallTipus = retallThresh[125:300, 20:100]
        
        #Retallem una zon on posegur k esta el rank i el tipus de la carta, aquest param depen de la resolucio
        #aixo es podria fer mitjançant un % i la X i Y que hem trobat mes amunt
        print(y)
        print(x)
        retallRank = retallThresh[int(15*y/100):int(67*y/100), int(22*x/100):int(74*x/100)]
        retallTipus = retallThresh[int(67*y/100):int(150*y/100), int(22*x/100):int(74*x/100)]
        
        plt.imshow(retallRank, cmap='gray', vmin=0,vmax=255)
        plt.show()
        
        plt.imshow(retallTipus, cmap='gray', vmin=0,vmax=255)
        plt.show()
        
        #trobem amb el mateix procediment que hem fet amb la carta el rank
        contornsRank, hierarchy = cv2.findContours(retallRank, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contornsRank = sorted(contornsRank, key=cv2.contourArea, reverse=True)
        
        if len(contornsRank) != 0:
            xR,yR,wR,hR = cv2.boundingRect(contornsRank[0])
            retRank = retallRank[yR:yR+hR, xR:xR+wR]
            zoomRank = cv2.resize(retRank, (ZOOMW_RANK,ZOOMH_RANK), 0, 0)
            
            plt.imshow(retRank, cmap='gray', vmin=0,vmax=255)
            plt.show()
        
        #trobem amb el mateix procediment que hem fet amb la carta el rank
        contornsTipus, hier = cv2.findContours(retallTipus, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contornsTipus = sorted(contornsTipus, key=cv2.contourArea,reverse=True)
        
        if len(contornsTipus) != 0:
            xT,yT,wT,hT = cv2.boundingRect(contornsTipus[0])
            retTipus = retallTipus[yT:yT+hT, xT:xT+wT]
            zoomTipus = cv2.resize(retTipus, (ZOOMW_TIPUS, ZOOMH_TIPUS), 0, 0)
            
            plt.imshow(retTipus, cmap='gray', vmin=0,vmax=255)
            plt.show()
        
        #ho posem a les respectives llistes
        cartes.append(cartaColor)
        ranks.append(zoomRank)
        tipus.append(zoomTipus)
        
    return cartes, ranks, tipus

#funcio per detectar els valors, reb totes les imatges (imgRank i imgTipus) i els ranks i tipus detectats en les cartes
def detectarValors(imgsRanks, imgsTipus, ranks, tipus):
    
    respostaEv7= []
    respostaHandEv= []
    
    for r,t in zip(ranks,tipus):
        
        best_rank_match_diff = 1000000
        best_suit_match_diff = 1000000
        
        rImg = []
        sImg = []
        nomR = ""
        nomT = ""
        
        eval7Res = []
        handEvalRes = ""
        
        #per detectar el rank
        for rank, nom in imgsRanks:

            imgDiff = cv2.absdiff(r, rank)
            imgDiff = int(np.sum(imgDiff)/255)
                
            if imgDiff < best_rank_match_diff:
                best_rank_match_diff = imgDiff
                rImg = rank
                nomR = nom

        nomR = int(nomR);
        
        
        eval7Res.append(nomR)
        
        if nomR > 1 and nomR < 10:
            handEvalRes = str(nomR)
        elif nomR == 10:
            handEvalRes = "T"
        elif nomR == 11:
            handEvalRes = "J"
        elif nomR == 12:
            handEvalRes = "Q"
        elif nomR == 13:
            handEvalRes = "K"
        elif nomR == 14:
            handEvalRes = "A"

        # per detectar el tipus, fem el mateix que en els ranks
        for tip, nom in imgsTipus:
                
            imgDiff = cv2.absdiff(t, tip)
            imgDiff = int(np.sum(imgDiff)/255)
                
            if imgDiff < best_suit_match_diff:
                best_suit_match_diff = imgDiff
                sImg = tip
                nomT = nom
        
        nomT = int(nomT);
        
        eval7Res.append(nomT)
        
        if nomT == 1:
            handEvalRes = handEvalRes + "s"
        elif nomT == 2:
            handEvalRes = handEvalRes + "h"
        elif nomT == 3:
            handEvalRes = handEvalRes + "d"
        elif nomT == 4:
            handEvalRes = handEvalRes + "c"
        
        
        plt.imshow(rImg, cmap='gray', vmin=0,vmax=255)
        plt.show()  
        plt.imshow(sImg, cmap='gray', vmin=0,vmax=255)
        plt.show()
        
        respostaEv7.append(eval7Res)
        respostaHandEv.append(handEvalRes)
        
        
    return respostaEv7, respostaHandEv

def valorsCartesImg(img_roboot, numJug, nCartes):
    
    #zona jugador
    
    filIni = areas5jugC[numJug][0] #RETALLJUGADORS[numJug-1][0]
    filFi = areas5jugC[numJug][1] #RETALLJUGADORS[numJug-1][1]
    colIni = areas5jugC[numJug][2] #RETALLJUGADORS[numJug-1][2]
    colFi = areas5jugC[numJug][3] # RETALLJUGADORS[numJug-1][3]
    # areas5jugC[numJug][0]:numJug][1], numJug][2]:numJug][3]
    
    #retallem imatge i fem un flip (com si fos un mirall) perque la cam la veu al reves
    cut_img = img_roboot[filIni:filFi, colIni:colFi]
    #cut_img = cv2.flip(cut_img, 0)

    plt.imshow(cut_img)
    plt.show()  

    #binaritzem imatge retallada
    img_GRAY = cv2.cvtColor(cut_img, cv2.COLOR_RGB2GRAY)
    ret, cut_thresh = cv2.threshold(img_GRAY,150,255,cv2.THRESH_BINARY)

    #plt.imshow(cut_img, cmap='gray', vmin=0,vmax=255)
    #plt.show()
    #plt.imshow(cut_thresh, cmap='gray', vmin=0,vmax=255)
    #plt.show()
    
    #el retorn "card" no es fa servir
    cards, ranks, tipus = detectarCartes(cut_thresh,cut_img,nCartes)
    
    return detectarValors(imgsRanks, imgsTipus, ranks, tipus)
