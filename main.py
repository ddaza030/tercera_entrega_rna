# main.py
import streamlit as st


def main():
    # Título principal
    st.title("Sistema holis Inteligente Integrado para Predicción, Clasificación y Recomendación en Comercio Electrónico")

    # Información del curso y equipo
    st.markdown("### Redes Neuronales y Algoritmos Bio-inspirados")
    st.markdown("Universidad Nacional de Colombia sede Medellín - 2024-2")

    # Equipo de trabajo
    st.markdown("### Equipo de Desarrollo")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - Juan Manuel Vera Echeverri (jverae@unal.edu.co)
        - Daniel Daza Macías (dadazam@unal.edu.co)
        """)
    with col2:
        st.markdown("""
        - Carlos Sebastián Zamora Rosero (cazamorar@unal.edu.co)
        - Alejandra Uribe Sierra (aluribes@unal.edu.co)
        """)

    # Descripción del proyecto
    st.markdown("### Descripción del Proyecto")
    st.write("""
    Este sistema integrado basado en aprendizaje profundo aborda tres problemas fundamentales 
    en la gestión de una plataforma de comercio electrónico:
    """)

    # Módulos principales
    st.markdown("### Módulos Principales")

    # Predicción de Demanda
    st.markdown("#### 1. Predicción de Demanda")
    st.write("""
    - Anticipación de ventas para los próximos 30 días
    - Optimización de gestión de inventario
    - Análisis de series temporales
    """)

    # Clasificación de Productos
    st.markdown("#### 2. Clasificación Automática de Productos")
    st.write("""
    - Categorización automática mediante análisis de imágenes
    - Organización eficiente del inventario
    - Clasificación en categorías como Televisores, Sofás, Jeans y Camisetas
    """)

    # Sistema de Recomendación
    st.markdown("#### 3. Sistema de Recomendación")
    st.write("""
    - Recomendaciones personalizadas basadas en historial de compras
    - Mejora de la experiencia del usuario
    - Optimización de ventas cruzadas
    """)

    # Objetivos del Sistema
    st.markdown("### Objetivos del Sistema")
    st.write("""
    - Mejorar la toma de decisiones en gestión de inventario
    - Optimizar recursos operativos
    - Brindar una experiencia superior a los clientes
    - Maximizar eficiencia en la categorización de productos
    - Aumentar las ventas mediante recomendaciones personalizadas
    """)

    # Nota sobre la navegación
    st.info("""
    📌 Utilice el menú lateral para navegar entre los diferentes módulos del sistema.
    Cada módulo permite interactuar con los modelos desarrollados y visualizar resultados en tiempo real.
    """)

    # Footer
    st.markdown("---")
    st.markdown("*Sistema desarrollado como proyecto del curso de Redes Neuronales y Algoritmos Bio-inspirados*")


if __name__ == "__main__":
    main()