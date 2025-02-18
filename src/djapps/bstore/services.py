import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


class BlockFetcherBase:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_latest_block(self):
        raise NotImplementedError


class CoinMarketCapFetcher(BlockFetcherBase):
    def get_latest_block(self):
        headers = {
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        url = 'https://pro-api.coinmarketcap.com/v1/blockchain/statistics/latest'
        params = {'symbol': 'BTC'}

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not data:
            return data
        if 'data' not in data or 'btc' not in data['data']:
            return data
        return {
            'block_number': data['data']['btc']['latest_block_height'],
            'block_created_at': datetime.fromtimestamp(
                data['data']['btc']['latest_block_timestamp']
            ),
        }


class BlockchairFetcher(BlockFetcherBase):
    def get_latest_block(self):
        if self.api_key and self.api_key.strip() != '0':
            url = f'https://api.blockchair.com/ethereum/stats?key={self.api_key}'
        else:
            url = f'https://api.blockchair.com/ethereum/stats'
        response = requests.get(url)
        data = response.json()
        logger.info(f"BlockchairFetcher data: {data}")
        print(f"BlockchairFetcher data: {data}")

        # Ensure we have valid data structure
        if not data or 'data' not in data or not data['data']:
            return None

        block_data = data['data']

        # Extract correct block number and timestamp
        if 'best_block_height' not in block_data or 'best_block_time' not in block_data:
            return None

        return {
            'block_number': block_data['best_block_height'],
            'block_created_at': datetime.strptime(
                block_data['best_block_time'], "%Y-%m-%d %H:%M:%S"
            ),
        }
