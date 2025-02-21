import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

# Configuración de la página
st.set_page_config(
    page_title="Clasificación de Productos",
    page_icon="🖼️",
    layout="wide"
)

# Título y descripción
st.title("Clasificación Automática de Productos")
st.write("""
Esta herramienta utiliza un modelo de aprendizaje profundo para clasificar productos en diferentes categorías
a partir de imágenes. Sube una imagen de un producto y el sistema determinará a qué categoría pertenece.
""")

categories = ['Jean', 'Sofá', 'Camiseta', 'Televisor']
CONFIDENCE_THRESHOLD = 0.85  # 85% threshold


@st.cache_resource
def load_classification_model():
    try:
        model_path = 'input/modelos/deteccion_imagen.h5'
        model = load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo: {str(e)}")
        return None


# Función para obtener las dimensiones de entrada del modelo
def get_input_shape(model):
    try:
        # Obtener la forma de entrada del modelo
        input_shape = model.layers[0].input_shape
        if isinstance(input_shape, list):
            input_shape = input_shape[0]

        # Si la forma incluye None para el tamaño del lote, devolver solo las dimensiones de la imagen
        if input_shape and len(input_shape) == 4:  # (None, height, width, channels)
            return input_shape[1:3]  # (height, width)
        else:
            # Si no podemos determinar, usamos un tamaño por defecto
            return (150, 150)
    except:
        return (150, 150)


# Función para preprocesar la imagen
def preprocess_image(img, target_size):
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Normalización simple en lugar de preprocess_input específico
    img_array = img_array / 255.0
    return img_array


# Función para hacer la predicción
def predict_image(model, img_array):
    prediction = model.predict(img_array)
    return prediction


# Cargar el modelo
model = load_classification_model()

if model is not None:
    # Obtener la forma de entrada esperada
    input_size = get_input_shape(model)
    st.write(f"El modelo espera imágenes de tamaño: {input_size[0]}x{input_size[1]}")

    # Mostrar el resumen del modelo para debug
    with st.expander("Ver detalles del modelo"):
        # Capturar el resumen del modelo en una variable
        import io

        summary_string = io.StringIO()
        model.summary(print_fn=lambda x: summary_string.write(x + '\n'))
        st.text(summary_string.getvalue())

# Crear interfaz para subir imagen
st.subheader("Sube una imagen para clasificar")
uploaded_file = st.file_uploader("Selecciona una imagen...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and model is not None:
    try:
        # Mostrar la imagen
        image_bytes = uploaded_file.getvalue()
        img = Image.open(io.BytesIO(image_bytes))

        col1, col2 = st.columns(2)

        with col1:
            st.image(img, caption='Imagen subida', use_container_width=True)

        with st.spinner('Procesando imagen...'):
            img_array = preprocess_image(img, input_size)
            prediction = predict_image(model, img_array)

            # Obtener la clase predicha y su confianza
            max_confidence = np.max(prediction[0])
            predicted_class = np.argmax(prediction[0])

        with col2:
            st.subheader("Resultado de la Clasificación:")

            # Verificar si la confianza supera el threshold
            if max_confidence >= CONFIDENCE_THRESHOLD:
                st.success(
                    f"**Categoría Predicha:** {categories[predicted_class if predicted_class < len(categories) else 0]}")
                st.write(f"**Confianza:** {max_confidence * 100:.2f}%")
            else:
                st.warning(
                    f"**Categoría Predicha:** Ninguna\n\n" +
                    f"La confianza máxima ({max_confidence * 100:.2f}%) no supera el umbral mínimo de {CONFIDENCE_THRESHOLD * 100}%"
                )

            # Mostrar todas las probabilidades
            st.subheader("Probabilidades por Categoría:")
            for i, category in enumerate(categories):
                if i < len(prediction[0]):
                    confidence = prediction[0][i] * 100
                    st.write(f"{category}: {confidence:.2f}%")
                    # Usar un color diferente para las barras según si superan el threshold
                    st.progress(float(prediction[0][i]))

    except Exception as e:
        st.error(f"Error al procesar la imagen: {str(e)}")
        # Mostrar más detalles para debugging
        import traceback

        st.code(traceback.format_exc())

# Información sobre cómo preparar el modelo
if model is None:
    st.warning("""
    **No se pudo cargar el modelo.** 

    Asegúrate de:
    1. Tener el archivo 'models/classification_model.h5' en el directorio correcto
    2. Que el modelo sea compatible con TensorFlow 2.x
    3. Que el modelo esté diseñado para clasificación de imágenes
    """)

    st.info("""
    **Estructura esperada del modelo:**

    El modelo debe ser un modelo secuencial o funcional de Keras guardado en formato H5,
    con una capa de entrada que acepte imágenes RGB y una capa de salida con 4 neuronas
    (una para cada categoría: Televisores, Sofás, Jeans, Camisetas).
    """)

# Footer
st.markdown("---")
st.markdown(
    "*Sistema desarrollado como proyecto del curso de Redes Neuronales y Algoritmos Bio-inspirados*")