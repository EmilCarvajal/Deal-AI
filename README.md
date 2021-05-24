# [ROBOTICA] Deal-AI
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/foto_dealAI.JPG" align="center" width="600" alt="header pic"/>

Brazo mecánico que  permite actuar como  Dealer o Croupier en el juego del  Poker, concretamente la modalidad de Texas Holdem.
También ayuda a controlar el estado de la partida.


# Tabla de Contenidos
* [Descripción de proyecto](#descripción-del-proyecto)

* [Amazing contributions](#amazing-contributions)

* [Esquema Hardware](#esquema-hardaware)	

* [Piezas 3D](#piezas-3d)

* [Arquitectura software](#arquitectura-software)


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

Componentes unidos del brazo robótico (total de 4 piezas por separado).  
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/brazo.JPG" align="center" width="400" alt="header pic"/>

Base personalizada para colocar la baraja de cartas.  
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/base_cartas.JPG" align="center" width="400" alt="header pic"/>

Pieza que permite al robot voltear las cartas.  
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/flipeador.JPG" align="center" width="400" alt="header pic"/>

Mesa semicircular utilizada en el simulador como zona de juego (no se ha de imprimir en caso de realizarlo en la vida real).  
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/mesa.JPG" align="center" width="400" alt="header pic"/>


# Arquitectura software
Destacamos un total de 4 módulos imprescindibles en este proyecto los cuales, al sincronizarse, permiten al robot realizar un seguimiento eficiente de la partida de póker que se esté llevando a cabo. Dichos módulos son:
* Módulo de jugadores: Reconocimiento de comandos de voz (inputs) que permiten al robot poder avanzar en la partida o la acción a realizar en cada momento. También permite a los jugadores consultar dudas básicas que tengan.
* Módulo de cinemática inversa: Movimiento absoluto del robot, ya sea para repartir cartas, intercambiar fichas o dar la vuelta a las cartas. Este módulo en particular también permite la reorientación correcta de las cartas.
* Módulo de visión por computador: Reconocimiento de fichas y cartas. Es capaz de detectar el valor de las fichas estándar de póker (colores blanco, azul, verde, rojo, negro) y el valor y el palo de las cartas.
* Módulo de inteligencia artificial: Representa el cerebro del robot, el cual recibe los inputs de los demás módulos y genera los outputs que necesitan los demás módulos.
* Controladores: Estos relacionan los demás módulos entre si y permiten una perfecta sincronización entre ellos para poder efectuar las acciones necesarias.

<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/esquema_software.jpg" align="center" width="600" alt="header pic"/>
