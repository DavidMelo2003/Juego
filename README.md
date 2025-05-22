# Eco-Guardián Espacial MK.II (o el nombre de tu juego)

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
3.  Navega al directorio del proyecto en tu terminal.
4.  Ejecuta el juego:
    ```bash
    python eco_guardian_mk2.py
    ```
    (Reemplaza `eco_guardian_mk2.py` con el nombre de tu script principal si es diferente).

## Cómo Jugar (Usando Docker)

**Prerrequisitos para Docker:**
*   Docker instalado en tu sistema.
*   Un servidor X11 configurado en tu host si estás en Linux o macOS (XQuartz), o WSL con un servidor X como VcXsrv o X410 en Windows.

**Pasos:**
1.  Clona este repositorio.
2.  Navega al directorio del proyecto en tu terminal.
3.  Construye la imagen Docker:
    ```bash
    docker build -t nombre-de-tu-juego .
    ```
    (Ej: `docker build -t eco-guardian-mk2 .`)

4.  Ejecuta el contenedor (los comandos varían ligeramente según tu SO):

    *   **En Linux:**
        ```bash
        xhost +local:docker
        docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix nombre-de-tu-juego
        ```

    *   **En macOS (con XQuartz instalado y ejecutándose):**
        Abre XQuartz. En una terminal de XQuartz, obtén tu IP (ej: `ipconfig getifaddr en0` o `en1` para Wi-Fi).
        Luego, permite conexiones desde esa IP: `xhost +TU_DIRECCION_IP`
        ```bash
        docker run -it --rm -e DISPLAY=TU_DIRECCION_IP:0 nombre-de-tu-juego
        ```
        (Reemplaza `TU_DIRECCION_IP` con la IP de tu Mac, ej: `192.168.1.10:0`)

    *   **En Windows (con WSL y un servidor X como VcXsrv o X410 ejecutándose):**
        Asegúrate de que tu servidor X esté configurado para permitir conexiones.
        Dentro de tu terminal WSL:
        ```bash
        export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0 
        # O para WSL2 a veces es: export DISPLAY=$(hostname).local:0
        docker run -it --rm -e DISPLAY=$DISPLAY nombre-de-tu-juego
        ```
        *Nota: Para WSL2 y VcXsrv, a menudo necesitas deshabilitar el control de acceso en VcXsrv (ej. con `vcxsrv.exe :0 -ac -terminate -lesspointer -multiwindow -clipboard -wgl`) o configurar correctamente el firewall.*

**Controles del Juego:**
*   **Flechas Izquierda/Derecha:** Mover la nave.
*   **Espacio:** Disparar.
*   **ESC:** Salir del juego.

## Créditos y Personalización
Este juego es una personalización del proyecto base proporcionado para la actividad de "Inicios IOT", basado en la versión "MK.II".
*   **Desarrollador:** [Tu Nombre/Alias]
*   **Assets:** [Menciona si usaste assets de alguna fuente específica, ej: "Assets de OpenGameArt.org y Kenney.nl, modificados por mí", o "Todos los assets creados por [Tu Nombre/Alias]"]

---
