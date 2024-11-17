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
<div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
    <button id="speak-button" style="
        background: none;
        border: none;
        cursor: pointer;
        outline: none;
    ">
        <img src="https://raw.githubusercontent.com/tu_usuario/tu_repositorio/main/ruta_a_imagen/microfono.png" alt="Habla" style="width: 80px;">
    </button>
</div>
<script>
    // Vincular el botón con reconocimiento de voz
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
                const streamlitEvent = new CustomEvent("GET_TEXT", { detail: value });
                document.dispatchEvent(streamlitEvent);
            }
        };
        recognition.start();
    });
</script>
"""

# Mostrar el botón en Streamlit
st.markdown(button_html, unsafe_allow_html=True)

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
        ret= client1.publish("riego_Aqb", message)

    
    try:
        os.mkdir("temp")
    except:
        pass
