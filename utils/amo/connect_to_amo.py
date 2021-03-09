from amocrm.v2 import tokens

from data import config


def connect():
    params = config.CONNECT_PARAMS
    tokens.default_token_manager(
            client_id=params.get('client_id'),
            client_secret=params.get('client_secret'),
            subdomain=params.get('subdomain'),
            redirect_url=params.get('redirect_url'),
            storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )
    # tokens.default_token_manager.init(code=code, skip_error=False)
    tokens.default_token_manager.get_access_token()
    return tokens
