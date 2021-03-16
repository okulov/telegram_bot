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


code = 'def5020021fbcc7a90030c94e1e753b75a8b4350be08b6ee380fb92af18e9adcbecdd262bd5567e0246f8cb70c0e67880e56c4887e3e980babe85af14cd3709a1b367f1954ffd760049d3afa02d5f6e4af3959f219924045ad632303f38630647ac3c81b33fae90b50d575dbeaadb702e7bb3d751d8387be8446f427c11e624aba74848417ec5b68230a7c69d6564a489c8c9b503c3e9d79e026dae60c512005ba4b73bad62f75ecfcd19e5933c5d658bb756ecf9b1a354e13065e8f583e45d8325c560896129cea17614d90c62ce2bad93cd4e4359d566097c2869729346605452d018df3738e50739561f90e5baa6409f794ebe3d439edb87ef8da8554a25c23800efef8fe9a59882ca12580f433c4d0419cc6b050d9898d839361504d3c89337627836f6cea2226fa630e959d5b89f7c4e721aa099e94524082377b7d0899b5987e0c2220235d78227c706c5a2e1e1397b52c83a7cb823c60098eaddd508775a65f91a4bb56bb0eafaddf257499754d38b3b9fd6b7bebd8a561cb45956c62a13f1715471ac59f77e258bf31538c47c501076d021f925ab6caa3ab030f02ae67fe701b75019158aa760c450b57751cf103a01258a6c8ff950cc95f7c1151a8feeffc'
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
tokens.default_token_manager.init(code=code, skip_error=False)
# token_d = tokens.default_token_manager._storage.get_access_token()
# token_data = jwt.decode(token_d, options={"verify_signature": False})
# exp = datetime.datetime.utcfromtimestamp(int(token_data["exp"]))
# print(exp)
# tokens.default_token_manager.get_access_token()



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
