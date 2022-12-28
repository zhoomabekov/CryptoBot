import requests
import json
from config import tickers, factors

class APIException(Exception):
    pass

class CryptoConverter:      # обработка исключений и если их нет, возврат сыммы в требуемой валюте
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты "{base}"')

        if quote not in tickers:
            raise APIException(f'Неизвестная валюта "{quote}"')

        if base not in tickers:
            raise APIException(f'Неизвестная валюта "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')


        return amount * factors[f'{quote} / {base}']