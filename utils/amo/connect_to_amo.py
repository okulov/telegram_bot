from amocrm.v2 import tokens

from data import config
import redis
from urllib.parse import urlparse


def connect():
    params = config.CONNECT_PARAMS
    url = urlparse(config.REDIS_URL)
    r = redis.Redis(host=url.hostname,
                    port=url.port,
                    username=url.username,
                    password=url.password,
                    ssl=False,
                    ssl_cert_reqs=None)
    tokens.default_token_manager(
        client_id=params.get('client_id'),
        client_secret=params.get('client_secret'),
        subdomain=params.get('subdomain'),
        redirect_url=params.get('redirect_url'),
        storage=tokens.RedisTokensStorage(r.client()),  # by default FileTokensStorage
    )

    try:
        tokens.default_token_manager.get_access_token()
    except:
        tokens.default_token_manager.init(code=config.AMO_CODE, skip_error=False)

    return tokens
