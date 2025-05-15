# Projeto_Integrador_V

# 🧊 Controle de Acesso em Câmaras Frias com IoT

Projeto Integrador da UNIVESP que une ESP32, Django e tecnologias web para controlar o tempo de permanência de colaboradores em ambientes frios de forma segura e automatizada.

## 🚀 Funcionalidades
- Leitura RFID com ESP32 para entrada/saída
- Alertas sonoros e visuais (buzzer e dashboard)
- Temporizador individual por colaborador
- Cadastro automático de usuários

## 🛠️ Tecnologias Utilizadas
**Hardware:** ESP32, MFRC522 (RFID), buzzer passivo  
**Backend:** Python, Django  
**Frontend:** HTML, CSS, JavaScript  
**Protocolos:** HTTP, SPI

## 📊 Impacto
- Redução de riscos operacionais
- Conformidade com normas de segurança
- Fácil adaptação para outros ambientes industriais

## 📸 Imagens do Sistema
_Aqui você pode adicionar prints da interface, dashboard em tempo real e do hardware montado._

## Para rodar o servidor Django
- clonar o repositorio:

git clone https://github.com/Fernando8312/Projeto_Integrador_V.git

- instale os requirements:

pip install - r requirements.txt

- acessar a pasta cold_chamber

- rodar as migrations

python manage.py migrate

- rodar o servidor python

python manage.py runserver 0.0.0.0:8000

- acessar no navegador

http://localhost:8000/dashboard/

## 📂 Estrutura do Projeto
- `/backend`: aplicação Django
- `/frontend`: interface web estática
- `/hardware`: código do ESP32 e esquemas
- `/docs`: relatórios e documentação técnica