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

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("NANA")
client1.on_message = on_message



st.title("Garden Voice")
st.subheader("Control por Voz")
#image = Image.open('Instructor.png')
#st.image(image)
with open('voice.json') as source:
     animation=json.load(source)
st.lottie(animation,width =350)




st.write("Toca el Botón y habla ")

button_html = """
<button id="speak-button" style="background: none; border: none; cursor: pointer; outline: none;">
    <img src="https://github.com/aquintanab/Control_por_Voz/blob/riego/mic.png" alt="Habla" style="width: 80px;">
</button>
<script>
    document.getElementById('speak-button').addEventListener('click', function() {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = function (event) {
            var value = "";
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    value += event.results[i][0].transcript;
                }
            }
            if (value != "") {
                document.lastEventDetail = value;  // Guardar en variable global
            }
        };
        recognition.start();
    });
</script>
"""
st.markdown(button_html, unsafe_allow_html=True)

# Capturar texto del reconocimiento de voz
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
