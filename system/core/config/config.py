import os
from dotenv import load_dotenv
import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "nivel": record.levelname,
            "modulo": record.name,
            "mensagem": record.getMessage()
        }

        if hasattr(record, 'item_id'):
            log_data['item_id'] = record.item_id

        if record.exc_info:
            log_data['erro'] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_centralizado_logger(log_dir: str = './system/data/logs') -> logging.Logger:
    '''Configura um logger centralizado para toda a aplicação.'''
    logger = logging.getLogger('app')

    if logger.handlers:  # evita duplicar handlers
        return logger

    logger.setLevel(logging.DEBUG)

    # console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)

    # arquivo único centralizado
    os.makedirs(log_dir, exist_ok=True)
    arquivo_log = os.path.join(log_dir, 'app.log')

    file_handler = logging.FileHandler(arquivo_log, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    return logger


log = setup_centralizado_logger()


def carregar_config() -> dict:
    '''
    Puxa as configurações do .env e retorna um dicionário.

    Returns:
        dicionário com todas as configurações do projeto

    Raises:
        ValueError: se variáveis obrigatórias estiverem faltando
    '''
    load_dotenv(override=True) # pegar da .env msm

    # Validar variáveis obrigatórias
    coingecko_url = os.getenv("COINGECKO_URL")
    if not coingecko_url:
        raise ValueError("Variável de ambiente COINGECKO_URL é obrigatória")

    config = {
        # API CoinGecko
        "coingecko_url": coingecko_url,
        "coingecko_timeout": int(os.getenv("COINGECKO_TIMEOUT", "10")),  # tempo de retono
        
        # Configurações de processo
        "max_retries": int(os.getenv("MAX_RETRIES", "3")),  # numero maximo de tentativas
        "retry_delay_base": int(os.getenv("RETRY_DELAY_BASE", "2")), # delay para tenta novamente a requi

        # Diretorios de saída
        "data_dir": os.getenv("DATA_DIR", "./system/data"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),

        # Tipo de moeda retorno
        "moeda": os.getenv("MOEDA", "usd"),

        # Quantidade de criptomoedas
        "quantidade_criptos": int(os.getenv("QUANTIDADE_CRIPTOS", "5"))
    }

    return config
