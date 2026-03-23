import json
from datetime import datetime
from system.core.services.coingecko_service import CoinGeckoAPI
from system.core.config.config import carregar_config
from system.core.utils.csv import salvar_coins_csv
from system.core.utils.json import gerar_json


def main() -> bool:
    '''
    Executa o fluxo completo da api, ele extrai, coleta e salvar os arquivos
    '''
    config = carregar_config()
    service = CoinGeckoAPI(config, moeda=config.get('moeda', 'usd'))


    cryptos = service.buscar_lista_criptos(config.get('quantidade_criptos', 5))

    # define status da execução (uipath)
    if cryptos:
        status = 'success'
    else:
        status = 'failed'

    # criacao de arquivos
    arquivo_csv = salvar_coins_csv(cryptos, config.get('data_dir', './system/data'))
    arquivo_json = gerar_json(cryptos, config.get('data_dir', './system/data'))

    service.calcular_metricas_finais()

    resumo = {   # resumo da execução
        'timestamp': datetime.now().isoformat(),
        'status': status,
        'registros_retorno': len(cryptos),
        'arquivo_csv': arquivo_csv,
        'queue_json': arquivo_json,
        'metricas': service.metricas
    }

    print(json.dumps(resumo, ensure_ascii=False, indent=2))

    return status == 'success'


if __name__ == '__main__':
    main()
