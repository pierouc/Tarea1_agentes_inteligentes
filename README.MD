## 1. Introducción
Mediante el uso de agentes adversarios autonomos se puede lograr un contrincante en un ambiente totalmente estático para diferentes juegos clasicos como "El Gato", Ajedrez, o como en este caso, Connect 4

## 2. Objetivo:
Se busca crear un agente adversario a partir del algoritmo minimax con alpha-beta prunning. El agente debe ser capaz de optimizar su juego y minimizar las posibilidades adversario para ganar. Se premia crear conexiones más largas y se penaliza las jugadas del oponente en el que este puede ganar.

## 3. Metodología
Se encuentra el ambiente y se arregla y modifica un poco para poder aplicar el agente. Luego de que el ambiente corre, se opta por utilizar alpha-beta prunning, Con esto listo se comienza a buscar crear una heuristica para el juego sumando un puntaje diferente para cada linea de 2, 3 o 4 realizada por el agente pero no penalizando al jugador contrario en una primera instancia. Se ven temas como las lineas que son tapadas por el adversario o si es que es posible hacer una diagonal debido a si existe una ficha directamente abajo para lograr dicha diagonal. 
Luego de implmentar este tipo de heuristica con el algoritmo minimax no se logra llegar a una solucion concreta, debido a que el agente funciona de manera erratica.
Se opta por penalizar cuando el oponente este a una jugada de ganar y se cambia un poco el codigo para evitar redundancia y optimizar el tiempo de computo. Se comprueba que el agente este entrando en los lugares que debe, pero aun asi no se logra obtener resultados favorbles, hay veces que  bloquea jugadas o gana pero en otras ocaciones su comportamiento es errático.
En el siguiente [video demostrativo](https://www.youtube.com/watch?v=MMLtza3CZFM&t=4515s) podemos ver el funcionamiento del programa
