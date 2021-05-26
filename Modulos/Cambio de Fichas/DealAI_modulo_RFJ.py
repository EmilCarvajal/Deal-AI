# -*- coding: utf-8 -*-

"""
MODULO QUE RECOJE LAS FICHAS DE 1 JUGADOR APILADAS EN UNA ZONA
"""
from Variables_Main import *
####################################################
from DealAI_modulo_ReconFichasVC import *
############################################
"""
global n_FAzul;      n_FAzul = 8
global n_FVerdes;    n_FVerdes = 8
global n_FVermelles; n_FVermelles = 8
global n_FBlanques;  n_FBlanques = 8
global n_FNegres;    n_FNegres = 8
"""

#areas5jug = [[250, 410, 680 , 880],[150 , 300 , 600,780 ],
            # [160,260, 420,600],[150 , 300 , 258,415 ],[250, 410, 170 , 300]]
"""
AREAS DONDE SE VEN LAS CARTAS DE CADA: 5JUGADORES (PARA JOFRE)
j1 = [175, 410, 780 , 1012]
j2 = [20 , 250 , 630,860 ]
j3 = [20,200, 400,640]
j4 = [20 , 250 , 180,420 ]
j5=  [175, 394, 30 , 258]

"""
"""
#areas para cambio de fichas
areas5jug=[[300, 410, 710 , 850], #710 mod, de 680     
           [190 , 281 , 600,740 ] , #281 mod, de 300
           [160,260, 420,600],
           [200 , 300 , 320,415 ], #200 mod, de 210
           [280, 410, 210 , 300]]
"""
"""
c1=  [250, 410, 170 , 300]
c2 = [150 , 300 , 258,415 ]
c3 = [160,260, 420,600]
c4 = [150 , 300 , 600,780 ]
c5 = [250, 410, 680 , 880]
fn = c2
"""
def recogerFichasMonton(area):   #Recoge las fichas de 1 jugador y devuelve el Valor total sumado
    global fichasTotales_Banco 

    Suma_valor_fiches = 0
    f_inicial = area[0]#325   #100 margen [175: 394, 30 : 258] [250: 410, 170 : 300]
    f_final   = area[1] #425
    c_inicial = area[2]#700  #150 margen
    c_final   = area[3]#850
    
    img_Robot = get_image()
    color_chip, cx, cy = valorFichas(img_Robot[f_inicial:f_final,c_inicial:c_final])
    q=[0,0,0]
    while color_chip != 0:
        
        base = 0
        inv = 1  #depenede de la posicion de los objetos, derecha o izquierda
        co = 0
        if c_inicial +cx >= 512:
            base = c_inicial-512
            co = 1
        else:
            base = c_inicial
        inv = 1
        
        xi = ((base+ cx)) #1024-791     ((550col inicial imagen-512col medio sensor vision) + cx obejto)
    
        yi = (f_inicial)+cy  #(512 - 289)    (70 fila inicial imagen + cy obejto)
        if co ==1:
            x = N(xi*0.5/512,3)*inv   
        else: x = N(0.5-xi*0.5/512,3)*inv
        y = N(0.5-yi*0.5/512,3)
        print(xi,yi)
        print(x,y)
        subir_brazo(0.08)
        if co ==0:
            print("darCartaIzquierda")
            q = darCartaDerecha(-x, y)
            """
            z = 0.2
            z= z + 0.021
            eq1,eq2,eq3=ecuaciones(x,y,z)
            try:
                q=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=4)
            except:
                try:
                    q=nsolve((eq1,eq2,eq3),(theta1,theta2,d3),(1,1,1),prec=5)
                except:
                    print("No hay solución")
                    q=0
                    Standby()
                    print(q)
            if q != 0: mov_brazo(q)
            else: return 0,0
            """
        else: 
            print("darCartaDerecha")
            q = darCartaDerecha(x, y) #print(x,y)
        subir_brazo(0.13)
        if co==1:
            time.sleep(8)
        else:
            time.sleep(8)
        bajar_brazo(-dist_object()+0.084)
        time.sleep(2)
        CogerItem(False)
        time.sleep(1)
        
        subir_brazo(0.0)
        time.sleep(1)
        count_c = 0
        if color_chip == "red":
            CogerFichaRoja()
            count_c = fichasTotales_Banco[2]
            Suma_valor_fiches = Suma_valor_fiches+50
            fichasTotales_Banco[2]+=1
        elif color_chip == "green":
            CogerFichaVerde()
            count_c = fichasTotales_Banco[3]
            Suma_valor_fiches = Suma_valor_fiches+25
            fichasTotales_Banco[3]+=1
        elif color_chip == "blue":
            CogerFichaAzul()
            count_c = fichasTotales_Banco[4]
            fichasTotales_Banco[4]+=1
            Suma_valor_fiches = Suma_valor_fiches+10
        elif color_chip == "black":
            CogerFichaNegra()
            count_c = fichasTotales_Banco[1]
            fichasTotales_Banco[1]+=1
            Suma_valor_fiches = Suma_valor_fiches+100
        elif color_chip == "white":
            CogerFichaBlanca()
            count_c = fichasTotales_Banco[0]
            fichasTotales_Banco[0]+=1
            Suma_valor_fiches = Suma_valor_fiches+5
            
        #subir_brazo(0.13) 
        subir_brazo(0.0)
        time.sleep(3)
        f = (count_c+1) * 0.005
        print(count_c)
        time.sleep(2)
        #bajar_brazo(-(0.083-f))
        #bajar_brazo(-(0.083-0.050))
        #bajar_brazo(-(0.035))
        #bajar_brazo(-(0.035))
        #bajar_brazo(-(0.035))
        #bajar_brazo(0.0)
        bajar_brazo(-(0.090-f))
        time.sleep(5)
        DejarItem()
        time.sleep(3)
     
        subir_brazo(0.0)
        img_Robot = get_image()
        color_chip, cx, cy = valorFichas(img_Robot[f_inicial:f_final,c_inicial:c_final])
        
    return Suma_valor_fiches, q
#a,v = recogerFichasMonton(areas5jug[1])

#a,c = recogerFichasMonton(areas5jug[1]) 
#s =3