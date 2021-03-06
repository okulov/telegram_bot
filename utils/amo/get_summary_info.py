import locale
from datetime import datetime


def amount_clients(data):
    return len(data)

def payments(data):
    payments = 0
    i = 0
    row = 0
    for lead in data:
        for key, value in lead.items():
            if 'оплата' in key.lower().split() and str(value).isdigit():
                payments+= int(value)
                i+=1
    return payments/i


def dept(data):
    dept = 0
    for lead in data:
        for key, value in lead.items():
            if 'задолженность' in key.lower().split() and str(value).isdigit():
                dept+= int(value)
    return '{0:,}'.format(dept).replace(',', ' ')


def avo(data):
    #return round(payments(data),0)
    return '{0:,}'.format(round(payments(data),0)).replace(',', ' ')


def ltv(data):
    return ''


def plan_sum(data):
    plan = 0
    for lead in data:
        for key, value in lead.items():
            if 'план' in key.lower().split() and str(value).isdigit():
                plan+= int(value)
    return '{0:,}'.format(plan).replace(',', ' ')


def fact_sum(data):
    fact = 0
    for lead in data:
        for key, value in lead.items():
            if 'оплата' in key.lower().split() and str(value).isdigit():
                fact+= int(value)
    return '{0:,}'.format(fact).replace(',', ' ')


def select_mounth(data, type):
    # locale.setlocale(locale.LC_ALL, "")
    # mounth = datetime.now().strftime('%B')
    # fields = ['ID', 'Название сделки', mounth]
    # print(mounth)
    # data_new = data.copy()
    # for i, lead in enumerate(data):
    #     for key, value in lead.items():
    #         if mounth not in key.lower().split():
    #             del data_new[i][key]
    # print(data_new)
    return data


def get_summary_info(data: dict, filial: str, type: str):
    if type == 'Общая информация':
        type_str = ''
    else:
        type_str = f', {type.lower()}'

    if filial == 'all':
        header = f'Сводная информация, оба филиала{type_str}:\n'
    else:
        header = f'Сводная информация, {filial}{type_str}:\n'

    params_all = {
        'Количество клиентов': amount_clients(data),
        'Задолженность': dept(data),
        'Средний чек': avo(data),
        'Средний LTV': ltv(data)
    }

    if type != 'Общая информация':
        data = select_mounth(data, type)

    params_mounth = {
        'Количество клиентов': amount_clients(data),
        'Сумма оплат (план)': '',#plan_sum(data),
        'Сумма оплат (факт)': '',#fact_sum(data),
        'Задолженность': '',#dept(data),
        'Средний чек': '',#avo(data)

    }


    if type == 'Общая информация':
        result = header + ''.join([f'{key}: {value}\n' for key, value in params_all.items()])
    else:
        result = header + ''.join([f'{key}: {value}\n' for key, value in params_mounth.items()])

    return result
