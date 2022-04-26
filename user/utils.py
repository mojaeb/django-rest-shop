import json
import random
import requests


def generate_code(count=5):
    code = ''
    for n in range(count):
        code += str(random.randrange(10))
    return code


class SmsService:
    PATH = "https://rest.payamak-panel.com/api/SendSMS/%s"

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_data(self):
        return {
            'username': self.username,
            'password': self.password,
        }

    @staticmethod
    def post(url, data):
        result = requests.post(url, data=data)
        return result.json()

    def send(self, to, text, is_flash=False):
        url = self.PATH % "SendSMS"
        from_number = ''
        numbers = self.get_numbers()
        if len(numbers) > 0:
            from_number = numbers['Data'][0]['Number']
        else:
            return Exception
        data = {
            'to': to,
            'from': from_number,
            'text': text,
            'isFlash': is_flash
        }
        return self.post(url, {**data, **self.get_data()})

    def get_numbers(self):
        url = self.PATH % "GetUserNumbers"
        return self.post(url, self.get_data())
