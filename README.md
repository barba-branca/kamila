# Kamila - Assistente Pessoal Baseada em IA 🤖

Kamila é uma assistente virtual pessoal e inteligente construída em Python. O projeto tem como foco principal produtividade, memória persistente, e uma interação humanizada e focada. A Kamila permite a interação tanto por **Texto (CLI)** quanto por **Voz (Voice-First)**.

## 🚀 Funcionalidades Principais

* **Modos de Interação:**
  * **CLI Mode (`main_cli.py`):** Interface via texto pelo terminal, rápida e objetiva, ideal para ambientes de desenvolvimento ou quando você não pode falar.
  * **Voice Mode (`main_voice.py`):** Sistema de escuta ativa (Wake Word). Responde a comandos iniciados pela palavra **"Kamila"** ou **"Camila"**. 

* **Gerenciamento de Rotina:**
  * **Diário Pessoal:** Fluxos interativos (via voz ou texto) para registrar os acontecimentos do dia.
  * **Controle de Hábitos:** Criação e check-in de novos hábitos diários ("novo hábito", "fiz o hábito").
  * **Lembretes Rápidos:** Crie lembretes simples com comandos como "lembrar de...".

* **Inteligência e Memória:**
  * Integração com a API do **Gemini (Google)** para conversação natural e respostas contextuais.
  * Sistema de **Memória Persistente**, armazenando o histórico de conversas, hábitos e anotações. O assistente "lembra" do que já foi discutido.

* **Reconhecimento e Síntese de Voz:**
  * **STT (Speech-to-Text):** Processamento de áudio em texto via `speech_recognition` (Google Speech API).
  * **TTS (Text-to-Speech):** Síntese de voz offline utilizando a biblioteca `pyttsx3`.

## 📁 Estrutura do Projeto

* `main_cli.py`: Ponto de entrada para uso em modo texto (Interface de Linha de Comando).
* `main_voice.py`: Ponto de entrada para modo voz, escutando de forma contínua o microfone do sistema.
* `.kamila/core/`: Contém os motores principais do projeto.
  * `memory_manager.py`: Módulo responsável pela gestão de banco de memórias.
  * `tts_engine.py`: Motor de fala (Text-To-Speech).
* `kamila_ia_models/`: Interfaces de IA.
  * `llm_interface.py`: Responsável por fazer a ponte entre as chamadas do usuário e a API do Google Gemini.
* `requirements.txt`: Dependências do projeto.
* `.env`: Arquivo (não versionado) de variáveis de ambiente com chaves de API (ex: `GOOGLE_AI_API_KEY`).

## 🛠️ Como Instalar e Rodar

### Pré-requisitos
* Python 3.9+ instalado no sistema.
* Um microfone configurado (para o `main_voice.py`).

### 1. Clonar e Configurar o Ambiente

```bash
git clone https://github.com/seu-usuario/Kamila.git
cd Kamila

# Recomenda-se criar um ambiente virtual (venv)
python -m venv .venv

# Ativando o venv (No Windows)
.venv\Scripts\activate
# Ativando o venv (No Linux/Mac)
source .venv/bin/activate
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Variáveis de Ambiente

Crie um arquivo `.env` (você pode copiar o `.env.example` caso exista) na raiz do projeto com as suas chaves de API.
Exemplo:
```ini
GOOGLE_AI_API_KEY=sua_chave_do_google_gemini_aqui
```
*(Nota: O `.env` está no `.gitignore` para sua segurança)*

### 4. Executando a Kamila

* **Modo CLI (Texto):**
  ```bash
  python main_cli.py
  ```
  *Exemplo de Comandos no CLI:* `novo hábito: ler`, `fiz ler`, `registrar meu dia`.

* **Modo Voz (Escuta Ativa):**
  ```bash
  python main_voice.py
  ```
  *(Aguarde o microfone calibrar e chame "Kamila..." antes dos seus comandos)*

## 📦 Dependências Principais
* `python-dotenv`: Gerenciamento de variáveis.
* `pyttsx3`: Síntese de voz nativa do OS.
* `speechrecognition`: Reconhecimento de áudio via microfone.
* `google-generativeai`: SDK para integração com o Gemini LLM.

## 🚧 Melhorias Futuras e TODOs
A Kamila está em desenvolvimento contínuo. Confira os arquivos de `TODO_*.md` espalhados no repositório para acompanhar o que está sendo planejado, como:
* Melhorias de detecção de contexto em conversas longas.
* Implementação de automação de interface (PyAutoGUI).
* Processamento com visão computacional (OpenCV).
