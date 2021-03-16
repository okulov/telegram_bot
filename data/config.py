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
    'code' : 'def5020021fbcc7a90030c94e1e753b75a8b4350be08b6ee380fb92af18e9adcbecdd262bd5567e0246f8cb70c0e67880e56c4887e3e980babe85af14cd3709a1b367f1954ffd760049d3afa02d5f6e4af3959f219924045ad632303f38630647ac3c81b33fae90b50d575dbeaadb702e7bb3d751d8387be8446f427c11e624aba74848417ec5b68230a7c69d6564a489c8c9b503c3e9d79e026dae60c512005ba4b73bad62f75ecfcd19e5933c5d658bb756ecf9b1a354e13065e8f583e45d8325c560896129cea17614d90c62ce2bad93cd4e4359d566097c2869729346605452d018df3738e50739561f90e5baa6409f794ebe3d439edb87ef8da8554a25c23800efef8fe9a59882ca12580f433c4d0419cc6b050d9898d839361504d3c89337627836f6cea2226fa630e959d5b89f7c4e721aa099e94524082377b7d0899b5987e0c2220235d78227c706c5a2e1e1397b52c83a7cb823c60098eaddd508775a65f91a4bb56bb0eafaddf257499754d38b3b9fd6b7bebd8a561cb45956c62a13f1715471ac59f77e258bf31538c47c501076d021f925ab6caa3ab030f02ae67fe701b75019158aa760c450b57751cf103a01258a6c8ff950cc95f7c1151a8feeffc',
    'redirect_url' : 'https://barcaacademy.ru/',
    'client_id' : '80c88f56-1922-478c-9a03-fc8b3fd9a232',
    'client_secret' : '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz',
    'subdomain' : "barcaacademy",
}