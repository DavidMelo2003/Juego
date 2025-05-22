# Eco-Guardián Espacial MK.III

## Descripción
"Eco-Guardián Espacial MK.III" es un juego de disparos espaciales desarrollado en Pygame. El jugador controla una nave espacial con el objetivo de defenderse de oleadas de naves enemigas. A medida que el jugador avanza, la dificultad aumenta con enemigos más rápidos y en mayor número. ¡Recolecta power-ups para mejorar tu cadencia de fuego y sobrevive el mayor tiempo posible!

**Características Principales:**
*   Movimiento clásico de la nave del jugador (izquierda/derecha).
*   Disparo de balas por el jugador.
*   Múltiples tipos de enemigos que se mueven y descienden en formación.
*   Algunos enemigos tienen la capacidad de disparar al jugador.
*   Power-up de "Disparo Rápido" que aumenta temporalmente la cadencia de fuego.
*   Sistema de oleadas de enemigos con dificultad progresiva.
*   Puntuación y sistema de vidas.
*   Pantallas de inicio y "Game Over".
*   Fondo con efecto de scroll.
*   Efectos de sonido para disparos y explosiones.

## Personajes y Elementos

*   **Jugador (Nave Espacial):** La nave controlada por el usuario, capaz de moverse lateralmente y disparar.
*   **Enemigos:**
    *   **Nave Enemiga Tipo 1/2/3:** Diferentes sprites para naves enemigas que se mueven en formación y pueden disparar. Su velocidad aumenta con las oleadas.
*   **Power-ups:**
    *   **Disparo Rápido:** Un ítem que, al ser recolectado, permite al jugador disparar más rápido por un tiempo limitado.
*   **Escenarios:** Un fondo espacial con efecto de scroll que simula el movimiento a través del cosmos.

## Requisitos (para ejecución local sin Docker)
*   Python 3.7+
*   Pygame 2.0+

## Cómo Jugar (Localmente)
1.  Clona este repositorio o descarga los archivos.
2.  Asegúrate de tener Python y Pygame instalados.
    ```bash
    pip install pygame
    ```
3.  Navega al directorio del proyecto en el terminal.
4.  Ejecuta el juego:
    ```bash
    python eco_guardian_mk3.py
    ```

## Cómo Jugar (Usando Docker)

**Prerrequisitos para Docker:**
*   Docker instalado en tu sistema.
*   Un servidor X11 configurado en tu host si estás en Linux o macOS (XQuartz), o WSL con un servidor X como VcXsrv o X410 en Windows.

**Pasos:**
1.  Clona este repositorio.
2.  Navega al directorio del proyecto en tu terminal.
3.  Construye la imagen Docker:
    ```bash
    docker build -t eco-guardian-mk3 .
    ```

4.  Ejecuta el contenedor:
        ```bash
        xhost +local:docker
        docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix eco-guardian-mk3
        ```
    
si existe algun problema con el audio usar:
         ```bash
        xhost +local:docker
        docker run -it --rm -e DISPLAY=$DISPLAY -e SDL_AUDIODRIVER=dummy  -v /tmp/.X11-unix:/tmp/.X11-unix eco-guardian-mk3
        ```

**Controles del Juego:**
*   **Flechas Izquierda/Derecha:** Mover la nave.
*   **Espacio:** Disparar.
*   **ESC:** Salir del juego.
