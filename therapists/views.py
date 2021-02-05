import requests
from django.http import HttpResponse
from django.shortcuts import render

AIRTABLE_BASE_ID = 'appPFtPl42cKzPk1f'
AIRTABLE_TABLE_NAME = 'Psychotherapists'
API_KEY = 'keyTB6bXM5hmHID2v'

ENDPOINT = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'


def get_data(request):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    r = requests.get(url=ENDPOINT, headers=headers)

    return r


def index(request):
    """
    рендер страницы всех специалистов
    """

    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(url=ENDPOINT, headers=headers)
    qty = len(response.json()['records'])
    name = []
    for i in range(qty):
        name.append(response.json()['records'][i]['fields']['Имя'])
    return render(request, 'index.html', {'names': name})


def therapist_page(request):
    return render(request, 'therapist_page.html')

# RESPONSE
# r['records'][0]['fields'] - list of fields
# r['records'][0]['fields']['Методы'] - list of methods
# r['records'][0]['fields']['Имя'] - name
# r['records'][0]['fields'][0]['Фотография']['url'] - main photo link
#
# {'records': [{'id': 'rec9dKijJaU9vWtoK',
#               'fields': {'Методы': ['Психоанализ', 'Коучинг', 'Музыкотерапия'],
#                          'Имя': 'Василий',
#                          'Фотография': [
#                               {'id': 'attY7G4ysiIDnSaUw',
#                               'url': 'https://dl.airtable.com/.attachments/7da0d4c7963babf742137abc4e9a1a99/5f547505/1.jpg',
#                               'filename': '1.jpg', 'size': 1045553, 'type': 'image/jpeg',
#                               'thumbnails':
#                                           {'small': {'url': 'https://dl.airtable.com/.attachmentThumbnails/33589c8479683db065f99673a5f5a4fe/0c0abe62', 'width': 27, 'height': 36},
#                                            'large': {'url': 'https://dl.airtable.com/.attachmentThumbnails/294c23dbb27ebc13b3b83f5225dcd90f/c31bee49', 'width': 512, 'height': 683},
#                                            'full': {'url': 'https://dl.airtable.com/.attachmentThumbnails/90e6285452aacd6ffa975e76cc2dfea3/e74d7881', 'width': 3000, 'height': 3000}}}
#                                            ]
#                       },
#              'createdTime': '2021-02-02T14:29:36.000Z'},
#              {'id': 'recrGGaxQyoeV6k9c',
#               'fields': {'Методы': ['Психоанализ', 'Музыкотерапия', 'Сказкотерапия'], 'Имя': 'Георгий', 'Фотография': [
#                   {'id': 'att9KnVSSmHaLJNUm',
#                    'url': 'https://dl.airtable.com/.attachments/c15cce685652a0670beb0f4bb2485041/0d0720fe/3.jpg',
#                    'filename': '3.jpg', 'size': 2364068, 'type': 'image/jpeg', 'thumbnails': {'small': {
#                       'url': 'https://dl.airtable.com/.attachmentThumbnails/e83fac2bf60a89ff000b8056a182fd90/1df30433',
#                       'width': 54, 'height': 36}, 'large': {
#                       'url': 'https://dl.airtable.com/.attachmentThumbnails/18704e5905c6c8c0185cba3984ffc973/f553ab3e',
#                       'width': 768, 'height': 512}, 'full': {
#                       'url': 'https://dl.airtable.com/.attachmentThumbnails/cd731c2c56e3269e6dce5007489e051d/33442513',
#                       'width': 3000, 'height': 3000}}}]}, 'createdTime': '2021-02-02T14:29:36.000Z'},
#              {'id': 'recuJ6e1pvG6tkRdC',
#               'fields': {'Методы': ['Гештальт-терапия', 'Коучинг', 'Психосинтез', 'Сказкотерапия'], 'Имя': 'Иннокентий',
#                          'Фотография': [{'id': 'atttxEgUknSdwDjme',
#                                          'url': 'https://dl.airtable.com/.attachments/fa70928a82a214d22c4b7a2eeace79d2/e5a12360/2.jpg',
#                                          'filename': '2.jpg', 'size': 1903305, 'type': 'image/jpeg', 'thumbnails': {
#                                  'small': {
#                                      'url': 'https://dl.airtable.com/.attachmentThumbnails/a5197ff79b297a147e1a7239edd488cb/9e3f3aa4',
#                                      'width': 24, 'height': 36}, 'large': {
#                                      'url': 'https://dl.airtable.com/.attachmentThumbnails/858d861294660b22f72d24e36de00dc5/189227b8',
#                                      'width': 512, 'height': 768}, 'full': {
#                                      'url': 'https://dl.airtable.com/.attachmentThumbnails/b731295b2d227b2b70bf9d19829f954c/87be7931',
#                                      'width': 3000, 'height': 3000}}}]}, 'createdTime': '2021-02-02T14:29:36.000Z'}]}
