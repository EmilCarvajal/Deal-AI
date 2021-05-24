# -*- coding: utf-8 -*-
#areas para cambio de fichas
areas5jug=[[300, 410, 710 , 850], #710 mod, de 680     
           [190 , 281 , 600,740 ] , #281 mod, de 300
           [160,260, 420,600],
           [200 , 300 , 320,415 ], #200 mod, de 210
           [280, 410, 210 , 300]]
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