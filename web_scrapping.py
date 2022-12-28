import requests
from bs4 import BeautifulSoup
from datetime import date
import redis
import json

red = redis.Redis(
    host='redis-15580.c299.asia-northeast1-1.gce.cloud.redislabs.com',
    port=15580,
    password='jwLyACS7jf3iFaXZMPkYTzBDq9kcOr6T'
)

def scrapper():
    url = "https://nationalbank.kz/en/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut"
    html = requests.get(url)

    s = BeautifulSoup(html.content, 'html.parser')
    results = s.find(class_='table table--striped text-center text-primary text-size-xs')
    curr = results.find_all('td')
    convertion_rates = {}
    i = 0
    while True:
        if len(convertion_rates) == 3:
            break
        elif curr[i].text in ['USD / KZT', 'EUR / KZT', 'RUB / KZT']:
            convertion_rates[curr[i].text] = curr[i + 1].text
            i += 2
        else:
            i += 1

    factors = {
        'USD / KZT': float(convertion_rates['USD / KZT']),
        'KZT / USD': 1 / float(convertion_rates['USD / KZT']),

        'EUR / KZT': float(convertion_rates['EUR / KZT']),
        'KZT / EUR': 1 / float(convertion_rates['EUR / KZT']),

        'RUB / KZT': float(convertion_rates['RUB / KZT']),
        'KZT / RUB': 1 / float(convertion_rates['RUB / KZT']),

        'USD / EUR': float(convertion_rates['USD / KZT']) / float(convertion_rates['EUR / KZT']),
        'EUR / USD': float(convertion_rates['EUR / KZT']) / float(convertion_rates['USD / KZT']),

        'EUR / RUB': float(convertion_rates['EUR / KZT']) / float(convertion_rates['RUB / KZT']),
        'RUB / EUR': float(convertion_rates['RUB / KZT']) / float(convertion_rates['EUR / KZT']),

        'USD / RUB': float(convertion_rates['USD / KZT']) / float(convertion_rates['RUB / KZT']),
        'RUB / USD': float(convertion_rates['RUB / KZT']) / float(convertion_rates['USD / KZT'])
    }

    # red.set('factors', json.dumps(factors))
    # red.set('today', json.dumps({'last_date': date.today()}, default=str))
    return factors


try:                            # Проверяем был ли last_date ранее назначен, если нет, то это первый запуск программы
    last_date
except Exception:
    scrapper()
    last_date = date.today()
else:
    if last_date != date.today():
        scrapper()
        last_date = date.today()