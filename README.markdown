# Cotizador de Reciclaje de Equipos Electrónicos

Aplicación web desarrollada en Streamlit para calcular el precio de cobro por el reciclaje de múltiples equipos electrónicos (laptops, CPUs, servidores). Permite agregar varios equipos con sus cantidades y muestra únicamente el precio total a cobrar, basado en procesos de sorting, desensamblaje, pesaje y almacenaje.

## Características
- Selección de múltiples equipos (Laptop, CPU, Servidor) con cantidades.
- Cálculo automático del precio de cobro total para todos los equipos.
- Interfaz web interactiva desplegada en Streamlit Cloud.
- Sin desglose de costos por proceso, solo precio final.

## Requisitos
- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación Local
1. Clona el repositorio:
   ```bash
   git clone https://github.com/<tu-usuario>/cotizador_reciclaje.git
   ```
2. Navega al directorio:
   ```bash
   cd cotizador_reciclaje
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```
5. Abre el enlace proporcionado (e.g., `http://localhost:8501`) en tu navegador.

## Archivos
- `app.py`: Script principal de Streamlit que implementa la interfaz y la lógica del cotizador.
- `equipos_reciclaje.csv`: Base de datos con los tiempos, operarios y costos de los equipos.
- `requirements.txt`: Lista de dependencias para el despliegue.
- `README.md`: Este archivo.

## Despliegue en Streamlit Cloud
1. Sube el repositorio a GitHub.
2. Regístrate en [Streamlit Cloud](https://streamlit.io/cloud) con tu cuenta de GitHub.
3. Crea una nueva aplicación:
   - Selecciona el repositorio `cotizador_reciclaje`.
   - Especifica la rama `main`.
   - Indica el archivo principal: `app.py`.
   - Despliega la aplicación.
4. Accede a la URL proporcionada por Streamlit Cloud.

## Uso
1. Abre la aplicación en el navegador.
2. Agrega equipos:
   - Selecciona un equipo desde el menú desplegable (e.g., "Laptop").
   - Ingresa la cantidad de piezas.
   - Haz clic en "Agregar Equipo".
   - Repite para más equipos.
3. Haz clic en "Calcular Precio Total".
4. Revisa el precio de cobro total para todos los equipos.

## Ejemplo de Cotización
Para 10 laptops y 5 CPUs:
- Laptop (10 piezas): $280.0
- CPU (5 piezas): $182.5
- Precio total de cobro al cliente: $462.5

## Contribuciones
Siéntete libre de abrir issues o pull requests para mejoras o correcciones.

## Licencia
MIT License