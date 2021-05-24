# [ROBOTICA] Deal-AI
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/foto_dealAI.JPG" align="center" width="600" alt="header pic"/>

Brazo mecánico que  permite actuar como  Dealer o Croupier en el juego del  Poker, concretamente la modalidad de Texas Holdem.
También ayuda a controlar el estado de la partida.


# Tabla de Contenidos
* [Descripción de proyecto](#descripción-del-proyecto)
* Esquema Hardware	
* Arquitectura de software
* Inteligencia Artificial 
* Componentes y piezas 3D extras	

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
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/esquema_hardware.jpg" align="center" width="600" alt="header pic"/>

# Arquitectura de software
<img src="https://github.com/emilsj2/Deal-AI/blob/main/img/esquema_software.jpg" align="center" width="600" alt="header pic"/>
