from amocrm.v2 import tokens


def connect():
    code = 'def50200e5ebcfff6f7cc247eb5c429b487e78b6d2d3ee51a9a478f421071b4bf4b764b822d4eaabde56bb8da7e4770af5bfe0b9b0eec2c3e48c24a1b117b84886aecadf03786c8bb5149463b6befcbf36ca2c10ccdf0110e900bbe217548c0eedb33eb30aaeebcabcbcb5d94706b9ab368a1f6eb86e767cf2d2a2a1d9126ae1c1cb88559e36a7f715260cf5b89deeea5eca4278bf9321e3712ff912f9a48bd1e96db0b17b4725b73d9a50d30649efb05b89a2ea63bba66df3ae43993d7095ca15cfd99b199d84927f9324df0a022fb3dc184492d39da57ac498941ed35280cff8bc78ceec06a66edcd77878f2a257e1ed7d412e43f811b222bbdf17be896fa6069d9378289f895a49e488394ea794d639d01477acc971b2e2806619d751a9bb3a08d23747cfe8a1337b8bf6e7e31445f68ca3e804bbfd1df8da4cabb84d865a1f808bc1cce8ab03775a60522af12f7a9a541d6f5211eb2be62ca92445c3f090790d39fd6589fb44780b56363b494f3d264b256c1aaac9d1115e4708630fd27c14a4e0046ac98ccdb40a30ef5c34b0157f0c10be45a3cc6f0d2eb299c8cf626d487b1a6e714a1bcb5816a0eac5fb0e4f5a025e30d00f7b33051ed0cc0d0e01646ebcd6'
    redirect_url = 'https://barcaacademy.ru/'
    client_id = '80c88f56-1922-478c-9a03-fc8b3fd9a232'
    client_secret = '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz'

    tokens.default_token_manager(
        client_id=client_id,
        client_secret=client_secret,
        subdomain="barcaacademy",
        redirect_url=redirect_url,
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
    )
    # tokens.default_token_manager.init(code=code, skip_error=False)
    tokens.default_token_manager.get_access_token()
    return tokens
