import csv

import xlwt
from pip._vendor import chardet


# pyinstaller --onedir --onefile --name=take_payments "main.py"
from data import config


def get_mounth(dict, params):
    actual_mounth = set()
    for client in dict[1:2]:
        for field, value in client.items():
            for mounth in params.get('mounths'):
                if mounth in field.split() and (
                        set(params.get('years')).intersection(field.split()) != set()) and params.get(
                    'goal') in field.split():
                    actual_mounth.add(str(mounth))

    a_mounth = []
    for m in params.get('mounths'):
        if m in actual_mounth:
            a_mounth.append(m)

    act_mounth = {}
    for client in dict[1:2]:
        for year in params.get('years'):
            act_mounth[year] = set()
            for field, value in client.items():
                for mounth in params.get('mounths'):
                    if mounth in field.split() and (year in field.split()) and params.get('goal') in field.split():
                        act_mounth[year].add(str(mounth))

        year_mounths = {}
    for y, m in act_mounth.items():
        year_mounths[y] = []
        for month in params.get('mounths'):
            if month in m:
                year_mounths[y].append(month)
    return year_mounths


def read_csv(file: str) -> list:
    dict = []
    with open(file, 'rb') as det:
        str_bytes = det.read()
    coding = chardet.detect(str_bytes)['encoding']
    with open(file, encoding=coding) as f:
        reader = csv.DictReader(f)
        HEADERS = reader.fieldnames
        for row in reader:
            dict.append(row)
    print('Исходник csv прочитан')
    return dict


def is_data(field: str, data_str='дата') -> bool:
    fields = field.lower().split()
    return data_str in fields


def has_index_pay(field: str) -> bool:
    fields = field.lower().split()
    return fields[0].isdigit()


def index_pay(field: str) -> int:
    fields = field.lower().split()
    return fields[0]


def is_date_or_fact(field: str, params) -> bool:
    return (params.get('goal') in field.lower().split()) or (params.get('data_str') in field.lower().split())


def find_pay(client: dict, field: str, mounth: str, params: dict) -> []:
    index = None
    other_field = ''
    other = ''
    not_null = None
    if has_index_pay(field):
        index = index_pay(field)
    for key, value in client.items():
        if (is_date_or_fact(key, params=params)) and (key != field) and (
                set(params.get('years')).intersection(key.split()) != set()) and (
                mounth in key.lower().split()):
            if index:
                if (index == index_pay(key)):
                    other = value
                    other_field = key
            else:
                other = value
                other_field = key
    if is_data(field):
        data = client[field]
        payment = other if other != '0' else ''
    else:
        payment = client[field] if client[field] != '0' else ''
        data = other
    if payment or data:
        not_null = True
    return [data, payment, other_field, not_null]


def take_payments(dict: dict, params: dict) -> []:
    list = []
    client_info = {}
    for client in dict:
        client_info[params.get('name_id')] = client[params.get('name_id')]
        client_info[params.get('name_for_client')] = client[params.get('name_for_client')]
        client_info[params.get('name_for_pay')] = {}
        client_info['amount_payments'] = {}
        for year, mounths in params.get('year_mounths').items():
            client_info[params.get('name_for_pay')][year] = {}
            client_info['amount_payments'][year] = {}
            for mounth in mounths:
                client_info[params.get('name_for_pay')][year][mounth] = []

        second_filed = ''
        for field, value in client.items():
            amount_payments = 0

            for year, mounths in params.get('year_mounths').items():
                for mounth in mounths:
                    if mounth in field.split() and year in field.split() and params.get('goal') in field.split():
                        if field != second_filed:
                            fields_to_fact = find_pay(client, field, mounth, params)
                            client_info['amount_payments'][year][mounth] = amount_payments
                            client_info[params.get('name_for_pay')][year][mounth].append(
                                (fields_to_fact[0], fields_to_fact[1]))
                            second_filed = fields_to_fact[2]

        list.append(client_info)
        client_info = {}
    return list


def take_amount(list_client: list, params: dict) -> []:
    for k, client in enumerate(list_client):
        for year, mounths in client[params.get('name_for_pay')].items():
            for mounth, payments in client[params.get('name_for_pay')][year].items():
                i = 0
                for payment in payments:
                    if payment[0] or payment[1]:
                        i += 1
                list_client[k]['amount_payments'][year][mounth] = i if i > 0 else 1
    return list_client


def take_plan(dict: [], list: [], params: dict) -> []:
    for client in list:
        for record in dict:
            if client[params.get('name_id')] == record[params.get('name_id')]:
                client[params.get('name_for_plan')] = {}
                for year, mounths in params.get('year_mounths').items():
                    client[params.get('name_for_plan')][year] = {}
                    for field, value in record.items():
                        for mounth in mounths:
                            if mounth in field.split() and year in field.split() and params.get(
                                    'plan') in field.split():
                                client[params.get('name_for_plan')][year][mounth] = int(value) if str(
                                    value).isdigit() else 0
    return list


def take_debt(list: [], params: dict) -> []:
    for client in list:
        client[params.get('name_for_debt')] = {}
        for year, mounths in params.get('year_mounths').items():
            client[params.get('name_for_debt')][year] = {}
            for mounth in mounths:
                if client[params.get('name_for_plan')][year][mounth]:
                    debt = int(client[params.get('name_for_plan')][year][mounth]) if str(
                        client[params.get('name_for_plan')][year][mounth]).isdigit() else 0
                else:
                    debt = 0
                for pay in client[params.get('name_for_pay')][year][mounth]:
                    if pay[1].isdigit():
                        debt -= int(pay[1])
                    elif pay[1] == '':
                        debt -= 0
                client[params.get('name_for_debt')][year][mounth] = debt
    return list


def take_final_list(list_clients, params: dict) -> []:
    list_final = []
    for client in list_clients:
        num_rows = 1
        client_out = {}
        for year, mounths in params.get('year_mounths').items():
            for mounth in mounths:
                if client['amount_payments'][year][mounth] > num_rows:
                    num_rows = client['amount_payments'][year][mounth]
        for row in range(num_rows):
            client_out[params.get('name_id')] = int(client[params.get('name_id')])
            client_out[params.get('name_for_client')] = client[params.get('name_for_client')]
            for year, mounths in params.get('year_mounths').items():
                for mounth in mounths:
                    name_coll_amount = ' '.join([params.get('name_for_pay'), mounth, year])
                    name_coll_date = ' '.join([params.get('name_for_pay'), params.get('data_str'), mounth, year])
                    name_coll_debt = ' '.join([params.get('name_for_debt'), mounth, year])
                    name_coll_plan = ' '.join([params.get('name_for_plan'), mounth, year])
                    if len(client[params.get('name_for_pay')][year][mounth]) >= (row + 1):
                        if row == 0:
                            client_out[name_coll_plan] = client[params.get('name_for_plan')][year][mounth]
                        else:
                            client_out[name_coll_plan] = ''
                        client_out[name_coll_amount] = int(client[params.get('name_for_pay')][year][mounth][row][1]) if \
                            client[params.get('name_for_pay')][year][mounth][row][1].isdigit() else \
                            client[params.get('name_for_pay')][year][mounth][row][1]
                        client_out[name_coll_date] = client[params.get('name_for_pay')][year][mounth][row][0]
                        if row == client['amount_payments'][year][mounth] - 1:
                            client_out[name_coll_debt] = int(client[params.get('name_for_debt')][year][mounth])
                        else:
                            client_out[name_coll_debt] = ''
                    else:
                        client_out[name_coll_plan] = ''
                        client_out[name_coll_amount] = ''
                        client_out[name_coll_date] = ''
                        client_out[name_coll_debt] = ''
            list_final.append(client_out)
            client_out = {}
    return list_final


def save_xls(list_clients, file_out):
    name_file = file_out
    # font0 = xlwt.Font()
    # font0.name = 'Times New Roman'
    # font0.colour_index = 2
    # font0.bold = True

    style = xlwt.XFStyle()
    style.alignment.wrap = 1
    style.alignment.horz = style.alignment.HORZ_CENTER
    style.alignment.vert = style.alignment.VERT_CENTER
    style.borders.left = False
    style.borders.right = False
    style.borders.bottom = False
    style.borders.top = False

    style1 = xlwt.XFStyle()
    style1.font.bold = True
    style1.alignment.wrap = 1
    style1.alignment.vert = style1.alignment.VERT_CENTER
    style1.alignment.horz = style1.alignment.HORZ_CENTER
    style1.borders.bottom = True
    style1.borders.left = True
    style1.borders.right = True
    style1.borders.top = True

    style2 = xlwt.XFStyle()
    style2.font.bold = True
    style2.alignment.wrap = 1
    style2.alignment.horz = style2.alignment.HORZ_LEFT
    style2.alignment.vert = style2.alignment.VERT_CENTER
    style2.borders.bottom = True
    style2.borders.left = True
    style2.borders.right = True
    style2.borders.top = True

    style3 = xlwt.XFStyle()
    style3.alignment.wrap = 1
    style3.alignment.horz = style3.alignment.HORZ_CENTER
    style3.alignment.vert = style3.alignment.VERT_CENTER
    style3.borders.left = True
    style3.borders.right = False
    style3.borders.bottom = False
    style3.borders.top = False

    tall_style = xlwt.easyxf('font:height 250;')

    wb = xlwt.Workbook()
    ws = wb.add_sheet('payments')
    first_col = ws.col(1)
    other_col = 256 * 35
    first_col.width = 256 * 35  # 25 characters wide (-ish)
    # first_row = ws.row(0)

    y = 0
    x = 0
    for header in list_clients[0].keys():
        if y == 1:
            ws.col(y).width = other_col
        ws.write(x, y, header, style1)
        y += 1
    y = 0
    x = 1
    for row in list_clients:
        y = 0
        # style_for_content = style
        for t, v in row.items():
            if y <= 1:
                style_for_content = style2
            else:
                style_for_content = style
            if (y >= 6) and ((y - 2) % 4 == 0):
                style_for_content = style3
                # ws.write(y, x, t, style1)
            # else:
            # ws.col(y).width = other_col
            ws.write(x, y, v, style_for_content)
            # ws.col(y).set_style(tall_style)
            y += 1
        x += 1

    wb.save(name_file)
    print(f'Файл xls сохранен в той же папке, что и исходный файл, под именем: {name_file}')


def get_report(data_in, data_out: str, debug=False, method_in='file', method_out='file'):
    # mask = 'amocrm_export_leads*.csv'
    # try:
    #     file = glob.glob(mask, recursive=True)[0]
    #     print("Файл найден:", file)
    #     print('Полный путь файла:', os.path.abspath(file))
    # except IndexError:
    #     print('Ошибка при чтении файла - файл не найден, проверьте директорию расположения файлов!')
    #     print('CSV-файл должен лежать в директории:', os.path.abspath(os.curdir))
    #     sys.exit()

    if method_in == 'file':
        file = data_in
        dict = read_csv(file)
    elif method_in == 'dict':
        dict = data_in

    params = config.PARAMS_AMO

    test = debug
    a = 14
    b = 16
    if test:
        print(dict[1:2])

    params['year_mounths'] = get_mounth(dict, params)

    # dict = dict[0:5]

    if test:
        for i in dict[a:b]:
            print(i)
        print('1')
    list_payment = take_payments(dict, params)
    if test:
        for i in list_payment[a:b]:
            print(i)
        print('2')
    list_payment = take_plan(dict, list_payment, params)
    if test:
        for i in list_payment[a:b]:
            print(i)
        print('3')

    list_payment = take_debt(list_payment, params)
    list_payment = take_amount(list_payment, params)
    if test:
        for i in list_payment[a:b]:
            print(i)
        print('4')
    list_final = take_final_list(list_payment, params)
    x = [x[params.get('name_id')] for x in list_final]

    if test:
        for i in list_final[a:b]:
            print(i)

    if method_out == 'file':
        save_xls(list_final, data_out)
        return len(set(x))
    else:
        return list_final


if __name__ == '__main__':
    file_in = 'amocrm_export_leads_2021-02-13.csv'
    file_out = 'payments_2021-02-20.xls'
    get_report(file_in, file_out)
