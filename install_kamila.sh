#!/bin/bash
echo "[🔧] Instalando dependências..."
sudo apt update
sudo apt install -y python3-pip ffmpeg portaudio19-dev unzip wget xdg-utils
pip3 install vosk sounddevice edge-tts flask pyautogui tinydb

echo "[📁] Criando diretórios ocultos..."
mkdir -p ~/.kamila
cp -r .kamila/* ~/.kamila/

echo "[⬇️] Baixando modelo offline do Vosk..."
mkdir -p ~/.kamila/modelos
cd ~/.kamila/modelos
wget -q https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip
unzip -o vosk-model-small-pt-0.3.zip
mv vosk-model-small-pt-0.3 pt

echo "[⚙️] Instalando serviço systemd..."
sudo cp kamila.service /etc/systemd/system/kamila.service
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable kamila.service
echo "[✅] Kamila configurada para iniciar com o sistema!"

echo "[🚀] Para iniciar manualmente, use: systemctl start kamila"
echo "[📄] Logs em tempo real: journalctl -fu kamila"
