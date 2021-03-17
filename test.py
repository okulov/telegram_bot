import datetime
import json
import os

import jwt
import requests
from amocrm.v2 import tokens, Contact as _Contact, Lead as _Lead, Pipeline as _Pipeline
from amocrm.v2.entity import custom_field
from amocrm.v2.filters import Filter, SingleFilter, MultiFilter, SingleListFilter
from data import config
from utils import get_csv_report


def make_names_fields():
    fields = config.AMO_PAYMENT_FILEDS
    return fields


code = config.AMO_CODE

redirect_url = 'https://barcaacademy.ru/'
client_id = config.CONNECT_PARAMS['client_id']
client_secret = config.CONNECT_PARAMS['client_secret']

import redis
from urllib.parse import urlparse

url = urlparse(config.REDIS_URL)
r = redis.Redis(host=url.hostname,
                port=url.port,
                username=url.username,
                password=url.password,
                ssl=False,
                ssl_cert_reqs=None)
tokens.default_token_manager(
    client_id=client_id,
    client_secret=client_secret,
    subdomain="barcaacademy",
    redirect_url=redirect_url,
    storage=tokens.RedisTokensStorage(r.client()),  # by default FileTokensStorage
)

try:
    tokens.default_token_manager.get_access_token()
    token_d = tokens.default_token_manager._storage.get_access_token()
    token_data = jwt.decode(token_d, options={"verify_signature": False})
    exp = datetime.datetime.utcfromtimestamp(int(token_data["exp"]))
except:
    tokens.default_token_manager.init(code=code, skip_error=False)


class Contact(_Contact):
    custom_fields = config.CONTACTS_FIELDS
    for field in custom_fields:
        if field in ['Телефон', 'Email']:
            setattr(_Contact, field, custom_field.MultiSelectCustomField(field))
        else:
            setattr(_Contact, field, custom_field.TextCustomField(field))

class Lead(_Lead):
    name_fields = make_names_fields()
    i = 0
    for field in name_fields:
        i += 1
        name_str = f'var{i}'
        if 'Дата' in field:
            setattr(_Lead, name_str, custom_field.DateCustomField(field))
        else:
            setattr(_Lead, name_str, custom_field.TextCustomField(field))


class Pipeline(_Pipeline):
    pass


name_statuses = {
    'Неразобранное', 'Входящее обращение', 'Не дозвон (!ТОЛЬКО НОВЫЕ!)', 'Проведена консультация',
    'Записан на просмотр', 'Пришли на просмотр', 'Выдан Договор и приложения', 'Лист ожидания', 'Заключен договор',
    'Начал заниматься (не оплатил)', 'Получена оплата', 'Отказ'
}


# filter[statuses][0][pipeline_id]={pipeline_id}&filter[statuses][0][status_id]={status_id}

class StatusFilter(MultiFilter):
    def _as_params(self):
        second_name = 'status_id' if self._name == 'statuses' else self._name
        return {"filter[statuses][0][{}]".format(second_name): self._values}


id_pipeline = 1261522
final_statuses_id = [20820373, 21670282, 142]
final_statuses = ['Заключен договор', 'Начал заниматься (не оплатил)', 'Получена оплата']
final_statuses = 'Получена оплата'
final_statuses_id = 142

pipeline_other_id = [1261819, 1261774]
f1 = SingleFilter('pipeline_id')
f1(id_pipeline)
f2 = StatusFilter('statuses')
f2(final_statuses_id)
# print(f2._as_params())
f3 = SingleFilter('id')
f3(9991369)
f4 = StatusFilter('pipeline_id')
f4(id_pipeline)
# print(f4._as_params())
pipeline = Pipeline.objects.get(id_pipeline)
# leads = Lead.objects.filter(filters=(f4, f2,))
# print(len(list(leads)))
# for i in leads:
#     print(i.var3)

# print([(s.id, s.name) for s in pipeline.statuses])
# leads_gen = Lead.objects.get('9991369')
# leads_gen = Lead.objects.filter(filters=(f4, f2,), query = '')
leads_gen = Lead.objects.filter(filters=(), query='27912557')
leads_gen = Lead.objects.filter(filters=(), query='27981413')
leads_gen = Lead.objects.filter(filters=(), query='22636773')
#leads_gen = Lead.objects.filter(filters=(), query='10927499')
# print(len(list(leads_gen)))
for l in leads_gen:
    print(l)
    contacts = l.contacts
    print(contacts)
    print(l.status.name)
    print(l.price)
    tags = l.tags
    print(*[t.name for t in tags])
    print(l.name)
    link = f'https://barcaacademy.amocrm.ru/leads/detail/{l.id}'
    print(link)

for contact in contacts:
    # print(contact)
    c = Contact.objects.get(contact.id)
    print(c.__dict__)
    email_list = getattr(c, 'Email')
    phone_list = getattr(c, 'Телефон')
    print(c.id, c.name, getattr(c, 'Название школы'), getattr(c, 'Тип'))
    if getattr(c, 'Тип') in ['Родитель', None]:
        for email in email_list:
            print(email.value)
        for phone in phone_list:
            print(phone.value)
print('-----')
#leads_gen = Contact.objects.filter(filters=(), query='Ходынка')
leads_gen = Contact.objects.get('27086925')
#print(len(list(leads_gen)))

for c in leads_gen:
    print(contact)
    print(c.__dict__)
    email_list = getattr(c, 'Email')
    phone_list = getattr(c, 'Телефон')
    print(c.id, c.name, getattr(c, 'Название школы'), getattr(c, 'Тип'))
    if getattr(c, 'Тип') in ['Родитель', None]:
        for email in email_list:
            print(email.value)
        for phone in phone_list:
            print(phone.value)
# leads = []
# for l in leads_gen:
#     lead = {}
#     lead['ID'] = l.id
#     lead['Название сделки'] = l.name
#     names_fields = make_names_fields()
#     for i in range(len(names_fields)):
#         var = f'var{i + 1}'
#         lead[names_fields[i]] = getattr(l, var) if getattr(l, var) != None else ''
#         if 'дата' in names_fields[i].lower().split() and lead[names_fields[i]] != '':
#             lead[names_fields[i]] = datetime.datetime.strftime(lead[names_fields[i]], "%d.%m.%y")
#     leads.append(lead)
# print(len(leads))
# print(leads)


# get_report(leads, 'payments.xls',debug=False, method='dict')

# print(list(leads.tags))
# contact = leads.contacts
# print(list(contact)[0])
#
# contact = Contact.objects.get(list(contact)[0].id)
# print(contact.id, contact.first_name, contact.tel)
