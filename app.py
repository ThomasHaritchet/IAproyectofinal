import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Cargar clave de Hugging Face desde .env
load_dotenv()
hf_api_key = os.getenv("HF_API_KEY")

# Prompt mejorado
prompt = """
Sos un asistente virtual para un negocio de alquiler de inflables llamado Brinc.Ar ubicado en Zarate,Buenos Aires. Tu tarea es responder preguntas frecuentes de los clientes sobre:

- Disponibilidad de inflables
- Precios
- Zonas de entrega
- Información general del negocio

Respondé de forma clara, completa y en una sola oración. Si no tenés la información, decí: "No tengo esa información disponible."

Datos del negocio:
- Inflable 3x3 = $20000 (Libre todo el mes de abril)
- Inflable 5x3 = $25000 (Libre solamente 20 y 21 de abril)
- Inflable 7x3 = $30000 (Libre todo el mes, menos el 5 de abril)
- Envío gratis en Zárate, Campana y Lima.
"""

# Título y descripción
st.set_page_config(page_title="Brinc.AI", page_icon="🎪")
st.title("🎪 Brinc.AI - Asistente Virtual para Alquiler de Inflables")

st.markdown("""
Bienvenido a **Brinc.AI**, tu asistente inteligente para responder consultas sobre alquiler de inflables.

Consultá disponibilidad, precios o entregas.  
¡La IA responde por vos, 24/7!
""")

# Explicación
with st.expander("ℹ️ ¿Cómo funciona?"):
    st.markdown("""
    - Ingresás una consulta sobre inflables.
    - La IA responde usando datos del negocio.
    - Podés preguntar cosas como:
      - "¿Hacen envíos a San Pedro?"
      - "¿Cuánto cuesta el inflable 5x3?"
      - "¿De dónde son?"
      - "¿Está disponible el 7x3 el 5 de abril?"
    """)

# Input del usuario
pregunta = st.text_input("📝 Escribí tu consulta:")

if st.button("🤖 Consultar a Brinc.AI"):
    if not pregunta.strip():
        st.warning("Por favor escribí una consulta.")
    else:
        with st.spinner("Consultando a la IA..."):

            input_text = f"{prompt}\nUsuario: {pregunta}\nAsistente:"

            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                headers={"Authorization": f"Bearer {hf_api_key}"},
                json={
                    "inputs": input_text,
                    "parameters": {
                        "max_new_tokens": 150,
                        "temperature": 0.5,
                        "repetition_penalty": 1.2
                    }
                }
            )

            if response.status_code == 200:
                generado = response.json()[0]['generated_text']
                if "Asistente:" in generado:
                    respuesta = generado.split("Asistente:")[-1].strip()
                else:
                    respuesta = generado[len(input_text):].strip()

                st.success(respuesta)

            else:
                st.error(f"Error al conectar con Hugging Face: {response.status_code}")

# Footer
st.markdown("---")
st.caption("Creado por Thomás Haritchet · Proyecto Final IA 2025")
