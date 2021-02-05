import psycopg2
from datetime import date
import requests

# СКРИПТ
#
# + Получить из Airtable все записи
# + Получить из таблицы постгре все записи
# - Проверить, какие записи из Airtable не существуют в Постгрес
#   - добавить записи в постгрес
# - Если в Airtable нет записей, которые есть в Постгрес:
#   - удалить из Постгрес
# - загрузить raw data в таблицу


# выгружаем сырые данные из Airtable
AIRTABLE_BASE_ID = 'appPFtPl42cKzPk1f'
AIRTABLE_TABLE_NAME = 'Psychotherapists'
API_KEY = 'keyTB6bXM5hmHID2v'

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

headers = {'Authorization': f'Bearer {API_KEY}'}
raw_data = requests.get(url=ENDPOINT, headers=headers).json()

# распарсиваем данные из json в словарь с ключом - id записи в Airtable
cleaned_data = {}

for i in range(len(raw_data['records'])):
    id = raw_data['records'][i]['id']
    tmp = []
    tmp.append(raw_data['records'][i]['fields']['Имя'])
    tmp.append(raw_data['records'][i]['fields']['Методы'])
    tmp.append(raw_data['records'][i]['fields']['Фотография'][0]['id'])
    tmp.append(raw_data['records'][i]['fields']['Фотография'][0]['url'])
    tmp.append(raw_data['records'][i]['createdTime'])
    cleaned_data[id] = tmp

print(cleaned_data)

"""
Нужно обработать 4 случая:
    - запись есть в Airtable, но отсутствует в Postgres -> добавить запись
    - записи нет в Airtable, но она есть в Postgres -> удалить запись
    - запись есть в обеих базах, но в Airtable изменились данные -> обновить данные
    - запись есть в обеих базах и изменений нет -> skip
"""

# подключаемся к базе данных PostgreSQL
conn = psycopg2.connect("dbname=meta_db user=postgres password=MetaMeta1")
cur = conn.cursor()



# cur.execute("INSERT INTO therapists_therapist(therapist_id, name, methods, photo_id, photo_link, created_time) "
#             "VALUES(%s, %s, %s, %s, %s, %s)", ('rec9dKijJaU9vWtoK',
#                                                'Василий',
#                                                ['Психоанализ', 'Коучинг', 'Музыкотерапия'],
#                                                'attY7G4ysiIDnSaUw',
#                                                'https://dl.airtable.com/.attachments/7da0d4c7963babf742137abc4e9a1a99/5f547505/1.jpg',
#                                                '2021-02-02T14:29:36.000Z'))

# для проверки наличия/ отсутствия записей используем therapist_id
cur.execute("SELECT therapist_id FROM therapists_therapist ")
ids_from_airtable = cur.fetchall()

# пробегаем по ключам в Postgres и удаляем те записи, которых нет в Airtable
for i in ids_from_airtable:
    if i[0] not in cleaned_data.keys():
        id_to_delete = i[0]
        cur.execute("DELETE FROM therapists_therapist WHERE therapist_id = (%s,)", (id_to_delete))

# postgres_table = cur.fetchall()
# print(postgres_table)


# добавляем сырые данные и дату выгрузки в таблицу raw_data
# raw_data_to_add = str(raw_data)
# date_today = date.today()
# cur.execute(
#     "INSERT INTO therapists_rawdata (date, raw_data) "
#     "VALUES (%s, %s)", (date_today, raw_data_to_add))
#
# # можно сразу проверить успешность выгрузки в консоли
# cur.execute("SELECT * FROM therapists_rawdata;")
# r = cur.fetchall()
# print(r)

conn.commit()

cur.close()
conn.close()
