# -*- coding: utf-8 -*-

#----- SL module and switch
import speakAndListen as sl
import random
from functools import partial
from DealAI_modulo_RFJ import *
#--- DealAI_MD_IK.py
from DealAI_modulo_IK_v3D import *

from change_module import *

#---- Modulo de Cartas VC
from ValoresCalc_VC_Cartas import *
#--- Vars Compartidas
from Variables_Main import *
# VARIABLES GLOBALES ------
global endBucle; endBucle = False
global nJug; nJug = 1
global dealer; dealer = 1
imssmi = get_image()
#--------------------------------------------------
#---TESTS INICIALES
#Colocar3CartasCentrales(); Standby()

#Colocar4CartaCentral();
#Colocar5CartaCentral(); Standby()
#get_image()
#valor_fichas,posicion = recogerFichasMonton(areas5jug[4] )#areas5jug[0])    # Robot coge fichas del area(aJug)
#l_cambio = cambiar_fichas_greedy(valor_fichas,1)                    #lista con el cambio
#dar_Cambio(l_cambio, posicion) 

#area_central = [110:175,175:370]
"""
x = 1
for p in pos_j:
    print('JUGADOR ', x)
    darCartaJugador(p[0],p[1], p[2])
    x+=1
"""
"""
#Colocar3CartasCentrales() 
Standby()
#----
quemarCarta()
Colocar4CartaCentral()
Standby()

#----
quemarCarta()
Colocar5CartaCentral()
Standby()
img_roboot = get_image()
"""
#---------------------------
# CASES NUM JUGADORES ------------------

def num_players(n):
    global nJug; nJug = n
    global endBucle; endBucle = True
    
def num_dealer(n):
    global nJug;
    if n == 0:
        n = random.randint(1, nJug)
    if n > nJug:
        error_num_players()
    else:
        global dealer; dealer = n
        global endBucle; endBucle = True
    
def error_num_players():
    sl.hablar("Numero de jugadores incorrecto")
    #sl.hablar("Han de haber entre 1 y 4 jugadores")

switch_players = {
    "dos" : partial(num_players, 2),
    "tres" : partial(num_players, 3),
    "cuatro" : partial(num_players, 4),
    "cinco" : partial(num_players, 5),
}

switch_dealer = {
    "uno" : partial(num_dealer, 1),
    "dos" : partial(num_dealer, 2),
    "tres" : partial(num_dealer, 3),
    "cuatro" : partial(num_dealer, 4),
    "aleatorio" : partial(num_dealer, 0),
}

def condWildRonda(listaHanJugado): 
    for x in listaHanJugado:
        if x == False:
            return False
    return True

def main_cambio(modo,actual_j):
    sl.hablar("Coloca tus fichas de cambio ")
    time.sleep(4)
    valor_fichas, posicion= recogerFichasMonton(areas5jug[actual_j-1])  
    if valor_fichas!=0: 
        l_cambio = cambiar_fichas_greedy(valor_fichas,modo) #modo 0 o 1                   
        dar_Cambio(l_cambio, posicion) 
        time.sleep(6)
    else: 
        print("Error Nsolve")
        sl.hablar("Error Nsolve")

#--------------------------
def main():
    #Pedir cantidad de jugadores
    #sl.hablar("De locos")
    """
    global endBucle; 
    #Pregunta al usuario hasta que dice un numero del rango que estamos buscando (1 - 4)
    sl.hablar("Buenos dias")
    endBucle = True
    while endBucle == False:

        sl.hablar("Numero de jugadores?")

        txt = sl.escucharJugador()
        
        switch_players.get(txt, error_num_players)()
    sl.hablar("Preparando tablero, no obstaculicen la zona de juego")
    """
    #--- main vo01_2
    Standby()
    ciega_pequeña = 5
    ciega_grande = 2*ciega_pequeña
    nJug = 5
    pos_j = posicionJugadores(5); 
    dealer = 2
    dealers_p = [x for x in range(1,nJug+1)]
    d_it = dealer-1

    MANO = 0
    ganadorP = False
    ### ------ BUCLE ENORME  DE MANOS ----
    while MANO < 3 and ganadorP == False:
        print("DP:", dealers_p)
        sl.hablar("MANO  " +str(MANO))
        print("MANO: ",MANO,"--------------")
        
        Ronda= 0
        players_p = dealers_p.copy()
        #players_p= [2,3]
        sl.hablar("El dÍler es el jugador" +str(dealer))
        # INICIO ---------
        #sl.hablar("La ciega pequeña es de"+str(ciega_pequeña)+" i la grande de"+str(ciega_grande))
    
        txt =0; a = 0; next_j = 2
        opciones = ["paso","voy","me retiro","subo","check","lo veo","igualo"]
        #--------------
        opciones_subir = [ str(5*x) for x in range(1,101)] #Numero multiples de 5
        
        #cop_Repartir_Cartas()
        
        # ----------- DETERMINAR QUIEN EMPIEZA ----- el +3 del de la pos del dealer o el +1 de la pos del dealer
        dealer_index = dealers_p.index(dealer)
        
        jugador_empieza_r0 = -1
        pos_cg = -1
        if len(dealers_p) == 2: # si solo hay 2 jugadores
            jugador_empieza_r0 = dealers_p[1]
            if dealer_index == 1:
                jugador_empieza_r0 = dealers_p[0]
            pos_cg = dealer_index # La ciega grande es el propio Dealer
        else:                  
            pos = dealer_index +3 
            if  pos >= len(dealers_p): # +1 ciega peque, +2 ciega grande, empieza +3
                pos = pos - len(dealers_p) 
    
            jugador_empieza_r0 = dealers_p[pos]
                
            #--------ciega grande -1 pos de  next_j o +2 pos del Dealer NO HACER CASO
            pos_cg = pos-1 
            if pos -1 < 0:
                pos_cg = len(dealers_p)-1
        #--------
        jugador_izquierda=-1
        if dealer_index +1 == len(dealers_p):
            jugador_izquierda = dealers_p[0]
        else:
            jugador_izquierda = dealers_p[dealer_index +1]
        ji_ind =dealer_index #jug izquierda index inicial 
        next_j = jugador_empieza_r0
        ganadorR = False
        
        while Ronda <4 and ganadorR == False: # RONDAS
            
            sl.hablar("RONDA  " +str(Ronda))
            print("RONDA: ",Ronda,"--------------")
            if Ronda != 0:  next_j = jugador_izquierda #jugador izuiqerda de dealer o si ha abandonado este, el siguiente
            it = players_p.index(next_j) 
            ha_jugado = [False for x in range(1,len(players_p)+1)]
            #--------
            if Ronda == 0: 
                sl.hablar(" el jugador " +str(dealers_p[pos_cg])+ " es la ciega grande")
                sl.hablar("Preparando tablero, no obstaculicen la zona de juego")

                #REPARTICION DE CARTAS M0 ---------      
                for p in players_p:                   
                    sl.hablar('DANDO CARTA A JUGADOR '+str(p))
                    darCartaJugador(pos_j[p-1][0],pos_j[p-1][1], pos_j[p-1][2])
                Standby()   
    
            elif Ronda == 1: 
                sl.hablar("Atencion!, Colocando cartas centrales")
                Colocar3CartasCentrales(); Standby()
            elif Ronda == 2: 
                sl.hablar("Atencion!, Colocando carta 4")
                quemarCarta();Colocar4CartaCentral(); Standby()
            elif Ronda == 3: 
                sl.hablar("Atencion!, Colocando carta 5")
                quemarCarta();Colocar5CartaCentral(); Standby()
            sl.hablar("empieza el jugador " +str(next_j))
           
            opciones = ["paso","voy","me retiro","subo","check","lo veo",
                            "siguiente", "cambio a la alta","cambio a la baja","abandono", "retiro"]
            while condWildRonda(ha_jugado) == False:   #txt != "siguiente": # dentro de 1 mano
                txt = 0
                sl.hablar("Turno del jugador " +str(next_j))
                actual_j = next_j
                print("- ...........")
                print("- TURNO DEL JUGADOR: ",actual_j)
                actual_j_pos = it #-1 por la pos de la lista
                print("actual_j_pos: ", actual_j_pos)
            
                
                while txt not in opciones:
                    txt = sl.escucharJugador()
                
                se_ha_retirado = False
                if txt == "me retiro" or txt == "abandono" :
                    #-- Caso retiro, se aplica tambien si se abandona  ----  
                    se_ha_retirado = True
                    players_p.remove(actual_j)
                    ha_jugado.pop(actual_j_pos)
                    print("len: ",len(players_p))
                    if it == len(players_p):
                        next_j = players_p[0]
                        it=0
                    else:
                        next_j = players_p[it]
                    if 1 == len(players_p):
                        sl.hablar("Ganador jugador MANO : "+str(players_p[0]))
                        ganadorR = True
                        break
                    #-- Caso abandono ----    
                    if txt == "abandono":
                        dealers_p.remove(actual_j)

                        if 1 == len(dealers_p):
                            sl.hablar("Ganador jugador POKER "+str(players_p[0]))
                            ganadorP = True
                            break
                    #-- Si abandona el jugador de la izquierda se actualiza jugIz i index
                    if actual_j == jugador_izquierda:
                        if ji_ind +1 == len(players_p):
                            jugador_izquierda = players_p[0]
                        else:
                            jugador_izquierda = players_p[ji_ind +1]
                        ji_ind = players_p.index(jugador_izquierda)
                        
                elif it == len(players_p)-1:
                    next_j = players_p[0]
                    it=0
                else:
                    it+=1
                    next_j = players_p[it]
                #----Cambios
                if txt == "cambio a la baja":
                    main_cambio(0,actual_j)
                    while txt not in opciones:
                        txt = sl.escucharJugador()
                elif txt == "cambio a la alta":
                    main_cambio(1,actual_j)
                        
                    while txt not in opciones:
                        txt = sl.escucharJugador()
                        
                
                if txt == "subo":
                    sl.hablar("Cuanto subes?")
                    print("Cuanto subes?")
                    while txt not in opciones_subir:
                        txt = sl.escucharJugador()
                    ha_jugado = [False for x in range(1,len(players_p)+1)] # Reseteamos FALSE a todos
                
                print(txt)
                if se_ha_retirado == False:
                    ha_jugado[actual_j_pos] = True
                print("PP:",players_p)
                print(ha_jugado)
                time.sleep(1)
                
            if Ronda ==3: #Ronda Final
                sl.hablar("Jugadores, muestren sus cartas ")
                time.sleep(15) # -9.0006e+01   Gamma
                ganador, combo_ganador = decirGanador(players_p) #modulo VC+ Algoritmo combinaciones (Jofre)
                sl.hablar("EL GANADOR es el jugador "+str(ganador))
                print("Ganador de Ronda:", ganador )
                sl.hablar("EL COMBO GANADOR ES "+str(combo_ganador))
                sl.hablar("Jugador "+str(ganador)+"recoge tus ganacias")
                sl.hablar("Fin de MANO, Recojan las cartas de la mesa")
                time.sleep(6)
                
            Ronda+=1     
        
        if d_it == len(dealers_p)-1:
            dealer = dealers_p[0]
            d_it=0
        else:
            d_it+=1
            dealer = dealers_p[d_it]
        
        MANO+=1
    sl.hablar("POKER FINALIZADO")
    print("----POKER FINALIZADO----")
   
    
    
    ###################### codigo para repartir cartas jugadores y fichas turno 1

    #REPARTICION DE CARTAS M0 --------- 
    """
    pos_j = posicionJugadores(nJug)
    x = 1
    for p in pos_j:
        print('JUGADOR ', x)
        darCartaJugador(p[0],p[1], p[2])
        x+=1
    """
    #Standby() # Posicion Base Robot
    
    ##################### declaracion dealer, opciones: nº jugador o random ("aleatorio")
    #endBucle = False
    
    
    """
    if MANO == 0:
        switch_dealer.get("Aleatorio", error_num_players)()
    else:
        dealer = dealers_p[dealer]  # 
    sl.hablar("El diler es el jugador" +str(dealer))
    ################# apuesta menor, apuesta mayor y ronda de apuetas hasta que todos hayan apostado la misma cantidad
    
    # INICIO ---------
    sl.hablar("La ciega pequeña es de"+str(ciega_pequeña)+" i la grande de"+str(ciega_grande))

    txt =0; a = 0; next_j = 2
    opciones = ["paso","voy","me retiro","subo","check","lo veo","igualo"]

    players_p = [x for x in range(1,nJug+1)]
 
    while Ronda <4 : 
        # ----------- DETERMINAR QUIEN EMPIEZA ----- el +3 del de la pos del dealer o el +1 de la pos del dealer
        dealer_index = dealers_p.index(dealer)
        if Ronda = 0:
            if  dealer_index +3 >= len(dealers_p): # +1 ciega peque, +2 ciega grande, empieza +3
                pos = dealer_index +3 - len(dealers_p) 
            else:
                pos = dealer_index +3 
            next_j = dealers_p[pos]
            
            #--------ciega grande -1 pos de  next_j o +2 pos del Dealer NO HACER CASO
            
            if pos -1 < 0
                pos_cg = len(dealers_p)
            else:
                pos_cg = pos-1  
            
        else:
            if dealer_index +1 == len(dealers_p):
                next_j = dealers_p[0]
            else:
                next_j = dealer_p[dealer_index +1]
        it = next_j-1      
         # ----------- DETERMINAR CIEGA grande----- el +2 del de la pos del dealer       
                
        ha_jugado = [False for x in range(1,players_p+1)]
        #ha_jugado[pos_cg] = True #  La ciega grande  NO HACER CASO
        elif Ronda == 1: Colocar3CartasCentrales(); Standby()
        elif Ronda == 2: quemarCarta();Colocar4CartasCentrales(); Standby()
        elif Ronda == 3: quemarCarta();Colocar5CartasCentrales(); Standby()

        while txt != "siguiente": # dentro de 1 mano
            txt = 0    
            actual_j = next_j
            print("---- TURNO DEL JUGADOR: ",actual_j)
            actual_j_pos = it #-1 por la pos de la lista
        
            opciones = ["paso","voy","me retiro","subo","check","lo veo",
                        "siguiente", "cambio a la alta","cambio a la baja", "abandono"]
            
            while txt not in opciones:
                txt = sl.escucharJugador()
                
            if txt == "me retiro":
                players_p.remove(actual_j)
                print("len: ",len(players_p))
                if it == len(players_p):
                    next_j = players_p[0]
                    it=0
                else:
                    next_j = players_p[it]
                if 1 == len(players_p):
                    sl.hablar("Ganador jugador "+str(players_p[0]))
                    
            elif it == len(players_p)-1:
                next_j = players_p[0]
                it=0
            else:
                it+=1
                next_j = players_p[it]
            
            if txt == "cambio a la baja":
                valor_fichas,posicion = recogerFichasMonton(areas5jug[actual_j])    # Robot coge fichas del area(aJug)
                l_cambio = cambiar_fichas_greedy(valor_fichas,0)                    #lista con el cambio
                dar_Cambio(l_cambio, posicion)
                time.sleep(6)                                      #Robot da el cambio
            elif txt == "cambio a la alta":
                valor_fichas, posicion= recogerFichasMonton(areas5jug[actual_j-1])  
                l_cambio = cambiar_fichas_greedy(valor_fichas,1)                   
                dar_Cambio(l_cambio, posicion) 
                time.sleep(6)
            time.sleep(3)
            print ("Fichas Banco:")  
            for f in fichasTotales_Banco:
                print (f,": ",fichasTotales_Banco[f])
            print(players_p)
        
        Ronda+=1
    """
    ################################## codigo para repartir las 3 cartas de la "banca"
    
    

    ################################## codigo siguiente turno
    
    #Notas: se puede hacer todo con un switch?
    #Explicacion: bucle infinito que este escuchando al usuario en todo momento
    #tener guardado en unas variables el turno del jugador, si ya han apostado todos la misma cantidad y ronda por la que vamos
    #si alguien dice "cambio de turno o finalizar turno" por ejemplo, se aumenta el turno de jugador para que pueda hacer cambio de fichss, apostar, retirarse, ...
    #si alguien dice "cambio" se hace cambio de fichas del jugador que esta jugando ahora mismo cuyo turno tenemos guardado su turno en una variable
    #si al hacer el cambio de turno de jugador todo el mundo ha apostado la misma cantidad, automaticamente se funaliza la ronda y se pasa a la siguiente
    
    ##########################################
    
    
if __name__ == "__main__":
    main()