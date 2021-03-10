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
    'code' : 'def50200b46e47518880d4e23cad44e9633471ede43571f7495677bb3925c4780aff5beea77c9ad07f9230327305592b8d164f645d9e55ea310289c93d5a99452fe8f6f2f90a66a54c284ed5cd5448f25c747a12dc5b921ad0c6799175004bb501fb29f568f013a987c7c5d656e32fa39a884d05dcab9091a73c7ae19f5a188760950ccc20d994593f6c8e502a6f66b3b981d101051d678b95e6818fedbd4429eff9795230eeb8d4d0e152ef243aa5106cf016609ee5fa7aa47947930617c5e1e59b894b2461ab0322a519ee2e7c85c8e91a51ec8b87b37459e4ac96261b1c5992fa4572f1f1c21eac078b70e0004457c3f66af2e6244792fa002deb8c692fcf758c83d311bb42bfcb049c9d091f4930e13150509525e384c504be8160a64f0f6ff5c33a15ee79716e71cab9ecc380210725e905cde663c5f09bf1a9f4b408ae4f740e6d86109ac5e0b11797a0b8994e85c05447e2131385998cffb0d187364e37e5507f873729cb2801ef6d224c906af26764430067aca45a7ff7912eddb16d4d0b1450354a1de640fa404b2edbdcf629556cdc261b3231b01901687a66954a53895ca28b9df1df61ecfbc78503281e49b825d4dd86e0f22f05dd231a65b754510d11',
    'redirect_url' : 'https://barcaacademy.ru/',
    'client_id' : '80c88f56-1922-478c-9a03-fc8b3fd9a232',
    'client_secret' : '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz',
    'subdomain' : "barcaacademy",
}