import spacy
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Cargar el modelo preentrenado de spaCy para español
try:
    nlp = spacy.load('es_core_news_sm')
except OSError:
    print("El modelo 'es_core_news_sm' de spaCy no está disponible. Asegúrate de haberlo descargado.")
    raise

class Chatbot:
    def __init__(self):
        # Inicializar el modelo SentenceTransformer
        self.modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
        # Cargar el archivo JSON de preguntas y respuestas
        try:
            with open('intents.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.preguntas_respuestas = data['intents']
        except FileNotFoundError:
            print("El archivo 'intents.json' no se encontró.")
            raise
        except json.JSONDecodeError:
            print("El archivo 'intents.json' no tiene un formato JSON válido.")
            raise

    def preprocesar_texto(self, texto):
        """Preprocesa el texto eliminando stop words y lematizando"""
        texto = str(texto).lower()  # Convertir a minúsculas
        doc = nlp(texto)
        texto = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
        return texto.strip()

    def encontrar_mejor_respuesta(self, pregunta_usuario):
        """Encuentra la mejor respuesta según la similitud de coseno"""
        if not pregunta_usuario or not pregunta_usuario.strip():
            return "Por favor, ingresa una pregunta válida."
        
        pregunta_usuario_procesada = self.preprocesar_texto(pregunta_usuario)
        vector_usuario = self.modelo.encode(pregunta_usuario_procesada, convert_to_tensor=True)

        mejor_similitud = -1
        mejor_respuesta = "Lo siento, no entendí tu pregunta."

        for intent in self.preguntas_respuestas:
            for pregunta in intent['pregunta']:
                pregunta_procesada = self.preprocesar_texto(pregunta)
                vector_pregunta = self.modelo.encode(pregunta_procesada, convert_to_tensor=True)
                similitud = util.pytorch_cos_sim(vector_usuario, vector_pregunta).item()

                if similitud > mejor_similitud:
                    mejor_similitud = similitud
                    mejor_respuesta = intent['respuesta'][0]

        if mejor_similitud > 0.6:
            return mejor_respuesta
        else:
            return "Lo siento, no entendí tu pregunta."