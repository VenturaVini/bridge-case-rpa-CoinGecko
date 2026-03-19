import os
from dotenv import load_dotenv


def carregar_config() -> dict:
    '''
    Puxa as configurações do .env e retorna um dicionário.

    Returns:
        dicionário com todas as configurações do projeto
    '''
    load_dotenv(override=True) # pegar da .env msm
    
    config = {
        # API CoinGecko
        "coingecko_url": os.getenv("COINGECKO_URL", "https://api.coingecko.com/api/v3"),
        "coingecko_timeout": int(os.getenv("COINGECKO_TIMEOUT", "10")),  # tempo de retono
        
        # Configurações de processo
        "max_retries": int(os.getenv("MAX_RETRIES", "3")),  # numero maximo de tentativas
        "retry_delay_base": int(os.getenv("RETRY_DELAY_BASE", "2")), # delay para tenta novamente a requi

        # Diretorios de saída
        "data_dir": os.getenv("DATA_DIR", "./system/data"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),

        # Tipo de moeda retorno
        "moeda": os.getenv("MOEDA", "usd")
    }
    
    return config
