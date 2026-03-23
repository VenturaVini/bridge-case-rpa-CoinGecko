from time import time, sleep
from typing import List, Dict, Optional
import requests
from system.core.config.config import log


class CoinGeckoAPI:
    '''
    API client do CoinGenko para buscar dados de criptomoedas.
    '''

    def __init__(self, config: dict, moeda: str = 'usd'):
        self.log = log
        self.config = config                                    # configuracao da .env
        self.base_url = config['coingecko_url']
        self.timeout = config['coingecko_timeout']  # configuracao da .env
        self.moeda = moeda  # tipo de moeda a url padrao vem moeda usd
        
        # métricas de execução
        self.metricas = {
            "requisicoes_feitas": 0,
            "requisicoes_sucesso": 0,
            "requisicoes_falha": 0,
            "tempo_medio_resposta": 0.0,
            "taxa_sucesso": 0.0
        }
        
        self.tempos_resposta = []
    
    
    def buscar_lista_criptos(self, limite: int = 5) -> List[Dict]:
        '''
        Puxa lista das principais criptomoedas da API CoinGecko

        Args:
            limite: número máximo de criptos a retornar

        Returns:
            lista de dicionários com dados das criptos
        '''
        endpoint = f"{self.base_url}/coins/markets"
        params = {
            
            'vs_currency': self.moeda,      # vs_currency: moeda para retorno da api (exemplo: brl = Real do brasil)
            'order': 'market_cap_desc',   # ordem de capitalização de mecado
            'per_page': limite,     # número de registros por página
            'page': 1, # numero da página ( padrao 1)
            'sparkline': False # sem graficos de preço
        }

        dados = self._fazer_requisicao(endpoint, params)
        if dados:
            self.log.info(f"buscou {len(dados)} criptomoedas da API", extra={'item_id': 'coins'})
            return dados
        else:
            self.log.error("falhou ao buscar lista de criptos", extra={'item_id': 'coins'})
            return []
    
    def _fazer_requisicao(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        '''
        Faz uma requisição HTTP com retry automático.

        Args:
            endpoint: URL endpoint
            params: parâmetros da query

        Returns:
            dados JSON da resposta ou None se der erro
        '''
        max_tentativas = self.config['max_retries'] # maximo de tetativas
        delay_base = self.config['retry_delay_base'] # delay do back
        
        for tentativa in range(max_tentativas):
            try:
                tempo_inicio = time()
                
                self.metricas['requisicoes_feitas'] += 1 # conta a tentativa de requisicao, se chegar ao maximo ele para e retorna vazio
                
                resposta = requests.get(
                    endpoint,
                    params=params,
                    timeout=self.timeout,
                    headers={'Accept': 'application/json'}
                )
                
                tempo_resposta = time() - tempo_inicio
                self.tempos_resposta.append(tempo_resposta)
                
                # verifica se a resposta foi ok
                resposta.raise_for_status() 
                
                dados = resposta.json()
                
                self.metricas['requisicoes_sucesso'] += 1
                self.log.debug(f"requisicao ok: {endpoint}", extra={'item_id': endpoint})

                return dados

            except requests.Timeout:
                delay = delay_base ** tentativa     # tenta de novo com delay exponencial
                self.log.warning(f"timeout na tentativa {tentativa + 1}, esperando {delay} segundos ", extra={'item_id': endpoint})
                sleep(delay)
                continue

            except requests.HTTPError as e:
                
                self.metricas['requisicoes_falha'] += 1     # erro de htpp - loga e para
                self.log.error(f"erro HTTP {resposta.status_code}: {endpoint}", extra={'item_id': endpoint})
                return None

            except Exception as e:
                self.metricas['requisicoes_falha'] += 1
                if tentativa < max_tentativas - 1: # se a tentativa for maior q o maximo, ele para e informa
                    delay = delay_base ** tentativa
                    self.log.warning(f"erro na tentativa {tentativa + 1}: {str(e)}, esperando {delay}s", extra={'item_id': endpoint})
                    sleep(delay)
                    continue
                else:
                    self.log.error(f"erro final apos {max_tentativas} tentativas: {str(e)}", extra={'item_id': endpoint})
                    return None
        
        return None
    
    def calcular_metricas_finais(self) -> None:
        '''
        Calcula as métricas da execução
        '''
        total_requisicoes = self.metricas['requisicoes_feitas']
        
        if total_requisicoes > 0:  # basicamente ele pega a taxa de sucesso e divide pelo total de vezes q rodou, pra ver se deu certo ex: 33% ou 100%
            self.metricas['taxa_sucesso'] = (self.metricas['requisicoes_sucesso'] / total_requisicoes) * 100
        
        if self.tempos_resposta:  
            #   Ja aqui ele soma todos os tempos da resposta e divide pela quantidade delas ex: rodou 1 vez de 3 segundos ele divide 
            #   pela quantidade que rodou (1) = 3/1 = 3 
            self.metricas['tempo_medio_resposta'] = sum(self.tempos_resposta) / len(self.tempos_resposta)
