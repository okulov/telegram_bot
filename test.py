import datetime
import json
import os

import jwt
import requests
from amocrm.v2 import tokens, Contact as _Contact, Lead as _Lead, Pipeline as _Pipeline
from amocrm.v2.entity import custom_field
from amocrm.v2.filters import Filter, SingleFilter, MultiFilter, SingleListFilter

from utils import get_csv_report

code = 'def50200609f3c865ff0de976345a438aa1b4cad1beec7bf132b9ce272a8947360810cf2fbbb471ddba18b2a28403ea36569124440234d49a53400b029256dba72656f6431ed76fd0f17e0fc3f70e30326162226d138d075469791e9b34cb4e99e45ad3ffce07b1187d25e2e22a72c03a521605cc5dc40c8dd4fd8376970b20b2af5db5434b6383b68b21e67722fe5621cb81beff151ef3afc938a739fd316c068d10bbddb700b6a98cb924ad231c40cb34bd60115c71ce2158e3048360fcc8323ca81be409fbcb6f3dd9b27fef5700fdf018fa9eab7bfd7cbfb29eb417f89a14fe2fa6eeebc117631d189b6d157fa4f1db4002a58f31414a4141796af5d6bd68576bc146f7ab6cf61d555b666aae9e817119381c643941fc3f860161378dbdb2e58a54c628bd5ed787b8065c3d055ce6c1c76c8ad3a3e1984d3ede321d49dd51bccd761eb7794fd0261b2e703c8d7620ce4e2f2771fe3adca20808d781a7c4a7d7ce2de182baab0d44929f03ab8e0250dd78f5b2007f58a32242dc661d1cc6d06a6c2850afb3a22378f9158c569b901d434488746dd8468f352e901a421e0b9512cb872f204e4e8ea389029bd1cb899cd90ae05bc4a152bc0355688a2a7b1504ec3ec'
redirect_url = 'https://barcaacademy.ru/'
client_id = '80c88f56-1922-478c-9a03-fc8b3fd9a232'
client_secret = '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz'
data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": redirect_url,

}


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


code = 'def50200e5ebcfff6f7cc247eb5c429b487e78b6d2d3ee51a9a478f421071b4bf4b764b822d4eaabde56bb8da7e4770af5bfe0b9b0eec2c3e48c24a1b117b84886aecadf03786c8bb5149463b6befcbf36ca2c10ccdf0110e900bbe217548c0eedb33eb30aaeebcabcbcb5d94706b9ab368a1f6eb86e767cf2d2a2a1d9126ae1c1cb88559e36a7f715260cf5b89deeea5eca4278bf9321e3712ff912f9a48bd1e96db0b17b4725b73d9a50d30649efb05b89a2ea63bba66df3ae43993d7095ca15cfd99b199d84927f9324df0a022fb3dc184492d39da57ac498941ed35280cff8bc78ceec06a66edcd77878f2a257e1ed7d412e43f811b222bbdf17be896fa6069d9378289f895a49e488394ea794d639d01477acc971b2e2806619d751a9bb3a08d23747cfe8a1337b8bf6e7e31445f68ca3e804bbfd1df8da4cabb84d865a1f808bc1cce8ab03775a60522af12f7a9a541d6f5211eb2be62ca92445c3f090790d39fd6589fb44780b56363b494f3d264b256c1aaac9d1115e4708630fd27c14a4e0046ac98ccdb40a30ef5c34b0157f0c10be45a3cc6f0d2eb299c8cf626d487b1a6e714a1bcb5816a0eac5fb0e4f5a025e30d00f7b33051ed0cc0d0e01646ebcd6'
redirect_url = 'https://barcaacademy.ru/'
client_id = '80c88f56-1922-478c-9a03-fc8b3fd9a232'
client_secret = '4jPrt8NO0pNrIpZppeoqDsDuOSRCLIAb5okd4qapHmPjfAMIXBWN2KzUzx8s0FIz'

tokens.default_token_manager(
        client_id=client_id,
        client_secret=client_secret,
        subdomain="barcaacademy",
        redirect_url=redirect_url,
        storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)
# tokens.default_token_manager.init(code=code, skip_error=False)
token_d = tokens.default_token_manager._storage.get_access_token()
token_data = jwt.decode(token_d, options={"verify_signature": False})
exp = datetime.datetime.utcfromtimestamp(int(token_data["exp"]))
print(exp)
tokens.default_token_manager.get_access_token()



class Contact(_Contact):
    tel = custom_field.TextCustomField("Телефон")
    email = ''


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
#print(f2._as_params())
f3 = SingleFilter('id')
f3(9991369)
f4 = StatusFilter('pipeline_id')
f4(id_pipeline)
#print(f4._as_params())
pipeline = Pipeline.objects.get(id_pipeline)
# leads = Lead.objects.filter(filters=(f4, f2,))
# print(len(list(leads)))
# for i in leads:
#     print(i.var3)

# print([(s.id, s.name) for s in pipeline.statuses])
#leads_gen = Lead.objects.get('9991369')
#leads_gen = Lead.objects.filter(filters=(f4, f2,), query = '')
leads_gen = Lead.objects.filter(filters=(), query = 'рига')
print(len(list(leads_gen)))
for l in leads_gen:
    print(l.status.name)
    print(l.price)
    tags = l.tags
    print(*[t.name for t in tags])
    print(l.name)
    link = f'https://barcaacademy.amocrm.ru/leads/detail/{l.id}'
    print(link)

leads = []
for l in leads_gen:
    lead = {}
    lead['ID'] = l.id
    lead['Название сделки'] = l.name
    names_fields = make_names_fields()
    for i in range(len(names_fields)):
        var = f'var{i+1}'
        lead[names_fields[i]] = getattr(l, var) if getattr(l, var)!=None else ''
        if 'дата' in names_fields[i].lower().split() and lead[names_fields[i]]!='':
            lead[names_fields[i]] = datetime.datetime.strftime(lead[names_fields[i]], "%d.%m.%y")
    leads.append(lead)
print(len(leads))
print(leads)
#get_report(leads, 'payments.xls',debug=False, method='dict')

# print(list(leads.tags))
# contact = leads.contacts
# print(list(contact)[0])
#
# contact = Contact.objects.get(list(contact)[0].id)
# print(contact.id, contact.first_name, contact.tel)
