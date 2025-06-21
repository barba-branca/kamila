# core/interpreter.py
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_intent(text):
    """
    Analisa o texto e identifica a intenção do usuário de forma mais flexível.
    """
    logging.info(f"Interpreter: Analisando texto -> '{text}'")
    text = text.lower() # Normaliza o texto

    # --- LÓGICA MELHORADA ---
    # Procura por palavras-chave em vez de frases exatas.
    
    # Intenção de obter a hora
    if "horas" in text or "hora" in text:
        logging.info("Interpreter: Intenção 'get_time' identificada.")
        return {'intent': 'get_time', 'params': {}}
        
    # Intenção de obter a previsão do tempo
    elif "tempo" in text or "previsão" in text or "clima" in text:
        logging.info("Interpreter: Intenção 'get_weather' identificada.")
        return {'intent': 'get_weather', 'params': {'location': 'São Paulo'}}
        
    # Nenhuma intenção conhecida foi encontrada
    else:
        logging.info("Interpreter: Nenhuma intenção conhecida foi identificada.")
        return {'intent': 'unknown', 'params': {}}