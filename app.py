import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
from streamlit_lottie import st_lottie
import json
from gtts import gTTS
from googletrans import Translator
import time
from streamlit_js_eval import streamlit_js_eval

def on_publish(client, userdata, result):  # Crear función para callback
    print("El dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)


broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Nana")
client1.on_message = on_message

st.title("Garden Voice")
st.subheader("Control por Voz")

# Animación Lottie
with open('voice.json') as source:
    animation = json.load(source)
st.lottie(animation, width=350)

st.write("Toca el Botón y habla")

st.markdown("""
    <style>
        /* Estilo para el contenedor del botón */
        .stButton {
            background-color: transparent !important;  /* Elimina cualquier fondo alrededor del botón */
            border: none !important;  /* Elimina el borde alrededor del contenedor */
            box-shadow: none !important;  /* Elimina cualquier sombra alrededor del contenedor */
        }

        /* Estilo para el botón */
        .stButton button {
            background-color: black !important;  /* Fondo negro para el botón */
            color: white !important;  /* Texto blanco para el botón */
            border: none !important;  /* Elimina cualquier borde del botón */
            padding: 10px 40px !important;  /* Espaciado interno del botón */
            font-size: 18px !important;  /* Tamaño de la fuente */
            cursor: pointer !important;  /* Cursor de mano al pasar sobre el botón */
            border-radius: 5px !important;  /* Bordes redondeados */
        }

        /* Cambio de color al pasar el ratón */
        .stButton button:hover {
            background-color: #333 !important;  /* Gris oscuro al pasar el ratón */
        }
    </style>
""", unsafe_allow_html=True)

stt_button = Button(label=" Habla 🎙️ ", width=100)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act1":result.get("GET_TEXT").strip()})
        ret= client1.publish("Eden", message)

    
    try:
        os.mkdir("temp")
    except:
        pass
