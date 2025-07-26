<<<<<<< HEAD
# main.py - Versão Final com Palavra de Ativação Customizada
import os
import struct
import pvporcupine
import pyaudio
from core import stt_engine, tts_engine, interpreter, actions, memory_manager
import logging
import time

# --- CONFIGURAÇÃO DO PORCUPINE ---
# !!! VERIFIQUE SE SUA ACCESSKEY REAL ESTÁ AQUI !!!
PICOVOICE_ACCESS_KEY = 'JJb+rGo+jdo7x9KzdMPjf4eLGQMJLdV6mIH4GuFXA5AwOm6MpCytAA==' 

# --- CAMINHO PARA SEU ARQUIVO .PPN ---
# Crie uma pasta 'wake_words' na raiz do seu projeto e coloque o arquivo .ppn dentro dela.
# Em seguida, coloque o nome exato do arquivo aqui.
WAKE_WORD_FILE_PATH = 'wake_words/computador_pt_windows_v3_0_0.ppn' 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def wait_for_wake_word(porcupine, audio_stream):
    """Escuta passivamente o áudio até que a palavra de ativação seja detectada."""
    # Extrai o nome da palavra-chave do caminho do arquivo para o log
    wake_word_name = os.path.basename(WAKE_WORD_FILE_PATH).split('_')[0].capitalize()
    logging.info(f"Aguardando a palavra de ativação ('{wake_word_name}')...")
    
    while True:
        try:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            
            keyword_index = porcupine.process(pcm)
            
            if keyword_index >= 0:
                logging.info(f"Palavra de ativação '{wake_word_name}' detectada!")
                tts_engine.speak("Sim?")
                return
        except IOError as e:
            logging.warning(f"Erro de buffer de áudio, continuando a escuta: {e}")
            continue

def main():
    porcupine = None
    pa = None
    audio_stream = None
    try:
        if PICOVOICE_ACCESS_KEY == 'SUA_ACCESS_KEY_AQUI':
            logging.error("A AccessKey da PicoVoice não foi definida. Por favor, edite o main.py.")
            return
        
        if not os.path.exists(WAKE_WORD_FILE_PATH):
            logging.error(f"Arquivo da palavra de ativação não encontrado em: '{WAKE_WORD_FILE_PATH}'")
            logging.error("Por favor, treine sua palavra-chave no console da PicoVoice e coloque o arquivo .ppn no local correto.")
            return

        logging.info(f"Inicializando Porcupine com o modelo customizado: {WAKE_WORD_FILE_PATH}")
        porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY,
            keyword_paths=[WAKE_WORD_FILE_PATH] # Usamos 'keyword_paths' para arquivos customizados
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        user_name = memory_manager.get_from_memory('user_name', 'amigo')
        logging.info(f"Kamila pronta para o usuário {user_name}.")
        
        while True:
            wait_for_wake_word(porcupine, audio_stream)
            
            comando = stt_engine.listen()

            if comando:
                # ... (resto da lógica de interação) ...
                interaction_count = memory_manager.get_from_memory('interactions', 0) + 1
                memory_manager.update_memory('interactions', interaction_count)
                memory_manager.update_memory('last_interaction_time', time.strftime("%Y-%m-%d %H:%M:%S"))
                logging.info(f"Comando recebido: '{comando}' (Interação nº {interaction_count})")
                
                intent_data = interpreter.analyze_intent(comando)
                if intent_data and intent_data.get('intent') != 'unknown':
                    resposta = actions.execute_action(intent_data)
                    if resposta:
                        tts_engine.speak(resposta)
                else:
                    tts_engine.speak("Desculpe, não sei como ajudar com isso ainda.")
            else:
                tts_engine.speak("Não entendi o comando, por favor, tente novamente.")

    except pvporcupine.PorcupineError as e:
        logging.error(f"Erro no Porcupine (Palavra de Ativação): {e}")
    except Exception as e:
        logging.error(f"Ocorreu um erro crítico no main: {e}", exc_info=True)
    finally:
        logging.info("Encerrando Kamila...")
        if porcupine is not None: porcupine.delete()
        if audio_stream is not None: audio_stream.close()
        if pa is not None: pa.terminate()

if __name__ == "__main__":
    main()
=======
from core import stt_engine, tts_engine, interpreter, memory_manager, actions
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def main():
    try:
        logging.info("Kamila iniciada. Dizendo a mensagem de boas-vindas.")
        tts_engine.speak("Oi Kauê, eu sou a Kamila. Estou ativa e pronta para ajudar.")
    except Exception as e:
        logging.error(f"Erro ao iniciar e falar a mensagem de boas-vindas: {e}")
        time.sleep(5)

    logging.info("Iniciando o loop principal de escuta.")
    while True:
        try:
            comando = stt_engine.listen()
            if comando:
                logging.info(f"Comando recebido: '{comando}'")
                intent_data = interpreter.analyze_intent(comando)
                if intent_data:
                    resposta = actions.execute_action(intent_data)
                    if resposta:
                        logging.info(f"Resposta gerada: '{resposta}'")
                        tts_engine.speak(resposta)
                    else:
                        logging.warning("Nenhuma resposta foi gerada pela ação.")
                else:
                    logging.warning("Nenhuma intenção foi extraída do comando.")
            else:
                logging.info("Nenhum comando foi ouvido, reiniciando o ciclo de escuta.")
            time.sleep(1)
        except Exception as e:
            logging.error(f"Ocorreu um erro inesperado no loop principal: {e}")
            try:
                tts_engine.speak("Ocorreu um erro interno. Estou reiniciando meu ciclo.")
            except:
                pass
            time.sleep(10)

if __name__ == "__main__":
    main()
>>>>>>> 61a3238 (Primeiro commit da kamila assistente virtual)
