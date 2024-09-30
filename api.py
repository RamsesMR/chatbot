from flask import Flask, request, jsonify
from chatbox import Chatbot
import os
import tensorflow as tf
import gunicorn
import spacy



gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)


# Desactivar la GPU en TensorFlow
tf.config.set_visible_devices([], 'GPU')

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)
chatbot = Chatbot()  # Instancia del chatbot sin tkinter

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        pregunta = data.get("pregunta")
        
        if not pregunta:
            return jsonify({"error": "No se ha proporcionado ninguna pregunta."}), 400
        
        respuesta = chatbot.encontrar_mejor_respuesta(pregunta)
        return jsonify({"respuesta": respuesta})
    except Exception as e:
        return jsonify({"error": f"Ha ocurrido un error: {str(e)}"}), 500

if __name__ == "__main__":
   port = int(os.environ.get('PORT', 8080))  # Render asignará el puerto automáticamente
   print(f"Running on port {port}")
    # app.run(host='0.0.0.0', port=port)