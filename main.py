# main.py

from src.chatbot.bot import Chatbot
import logging

def main():
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='chatbot.log'
    )
    
    # Criar e iniciar o chatbot
    try:
        bot = Chatbot()
        bot.run()
    except Exception as e:
        logging.error(f"Erro ao executar o chatbot: {e}")

if __name__ == "__main__":
    main()