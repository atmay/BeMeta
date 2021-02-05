import psycopg2
from datetime import date
import requests

"""
Получаем raw data из Airtable и превращаем их в словарь с ключом id записи в Airtable
"""

AIRTABLE_BASE_ID = 'appPFtPl42cKzPk1f'
AIRTABLE_TABLE_NAME = 'Psychotherapists'
API_KEY = 'keyTB6bXM5hmHID2v'
ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

headers = {'Authorization': f'Bearer {API_KEY}'}
raw_data = requests.get(url=ENDPOINT, headers=headers).json()

airtable_cleaned_data = {}

for i in range(len(raw_data['records'])):
    id = raw_data['records'][i]['id']
    tmp = [raw_data['records'][i]['fields']['Имя'],
           raw_data['records'][i]['fields']['Методы'],
           raw_data['records'][i]['fields']['Фотография'][0]['id'],
           raw_data['records'][i]['fields']['Фотография'][0]['url'],
           raw_data['records'][i]['createdTime']]
    airtable_cleaned_data[id] = tmp

print(airtable_cleaned_data)

""" 
Устанавливаем соединение с PostgreSQL
"""
conn = psycopg2.connect("dbname=meta_db user=postgres password=MetaMeta1")
cur = conn.cursor()

"""
Заливаем raw data в соответствующую таблицу
"""
# raw_data_to_add = str(raw_data)
# date_today = date.today()
# cur.execute(
#     "INSERT INTO therapists_rawdata (date, raw_data) "
#     "VALUES (%s, %s)", (date_today, raw_data_to_add))

# # опционально - можно сразу в консоли проверить успешность выгрузки
# cur.execute("SELECT * FROM therapists_rawdata;")
# r = cur.fetchall()
# print(r)

"""
Обновляем основную таблицу. Нужно обработать 4 случая:
    - запись есть в Airtable, но отсутствует в Postgres -> добавить запись
    - записи нет в Airtable, но она есть в Postgres -> удалить запись
    - запись есть в обеих базах, но в Airtable изменились данные -> обновить данные
    - запись есть в обеих базах и изменений нет -> skip
"""

"""
Для оптимизации удаления и добавления данных получаем только значения therapist_id из Postgres
"""
cur.execute("SELECT therapist_id FROM therapists_therapist ")
ids_from_postgres = cur.fetchall()
ids_from_postgres = [i[0] for i in ids_from_postgres]

"""
По полю therapist_id проверяем наличие в Postgres записей, которые были удалены из Airtable, удаляем их 
"""
for i in ids_from_postgres:
    if i not in airtable_cleaned_data.keys():
        cur.execute("DELETE FROM therapists_therapist WHERE therapist_id = %s", (i,))

"""
По полю therapist_id проверяем наличие в Airtable  записей, которые отсутствуют в Postgres, добавляем их
"""
for i in airtable_cleaned_data.keys():
    if i not in ids_from_postgres:
        ther_id = i
        ther_name = airtable_cleaned_data[i][0]
        ther_methods = airtable_cleaned_data[i][1]
        ther_photo_id = airtable_cleaned_data[i][2]
        ther_photo_link = airtable_cleaned_data[i][3]
        ther_created_time = airtable_cleaned_data[i][4]
        cur.execute("INSERT INTO therapists_therapist(therapist_id, name, methods, photo_id, photo_link, created_time) "
                    "VALUES(%s, %s, %s, %s, %s, %s)", (
                    ther_id, ther_name, ther_methods, ther_photo_id, ther_photo_link, ther_created_time
                    ))

"""
Проверяем на актуальность существующие записи в Postgres, при необходимости обновляем их
"""
for i in ids_from_postgres:
    # получаем строку из Postgres, приводим ее к тому же виду, что и запись ключ-значение в airtable_cleaned_data
    cur.execute("SELECT therapist_id, name, methods, photo_id, photo_link, created_time FROM therapists_therapist "
                "WHERE therapist_id = %s", (i,))
    postgres_row = cur.fetchall()
    postgres_cleaned_data = {}
    postgres_ther_id = i
    tmp = [postgres_row[0][1], postgres_row[0][2][1:-1].split(','), postgres_row[0][3], postgres_row[0][4], postgres_row[0][5]]
    postgres_cleaned_data[postgres_ther_id] = tmp
    if postgres_cleaned_data[i] == airtable_cleaned_data[i]:
        continue
    else:
        different = []
        for k in range(len(postgres_cleaned_data[i])):
            if postgres_cleaned_data[i][k] != airtable_cleaned_data[i][k]:
                different.append(k)
        print(f'DIFFERENT! {postgres_cleaned_data} != {airtable_cleaned_data}')

print(postgres_cleaned_data['recuJ6e1pvG6tkRdC'] == airtable_cleaned_data['recuJ6e1pvG6tkRdC'])
    # сравниваем значения соответствующих полей в двух таблицах и при несовпадении - обновляем значение переменной



# [('recuJ6e1pvG6tkRdC', 'Иннокентий', '{Гештальт-терапия,Коучинг,Психосинтез,Сказкотерапия}',
# 'atttxEgUknSdwDjme', 'https://dl.airtable.com/.attachments/fa70928a82a214d22c4b7a2eeace79d2/e5a12360/2.jpg',
# '2021-02-02T14:29:36.000Z')]
# postgres_table = cur.fetchall()
# print(postgres_table)

conn.commit()

cur.close()
conn.close()
