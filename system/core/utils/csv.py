import csv
import os
from datetime import datetime
from system.core.config.config import log


def salvar_coins_csv(cripto: list, saida: str) -> str:
    '''

    Verifica se existe no arquivo csv as cripts, se existir ele ignora, se nao ele adiciona.
    Cria uma lista caso tenham o arquivo csv, e antes de salvar ele verifica se tem o id da criptos, 
    se tiver ele ignora, se nao ele salva, e no fim ele salva o arquivo csv.

    Ele salva arquivo com idempotencia por dia.

    Args:
        cripto: lista de dicts com os dados das moedas
        saida: pasta onde o csv vai ser gravado

    Returns:
        caminho do arquivo csv
    '''
    os.makedirs(saida, exist_ok=True)
    data = datetime.now().strftime('%Y%m%d')
    arquivo_csv = os.path.join(saida, f'coins_{data}.csv')
    ids_existentes = set()

    log.info(f"extraindo {len(cripto)} criptos", extra={'item_id': 'coins_csv'})

    if os.path.exists(arquivo_csv):
        with open(arquivo_csv, 'r', encoding='utf-8', newline='') as f:  # lê o arquivo existente pra extrair os ids do csv (se existir)
            leitor = csv.DictReader(f)
            for linha in leitor:
                ids_existentes.add(linha.get('id'))
        log.debug(f"encontrados {len(ids_existentes)} registros existentes", extra={'item_id': 'coins_csv'})

    novos_registros = []
    ignorados = 0
    for c in cripto:                                    # verifica se o id da criptomoeda já existe no arquivo, se existir ele ignora, se nao ele adiciona na lista de novos registros
        if c.get('id') in ids_existentes:
            ignorados += 1
            continue
        ids_existentes.add(c.get('id'))
        novos_registros.append({
            'id': c.get('id'),
            'symbol': c.get('symbol'),
            'name': c.get('name'),
            'current_price': c.get('current_price'),
            'market_cap': c.get('market_cap'),
            'total_volume': c.get('total_volume')
        })

    log.info(f"processou {len(novos_registros)} novos, {ignorados} duplicados", extra={'item_id': 'coins_csv'})

    if not novos_registros:
        log.warning("nenhum registro novo pra salvar", extra={'item_id': 'coins_csv'})
        return arquivo_csv


    colunas = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']

    # abre em append se o arquivo já existe, senão cria novo
    if os.path.exists(arquivo_csv):
        escrever_modo = 'a' # adiciona
    else:
        escrever_modo = 'w' # escreve novo

    with open(arquivo_csv, escrever_modo, encoding='utf-8', newline='') as f:   # salva os novos registros no arquivo csv, se o arquivo já existe ele adiciona, se nao ele cria novo
        writer = csv.DictWriter(f, fieldnames=colunas)
        if escrever_modo == 'w':
            writer.writeheader()
        writer.writerows(novos_registros)

    log.info(f"salvou {len(novos_registros)} registros em {arquivo_csv}", extra={'item_id': 'coins_csv'})
    return arquivo_csv
