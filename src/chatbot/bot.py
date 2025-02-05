# src/chatbot/bot.py

import logging
from pathlib import Path
import yaml
import random
from ..utils.text_processor import TextProcessor

class Chatbot:
    """
    Classe principal do chatbot que gerencia a interação com o usuário,
    processa mensagens e gera respostas apropriadas.
    """
    
    def __init__(self, config_path='config/config.yml'):
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Carregar configurações
        self.config = self._load_config(config_path)
        
        # Inicializar processador de texto
        self.text_processor = TextProcessor(config_path)
        
        # Inicializar estado do chat
        self.context = {
            'last_intent': None,
            'last_entities': [],
            'conversation_history': [],
            'user_name': None
        }
        
        self.logger.info("Chatbot inicializado com sucesso")
    
    def _load_config(self, config_path):
        """Carrega as configurações do arquivo YAML"""
        try:
            # Converter para Path para manipulação mais segura do caminho
            config_file = Path(config_path)
            
            # Se o caminho não for absoluto, assumir relativo ao diretório atual
            if not config_file.is_absolute():
                config_file = Path.cwd() / config_path
            
            self.logger.info(f"Tentando carregar configuração de: {config_file}")
            
            if not config_file.exists():
                self.logger.error(f"Arquivo de configuração não encontrado: {config_file}")
                # Retornar configuração padrão em vez de dict vazio
                return {
                    'chatbot': {'name': 'Botinho'},
                    'responses': {
                        'saudacao': ['Olá!', 'Oi, como vai?', 'Olá, como posso ajudar?'],
                        'despedida': ['Até logo!', 'Tchau!', 'Foi bom conversar com você!'],
                        'ajuda': ['Como posso ajudar?', 'Estou aqui para ajudar!'],
                        'default': 'Desculpe, não entendi. Pode reformular?'
                    }
                }
            
            with open(config_file, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                self.logger.info("Configuração carregada com sucesso")
                return config
                
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
            # Retornar configuração padrão em caso de erro
            return {
                'chatbot': {'name': 'Botinho'},
                'responses': {
                    'saudacao': ['Olá!', 'Oi, como vai?', 'Olá, como posso ajudar?'],
                    'despedida': ['Até logo!', 'Tchau!', 'Foi bom conversar com você!'],
                    'ajuda': ['Como posso ajudar?', 'Estou aqui para ajudar!'],
                    'default': 'Desculpe, não entendi. Pode reformular?'
                }
            }
    
    def _get_response_by_intent(self, intent, entities=None):
        """Seleciona uma resposta apropriada com base na intenção detectada"""
        responses = self.config.get('responses', {})
        
        if intent in responses:
            # Se tivermos respostas específicas para esta intenção
            possible_responses = responses[intent]
            if isinstance(possible_responses, list):
                return random.choice(possible_responses)
            return possible_responses
        
        # Resposta padrão se não encontrarmos uma específica
        return responses.get('default', "Desculpe, não entendi. Pode reformular?")
    
    def _update_context(self, intent, entities, user_message):
        """Atualiza o contexto da conversa"""
        self.context['last_intent'] = intent
        self.context['last_entities'] = entities
        self.context['conversation_history'].append({
            'user': user_message,
            'intent': intent,
            'entities': entities
        })
    
    def _should_remember_context(self, intent):
        """Determina se devemos manter o contexto para esta intenção"""
        # Lista de intenções que devem manter contexto
        context_intents = ['informacao', 'ajuda']
        return intent in context_intents
    
    def process_message(self, message):
        """
        Processa a mensagem do usuário e retorna uma resposta apropriada.
        Este é o método principal que coordena todo o processo de resposta.
        """
        try:
            self.logger.info(f"Processando mensagem: {message}")
            
            # Processar o texto
            intent = self.text_processor.get_intent(message)
            self.logger.info(f"Intenção detectada: {intent}")
            
            entities = self.text_processor.extract_entities(message)
            self.logger.info(f"Entidades extraídas: {entities}")
            
            # Atualizar contexto
            self._update_context(intent, entities, message)
            
            # Gerar resposta
            response = self._get_response_by_intent(intent, entities)
            self.logger.info(f"Resposta gerada: {response}")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
            return "Desculpe, ocorreu um erro ao processar sua mensagem."
    
    def run(self):
        """Inicia o loop principal do chatbot"""
        print(f"Bot: {self.config['chatbot']['name']} iniciado. Digite 'sair' para encerrar.")
        
        while True:
            try:
                # Receber input do usuário
                user_input = input("Você: ").strip()
                
                # Verificar comando de saída
                if user_input.lower() == 'sair':
                    print("Bot: Até logo!")
                    break
                
                # Processar mensagem e gerar resposta
                response = self.process_message(user_input)
                
                # Mostrar resposta
                print(f"Bot: {response}")
                
            except KeyboardInterrupt:
                print("\nBot: Encerrando chatbot...")
                break
            except Exception as e:
                self.logger.error(f"Erro no loop principal: {e}")
                print("Bot: Desculpe, ocorreu um erro inesperado.")