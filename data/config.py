from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста

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
    'code' : 'def50200cd3c68686257a91c755e36b9a309a262a1e22a34593445fe1c5bbcb07e61dce8dda3431067985ea5efd3079a88e8d9cb606821f5d89981f8401aa98e3cc3d57e89483349e0f5d3a704613032b4db7a879c0554d7a5cb80543e578bd26b4b0bd13bd78ca05eb85edb7e81d1676e1254c905648fae7e32b6b7ffdf4c93b5a6b5c02a209aad0bb3d4a96577b29b31ff9df80c0ff567bc9d29e860be95a140fecc1ef311c2759d9eb009906bc7ba19fa50cd6e03ec5e6cde07f28ed2050defd5ab4bc4490b2f08177dd029d3cb507c542a193786843722c289bc80bf31be338889ab463d5303f086c5e7a5e09cd64a3beb7192f9bbe376a5087e328cac2db7e0ca1a23278d64619d8bd1bda8d312c195eb86ab64218f48c8e4eed5ce37352f53d1ede30c881206a7aaf4f2126fb6e0a01baa899c004ff641d55d068b66528ca70f6765595bacee9341652d8ea233808e4e87b48216bfd81adb8a5f1047a08d9d1fb39dc39a6400119af9fb6c38aca47a8c1055fe91e109d10505090c673dbc281bf1218c08d8fc0e6db3c5d45a31275be8ee283d0aaa747447b468f4bcb003ff5162ec3e4bdac5a21c71b837bbd3cb539979c459ce09b642b2de3254e03de62081',
    'redirect_url' : 'https://barcaacademy.ru/',
    'client_id' : '80c88f56-1922-478c-9a03-fc8b3fd9a232',
    'client_secret' : '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz',
    'subdomain' : "barcaacademy",
}