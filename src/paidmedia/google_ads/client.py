"""Thin read-only Google Ads wrapper. Write operations come in a later phase,
behind dry-run + audit logging."""
from ..config import load_google_ads_settings


def get_client():
    from google.ads.googleads.client import GoogleAdsClient  # needs `pip install .[google]`
    return GoogleAdsClient.load_from_dict(load_google_ads_settings().as_client_config())


def run_query(client, customer_id: str, gaql: str):
    service = client.get_service("GoogleAdsService")
    for batch in service.search_stream(customer_id=customer_id, query=gaql):
        for row in batch.results:
            yield row
