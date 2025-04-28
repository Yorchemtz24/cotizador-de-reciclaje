import pandas as pd
import streamlit as st
from fpdf import FPDF
from datetime import datetime
import io

# Configuración inicial de Streamlit
st.set_page_config(page_title="Cotizador de Reciclaje", page_icon="♻️")
st.title("Cotizador de Reciclaje de Equipos Electrónicos")
st.write("Seleccione el tipo de equipo y la cantidad de piezas para generar una cotización en PDF.")

# Cargar la base de datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("equipos_reciclaje.csv")

# Calcular costos y precio por equipo y cantidad
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

    # Costos por la cantidad total de piezas
    costo_mano_obra_total_cantidad = costo_mano_obra_total * cantidad
    costo_energia_total = costo_energia * cantidad
    costo_total_cantidad = costo_total_pieza * cantidad
    valor_materiales_total = valor_materiales * cantidad

    # Precio de cobro (30% margen + valor de materiales)
    precio_cobro_total = costo_total_cantidad * 1.3 + valor_materiales_total

    return {
        "costo_mano_obra_sorting": round(costo_mano_obra_sorting * cantidad, 2),
        "costo_mano_obra_desensamblaje": round(costo_mano_obra_desensamblaje * cantidad, 2),
        "costo_mano_obra_pesaje": round(costo_mano_obra_pesaje * cantidad, 2),
        "costo_mano_obra_almacenaje": round(costo_mano_obra_almacenaje * cantidad, 2),
        "costo_mano_obra_total": round(costo_mano_obra_total_cantidad, 2),
        "costo_energia_total": round(costo_energia_total, 2),
        "costo_total": round(costo_total_cantidad, 2),
        "valor_materiales_total": round(valor_materiales_total, 2),
        "precio_cobro_total": round(precio_cobro_total, 2)
    }

# Generar cotización en PDF
def generar_cotizacion_pdf(equipo, cantidad, resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Encabezado
    pdf.cell(200, 10, txt="COTIZACIÓN DE RECICLAJE", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="L")
    pdf.ln(10)

    # Información del equipo
    pdf.cell(200, 10, txt=f"Equipo: {equipo}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de piezas: {cantidad}", ln=True)
    pdf.ln(10)

    # Desglose de costos
    pdf.cell(200, 10, txt="Desglose de Costos:", ln=True)
    pdf.cell(200, 10, txt=f"Sorting: ${resultados['costo_mano_obra_sorting']}", ln=True)
    pdf.cell(200, 10, txt=f"Desensamblaje: ${resultados['costo_mano_obra_desensamblaje']}", ln=True)
    pdf.cell(200, 10, txt=f"Pesaje: ${resultados['costo_mano_obra_pesaje']}", ln=True)
    pdf.cell(200, 10, txt=f"Almacenaje: ${resultados['costo_mano_obra_almacenaje']}", ln=True)
    pdf.cell(200, 10, txt=f"Total mano de obra: ${resultados['costo_mano_obra_total']}", ln=True)
    pdf.cell(200, 10, txt=f"Energía: ${resultados['costo_energia_total']}", ln=True)
    pdf.cell(200, 10, txt=f"Valor estimado de materiales reciclables: ${resultados['valor_materiales_total']}", ln=True)
    pdf.cell(200, 10, txt=f"Total costos: ${resultados['costo_total']}", ln=True)
    pdf.ln(10)

    # Precio de cobro
    pdf.cell(200, 10, txt=f"Precio de cobro al cliente: ${resultados['precio_cobro_total']}", ln=True)
    pdf.ln(10)

    # Nota
    pdf.cell(200, 10, txt="Nota: Esta cotización es una estimación basada en la cantidad de piezas proporcionada.", ln=True)

    # Guardar PDF en un buffer
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# Interfaz de Streamlit
datos = cargar_datos()
equipos = datos["Equipo"].tolist()

with st.form("cotizador_form"):
    equipo = st.selectbox("Tipo de equipo", equipos)
    cantidad = st.number_input("Cantidad de piezas", min_value=1, step=1, value=1)
    submitted = st.form_submit_button("Generar Cotización")

    if submitted:
        try:
            datos_equipo = datos[datos["Equipo"] == equipo].iloc[0]
            resultados = calcular_cotizacion(datos_equipo, cantidad)

            # Mostrar resultados
            st.subheader("Resumen de la Cotización")
            st.write(f"**Equipo**: {equipo}")
            st.write(f"**Cantidad de piezas**: {cantidad}")
            st.write("**Desglose de Costos**:")
            st.write(f"- Sorting: ${resultados['costo_mano_obra_sorting']}")
            st.write(f"- Desensamblaje: ${resultados['costo_mano_obra_desensamblaje']}")
            st.write(f"- Pesaje: ${resultados['costo_mano_obra_pesaje']}")
            st.write(f"- Almacenaje: ${resultados['costo_mano_obra_almacenaje']}")
            st.write(f"- Total mano de obra: ${resultados['costo_mano_obra_total']}")
            st.write(f"- Energía: ${resultados['costo_energia_total']}")
            st.write(f"- Valor estimado de materiales reciclables: ${resultados['valor_materiales_total']}")
            st.write(f"- Total costos: ${resultados['costo_total']}")
            st.write(f"**Precio de cobro al cliente**: ${resultados['precio_cobro_total']}")

            # Generar y ofrecer descarga del PDF
            pdf_buffer = generar_cotizacion_pdf(equipo, cantidad, resultados)
            st.download_button(
                label="Descargar Cotización en PDF",
                data=pdf_buffer,
                file_name=f"Cotizacion_{equipo}_{cantidad}_piezas_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
        except IndexError:
            st.error("Equipo no encontrado en la base de datos.")

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