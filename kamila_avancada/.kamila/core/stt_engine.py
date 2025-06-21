import speech_recognition as sr
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.5

def listen():
    try:
        with sr.Microphone() as source:
            logging.info("STT Engine: Usando microfone padrão. Calibrando por 2 segundos...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            logging.info(f"STT Engine: Limiar de energia ajustado para: {recognizer.energy_threshold}")
            logging.info("STT Engine: Diga alguma coisa!")
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)
            logging.info("STT Engine: Reconhecendo...")
            transcribed_text = recognizer.recognize_google(audio, language='pt-BR')
            logging.info(f"STT Engine: Texto transcrito -> '{transcribed_text}'")
            return transcribed_text.lower()
    except sr.WaitTimeoutError:
        logging.info("STT Engine: Nenhum som foi detectado. Verifique o volume do microfone.")
        return None
    except sr.UnknownValueError:
        logging.warning("STT Engine: Áudio capturado, mas não foi possível entender as palavras.")
        return None
    except sr.RequestError as e:
        logging.error(f"STT-Engine: Erro de API; {e}")
        return None
    except Exception as e:
        logging.error(f"STT-Engine: Erro crítico ao acessar o microfone: {e}")
        return None

if __name__ == '__main__':
    print("Testando o módulo de escuta no microfone padrão.")
    comando = listen()
    if comando:
        print(f"Você disse: {comando}")
    else:
        print("Não consegui ouvir ou entender.")
