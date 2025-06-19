<<<<<<< HEAD
# core/interpreter.py
=======
>>>>>>> 61a3238 (Primeiro commit da kamila assistente virtual)
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_intent(text):
    """
<<<<<<< HEAD
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
=======
    Função esqueleto para analisar o texto e identificar a intenção do usuário.
    """
    logging.info(f"Interpreter: Analisando texto -> '{text}'")
    text = text.lower() # Normaliza o texto para minúsculas
    
    if "que horas são" in text or "me diga as horas" in text:
        logging.info("Interpreter: Intenção 'get_time' identificada.")
        return {'intent': 'get_time', 'params': {}}
    elif "qual a previsão do tempo" in text:
        logging.info("Interpreter: Intenção 'get_weather' identificada.")
        return {'intent': 'get_weather', 'params': {'location': 'São Paulo'}} # Exemplo com parâmetro
    else:
        logging.info("Interpreter: Nenhuma intenção conhecida foi identificada.")
        return {'intent': 'unknown', 'params': {}}

if __name__ == '__main__':
    # Teste rápido
    print("Testando o Módulo Interpreter...")
    resultado = analyze_intent("Kamila, que horas são agora?")
    print(f"Resultado da análise: {resultado}")
>>>>>>> 61a3238 (Primeiro commit da kamila assistente virtual)
