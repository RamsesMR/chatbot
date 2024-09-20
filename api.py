from flask import Flask, request, jsonify
from chatbox import Chatbot
import os
import tensorflow as tf
import spacy

# Manejar la descarga del modelo de spaCy si es necesario


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
    port = int(os.environ.get('PORT', 8080))  # Puerto correcto para Render
    print(f"Running on port {port}")
    app.run(host='0.0.0.0', port=port)