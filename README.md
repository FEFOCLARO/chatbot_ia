<<<<<<< HEAD
# chatbot_ia
Chatbot com IA feito em Python
=======
# Chatbot IA

Um chatbot inteligente construído com Python e processamento de linguagem natural.

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/chatbot-ia.git
cd chatbot-ia
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
chatbot_ia/
│
├── src/                    # Código-fonte
│   ├── chatbot/           # Módulo principal do chatbot
│   └── utils/             # Funções utilitárias
│
├── tests/                 # Testes automatizados
├── data/                  # Arquivos de dados
├── docs/                  # Documentação
├── config/               # Arquivos de configuração
├── requirements.txt      # Dependências do projeto
└── README.md            # Este arquivo
```

## Uso

Para iniciar o chatbot:

```python
from src.chatbot.bot import SimpleChatbot

bot = SimpleChatbot()
bot.iniciar_chat()
```

## Desenvolvimento

- Use `black` para formatar o código: `black src/`
- Execute os testes: `pytest tests/`
- Verifique o estilo do código: `flake8 src/`

## Licença

Este projeto está sob a licença MIT.
>>>>>>> ceb391c (Primeiro commit, primeira implementação)
