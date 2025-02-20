import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(page_title="Predicción de Demanda", layout="wide")

# Título de la aplicación
st.title("📊 Visualización de Predicción de Demanda")


# Función para cargar y validar datos
def load_data(file):
    try:
        df = pd.read_csv(file)

        # Verificar columnas requeridas
        required_columns = ['fecha_inicio_semana', 'ventas_semana']
        if not all(col in df.columns for col in required_columns):
            st.error(
                "El archivo CSV debe contener las columnas: 'fecha_inicio_semana' y 'ventas_semana'")
            st.stop()

        # Convertir y validar fechas
        try:
            df['fecha_inicio_semana'] = pd.to_datetime(df['fecha_inicio_semana'])
        except:
            st.error(
                "Error al convertir las fechas. Asegúrate de que estén en formato YYYY-MM-DD")
            st.stop()

        # Verificar que no hay fechas duplicadas
        if df['fecha_inicio_semana'].duplicated().any():
            st.warning(
                "Se encontraron fechas duplicadas. Se mantendrá solo el último valor para cada fecha.")
            df = df.drop_duplicates(subset=['fecha_inicio_semana'], keep='last')

        # Ordenar por fecha
        df = df.sort_values('fecha_inicio_semana')

        # Verificar valores numéricos en ventas
        if not pd.to_numeric(df['ventas_semana'], errors='coerce').notna().all():
            st.error("La columna 'ventas_semana' debe contener solo valores numéricos")
            st.stop()

        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        st.stop()


# Cargar datos con manejo de errores
try:
    file_path = os.path.join('input', 'modelos', 'demanda.csv')
    if not os.path.exists(file_path):
        st.error(f"No se encontró el archivo en la ruta: {file_path}")
        st.stop()

    df = load_data(file_path)
except Exception as e:
    st.error(f"Error inesperado: {str(e)}")
    st.stop()

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Obtener lista de fechas disponibles
available_dates = df['fecha_inicio_semana'].dt.date.unique()
available_dates.sort()

# Selector de fecha inicial con solo fechas disponibles
start_date = st.sidebar.selectbox(
    "Fecha inicial",
    options=available_dates[:-1],
    index=0,
    format_func=lambda x: x.strftime('%Y-%m-%d')
)

# Calcular número máximo de semanas disponibles desde la fecha seleccionada
start_date = pd.to_datetime(start_date)
available_weeks = len(df[df['fecha_inicio_semana'] >= start_date])
max_weeks = max(1, available_weeks)

# Selector de número de semanas con validación
num_weeks = st.sidebar.slider(
    "Número de semanas a mostrar",
    min_value=1,
    max_value=max_weeks,
    value=min(max_weeks, 52)
)

# Aplicar filtros con validación
end_date = start_date + timedelta(weeks=num_weeks)
df_filtered = df[
    (df['fecha_inicio_semana'] >= start_date) &
    (df['fecha_inicio_semana'] < end_date)
    ].copy()

if df_filtered.empty:
    st.warning("No hay datos disponibles para el rango de fechas seleccionado.")
    st.stop()

# Mostrar resumen de filtros aplicados
st.sidebar.info(f"Mostrando datos desde {start_date.strftime('%Y-%m-%d')} "
                f"hasta {end_date.strftime('%Y-%m-%d')}")

# Métricas generales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Fecha Inicial", f"{start_date.strftime('%Y-%m-%d')}")
with col2:
    st.metric("Número de Semanas", f"{len(df_filtered):,.0f}")
with col3:
    st.metric("Ventas Totales", f"{df_filtered['ventas_semana'].sum():,.0f}")
with col4:
    st.metric("Promedio Semanal", f"{df_filtered['ventas_semana'].mean():,.0f}")

# Gráfico de línea principal
st.subheader("Tendencia de Ventas Semanales")
fig_line = px.line(
    df_filtered,
    x='fecha_inicio_semana',
    y='ventas_semana',
    title='Evolución de Ventas Semanales',
    labels={
        'fecha_inicio_semana': 'Fecha',
        'ventas_semana': 'Ventas'
    }
)
fig_line.update_traces(line_color='#2E86C1')
st.plotly_chart(fig_line, use_container_width=True)