import logging
import json
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


def setup_logger(modulo: str) -> logging.Logger:
    '''
    Configura um logger para o módulo com formatação JSON.

    Args:
        modulo: nome do módulo (ex: modulo_a, modulo_e)

    Returns:
        logger configurado e pronto pra usar
    '''
    logger = logging.getLogger(modulo)
    logger.setLevel(logging.DEBUG)
    
    # handler pra console
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(JsonFormatter())
    
    logger.addHandler(handler)
    
    return logger
