from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")

PARAMS_AMO = {
        'mounths': ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                    'ноябрь', 'декабрь'],
        'mounths_d':['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
        'years': ['2020', '2021'],
        'goal': 'факт',
        'plan': 'план',
        'data_str': 'дата',
        'name_for_pay': 'Оплата',
        'name_for_plan': 'План',
        'name_for_debt': 'Задолженность',
        'name_for_client': 'Название сделки',
        'name_id': 'ID',
    }

CONNECT_PARAMS = {
    'code' : 'def50200a3984c9c84e7aaed3cd05fa58f1cecbe056515b7ea5812fdcae0eb57c3b4d15eb765a61a79bc2daedd220067923b422490cb89e1a901defb5167dbf216ad387fbd10a7b82e6e9c0167905ebf009f433cba1767f8fe531e58fbee9bb4025d4a848cb979840bfc832cf910dbf13dce203b5c66c1fcb8a1440aa0ee7a0ab2ba7b6bea455f041d7b402604c84b45bdafc86b38c14fa1caa31661be315012bce273d514f76371ea74d47a8689bf27ca2d947146b778d63e184d9641ae70323e3a79ef456a1fc95f42803470af2aad59740f3588c26958eebf70a594d32eb42e1383d2ebebbad61fc410b0e0dc49147de70b0eee5b907b8de8847b2b6cd675b12343855aa03235b6dd0b1a8490ed839c317eef7d3fe4e15d8192b3b5dbdb56888ef115c52c5873b8cfd9cc9379ffdfaf4414e8fe4cd39e70ad667c44c111a7ca7bd5668e227748f4173038cb9681d8f8e44cec70bbc29c89b089f87f8b22f4094dfe4c248ea49fca41999e22bd5033f42c40c8d2eab88f93f01afe4c8454e3037f57fcca66d2da47ee564f8fafe4f652273b4243a1cc6c71a245596b60e7d32834ec405955d1f391a0adb6975ffff8803f1a73c26ed539f02b8ec45144ea868fa8b4',
    'redirect_url' : 'https://barcaacademy.ru/',
    'client_id' : '80c88f56-1922-478c-9a03-fc8b3fd9a232',
    'client_secret' : '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz',
    'subdomain' : "barcaacademy",
}