import os

from google.oauth2 import service_account
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]  # Указываем параметры для работы с таблицей
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')  # Указываем путь до файла с нашими реквизитами

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# Собираем наши реквизиты и параметры

SAMPLE_SPREADSHEET_ID = '15O8tQ8DE6r1XJsiqJ94TN6b5qSZVe4gIUSz7R0lhejc'  # указываем таблицу в google sheets
SAMPLE_RANGE_NAME = 'TestLst'  # указываем лист в таблице

service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()

#  Далее вызов API
data = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
#

print('Start show table')
for key, value in data.items():
    print(key, value)
print('End show table', end='\n\n')

def take_max_line_a() -> int:
    print(data.get('values'))
    return len(data.get('values'))  # Получаем наибольшее значение строки A


range_ = 'TestLst!A1:C5'  # Название листа!в какие ячейки вносить изменения
range_to_clear_all = 'TestLst'
content = {'values': [[1, 2, 3], [1, None, 2], [2, 'algorithm'], ['', 1, 2], [12, 1, 'Аргументация']]}
# Контент который хотим ввести

service.append(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    range=range_,
    valueInputOption='USER_ENTERED',
    body=content
).execute()
# Добавление в таблицу

service.clear(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    range=range_to_clear_all,
).execute()

content = {'values': [[1, 2, 3], [1, None, 2], [2, 3], ['', 1, 2], [f'=SUM(A1:A{take_max_line_a()-1})',
                                                                    1, 'Аргументация']]}  # Переопределим контент

service.append(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    range=range_,
    valueInputOption='RAW',
    body=content
).execute()
# Добавление в таблицу но вместо формулы будет записана строка

service.append(
    spreadsheetId=SAMPLE_SPREADSHEET_ID,
    range=range_,
    valueInputOption='USER_ENTERED',
    body=content
).execute()
# Изменение таблицы

