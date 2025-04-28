# Cotizador de Reciclaje de Equipos Electrónicos

Aplicación web desarrollada en Streamlit para generar cotizaciones de reciclaje de equipos electrónicos (laptops, CPUs, servidores). Calcula costos basados en procesos de sorting, desensamblaje, pesaje y almacenaje, y genera un PDF descargable con el desglose de costos y el precio final.

## Características
- Selección de equipo (Laptop, CPU, Servidor).
- Entrada de cantidad de piezas.
- Cálculo automático de costos (mano de obra, energía, materiales reciclables).
- Generación y descarga de cotizaciones en PDF.
- Interfaz web interactiva desplegada en Streamlit Cloud.

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
2. Selecciona un equipo desde el menú desplegable (e.g., "Laptop").
3. Ingresa la cantidad de piezas.
4. Haz clic en "Generar Cotización".
5. Revisa el resumen de costos y descarga el PDF.

## Ejemplo de Cotización
Para 10 laptops:
- Sorting: $20.0
- Desensamblaje: $30.0
- Pesaje: $10.0
- Almacenaje: $10.0
- Total mano de obra: $70.0
- Energía: $30.0
- Materiales reciclables: $150.0
- Total costos: $100.0
- Precio de cobro: $280.0

## Contribuciones
Siéntete libre de abrir issues o pull requests para mejoras o correcciones.

## Licencia
MIT License