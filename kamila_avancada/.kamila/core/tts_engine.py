# core/tts_engine.py
<<<<<<< HEAD
import pyttsx3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Inicializa o motor pyttsx3, que usa as vozes nativas do Windows
    engine = pyttsx3.init()
    engine.setProperty('rate', 180) # Ajusta a velocidade da fala
except Exception as e:
    logging.error(f"Não foi possível inicializar o motor pyttsx3: {e}")
    engine = None

def speak(text_to_speak):
    """
    Usa o motor pyttsx3 para falar o texto de forma offline e rápida no Windows.
    """
    if not engine:
        logging.error("Motor TTS não está disponível. Não é possível falar.")
        return

    try:
        if not text_to_speak:
            return
            
        logging.info(f"TTS Engine (pyttsx3): Falando -> '{text_to_speak}'")
        engine.say(text_to_speak)
        engine.runAndWait() # Espera a fala terminar
        logging.info("TTS Engine: Finalizou a fala.")
    except Exception as e:
        logging.error(f"Erro no motor TTS (pyttsx3): {e}")

if __name__ == '__main__':
    print("Testando a voz do Windows com pyttsx3...")
    speak("Olá, Martins. Se você está me ouvindo, a configuração no Windows está completa.")
=======
import os
import logging
import shlex
import subprocess

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def speak(text_to_speak):
    try:
        if not text_to_speak:
            logging.warning("TTS Engine: Recebeu um texto vazio para falar. Ignorando.")
            return

        logging.info(f"TTS Engine (espeak): Falando -> '{text_to_speak}'")
        
        # Adicionamos -a 80 para controlar o volume
        command = ["espeak", "-v", "pt+f3", "-s", "160", "-a", "80", text_to_speak]
        
        subprocess.run(command, check=True, capture_output=True, text=True)
        
        logging.info("TTS Engine: Finalizou a fala.")

    except FileNotFoundError:
        logging.error("Erro Crítico: 'espeak' não foi encontrado.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erro ao executar o espeak: {e.stderr}")
    except Exception as e:
        logging.error(f"Erro inesperado no motor TTS (espeak): {e}")

if __name__ == '__main__':
    speak("Olá, Martins. Este é um teste com o motor de fala e-speak.")
>>>>>>> 61a3238 (Primeiro commit da kamila assistente virtual)
