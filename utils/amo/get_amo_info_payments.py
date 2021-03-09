from datetime import datetime

from amocrm.v2 import Lead as _Lead
from amocrm.v2.entity import custom_field
from amocrm.v2.filters import MultiFilter, SingleFilter

from . import connect
from .get_summary import get_summary_lead_info
from .. import get_report


def make_names_fields():
    fields = ['Оплата план сентябрь', 'Оплата факт сентябрь', 'Оплата план октябрь', 'Оплата факт октябрь',
              'Оплата план ноябрь', 'Оплата факт ноябрь', 'Оплата план декабрь', 'Оплата факт декабрь',
              'Оплата план январь', 'Оплата факт январь', 'Оплата план февраль', 'Оплата факт февраль',
              'Оплата план март', 'Оплата факт март', 'Оплата план апрель', 'Оплата факт апрель', 'Оплата план май',
              'Оплата факт май', 'Оплата план июнь', 'Оплата факт июнь', 'Оплата план июль', 'Оплата факт июль',
              'Оплата план август', 'Оплата факт август', 'Оплата план сентябрь 2019', 'Оплата факт сентябрь 2019',
              'Оплата план октябрь 2019', 'Оплата факт октябрь 2019', 'Оплата план ноябрь 2019',
              'Оплата факт ноябрь 2019', 'Оплата план декабрь 2019', 'Оплата факт декабрь 2019',
              'Оплата план январь 2020', 'Оплата факт январь 2020', 'Оплата план февраль 2020',
              'Оплата факт февраль 2020', 'Оплата план март 2020', 'Оплата факт март 2020', 'Оплата план апрель 2020',
              'Оплата факт апрель 2020', 'Оплата план май 2020', 'Оплата факт май 2020', 'Оплата план июнь 2020',
              'Оплата факт июнь 2020', 'Оплата план июль 2020', 'Оплата факт июль 2020', 'Оплата план август 2020',
              'Оплата факт август 2020', 'Оплата план сентябрь 2020', 'Оплата факт сентябрь 2020',
              'Оплата план октябрь 2020', '1 - Оплата факт октябрь 2020', '1 - Дата оплаты факт октябрь 2020',
              '2 - Оплата факт октябрь 2020', '2 - Дата оплаты факт октябрь 2020', '3 - Оплата факт октябрь 2020',
              '3 - Дата оплаты факт октябрь 2020', 'Оплата план ноябрь 2020', '1 - Оплата факт ноябрь 2020',
              '1 - Дата оплаты факт ноябрь 2020', '2 - Оплата факт ноябрь 2020', '2 - Дата оплаты факт ноябрь 2020',
              '3 - Оплата факт ноябрь 2020', '3 - Дата оплаты факт ноябрь 2020', 'Оплата план декабрь 2020',
              '1- Оплата факт декабрь 2020', '1 - Дата оплаты факт декабрь 2020', '2- Оплата факт декабрь 2020',
              '2 - Дата оплаты факт декабрь 2020', '3- Оплата факт декабрь 2020', '3 - Дата оплаты факт декабрь 2020',
              'Оплата план январь 2021', '1 - Оплата факт январь 2021', '1 - Дата оплаты факт январь 2021',
              '2 - Оплата факт январь 2021', '2 - Дата оплаты факт январь 2021', '3 - Оплата факт январь 2021',
              '3 - Дата оплаты факт январь 2021', 'Оплата план февраль 2021', '1 - Оплата февраль факт 2021',
              '1 - Дата оплаты факт февраль 2021', '2 - Оплата февраль факт 2021', '2 - Дата оплаты факт февраль 2021',
              '3 - Оплата февраль факт 2021', '3 - Дата оплаты - факт февраль 2021', 'Оплата план март 2021',
              '1 - Оплата факт март 2021', '1 - Дата оплаты - факт март 2021', '2 - Оплата факт март 2021',
              '2 - Дата оплаты факт март 2021', '3 - Оплата факт март 2021', '3 - Дата оплаты факт март 2021',
              'Оплата план апрель 2021', '1 - Оплата факт апрель 2021', '1 - Дата оплаты факт апрель 2021',
              '2 - Оплата факт апрель 2021', '2 - Дата оплаты факт апрель 2021', '3 - Оплата факт апрель 2021',
              '3 - Дата оплаты - факт апрель 2021', 'Оплата план май 2021', '1 - Оплата факт май 2021',
              '1 - Дата оплаты факт май 2021', '2 - Оплата факт май 2021', '2 - Дата оплаты - факт май 2021',
              '3 - Оплата факт май 2021', '3 - Дата оплаты - факт май 2021', 'Оплата план июнь 2021',
              '1 - Оплата факт июнь 2021', '1 - Дата оплаты факт июнь 2021', '2 - Оплата факт июнь 2021',
              '2 - Дата оплаты факт июнь 2021', '3 - Оплата факт июнь 2021', '3 - Дата оплаты факт июнь 2021']
    return fields


class Lead(_Lead):
    name_fields = make_names_fields()
    i = 0
    for field in name_fields:
        i += 1
        name_str = f'var{i}'
        if 'дата' in field.lower().split():
            setattr(_Lead, name_str, custom_field.DateCustomField(field))
        else:
            setattr(_Lead, name_str, custom_field.TextCustomField(field))


class StatusFilter(MultiFilter):
    def _as_params(self):
        second_name = 'status_id' if self._name == 'statuses' else self._name
        return {"filter[statuses][0][{}]".format(second_name): self._values}


def get_amo_data(filial, islead='', file_out='', method_out='file'):
    id_pipeline = 1261522
    final_statuses_id = 142
    token = connect()
    f1 = StatusFilter('statuses')
    f1(final_statuses_id)
    f2 = StatusFilter('pipeline_id')
    f2(id_pipeline)
    f_pipe = SingleFilter('pipeline_id')
    f_pipe(id_pipeline)
    if islead:
        leads_gen = Lead.objects.filter(filters=(f_pipe,), query=islead)
    elif filial != 'all':
        leads_gen = Lead.objects.filter(filters=(f2, f1,), query=filial)
    else:
        leads_gen = Lead.objects.filter(filters=(f2, f1,), query='')

    leads = []
    k = 0
    for l in leads_gen:
        k += 1
        lead = {}
        lead['ID'] = l.id
        lead['Название сделки'] = l.name
        if islead:
            lead['Статус'] = l.status.name
            lead['Бюджет'] = l.price
            lead['Тэги'] = [t.name for t in l.tags]
            lead['Ссылка'] = f'https://barcaacademy.amocrm.ru/leads/detail/{l.id}'
        names_fields = make_names_fields()
        for i in range(len(names_fields)):
            var = f'var{i + 1}'
            lead[names_fields[i]] = getattr(l, var) if getattr(l, var) != None else ''
            if 'дата' in names_fields[i].lower().split() and lead[names_fields[i]] != '':
                lead[names_fields[i]] = datetime.strftime(lead[names_fields[i]], "%d.%m.%y")
        leads.append(lead)
        if k==11 and islead:
            return f'Слишком общий запрос (результатов более {len(list(leads_gen))}), уточните фамилию или ID.'
    if islead:
        return get_summary_lead_info(leads)
    else:
        return get_report(leads, file_out, debug=False, method_in='dict', method_out=method_out)
