# src/utils/text_processor.py

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import yaml
import logging
from pathlib import Path
import re

class TextProcessor:
    """
    Classe responsável pelo processamento de texto do chatbot.
    Realiza operações como tokenização, remoção de stopwords e lematização.
    """
    
    def __init__(self, config_path='config/config.yml'):
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Carregar configurações
        self.config = self._load_config(config_path)
        
        # Inicializar componentes NLTK
        self._initialize_nltk()
        
        # Criar lematizador
        self.lemmatizer = WordNetLemmatizer()
        
        self.logger.info("Processador de texto inicializado com sucesso")
    
    def _load_config(self, config_path):
        """Carrega as configurações do arquivo YAML"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
            return {}
    
    def _initialize_nltk(self):
        """Inicializa e baixa recursos necessários do NLTK"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            self.stopwords = set(stopwords.words('portuguese'))
        except Exception as e:
            self.logger.error(f"Erro ao inicializar NLTK: {e}")
            self.stopwords = set()
    
    def preprocess_text(self, text):
        """
        Realiza o pré-processamento completo do texto:
        1. Converte para minúsculas
        2. Remove caracteres especiais
        3. Tokeniza
        4. Remove stopwords
        5. Lematiza (se configurado)
        """
        # Converter para minúsculas
        text = text.lower()
        
        # Remover caracteres especiais
        text = re.sub(r'[^\w\s]', '', text)
        
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Remover stopwords (se configurado)
        if self.config.get('nlp', {}).get('stopwords', True):
            tokens = [token for token in tokens if token not in self.stopwords]
        
        # Lematizar (se configurado)
        if self.config.get('nlp', {}).get('lemmatization', True):
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        self.logger.debug(f"Texto processado: {tokens}")
        return tokens
    
    def calculate_similarity(self, text1, text2):
        """
        Calcula a similaridade entre dois textos usando uma métrica simples de
        sobreposição de palavras. Pode ser expandido para usar técnicas mais
        avançadas como embeddings ou similaridade coseno.
        """
        tokens1 = set(self.preprocess_text(text1))
        tokens2 = set(self.preprocess_text(text2))
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def extract_entities(self, text):
        """
        Extrai entidades do texto. Esta é uma implementação básica que pode
        ser expandida para usar reconhecimento de entidades nomeadas (NER).
        """
        tokens = self.preprocess_text(text)
        # Por enquanto, retorna apenas os tokens como entidades
        # Pode ser expandido para usar NLTK NER ou spaCy
        return tokens
    
    def get_intent(self, text):
        """
        Identifica a intenção do texto. Esta é uma implementação básica
        que pode ser expandida para usar classificação de texto mais avançada.
        """
        tokens = self.preprocess_text(text)
        
        # Dicionário básico de intenções
        intents = {
            'saudacao': ['oi', 'ola', 'Oi', 'Olá', 'olá', 'buenas', 'salve', 'opa', 'eae', 'bom', 'dia', 'tarde', 'noite'],
            'despedida': ['tchau', 'adeus', 'ate', 'logo', 'fim'],
            'ajuda': ['ajuda', 'ajudar', 'como', 'pode', 'auxilio'],
            'informacao': ['quero', 'saber', 'informacao', 'sobre', 'explique']
        }
        
        # Calcular pontuação para cada intenção
        scores = {}
        for intent, keywords in intents.items():
            score = sum(1 for token in tokens if token in keywords)
            scores[intent] = score
        
        # Retornar a intenção com maior pontuação
        max_intent = max(scores.items(), key=lambda x: x[1])
        
        # Se a pontuação for 0, retornar intent desconhecido
        if max_intent[1] == 0:
            return 'desconhecido'
            
        return max_intent[0]