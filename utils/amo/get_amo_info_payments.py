from datetime import datetime

from amocrm.v2 import Lead as _Lead
from amocrm.v2 import Contact as _Contact
from amocrm.v2.entity import custom_field
from amocrm.v2.filters import MultiFilter, SingleFilter, Filter

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


class Contact(_Contact):
    custom_fields = config.CONTACTS_FIELDS
    for field in custom_fields:
        if field in ['Телефон', 'Email']:
            setattr(_Contact, field, custom_field.MultiSelectCustomField(field))
        else:
            setattr(_Contact, field, custom_field.TextCustomField(field))


class StatusFilter(MultiFilter):
    def _as_params(self):
        second_name = 'status_id' if self._name == 'statuses' else self._name
        return {"filter[statuses][0][{}]".format(second_name): self._values}


# ?filter[custom_fields_values][{field_id}][] = {enum_id2}


class CustomFieldsFilter(Filter):
    def __call__(self, value):
        self._field_id = self._name
        self._enum_id = value

    def _as_params(self):
        return {"filter[custom_fields_values][{}][]".format(self._field_id): self._enum_id}


def get_amo_payments_data(filial, islead='', file_out='', method_out='file'):
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


def get_amo_contacts_data(query=''):
    id_pipeline = 1261522
    final_statuses_id = 142
    token = connect()
    f1 = StatusFilter('statuses')
    f1(final_statuses_id)
    f2 = StatusFilter('pipeline_id')
    f2(id_pipeline)
    f_pipe = SingleFilter('pipeline_id')
    f_pipe(id_pipeline)
    id_name_school_filed = 388253
    f_contact = CustomFieldsFilter(id_name_school_filed)
    if query == 'Новая Рига':
        f_contact(754847)
    elif query == 'Ходынка':
        f_contact(754845)

    leads_gen = [Contact.objects.filter()]

    if query == "all_leads":
        #leads_gen = [Contact.objects.filter()]
        is_all = True
    elif query != 'all':
        #leads_gen = [Contact.objects.filter(query=query)]
        filials =[query]
        is_all = False
    else:
        # f_contact(754847)
        # leads_gen1 = Contact.objects.filter(query='Новая Рига')
        # f_contact(754845)
        # leads_gen2 = Contact.objects.filter(query='Ходынка')
        # leads_gen = [leads_gen1, leads_gen2]
        filials = ['Новая Рига', 'Ходынка']
        is_all = False

    result = []
    for lead in leads_gen:
        for c in lead:
            out = {}
            if getattr(c, 'Тип') in ['Родитель', None]:
                num_phone = len(getattr(c, 'Телефон')) if getattr(c, 'Телефон') else 0
                num_email = len(getattr(c, 'Email')) if getattr(c, 'Email') else 0
                for i in range(max(num_phone, num_email)):
                    out['ID'] = c.id
                    out['Имя контакта'] = c.name
                    out['Статус'] = getattr(c, 'Статус')
                    out['Название школы'] = getattr(c, 'Название школы')
                    out['Программа'] = getattr(c, 'Программа')
                    out['ФИО ребенка'] = getattr(c, 'ФИО ребенка')
                    out['Полных лет ребёнку'] = getattr(c, 'Полных лет ребёнку')
                    out['Тренер'] = getattr(c, 'Тренер')
                    try:
                        out['Телефон'] = getattr(c, 'Телефон')[i].value if getattr(c, 'Телефон') else ''
                    except IndexError:
                        out['Телефон'] = ''
                    try:
                        out['Email'] = getattr(c, 'Email')[i].value if getattr(c, 'Email') else ''
                    except:
                        out['Email'] = ''
                    if not is_all:
                        if out['Название школы'] in filials:
                            result.append(out.copy())
                    else:
                        result.append(out.copy())
    return result
