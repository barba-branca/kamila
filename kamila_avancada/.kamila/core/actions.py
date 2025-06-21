import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_time(params):
    """Ação para obter e retornar a hora atual."""
    logging.info("Actions: Executando ação 'get_time'.")
    now = datetime.datetime.now()
    response = f"Agora são {now.hour} horas e {now.minute} minutos."
    return response

def get_weather(params):
    """Ação para obter a previsão do tempo."""
    location = params.get('location', 'local desconhecido')
    logging.info(f"Actions: Executando ação 'get_weather' para {location}.")
    # Simulação de uma chamada de API
    response = f"A previsão para {location} é de tempo ensolarado."
    return response

def unknown_intent(params):
    """Ação para quando a intenção não é reconhecida."""
    logging.info("Actions: Executando ação 'unknown_intent'.")
    return "Desculpe, eu não entendi o que você disse."

# Mapeamento de intenções para funções
ACTION_MAP = {
    'get_time': get_time,
    'get_weather': get_weather,
    'unknown': unknown_intent
}

def execute_action(intent_data):
    """
    Recebe os dados da intenção e executa a ação correspondente.
    """
    intent = intent_data.get('intent', 'unknown')
    params = intent_data.get('params', {})
    
    action_function = ACTION_MAP.get(intent)
    
    if action_function:
        return action_function(params)
    else:
        # Caso a intenção seja válida mas não haja uma função mapeada
        return unknown_intent(params)
