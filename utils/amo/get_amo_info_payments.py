from datetime import datetime

from amocrm.v2 import Lead as _Lead
from amocrm.v2.entity import custom_field
from amocrm.v2.filters import MultiFilter, SingleFilter

from data import config
from . import connect
from .get_summary import get_summary_lead_info
from .. import get_report


class Lead(_Lead):
    name_payment_fields = config.AMO_PAYMENT_FILEDS
    custom_fields = config.LEAD_CUSTOM_FIELDS
    i = 0
    for field in name_payment_fields:
        i += 1
        name_str = f'var{i}'
        if 'дата' in field.lower().split():
            setattr(_Lead, name_str, custom_field.DateCustomField(field))
        else:
            setattr(_Lead, name_str, custom_field.TextCustomField(field))

    for field in custom_fields:
        setattr(_Lead, field, custom_field.TextCustomField(field))


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
        if islead:  # TODO: убрать в config названия полей и их значения
            lead['Статус'] = l.status.name
            lead['Бюджет'] = l.price
            lead['Тэги'] = [t.name for t in l.tags]
            lead['Ссылка'] = f'https://barcaacademy.amocrm.ru/leads/detail/{l.id}'

        names_fields = config.AMO_PAYMENT_FILEDS
        for i in range(len(names_fields)):
            var = f'var{i + 1}'
            lead[names_fields[i]] = getattr(l, var) if getattr(l, var) != None else ''
            if 'дата' in names_fields[i].lower().split() and lead[names_fields[i]] != '':
                lead[names_fields[i]] = datetime.strftime(lead[names_fields[i]], "%d.%m.%y")

        custom_fields = config.LEAD_CUSTOM_FIELDS
        for field in custom_fields:
            lead[field] = getattr(l, field) if getattr(l, field) != None else ''

        leads.append(lead)
        if k == 11 and islead:
            return f'Слишком общий запрос (результатов более {len(list(leads_gen))}), уточните фамилию или ID.'
    if islead:
        return get_summary_lead_info(leads)
    else:
        return get_report(leads, file_out, debug=False, method_in='dict', method_out=method_out)
