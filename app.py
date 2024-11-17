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
client1 = paho.Client("NANA")
client1.on_message = on_message

st.title("Garden Voice")
st.subheader("Control por Voz")

# Animación Lottie
with open('voice.json') as source:
    animation = json.load(source)
st.lottie(animation, width=350)

st.write("Toca el Botón y habla")

button_html = """
    <button id="speak-button" style="font-size: 50px; background: none; border: none; cursor: pointer; outline: none;">
        🎙️
    </button>
    <script>
        let recognition;
        document.getElementById('speak-button').addEventListener('click', function() {
            if (!recognition) {
                // Solicitar acceso al micrófono
                recognition = new webkitSpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;
                recognition.lang = 'es-ES';  // Establecer el idioma a español

                recognition.onstart = function() {
                    console.log("Reconocimiento de voz iniciado.");
                };

                recognition.onerror = function(event) {
                    console.log("Error en el reconocimiento: " + event.error);
                    alert("Hubo un error al intentar acceder al micrófono.");
                };

                recognition.onresult = function (event) {
                    var value = "";
                    for (var i = event.resultIndex; i < event.results.length; ++i) {
                        if (event.results[i].isFinal) {
                            value += event.results[i][0].transcript;
                        }
                    }
                    if (value != "") {
                        document.lastEventDetail = value;  // Guardar en variable global
                        window.parent.postMessage({ type: "streamlit_set_value", value: value }, "*");  // Enviar el valor a Streamlit
                    }
                };

                // Iniciar el reconocimiento de voz
                recognition.start();
            }
        });
    </script>
"""

st.markdown(button_html, unsafe_allow_html=True)

# Capturar el texto del reconocimiento de voz utilizando streamlit_js_eval
captured_text = streamlit_js_eval(js_code="document.lastEventDetail || ''", key="capture")

if captured_text:
    st.write(f"Texto reconocido: {captured_text}")
    # Publicar el mensaje al servidor MQTT
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": captured_text.strip()})
    client1.publish("riego_Aqb", message)

    try:
        os.mkdir("temp")
    except FileExistsError:
        pass
