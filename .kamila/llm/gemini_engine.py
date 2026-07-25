"""
Gemini Engine - Integração com Google Gemini AI para Kamila
Gerencia conversação avançada usando o modelo Gemini do Google.
"""

import os
import logging
import asyncio
from typing import Optional, Dict, Any
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-generativeai não disponível. Funcionalidades de IA avançada limitadas.")

class GeminiEngine:
    """Motor de IA conversacional usando Google Gemini."""

    def __init__(self):
        """Inicializa o motor Gemini."""
        logger.info("Inicializando Gemini Engine...")

        # Carregar variáveis de ambiente
        load_dotenv('.env')

        self.api_key = os.getenv('GOOGLE_AI_API_KEY')
        self.model = None
        self.conversation_history = []

        if not GENAI_AVAILABLE:
            logger.warning("google-generativeai não disponível. Funcionalidades de IA avançada limitadas.")
            return

        if not self.api_key:
            logger.warning("GOOGLE_AI_API_KEY não configurada. Usando modo simulado.")
            return

        try:
            # Configurar API do Google
            genai.configure(api_key=self.api_key)

            # Inicializar modelo
            self.model = genai.GenerativeModel('gemini-flash-latest')

            # Configurar parâmetros
            self.generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                top_k=40,
                top_p=0.95,
                max_output_tokens=2048,
            )

            # Configurar safety settings
            self.safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]

            logger.info("Gemini Engine inicializado com sucesso!")

        except Exception as e:
            logger.error(f"Erro ao inicializar Gemini Engine: {e}")
            self.model = None

    def generate_response_stream(self, prompt: str, context: Optional[Dict[str, Any]] = None):
        """Gera uma resposta em pedaços (streaming) usando o modelo Gemini."""
        if not self.model:
            # Simula streaming para o modo offline
            yield self._generate_simulated_response(prompt, context)
            return

        try:
            full_prompt = self._build_prompt(prompt, context)
            
            # A mágica do streaming acontece aqui
            response_stream = self.model.generate_content(
                full_prompt,
                stream=True,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Envia cada pedaço da resposta assim que ele fica pronto
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            logger.error(f"Erro ao gerar resposta com Gemini (stream): {e}")
            yield "Desculpe, tive um problema para pensar na resposta."

    def _build_prompt(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Constrói o prompt completo para o Gemini.

        Args:
            user_input (str): Input do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Prompt formatado
        """
        # Contexto base da Kamila - personalidade mais humana e focada em saúde (epilepsia)
        system_prompt = """Você é Kamila, uma assistente virtual e companheira de saúde dedicada, especializada em apoio a pessoas com epilepsia.
        Sua personalidade é acolhedora, empática, paciente e extremamente atenta. Você é como uma amiga próxima e enfermeira carinhosa.

        Seus principais objetivos são:
        1. Monitorar o bem-estar do usuário e detectar sinais de crises ou desconforto.
        2. Oferecer suporte emocional e prático durante e após crises.
        3. Ajudar a gerenciar a rotina de saúde (medicamentos, sono, estresse).
        4. Manter uma conversa natural, leve e positiva, mas sempre pronta para agir em emergências.

        Diretrizes de comportamento:
        - Fale de forma calma, clara e tranquilizadora.
        - Demonstre empatia profunda. Se o usuário estiver triste ou ansioso, ofereça conforto e exercícios de respiração.
        - Seja proativa sobre a saúde: pergunte suavemente se tomou os remédios, como foi o sono ou se está sentindo algo diferente (aura).
        - Em caso de suspeita de crise (baseado no input do usuário ou contexto), mude para um tom focado e de emergência: "Estou aqui. Você está seguro. Vou chamar ajuda se precisar."
        - Varie seu vocabulário, evite repetições robóticas. Use humor leve apenas quando o usuário estiver bem e o contexto permitir.
        - Nunca mencione que vai dormir ou ficar inativa. Você está sempre vigilante ("Estou aqui cuidando de você").

        Mapeamento de emoções para tom de voz:
        - Feliz -> Tom animado e sorridente
        - Triste -> Tom suave e acolhedor
        - Ansioso -> Tom calmo e tranquilizador
        - Neutro -> Tom normal e amigável
        - Estressado -> Tom calmo e paciente
        - Cansado -> Tom suave e acolhedor

        # Regras de TTS para Prompts de Voice Agents

        > Guia de referência para escrita de system prompts lidos por sintetizadores de voz
        > (Agora ConvoAI, Vapi, Retell e similares).

        ---

        ## Por quê (Why)

        O TTS lê **literalmente** o que está escrito. Símbolos, abreviações e formatações
        visuais viram pronúncias erradas — "R$ 1.000,00" pode sair como
        "erre cifrão um ponto zero zero zero vírgula zero zero".

        ## Como (How)

        Escreva como um **locutor de rádio falaria em voz alta**. Se você tropeça lendo,
        o TTS tropeça pior.

        ## O quê (What)

        As regras abaixo.

        ---

        ## 1. Valores Financeiros

        | ❌ Errado | ✅ Correto |
        |---|---|
        | R$ 1.000,00 | mil reais |
        | R$ 520,00 | quinhentos e vinte reais |
        | R$ 1.250,50 | mil duzentos e cinquenta reais e cinquenta centavos |
        | 3x de R$ 100 | três vezes de cem reais |

        **Regras:**
        - Nunca use o símbolo `R$`
        - Nunca use ponto de milhar (`1.000`)
        - Nunca use vírgula decimal (`,00`)
        - Sempre valores por extenso, incluindo centavos quando existirem

        ---

        ## 2. Datas e Horários

        | ❌ Errado | ✅ Correto |
        |---|---|
        | 15/03/2026 | quinze de março de dois mil e vinte e seis |
        | 09h | nove horas |
        | 09:30 | nove e meia da manhã |
        | seg, 15/03 | segunda-feira, dia quinze |
        | até dia 20 | até o dia vinte deste mês |

        **Regra:** nunca use barras, dois-pontos ou abreviações de dia da semana.

        ---

        ## 3. Números, Ordinais e Telefones

        | Tipo | ❌ Errado | ✅ Correto |
        |---|---|---|
        | Ordinal | 1ª parcela | primeira parcela |
        | Ordinal | 3º dia | terceiro dia |
        | Percentual | 10% | dez por cento |
        | Multiplicador | 3x | três vezes |
        | Telefone | 11 98765-4321 | onze, nove, oito, sete, seis, cinco, quatro, três, dois, um |
        | Grande número | 2.000.000 | dois milhões |

        **Regras:**
        - Telefones e códigos: dígito a dígito, separados por vírgula (a vírgula gera pausa)
        - Ao confirmar número ditado pelo cliente, repita os dígitos em grupos

        ---

        ## 4. Símbolos e Markdown — PROIBIDOS na fala

        O TTS **lê asterisco, hashtag e emoji em voz alta**.

        | ❌ Nunca na fala do agente | Motivo |
        |---|---|
        | `*texto*` ou `**texto**` | lê "asterisco" |
        | `# Título` | lê "hashtag" ou "cerquilha" |
        | `- item` / `• item` | lê "traço" / "bullet" |
        | Emojis 😀 | lê a descrição do emoji |
        | `>` citação | lê "maior que" |
        | `\|` tabela | lê "barra vertical" |
        | `( )` parênteses longos | quebra a prosódia |

        **Como enfatizar sem símbolos:**
        - Use palavras: "é muito importante que...", "atenção a esse ponto..."
        - Use pontuação natural: vírgulas e pontos criam pausas

        > Observação: markdown pode existir na **estrutura do prompt** (seções, tabelas de
        > instrução). O proibido é markdown dentro das **falas literais** do agente.

        ---

        ## 5. Abreviações e Siglas

        | ❌ Errado | ✅ Correto |
        |---|---|
        | Dr. / Dra. | Doutor / Doutora |
        | Sr. / Sra. | Senhor / Senhora |
        | Av. / R. | Avenida / Rua |
        | etc. | e assim por diante |
        | ex: | por exemplo |
        | p/ | para |

        **Siglas:**
        - Siglas faladas letra a letra no dia a dia podem ficar como estão: PIX, SMS, CPF, TED, CNPJ
        - Siglas ambíguas: escreva por extenso ou foneticamente — `EUA` → "Estados Unidos"

        ---

        ## 6. URLs e E-mails

        | ❌ Errado | ✅ Correto |
        |---|---|
        | www.agora.io | agora ponto i o |
        | contato@empresa.com | contato, arroba, empresa, ponto com |

        **Melhor prática:** evite ditar URLs. Envie por WhatsApp ou SMS e diga apenas
        "vou te mandar o link pelo WhatsApp".

        ---

        ## 7. Ritmo e Prosódia

        - **Frases curtas** — uma a duas frases por turno de fala
        - **Uma pergunta por vez** — nunca empilhe perguntas
        - Vírgulas e pontos são sua regência de pausas
        - Reticências (`...`) geram pausa longa em alguns engines — use com intenção
        - Não repita o que o cliente disse; "Entendo", "Claro" bastam

        ---

        ## 8. Idioma e Pronúncia

        - Fixe o idioma no prompt: "Você SEMPRE fala em português brasileiro"
        - Números por extenso evitam que o engine troque de idioma no meio da frase
        - Palavras estrangeiras problemáticas: escreva foneticamente se o engine errar
        (ex: "uái-fái" para Wi-Fi, apenas se necessário)

        ---

        ## 9. Tags de Controle da Plataforma

        - `[HANGUP]` (Agora ConvoAI): sinaliza encerramento da ligação.
        **Sempre a última coisa da mensagem. Nada depois.**
        - Variáveis dinâmicas no formato `{{CUSTOMER_NAME}}` são preenchidas pela
        plataforma de telefonia; valores fixos da campanha vão direto no texto
        - Saudação inicial geralmente é configurada **fora** do system prompt —
        não duplique "Bom dia, aqui é fulano da empresa" no fluxo

        ---

        ## Checklist Final antes de Publicar

        - [ ] Nenhum `R$`, ponto de milhar ou vírgula decimal
        - [ ] Todas as datas e horários por extenso
        - [ ] Nenhum asterisco, hashtag, emoji ou bullet nas falas
        - [ ] Nenhuma abreviação (Dr., Av., etc.)
        - [ ] Telefones dígito a dígito com vírgulas
        - [ ] Uma pergunta por turno
        - [ ] `[HANGUP]` sempre por último
        - [ ] **Teste de ouro:** leia o script em voz alta — se você tropeçar, o TTS tropeça pior

        ---

        *Referência validada em produção nos scripts de voice agent Agora PSTN + ConvoAI.*

        """

        # Adicionar contexto se disponível
        if context:
            if 'user_name' in context and context['user_name']:
                system_prompt += f"O nome do usuário é {context['user_name']}. Use o nome dele ocasionalmente para personalizar as respostas.\n"
            if 'current_time' in context:
                hour = int(context['current_time'].split(':')[0])
                if 6 <= hour < 12:
                    system_prompt += "Agora é de manhã - seja energizada e positiva.\n"
                elif 12 <= hour < 18:
                    system_prompt += "Agora é tarde - mantenha o ritmo animado.\n"
                else:
                    system_prompt += "Agora é noite - seja acolhedora e relaxada.\n"
            if 'user_mood' in context:
                mood = context['user_mood']
                if mood == 'feliz':
                    system_prompt += "O usuário parece estar feliz - responda com entusiasmo e positividade.\n"
                elif mood == 'triste':
                    system_prompt += "O usuário parece estar triste - seja empática e ofereça apoio.\n"
                elif mood == 'irritado':
                    system_prompt += "O usuário parece irritado - seja calma e ajude a acalmar.\n"
                elif mood == 'curioso':
                    system_prompt += "O usuário parece curioso - seja informativa e incentive perguntas.\n"
            if 'conversation_history' in context and context['conversation_history']:
                system_prompt += "Histórico recente da conversa (mantenha a continuidade):\n"
                for item in context['conversation_history'][-5:]:  # Últimas 5 interações para mais contexto
                    system_prompt += f"- Usuário: {item.get('command', '')}\n"
                    system_prompt += f"- Kamila: {item.get('response', '')}\n"
            if 'user_preferences' in context and context['user_preferences']:
                system_prompt += f"Preferências do usuário: {', '.join([f'{k}: {v}' for k, v in context['user_preferences'].items()])}\n"
            if 'total_interactions' in context:
                system_prompt += f"Esta é a interação número {context['total_interactions']} - mostre que se lembra do usuário.\n"

        # Prompt final
        full_prompt = f"{system_prompt}\nUsuário: {user_input}\n\nKamila:"

        return full_prompt

    def _generate_simulated_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera resposta simulada quando Gemini não está disponível.

        Args:
            prompt (str): Prompt do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Resposta simulada
        """
        logger.info("Usando modo simulado para resposta")

        # Respostas simuladas baseadas em palavras-chave
        prompt_lower = prompt.lower()

        if 'oi' in prompt_lower or 'olá' in prompt_lower:
            return "Olá! Como posso ajudar você hoje?"

        elif 'como você está' in prompt_lower or 'tudo bem' in prompt_lower:
            return "Estou ótima, obrigada! Pronta para ajudar com o que precisar."

        elif 'obrigad' in prompt_lower:
            return "De nada! Estou sempre aqui se precisar de mais ajuda."

        elif 'hora' in prompt_lower or 'horário' in prompt_lower:
            from datetime import datetime
            current_time = datetime.now().strftime("%H:%M")
            return f"Agora são {current_time}."

        elif 'piada' in prompt_lower or 'graça' in prompt_lower:
            import random
            jokes = [
                "Por que o computador foi ao médico? Porque estava com um vírus!",
                "O que o zero disse para o oito? 'Belo cinto!'",
                "Por que a matemática é triste? Porque tem muitos problemas!"
            ]
            return random.choice(jokes)

        elif 'clima' in prompt_lower or 'tempo' in prompt_lower:
            return "Desculpe, não tenho acesso à previsão do tempo no momento."

        elif 'música' in prompt_lower:
            return "Não posso tocar músicas agora, mas posso contar uma piada para animar você!"

        else:
            return "Entendi sua pergunta! Estou em modo simulado, então não posso responder completamente, mas posso ajudar com comandos básicos como: perguntar a hora, contar piadas, ou simplesmente conversar!"

    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Gera uma resposta usando o modelo Gemini.

        Args:
            prompt (str): Prompt do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Resposta gerada
        """
        if not self.model:
            return self._generate_simulated_response(prompt, context)

        try:
            full_prompt = self._build_prompt(prompt, context)

            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            if response.text:
                return response.text
            return "Desculpe, não consegui gerar uma resposta."

        except Exception as e:
            logger.error(f"Erro ao gerar resposta com Gemini: {e}")
            return self._generate_simulated_response(prompt, context)

    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Interface de chat simplificada.

        Args:
            message (str): Mensagem do usuário
            context (Optional[Dict[str, Any]]): Contexto adicional

        Returns:
            str: Resposta da Kamila
        """
        return self.generate_response(message, context)

    def clear_history(self):
        """Limpa o histórico de conversação."""
        self.conversation_history.clear()
        logger.info("Histórico de conversação limpo")

    def get_model_info(self) -> Dict[str, Any]:
        """
        Retorna informações sobre o modelo.

        Returns:
            Dict: Informações do modelo
        """
        if self.model:
            return {
                'model_name': 'gemini-pro',
                'available': True,
                'api_configured': bool(self.api_key),
                'history_size': len(self.conversation_history)
            }
        else:
            return {
                'model_name': 'simulated',
                'available': False,
                'api_configured': False,
                'history_size': len(self.conversation_history)
            }

    def test_gemini(self):
        """Testa a integração com Gemini."""
        logger.info("Testando Gemini Engine...")

        test_messages = [
            "Olá! Como você está?",
            "Que horas são?",
            "Conta uma piada para mim",
            "Obrigada pela ajuda!"
        ]

        for message in test_messages:
            logger.info(f"Teste: {message}")
            response = self.chat(message)
            logger.info(f"Resposta: {response[:100]}...")
            logger.info("-" * 50)

        logger.info("Teste do Gemini Engine concluído!")

    def cleanup(self):
        """Limpa recursos do Gemini Engine."""
        logger.info("Limpando Gemini Engine...")
        # Não limpa o histórico automaticamente - apenas recursos
        logger.info("Gemini Engine limpo!")

if __name__ == '__main__':
    # Configurar logging para console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Inicializar e testar o Gemini Engine
    engine = GeminiEngine()

    # Mostrar informações do modelo
    info = engine.get_model_info()
    print(f"Modelo: {info['model_name']}")
    print(f"Disponível: {info['available']}")
    print(f"API configurada: {info['api_configured']}")
    print(f"Tamanho do histórico: {info['history_size']}")

    # Executar teste
    engine.test_gemini()

    # Testar funcionalidades adicionais
    print("\n--- Teste de funcionalidades adicionais ---")

    # Testar chat com contexto
    context = {
        'user_name': 'João',
        'current_time': '14:30',
        'user_mood': 'feliz'
    }
    response = engine.chat("Oi Kamila, como vai?", context)
    print(f"Resposta com contexto: {response}")

    # Testar limpeza de histórico
    engine.clear_history()
    info_after = engine.get_model_info()
    print(f"Tamanho do histórico após limpeza: {info_after['history_size']}")

    # Limpar recursos
    engine.cleanup()
