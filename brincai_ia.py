import requests
import os
from dotenv import load_dotenv

# Cargar el token desde .env
load_dotenv()
hf_api_key = os.getenv("HF_API_KEY")

# Prompt con info de Brinc.AI
prompt = """
Sos un asistente virtual para un negocio de alquiler de inflables llamado Brinc.Ar. Tu tarea es responder preguntas frecuentes de los clientes sobre:

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


pregunta_usuario = "¿Está libre el inflable 5x3 el 15 de abril?"

# Combinar prompt con pregunta
input_text = f"{prompt}\nUsuario: {pregunta_usuario}\nAsistente:"

# Hacer la petición a Hugging Face (modelo Mistral)
response = requests.post(
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
    headers={"Authorization": f"Bearer {hf_api_key}"},
    json={
    "inputs": input_text,
    "parameters": {
        "max_new_tokens": 100,
        "temperature": 0.5,
        "repetition_penalty": 1.2
    }
}

)

# Mostrar respuesta
if response.status_code == 200:
    generado = response.json()[0]['generated_text']
    if "Asistente:" in generado:
        respuesta = generado.split("Asistente:")[-1].strip()
    else:
        respuesta = generado[len(input_text):].strip()

    print("🤖 Respuesta de la IA:", respuesta)
else:
    print("❌ Error:", response.status_code, response.text)
