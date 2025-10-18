# Evaluacion2 - Geolocalizador para la Biblioteca Nacional

## Descripción del Proyecto

Este proyecto es parte de la Evaluación 2 y consiste en un script de Python que actúa como un software de geolocalización. Utiliza la API de **Graphhopper** para calcular la ruta entre dos puntos geográficos (especificados por latitud y longitud) y devuelve la distancia, la duración estimada del viaje y las instrucciones paso a paso en español.

Este script fue hecho para cumplir con los requisitos de la consultora "API Ltda." para el proyecto de la Biblioteca Nacional.

## Instrucciones de Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/MartinEnzoUC/Evaluacion2.git
    cd Evaluacion2
    ```

2.  **Instalar dependencias:** El script solo requiere la librería `requests`. Si no la tienes, puedes instalarla con pip.
    ```bash
    pip install requests
    ```

3.  **Obtener una API Key:**
    - Ve al [sitio de Graphhopper](https://www.graphhopper.com/developers/) y regístrate para obtener una API Key gratuita.

4.  **Configurar el script:**
    - Abre el archivo `geolocalizador.py` en un editor de texto.
    - Busca la línea: `graphhopper_key = "AQUI_VA_TU_API_KEY_DE_GRAPHOPPER"`
    - Reemplaza el texto `"AQUI_VA_TU_API_KEY_DE_GRAPHOPPER"` con tu API Key.

5.  **Ejecutar el script:**
    - Desde tu terminal, ejecuta el siguiente comando:
    ```bash
    python geolocalizador.py
    ```
    - Sigue las instrucciones en pantalla para ingresar las coordenadas de inicio y destino. Ejemplo: `-33.4430,-70.6534`.
