import time
import requests
import telegram
import os
from dotenv import load_dotenv
from textwrap import dedent


def main():
    load_dotenv()
    bot = telegram.Bot(
        token=os.getenv('TELEGRAM_TOKEN')
    )
    timestamp = time.time()
    while True:
        url = 'https://dvmn.org/api/long_polling/'
        headers = {
            'Authorization': f'Token {os.getenv("DVMN_TOKEN")}'
        }
        params = {
            'timestamp': timestamp
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        dvmn_request = response.json()
        try:
            if dvmn_request['status'] == 'found':
                timestamp = dvmn_request['last_attempt_timestamp']
                if dvmn_request['new_attempts'][0]['is_negative']:
                    text = f'''
                        Преподаватель проверил работу!
                        К сожалению, в работе нашлись ошибки!
                        {dvmn_request["new_attempts"][0]["lesson_url"]}
                        '''

                    bot.send_message(
                        chat_id=os.getenv('TG_CHAT_ID'),
                        text=dedent(text)
                    )
                else:
                    text = f'''Преподаватель проверил работу!
                    Преподавателю все понравилось!
                    {dvmn_request["new_attempts"][0]["lesson_url"]}
                    '''
                    bot.send_message(
                        chat_id=os.getenv('TG_CHAT_ID'),
                        text=dedent(text)
                    )
            elif dvmn_request['status'] == 'timeout':
                timestamp = dvmn_request['timestamp_to_request']
        except requests.exceptions.HTTPError:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(3)
            continue


if __name__ == '__main__':
    main()
