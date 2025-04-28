import pandas as pd
import streamlit as st

# Configuración inicial de Streamlit
st.set_page_config(page_title="Cotizador de Reciclaje", page_icon="♻️")
st.title("Cotizador de Reciclaje de Equipos Electrónicos")
st.write("Agregue uno o más equipos y sus cantidades para obtener el precio total de cobro.")

# Cargar la base de datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("equipos_reciclaje.csv")

# Calcular precio de cobro para un equipo y cantidad
def calcular_cotizacion(datos_equipo, cantidad):
    tiempo_sorting = datos_equipo["TiempoSorting"]
    operarios_sorting = datos_equipo["OperariosSorting"]
    tiempo_desensamblaje = datos_equipo["TiempoDesensamblaje"]
    operarios_desensamblaje = datos_equipo["OperariosDesensamblaje"]
    tiempo_pesaje = datos_equipo["TiempoPesaje"]
    operarios_pesaje = datos_equipo["OperariosPesaje"]
    tiempo_almacenaje = datos_equipo["TiempoAlmacenaje"]
    operarios_almacenaje = datos_equipo["OperariosAlmacenaje"]
    
    costo_hora = datos_equipo["CostoHora"]
    costo_energia = datos_equipo["CostoEnergia"]
    valor_materiales = datos_equipo["ValorMateriales"]

    # Costo de mano de obra por proceso (por pieza)
    costo_mano_obra_sorting = (tiempo_sorting / 60) * operarios_sorting * costo_hora
    costo_mano_obra_desensamblaje = (tiempo_desensamblaje / 60) * operarios_desensamblaje * costo_hora
    costo_mano_obra_pesaje = (tiempo_pesaje / 60) * operarios_pesaje * costo_hora
    costo_mano_obra_almacenaje = (tiempo_almacenaje / 60) * operarios_almacenaje * costo_hora

    # Costo total de mano de obra por pieza
    costo_mano_obra_total = (
        costo_mano_obra_sorting +
        costo_mano_obra_desensamblaje +
        costo_mano_obra_pesaje +
        costo_mano_obra_almacenaje
    )

    # Costo total por pieza (mano de obra + energía)
    costo_total_pieza = costo_mano_obra_total + costo_energia

    # Costo total por la cantidad de piezas
    costo_total_cantidad = costo_total_pieza * cantidad
    valor_materiales_total = valor_materiales * cantidad

    # Precio de cobro (30% margen + valor de materiales)
    precio_cobro_total = costo_total_cantidad * 1.3 + valor_materiales_total

    return round(precio_cobro_total, 2)

# Inicializar estado de sesión para almacenar equipos
if 'equipos_seleccionados' not in st.session_state:
    st.session_state.equipos_seleccionados = []

# Cargar datos
datos = cargar_datos()
equipos = datos["Equipo"].tolist()

# Formulario para agregar un equipo
st.subheader("Agregar Equipo")
with st.form("agregar_equipo_form", clear_on_submit=True):
    equipo = st.selectbox("Tipo de equipo", equipos, key="equipo_select")
    cantidad = st.number_input("Cantidad de piezas", min_value=1, step=1, value=1, key="cantidad_input")
    agregar = st.form_submit_button("Agregar Equipo")

    if agregar:
        st.session_state.equipos_seleccionados.append({"equipo": equipo, "cantidad": cantidad})
        st.success(f"Agregado: {cantidad} {equipo}(s)")

# Mostrar equipos agregados
if st.session_state.equipos_seleccionados:
    st.subheader("Equipos Agregados")
    for i, item in enumerate(st.session_state.equipos_seleccionados):
        st.write(f"- {item['equipo']}: {item['cantidad']} piezas")
    if st.button("Limpiar Lista"):
        st.session_state.equipos_seleccionados = []
        st.rerun()

# Botón para calcular el precio total
if st.session_state.equipos_seleccionados and st.button("Calcular Precio Total"):
    try:
        precio_total = 0
        resumen = []
        for item in st.session_state.equipos_seleccionados:
            equipo = item["equipo"]
            cantidad = item["cantidad"]
            datos_equipo = datos[datos["Equipo"] == equipo].iloc[0]
            precio_equipo = calcular_cotizacion(datos_equipo, cantidad)
            precio_total += precio_equipo
            resumen.append({"equipo": equipo, "cantidad": cantidad, "precio": precio_equipo})

        # Mostrar resultado
        st.subheader("Resultado de la Cotización")
        for item in resumen:
            st.write(f"**{item['equipo']}** ({item['cantidad']} piezas): ${item['precio']}")
        st.write(f"**Precio total de cobro al cliente**: ${round(precio_total, 2)}")
    except IndexError:
        st.error("Uno o más equipos no encontrados en la base de datos.")

# Estilo CSS para mejorar la apariencia
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stSelectbox, .stNumberInput {
        background-color: #f9f9f9;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)