import os
import django
import requests
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import TelegramUser

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

def get_updates(offset=None):
    url = f'{BASE_URL}/getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()['result']

def send_message(chat_id, text):
    url = f'{BASE_URL}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=data)

def main():
    print('Bot started...')
    offset = None
    while True:
        try:
            updates = get_updates(offset)
        except Exception as e:
            print(f'Error fetching updates: {e}')
            continue
        for update in updates:
            offset = update['update_id'] + 1
            if 'message' in update and update['message'].get('text') == '/start':
                user = update['message']['from']
                telegram_id = str(user['id'])
                username = user.get('username')
                first_name = user.get('first_name')
                last_name = user.get('last_name')
                try:
                    TelegramUser.objects.get_or_create(
                        telegram_id=telegram_id,
                        defaults={
                            'username': username,
                            'first_name': first_name,
                            'last_name': last_name,
                            'date_added': timezone.now(),
                        }
                    )
                    send_message(update['message']['chat']['id'], 'Your username has been saved!')
                except Exception as e:
                    print(f'Error saving user: {e}')

if __name__ == '__main__':
    main() 