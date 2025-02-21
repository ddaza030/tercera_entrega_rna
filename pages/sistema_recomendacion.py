import streamlit as st
import pandas as pd
import numpy as np
import glob

# Configuración de la página
st.set_page_config(page_title="Sistema de Recomendación de Ropa", layout="wide")


# Función de recomendación
def recommend(cart_indices, df, similarity_matrix, top_n=5):
    sim_scores = np.mean([similarity_matrix[idx] for idx in cart_indices], axis=0)
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [item for item in sim_scores if item[0] not in cart_indices]

    unique_top_indices = []
    seen_names = set()
    for idx, score in sim_scores:
        product_name = df.iloc[idx]['name']
        if product_name not in seen_names:
            unique_top_indices.append(idx)
            seen_names.add(product_name)
        if len(unique_top_indices) >= top_n:
            break

    return df.iloc[unique_top_indices][
        ['name', 'main_category', 'sub_category', 'actual_price', 'ratings',
         'no_of_ratings', 'image', 'discount_price']]


# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('input/modelos/datos_ropa.csv')

    # Cargar y concatenar las partes de la matriz de similitud
    similarity_files = sorted(glob.glob('input/modelos/part_*.csv'))
    similarity_matrix = pd.concat([pd.read_csv(file) for file in similarity_files],
                                  ignore_index=True).values

    return df.head(50), similarity_matrix, df


df_cortado, similarity_matrix, df = load_data()

# Crear pestañas
tab1, tab2 = st.tabs(["Catálogo", "Recomendaciones"])

# Pestaña de Catálogo
with tab1:
    st.title("Catálogo de Productos")
    cols = st.columns(3)

    if 'selected_product' not in st.session_state:
        st.session_state.selected_product = None

    for idx, row in df_cortado.iterrows():
        col = cols[idx % 3]
        with col:
            st.image(row['image'], use_container_width=True)
            st.subheader(row['name'])
            st.write(f"⭐ {row['ratings']} ({row['no_of_ratings']} valoraciones)")
            st.write(f"💰 Precio con descuento: ₹{row['discount_price']}")
            st.write(f"📌 Precio original: ₹{row['actual_price']}")
            st.write(
                f"Descuento: {((row['actual_price'] - row['discount_price']) / row['actual_price'] * 100):.0f}%")

            if st.button(f"Seleccionar Producto #{idx}"):
                st.session_state.selected_product = idx
                st.rerun()
            st.write("---")

# Pestaña de Recomendaciones
with tab2:
    if st.session_state.selected_product is not None:
        st.title("Productos Recomendados")
        st.write(
            f"Basado en el producto seleccionado: {df.iloc[st.session_state.selected_product]['name']}")

        recommended_products = recommend([st.session_state.selected_product], df,
                                         similarity_matrix, top_n=6)
        cols = st.columns(3)
        for idx, row in recommended_products.iterrows():
            col = cols[idx % 3]
            with col:
                st.image(row['image'], use_container_width=True)
                st.subheader(row['name'])
                st.write(f"⭐ {row['ratings']} ({row['no_of_ratings']} valoraciones)")
                st.write(f"💰 Precio con descuento: ₹{row['discount_price']}")
                st.write(f"📌 Precio original: ₹{row['actual_price']}")
                st.write(
                    f"Descuento: {((row['actual_price'] - row['discount_price']) / row['actual_price'] * 100):.0f}%")
                st.write("---")
    else:
        st.info(
            "Por favor, seleccione un producto del catálogo para ver las recomendaciones.")
