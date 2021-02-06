import psycopg2
from psycopg2 import sql
from datetime import date
import requests
import os
from dotenv import load_dotenv

load_dotenv()

airtable_base_id = os.getenv('AIRTABLE_BASE_ID')
airtable_table_name = os.getenv('AIRTABLE_TABLE_NAME')
api_key = os.getenv('API_KEY')
ENDPOINT = f'https://api.airtable.com/v0/{airtable_base_id}/{airtable_table_name}'


def get_raw_data_from_airtable():
    """
    Получаем raw data из Airtable и превращаем их в словарь с ключом id записи в Airtable
    """
    headers = {'Authorization': f'Bearer {api_key}'}
    try:
        raw_data = requests.get(url=ENDPOINT, headers=headers, timeout=60).json()
        return raw_data

    except requests.exceptions.HTTPError as err:
        print('HTTP Error occured')
        print('Response is: {content}'.format(content=err.response.content))

    except requests.exceptions.ConnectTimeout:
        print('Connection timeout occured')


def clean_data_from_airtable(raw_data):
    """
    Очищаем данные и приводим их в нужный формат
    """
    airtable_cleaned_data = {}

    for i in range(len(raw_data['records'])):
        id_therapist = raw_data['records'][i]['id']
        tmp = [raw_data['records'][i]['fields']['Имя'],
               raw_data['records'][i]['fields']['Методы'],
               raw_data['records'][i]['fields']['Фотография'][0]['id'],
               raw_data['records'][i]['fields']['Фотография'][0]['url'],
               raw_data['records'][i]['createdTime']]
        airtable_cleaned_data[id_therapist] = tmp
    return airtable_cleaned_data


def update_postgres(raw_data, airtable_cleaned_data):
    """
    Устанавливаем соединение с PostgreSQL
    """
    conn = psycopg2.connect("dbname=meta_db user=postgres password=MetaMeta1")
    cur = conn.cursor()

    """
    Заливаем raw data в соответствующую таблицу
    """
    raw_data_to_add = str(raw_data)
    date_today = date.today()
    cur.execute(
        "INSERT INTO therapists_rawdata (date, raw_data) "
        "VALUES (%s, %s)", (date_today, raw_data_to_add))

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
    По полю therapist_id проверяем наличие в Airtable  записей, которых нет в Postgres, добавляем их
    """
    for i in airtable_cleaned_data.keys():
        if i not in ids_from_postgres:
            ther_id = i
            cur.execute(
                "INSERT INTO therapists_therapist("
                "therapist_id, name, methods, photo_id, photo_link, created_time) "
                "VALUES(%s, %s, %s, %s, %s, %s)", (
                    ther_id, *airtable_cleaned_data[i]
                ))

    """
    Проверяем на актуальность существующие записи в Postgres, при необходимости обновляем их
    """
    config = {
        0: "name",
        1: "methods",
        2: "photo_id",
        3: "photo_link",
        4: "created_time"
    }
    for i in ids_from_postgres:
        # получаем строку из Postgres, приводим ее к тому же виду, что и записи в airtable_cleaned_data
        cur.execute("SELECT therapist_id, name, methods, photo_id, photo_link, created_time "
                    "FROM therapists_therapist "
                    "WHERE therapist_id = %s", (i,))
        postgres_row = cur.fetchall()
        postgres_cleaned_data = {}
        postgres_ther_id = i
        tmp = list(postgres_row[0][1:])
        postgres_cleaned_data[postgres_ther_id] = tmp

        # сравниваем значения полей в двух таблицах, обновляем поля, которые были изменены
        if postgres_cleaned_data[i] != airtable_cleaned_data[i]:
            for k in range(len(postgres_cleaned_data[i])):
                if postgres_cleaned_data[i][k] != airtable_cleaned_data[i][k]:
                    cur.execute(sql.SQL("UPDATE therapists_therapist SET {} = %s "
                                        "WHERE therapist_id = %s").format(
                        sql.Identifier(config[k])),
                        (airtable_cleaned_data[i][k], i,))
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    raw = get_raw_data_from_airtable()
    cleaned = clean_data_from_airtable(raw)
    update_postgres(raw_data=raw, airtable_cleaned_data=cleaned)
