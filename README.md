# [ROBOTICA] Deal-AI
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/img_portada.JPG" align="right" width="300" alt="header pic"/>

Brazo mecánico que  permite actuar como  Dealer o Croupier en el juego del  Poker, concretamente la modalidad de Texas Holdem.
También ayuda a controlar el estado de la partida.


# Tabla de Contenidos
* [Descripción de proyecto](#descripción-del-proyecto)

* [Amazing contributions](#amazing-contributions)

* [Esquema Hardware](#esquema-hardware)	

* [Piezas 3D](#piezas-3d)

* [Arquitectura software](#arquitectura-software)

* [Módulos](#módulos)
  * [Módulo de Jugadores](#módulo-de-jugadores)  <br>
  * [Módulo de cinemática inversa](#módulo-de-cinemática-inversa)  <br>
  * [Módulo de visión por computador](#módulo-de-visión-por-computador)  <br> 
       * [Detección de cartas](#detección-de-cartas)  <br>
       * [Detección de fichas](#detección-de-fichas)  <br>
  * [Módulo de inteligencia artificial](#módulo-de-inteligencia-artificial) <br>
       * [Main](#main) <br>
       * [Módulo de cambio](#módulo-de-cambio) <br>
* [Vídeo](#vídeo)

* [Autores](#autores)

# Descripción del proyecto	
DEAL_AI es un robot que ayuda a dirigir el estado de una partida del clásico juego de cartas Poker actuando como Dealer o Croupier.
Básicamente consiste en un brazo mecánico de 4 ejes con la misma estructura de un robot SCARA que tiene acoplada una ventosa para poder distribuir las fichas y las cartas que están en juego. Este robot está diseñado para una mesa semicircular la cual está adaptada a su zona de trabajo.  Existe un componente situado al lado de la base el cual le permite girar las cartas simplemente soltándolas por encima del objeto. Para reconocer las fichas y las cartas tiene una cámara colocada en una torre central elevada.
Sus principales funciones son:
*	Funciones de Dealer: 
       *	Flop (mostrar las 3 cartas)
       * Mostar las 5 cartas
       * Voltear cartas
       *	Repartir cartas 
*	Intercambio de fichas mediante IA
*	Realizar movimientos y responder preguntas (órdenes captadas por reconocimiento de voz)
* Declarar ganador por medio de visión por computador.

# Amazing contributions
Gracias a su adaptación para permitir cualquier número de jugadores, DEAL_AI puede ser utilizado en partidas amateurs o en partidas profesionales.
En cuanto a las partidas amistosas o hechas por principiantes, el robot permite a los jugadores tener una mayor comprensión del juego gracias a su seguimiento por comandos de voz y a su automatización en el intercambio de fichas. 
Para los jugadores profesionales, es ideal tener un crupier robótico, pues uno de los mayores problemas en el póker es la realización de [trampas](https://www.pokernews.com/news/2020/05/the-muck-bill-perkins-dan-cates-alleged-cheating-37330.htm) en medio de la partida. Se han dado casos donde el jugador que repartía cartas (en caso de no haber crupier) realizaba trampas para manipular las cartas que recibía cada jugador y, en otras ocasiones, un jugador estaba [compinchado con el crupier](https://www.straitstimes.com/singapore/courts-crime/rws-casino-croupier-and-patron-charged-with-cheating), por tanto este manipulaba las cartas que repartía a cada jugador.
Además, gracias a su movilidad automatizada y adaptable a las circunstancias de la partida, DEAL_AI tiene acceso a todos los rincones de la zona de juego, así pues en mesas grandes donde un jugador debe realizar un esfurezo físico para alcanzar la zona, lo que puede suponer un problema sobretodo para gente mayor, con discapacidad o problemas físicos, el robot es capaz de alcanzar las cartas y las fichas de cada jugador, ahorrandoles este esfuerzo inecesario para disfrutar de la partida de póker.

# Esquema Hardware
El proyecto en cuestión roza los 100€ de presupuesto con componentes de media calidad. Es necesario que 3 de los servo-motores sean capaces de realizar una rotación de 360º. Cabe destacar que, cuanto mayor sea la definición de la cámara, más se reducirá la tasa de error del robot al realizar la detección de fichas y, sobretodo, de cartas: Recomendamos una cámara capaz de grabar en Full HD.

<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/esquema_hardware.jpg" align="center" width="600" alt="header pic"/>

# Piezas 3D
Para la realización de este proyecto, se han utilizado las siguientes piezas 3D:

**Componentes unidos del brazo robótico (total de 4 piezas por separado).**
<br>
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/brazo.JPG" align="center" width="400" alt="header pic"/>
<br>
<br>

**Base personalizada para colocar la baraja de cartas.**
<br>
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/base_cartas.JPG" align="center" width="400" alt="header pic"/>
<br>
<br>

**Pieza que permite al robot voltear las cartas.**
<br>
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/flipeador.JPG" align="center" width="400" alt="header pic"/>
<br>
<br>

**Mesa semicircular utilizada en el simulador como zona de juego (no se ha de imprimir en caso de realizarlo en la vida real).**
<br>
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/mesa.JPG" align="center" width="400" alt="header pic"/>
<br>
<br>
Todas y cada una de estas piezas se encuentran en la carpeta **Objetos STL** de este mismo repositorio. No obstante, las dimensiones de los objetos NO SON CORRECTAS, simplemente conservan las buenas proporciones y relaciones de tamaño, pero en caso de querer utilizarlos se ha de tener en cuenta que se han de escalar al tamaño deseado. En nuestro caso, al utilizar un simulador y trasladarlo todo a centímetros (por temas de capacidad de ejecución y limitación de los própios ordenadores), se han escalado la gran mayoría de piezas a un ratio de entre 0.001 y 0.01 de su tamaño original.

# Arquitectura software
Destacamos un total de 4 módulos imprescindibles en este proyecto los cuales, al sincronizarse, permiten al robot realizar un seguimiento eficiente de la partida de póker que se esté llevando a cabo. Dichos módulos son:
* Módulo de jugadores: Reconocimiento de comandos de voz (inputs) que permiten al robot poder avanzar en la partida o la acción a realizar en cada momento. También permite a los jugadores consultar dudas básicas que tengan.
* Módulo de cinemática inversa: Movimiento absoluto del robot, ya sea para repartir cartas, intercambiar fichas o dar la vuelta a las cartas. Este módulo en particular también permite la reorientación correcta de las cartas.
* Módulo de visión por computador: Reconocimiento de fichas y cartas. Es capaz de detectar el valor de las fichas estándar de póker (colores blanco, azul, verde, rojo, negro) y el valor y palo de las cartas.
* Módulo de inteligencia artificial: Representa el cerebro del robot, el cual recibe los inputs de los demás módulos y genera los outputs que necesitan los demás módulos.
* Controladores: Estos relacionan los demás módulos entre si y permiten una perfecta sincronización entre ellos para poder efectuar las acciones necesarias.

<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/esquema_software.jpg" align="center" width="600" alt="header pic"/>

# Módulos
## Módulo de jugadores
Representa el colectivo de seres humanos que están realizando una partida con el Deal AI. Estos son los que generarán los inputs principales, los cuales permitirán determinar al robot qué algoritmo utilizar y con qué módulos operar.

Para poder permitir esta interacción entre el boto y los jugadores, se han utilizado los módulos/librerías:
* speech_recognition (para el reconocimiento de voz, así dando la oportunidad de controlar las acciones del robot). 
> pip install SpeechRecognition
* gTTS (para poder leer con voz sintética (text-to-speech) las respuestas dadas por el robot)
> pip install gTTS
* playsound (para poder reproducir sonidos y poder leer los resultados obtenidos por el gTTS).
> pip install playsound

## Módulo de cinemática inversa
En este módulo se aplicará a los servo-motores los ángulos calculados para permitir al robot alcanzar el objeto o la posición deseada rotando sus ejes principales. Básicamente tras haber establecido la posición (módulo IA) el controlador ordenará a los componentes hardware la cinemática a realizar.

Lo principal para poder empezar a desplazar nuestro robot hacia las posiciones deseadas, es calcular las ecuaciones de movimiento del robot mediante una tabla de Denavit Hartenberg (tabla de D-H).

Para ello, hacemos los correspondientes cálculos en función de la diferencia entre las distancias y orientaciones de un servo-motor y otro. Al aplicar los cálculos correctos, obtenemos la siguiente matriz resultante para el cálculo de la cinemática inversa de un robot SCARA de 4 ejes:  

<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/DHscara4ejes.JPG" align="center" width="800" alt="header pic"/>

En esta ecuación conocemos los valores de la, lb, lc y l4 que equivalen a la distancia de cada brazo o link. Los datos que desconocemos son ϑ1, ϑ2, ϑ4 y d3, que equivaldrían a los ángulos de rotación de los servo-motores 1, 2 y 4 (los cuales son rotacionales) y la altura a la que está situada el manipulador (controlado por el servo-motor 3 que es de tipo prismático). Para saber qué rotación hay que aplicar a cada eje, utilizamos la última columna para realizar un sistema de ecuaciones que, al resolverlo, nos determinará las rotaciones a aplicar en cada eje. No obstante, si queremos saber la rotación correspondiente para punto geométrico (x, y, z), debemos restar estos valores a su ecuación correspondiente (la primera fila corresponde a la 'x', la segunda a la 'y' y la tercera a la 'z').

En nuestro caso utilizamos la librería sympy.
> import sympy as sp  
> from sympy import *

Dicha librería nos permite obtener una representación más visual de las ecuaciones y utilizar funciones de resolución de sistemas de ecuaciones para encontrar las incógnitas. En nuestro caso, mediante la matriz de DH mostrada previamente:
> nsolve(matrix, (theta1,theta2,d3,theta4),(1, 1, 1, 1))

Para facilitar la faena de los programadores, se crean módulos estándar que serán utilizados en las funciones principales, así pues, para repartir cartas a un jugador, en vez de reescribir el código de cinemática inversa, se utiliza un módulo de movimiento estándar que es llamado por la función de mayor nivel.

Con este sistema establecido, generamos las siguientes funciones de alto nivel:

*	**PosicionJugador(nJugadores):** Se pasa como parámetro ‘nJugadores’ que corresponde al número de participantes que jugarán a póker. La función calcula y devuelve las posiciones geométricas de cada jugador y el ángulo correspondiente (entre 90 y -90 grados porque es una mesa semicircular y el robot está orientado en el ángulo 0 grados).

<img src="https://github.com/EmilCarvajal/Deal-AI/blob/main/img/gifdarCartas.gif" align="right" width="300" alt="header pic"/>

*	**DarCartaJugador(x, y, angulo):** Se pasa como parámetro la posición central de un jugador. En esta función se le suma y resta a esta posición un coeficiente pequeño que determina la separación entre una carta y otra, pues en esta modalidad de póker ser reparten dos cartas a cada jugador. Una vez aplicado este cálculo, se determina de la posición central un total de 2 posiciones, que equivalen a las posiciones de cada carta. Puesto que se colocan las cartas de los jugadores en el perímetro del área, al colocar el eje rotacional en el ángulo 0 grados, las cartas quedan orientadas apuntando hacia el centro de la mesa.

*	**RevelarCartasCentrales():** En esta función se revelan las cartas correspondientes cuando da inicio una nueva ronda. En esta modalidad de póker, se revelan un total de 5 cartas: 3 cartas en la primera ronda, 1 carta en la segunda y 1 carta en la tercera.

<img src="https://github.com/EmilCarvajal/Deal-AI/blob/main/img/gifFlipeador.gif" align="right" width="200" alt="header pic"/>

* **Ir_a_flipeador():** Tras analizar y probar varios modelos de piezas 3D que permitan voltear una carta automáticamente, hemos encontrado la pieza necesaria para lograrlo. Tras situar la pieza en un lugar específico de la zona de juego, el brazo robótico únicamente debe colocar encima de la pieza la carta que desea voltear, rotando dicha carta para que quepa en la entrada y se voltee automáticamente, deslizándose hasta una pequeña zona donde se recogerá la carta.

*	**QuemarCarta():** En muchos juegos de cartas de apuestas antes de repartir cartas o de revelar cartas se realiza una acción denominada como “quemar carta” que simplemente consta en coger la primera carta del mazo y colocarla en una pila de descartes.

**Problema 1:** La función ‘nsolve’ muestra problemas para encontrar el camino óptimo que ha de recorrer el robot y, en ciertas ocasiones para llegar a la coordenada de destino realiza más vueltas de las necesarias (gira más de 360 grados).

**Solución 1:** En el módulo del cálculo de la cinemática inversa se aplica el módulo a la solución para así obtener un resultado entre 0 y 360 grados:

> angulo=angulo % 2π

En este caso, ‘angulo’ es el parámetro que nos devuelve la función ‘nsolve’ que equivaldría a la rotación que debería ejercer el servo-motor para alcanzar la coordenada en cuestión. 2π equivale a 360 grados en radianes.

**Problema derivado 1.1:** La operación módulo (%) no tiene en cuenta el signo del ángulo, es decir, si la variable ‘angulo’ es positiva, el resultado será positivo, pero en caso de ser un valor negativo, el resultado que devuelve es positivo cosa que no nos interesa, pues hay una gran diferencia entre girar 45 y -45 grados.

**Solución 1.1:** Puesto que no hay ninguna función que permita realizar la operación de módulo devolviendo el signo correcto, se detecta el signo antes de aplicar la operación y, en caso de ser negativo, se calcula el módulo con el valor positivo y luego se negativiza el resultado.

**Problema derivado 1.2:** La variable ‘angulo’ ahora está comprendida entre 0 y 360 grados, pero en ciertas ocasiones el brazo gira casi 360 grados para acceder a una posición cercana si se desplazara en dirección contraria. Por ejemplo, si el robot quiere situarse en el centro del 4to cuadrante (cuadrante (x, -y) entre los ángulos 270 y 360) podría acceder de manera rápida si rotara -45 grados, pero la función nos devuelve un valor de 315, por tanto el brazo rota un total de 315 grados lo cual no es óptimo.

**Solución 1.2:** Los brazos robóticos con capacidad de rotación de 360 grados pueden dividirse en dos zonas de movimiento óptimo: de 0 a 180 grados y de 0 a -180 grados (que equivaldría a la zona comprendida entre 180 y 360 grados). Si el robot quiere rotar 181 grados, es más eficaz que rote -179 grados, pues llegará a la misma posición rotando menos grados. Por tanto, se determina un condicional que si detecta que la variable ‘angulo’ supera los 180 grados (que en radianes equivale a π), entonces se le resta 360 grados a ‘angulo’ (equivalente a 2π), así pues, en el mismo caso de antes, si tenemos 181 grados y le restamos 360, obtenemos -179 que sería nuestro ángulo óptimo.

**Solución final:** Juntando todas estas soluciones, obtenemos un módulo capaz de corregir cualquier ángulo y transformarlo en uno óptimo (si es que no lo era antes):

Cuanto a los módulos de bajo nivel, mencionamos algunos que creemos que son interesantes mencionar:
* **CogerItem():** Activa la válvula de vacío.
* **CogerCarta():** Automatiza la acción de coger una carta de la baraja (utilizando la función CogerItem()).
* **DejarItem():** Desactiva la válvula de vacío.

## Módulo de visión por computador:
Entendemos este módulo como el que recoge la información de la situación en la zona de juego. Dicha información se utilizará posteriormente para poder establecer las posiciones de los elementos a manipular por el robot (cartas y fichas) y para que pueda determinar la situación en tiempo real de la partida (reconocimiento de las cartas).

Finalmente, para este módulo se ha decidido hacerlo junto con el proyecto final de la asignatura “Visión por Computador”. El robot será capaz de detectar tanto cartas como fichas. Además de detectarlos podrá saber sus valores concretos.

### Detección de cartas
Se ha limitado una zona para cada jugador donde se encontrarán las cartas y fichas correspondientes de cada jugador. Se ha implementado una función llamada “**detectarCartes()**” que se le pasan por parámetro la región de la imagen del jugador recortada y otra igual pero binarizada (en blanco y negro) y la cantidad de cartas que se esperan que se detecten (2 si son la de los jugadores y 5 si son las de la máquina). Esta función se encarga de tractar las imágenes que recibe para devolver 3 vectores, el primero contiene una imagen de cada carta, el segundo una imagen del rango / valor de las cartas detectadas (A, 1, 2, 3, …, Q,K) y el tercero contiene una imagen del palo de cada carta detectada (corazón, picas, tréboles, rombos).  
<img src="https://github.com/EmilCarvajal/Deal-AI/blob/main/img/Card.gif" align="right" width="300" alt="header pic"/>
También, se ha implementado una función llamada “**detectarValors()**” que recibe las imágenes de los valores y tipos obtenidos en la función “**detectarCartes()**” y un dataset de valores de cartas y un dataset de valores de palos de Póker. En esta función se usan los dataset que se pasan por parámetro para clasificar los palos y valores de cada una de las imágenes que también recibe y devolver 2 vectores en un formato específico para posteriormente determinar quién es el ganador.  
Para poder saber quién es el ganador, se ha implementado una función llamada “**comboJugador()**” que mediante los vectores que devuelve “**detectarValors()**” le da una puntuación al jugador sobre la mano que tiene y con qué combo (pareja, doble pareja, escalera, …) ha obtenido esa puntuación (el jugador que obtenga la mayor puntuación será el ganador).


### Detección de fichas
Para esta detección, no se utilizan las mismas zonas que para las cartas porque estas no coinciden con la zona natural donde un jugador podría dejar sus fichas (entendemos que un jugador no situaría las fichas que quiere cambiar encima de sus cartas sino un poco más alejado de ellas). Así pues, antes de que el robot las detecte, sume su valor y pueda recogerlas y llevarlas a la banca de fichas para su intercambio, lo primero que se ha realizar es determinar las áreas de cambio.  
Se ha creado la función "**valorFichas(img_Robot)**" que se encarga de determinar el valor de una ficha. Esta recibe una imagen de la área determinada por el jugador que pide cambio de fichas. La imagen contiene varias fichas, pero al estar apiladas solo ve la que está más por encima.
Los pasos que emplea son:
*	Eliminación del ruido 
*	Encuentra el área del fondo 
*	Encuentra el área segura que pertenece a la ficha
*	Encuentra la región desconocida (bordes)
*	Etiquetado de las manchas que detecta
*	Adiciona 1 a todas las etiquetas para asegurra que el fondo sea 1 en lugar de cero
*	Se marca la región desconocida con ceros
*	Utiliza técnica “watershed” para dividir las manchas
*	Se binariza la imagen
*	Buscamos los contornos las manchas restantes con la función cv2.findContours()
*	Recortamos la mancha
*	Le añadimos brillo mediante la función increase_brightness()
*	Realizamos una media de pixeles y vemos que color es más cercano para asociarle

![2](https://github.com/EmilCarvajal/Deal-AI/blob/main/img/gif_fichas2.gif)

## Módulo de inteligencia artificial
### Main
Este es el núcleo del robot, donde todos los inputs son transmitidos a este módulo el cual se encargará de dar una serie de órdenes al robot. Estas órdenes pasarán por su controlador en concreto y establecerá una acción: o bien utilizará el altavoz para dar un mensaje a los jugadores o bien realizará un movimiento para alcanzar una posición calculada previamente.

Este main representa el sistema del juego Póker en la modalidad Texas Holdem pero con ciertos cambios que permiten que se adapte a una partida cotidiana entre amigos.
Por eso, cada jugador empieza con una cantidad de fichas determinadas. El sistema está organizado por “Manos” y “Rondas”. Denominamos Manos a 4 Rondas completas donde en la última se decide quién es el jugador que ha ganado la Mano y se lleva todo el dinero situado en el bote. Un Ronda es terminada cuando todos los jugadores activos de la Mano han apostado la misma cantidad de fichas. En la Ronda 0 se reparten las cartas y se realizan las apuestas iniciales, en la Ronda 1 se colocan 3 cartas centrales en la mesa y en la ronda 2 y 3 se “quema” una carta y se coloca otra junto a las centrales. “Quemar” una carta no es más que coger una carta y descartarla colocándola en una pila de descartes.
El sistema controla la secuencia de juego y mantiene el estado de los jugadores que no se han retirado para pasar a la siguiente ronda. 
Controla en todo momento los jugadores que están activos y los que han abandonado la mesa (no se contemplan para las siguientes Manos y no se les reparte cartas).

Cuando es el turno de un jugador se le pregunta, por comandos de voz, qué acción desea realizar. Solo se ejecutan las acciones que ordena si se encuentran en el sistema. Estas acciones son típicas del juego como:
*	<ins> “Paso”:</ins> el jugador no desea subir la apuesta.
*	<ins> “Subo”:</ins> el jugador sube la apuesta y se reinicia el estado de los jugadores para confirmar sus nuevas acciones.
*	<ins> “Igualo, Voy”:</ins>  el jugador sigue la apuesta máxima y coloca sus fichas en la mesa.
*	<ins> “Me retiro”:</ins> Se retira de la Mano y no se le preguntará nada hasta la próxima Mano.
*	<ins> “Abandono”:</ins> Abandona la mesa y ya no se le tendrá en cuenta en las próximas Manos.
*	<ins> “Cambio a la alta/baja”:</ins> El jugador coloca sus fichas en su área de cambio según si desea cambio a valores altos o bajos. Implementado por el Módulo de Cambio.
*	<ins> Preguntas de estado:</ins>  Se le puede preguntar al sistema información sobre el estado del juego. Ej: “Dealer actual?”, “Ronda actual?, “Quién es la ciega grande?”, “Apuesta máxima?”… 

Cuando se ha llegado a la última Ronda de una Mano el sistema dice a los jugadores que han permanecido al final de la Mano que muestren sus cartas. 
El sistema reconoce todas las cartas que hay en la mesa gracias al módulo de visión por computador y determina el jugador que ha ganado y la combinación de cartas con lo que lo ha hecho. 

Para las siguientes Manos el sistema de juego es el mismo. Se termina el juego cuando solo queda un jugador en la mesa.

### Módulo de cambio
Este módulo controla el sistema de cambio de fichas. Se implementa en 3 etapas: reconocimiento de las fichas que se desean cambiar y llevarlas a la banca, tratamiento del valor total de las fichas para establecer cuantas monedas y de qué tipo ha de devolver y por último la secuencia de movimientos para colocar las fichas de cambio.

Funciones:
*	**recogerFichasMonton(area):** Por medio de un área establecida controla el módulo de visión por computador de las fichas para poder reconocerlas y luego a través de las funciones de cinemática inversa coloca esas fichas en su determinada posición de la banca.

*	**cambiar_fichas_greedy(suma_fichas,mode):** Algoritmo greedy (sacado  de la asignatura de la mención “Analisis y disseny d’algortimes” ) implementado para saber qué fichas ha de devolver el robot. Implementa 2 modos para devolver fichas con valores bajos o máximos.

*	**dar_Cambio(cambio, posicion):** Recibe qué fichas se han de devolver y la matriz de la posición donde el jugador dejó sus fichas de cambio.

# Vídeo
Haz click para ver el video:
[![Watch the video](https://github.com/EmilCarvajal/Deal-AI/blob/main/img/Simulacion.JPG)](https://www.youtube.com/watch?v=U3uC58L_5Mo&ab_channel=Emilsj2)

# Autores
Emil Carvajal - 1529821   
Marc Gordón - 1457460   
Jofre Gómez - 1526889   
Denís Montoya - 1527418   
