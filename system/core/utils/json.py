import json
import os
from datetime import datetime
from system.core.config.config import log


def gerar_json(criptos: list, saida: str) -> str:
    '''
    Salva os dados das moedas em JSON estruturado.

    Args:
        criptos: lista de itens com os dados das moedas
        saida: pasta onde o json vai ser gravado

    Returns:
        caminho do arquivo json gerado
    '''
    os.makedirs(saida, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arquivo_json = os.path.join(saida, f'coins_{timestamp}.json')

    log.info(f"estruturando {len(criptos)} criptos em JSON", extra={'item_id': 'coins_json'})

    itens = []
    for c in criptos:
        itens.append({
            'id': c.get('id'),
            'symbol': c.get('symbol'),
            'name': c.get('name'),
            'current_price': c.get('current_price'),
            'market_cap': c.get('market_cap'),
            'total_volume': c.get('total_volume')
        })

    with open(arquivo_json, 'w', encoding='utf-8') as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)

    log.info(f"salvou {len(itens)} itens em {arquivo_json}", extra={'item_id': 'coins_json'})
    return arquivo_json
