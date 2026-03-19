import logging
import json
import os
from datetime import datetime


class JsonFormatter(logging.Formatter):
    '''
    Formata logs em JSON estruturado. Inclui timestamp, nivel, modulo e mensagem.
    '''
    
    def format(self, record: logging.LogRecord) -> str:
        # constrói o dicionário do log
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "nivel": record.levelname,
            "modulo": record.name,
            "mensagem": record.getMessage()
        }
        
        # se tem item_id nos extras, adiciona
        if hasattr(record, 'item_id'):
            log_data['item_id'] = record.item_id
        
        # se tem erro, adiciona traceback
        if record.exc_info:
            log_data['erro'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


def setup_logger(modulo: str, log_dir: str = './system/data/logs') -> logging.Logger:
    '''
    Configura um logger para o módulo com formatação JSON.
    Salva em arquivo e imprime no console.

    Args:
        modulo: nome do módulo (ex: modulo_a, modulo_e)
        log_dir: pasta onde os logs serão salvos

    Returns:
        logger configurado e pronto pra usar
    '''
    logger = logging.getLogger(modulo)
    logger.setLevel(logging.DEBUG)

    # handler pra console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(JsonFormatter())
    logger.addHandler(console_handler)

    # handler pra arquivo
    os.makedirs(log_dir, exist_ok=True)
    data = datetime.now().strftime('%Y%m%d')
    arquivo_log = os.path.join(log_dir, f'{modulo}_{data}.log')

    file_handler = logging.FileHandler(arquivo_log, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    return logger
