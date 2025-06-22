import speech_recognition as sr
import logging

# Configuração de log para vermos tudo
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("--- INICIANDO TESTE COM LOG ---")

try:
    logging.info("Passo 1: Criando o objeto Recognizer...")
    r = sr.Recognizer()
    logging.info("Recognizer criado com sucesso.")

    logging.info("Passo 2: Tentando acessar o Microfone...")
    with sr.Microphone() as source:
        logging.info("Microfone acessado com sucesso! A entrada deve aparecer no pavucontrol AGORA.")
        
        logging.info("Passo 3: Ajustando para o ruído...")
        r.adjust_for_ambient_noise(source)
        logging.info("Ajuste de ruído completo.")

        print("\nDiga alguma coisa!")
        
        logging.info("Passo 4: Ouvindo o áudio...")
        audio = r.listen(source, timeout=7)
        logging.info("Áudio capturado.")
        
        print("Reconhecendo...")
        
        logging.info("Passo 5: Enviando para a API do Google...")
        texto = r.recognize_google(audio, language='pt-BR')
        logging.info("Resposta recebida do Google.")
        
        print("Você disse: " + texto)

except sr.UnknownValueError:
    logging.warning("Google não conseguiu entender o áudio.")
except sr.RequestError as e:
    logging.error(f"Erro no serviço do Google; {e}")
except Exception as e:
    logging.error(f"Ocorreu um erro CRÍTICO: {e}", exc_info=True)

logging.info("--- FIM DO TESTE ---")
