import copy
import locale
from datetime import datetime
from data import config


def amount_clients(data):
    x = [x[config.PARAMS_AMO.get('name_id')] for x in data]
    return len(set(x))


def payments(data):
    payments = 0
    i = 0
    row = 0
    for lead in data:
        for key, value in lead.items():
            if 'оплата' in key.lower().split() and str(value).isdigit():
                payments += int(value)
                i += 1
    return payments / i


def dept(data):
    dept = 0
    for lead in data:
        for key, value in lead.items():
            if 'задолженность' in key.lower().split() and value not in ['', ' ']:
                dept += float(value)
    return '{0:,}'.format(dept).replace(',', ' ')


def avo(data):
    # return round(payments(data),0)
    return '{0:,}'.format(round(payments(data), 0)).replace(',', ' ')


def ltv(data):
    list_years = config.PARAMS_AMO.get('years')
    list_mounth = config.PARAMS_AMO.get('mounths')
    pay_str = config.PARAMS_AMO.get('name_for_pay')
    plan_str = config.PARAMS_AMO.get('name_for_plan')
    today_mounth = list_mounth[int(datetime.now().strftime('%m')) - 1]
    today_year = datetime.now().strftime('%Y')
    sum_ltv = 0

    for lead in data:
        life_mounth = 0
        amount_mounths = 0
        for y in list_years:
            for m in list_mounth:
                amount_mounths += 1
                field_pay = pay_str + ' ' + m + ' ' + y
                field_plan = plan_str + ' ' + m + ' ' + y
                if field_pay in lead.keys() and field_plan in lead.keys():
                    if lead[field_pay] not in [0, ''] and lead[field_plan] not in [0, '']:
                        life_mounth += 1
                if m == today_mounth and y == today_year:
                    break
            if m == today_mounth and y == today_year:
                break
        sum_ltv += life_mounth

    ltv = sum_ltv / amount_clients(data)

    return round(ltv, 2)


def plan_sum(data):
    plan = 0
    for lead in data:
        for key, value in lead.items():
            if 'план' in key.lower().split() and str(value).isdigit():
                plan += float(value)
    return '{0:,}'.format(plan).replace(',', ' ')


def fact_sum(data):
    fact = 0
    for lead in data:
        for key, value in lead.items():
            if 'оплата' in key.lower().split() and value not in ['', ' '] and 'дата' not in key.lower().split():
                fact += float(str(value).replace(',', '.'))
    return '{0:,}'.format(fact).replace(',', ' ')


def select_mounth(data, type):
    list_mounth = config.PARAMS_AMO.get('mounths')

    if 'прошлый' in type.lower().split():
        if datetime.now().strftime('%m') == '01':
            mounth = 'декабрь'
            today_year = str(int(datetime.now().strftime('%Y')) - 1)
        else:
            mounth = list_mounth[int(datetime.now().strftime('%m')) - 2]
            today_year = datetime.now().strftime('%Y')
    elif 'текущий' in type.lower().split():
        mounth = list_mounth[int(datetime.now().strftime('%m')) - 1]
        today_year = datetime.now().strftime('%Y')

    base_fields = ['ID', 'Название сделки']
    data_new = copy.deepcopy(data)
    for i, lead in enumerate(data):
        for key, value in lead.items():
            if key in base_fields:
                continue
            if mounth not in key.lower().split() or today_year not in key.lower().split():
                del data_new[i][key]
    return data_new


def get_summary_info(data: list, filial: str, type: str):
    locale.setlocale(locale.LC_ALL, '')

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
        'Сумма оплат (план)': plan_sum(data),
        'Сумма оплат (факт)': fact_sum(data),
        'Задолженность': dept(data),
        'Средний чек': avo(data)

    }

    if type == 'Общая информация':
        result = header + ''.join([f'{key}: {value}\n' for key, value in params_all.items()])
    else:
        result = header + ''.join([f'{key}: {value}\n' for key, value in params_mounth.items()])

    return {'info': result, 'data': data}


def get_summary_lead_info(data: list):
    res = []
    for lead in data:
        lead_field = {
            'ID': lead['ID'],
            'Название сделки': lead['Название сделки'],
            'Статус': lead['Статус'],
            'Бюджет': lead['Бюджет'],
            'Тэги': ', '.join(lead['Тэги']),
            'Ссылка': lead['Ссылка']
        }
        result = ''.join([f'{key}:  {value}\n' for key, value in lead_field.items()])
        res.append(result)
    return '\n'.join(res)
