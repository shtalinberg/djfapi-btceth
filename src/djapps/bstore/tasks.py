import logging

from bstore.models import Block, Currency, Provider
from bstore.services import BlockchairFetcher, CoinMarketCapFetcher
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def fetch_latest_blocks():
    # Fetch BTC blocks
    btc_currency = Currency.objects.get(name='BTC')
    btc_provider = Provider.objects.get(name='CoinMarketCap')
    btc_fetcher = CoinMarketCapFetcher(btc_provider.api_key)

    btc_data = btc_fetcher.get_latest_block()
    if 'block_number' in btc_data:
        logger.info(f"Fetched BTC block: {btc_data}")
        Block.objects.create(
            currency=btc_currency,
            provider=btc_provider,
            block_number=btc_data['block_number'],
            block_created_at=btc_data['block_created_at'],
            created_at=timezone.now(),
        )
    else:
        logger.warning(f"Failed to fetch BTC block: {btc_data}")

    # Fetch ETH blocks
    eth_currency = Currency.objects.get(name='ETH')
    eth_provider = Provider.objects.get(name='BlockChair')
    eth_fetcher = BlockchairFetcher(eth_provider.api_key)

    eth_data = eth_fetcher.get_latest_block()
    if 'block_number' in eth_data:
        logger.info(f"Fetched ETH block: {eth_data}")
        Block.objects.create(
            currency=eth_currency,
            provider=eth_provider,
            block_number=eth_data['block_number'],
            block_created_at=eth_data['block_created_at'],
            created_at=timezone.now(),
        )
    else:
        logger.warning(f"Failed to fetch ETH block: {eth_data}")
