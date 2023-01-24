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
        checking_result = response.json()
        try:
            if checking_result['status'] == 'found':
                timestamp = checking_result['last_attempt_timestamp']
                if checking_result['new_attempts'][0]['is_negative']:
                    text = f'''
                        Преподаватель проверил работу!
                        К сожалению, в работе нашлись ошибки!
                        {checking_result["new_attempts"][0]["lesson_url"]}
                        '''

                    bot.send_message(
                        chat_id=os.getenv('TG_CHAT_ID'),
                        text=dedent(text)
                    )
                else:
                    text = f'''Преподаватель проверил работу!
                    Преподавателю все понравилось!
                    {checking_result["new_attempts"][0]["lesson_url"]}
                    '''
                    bot.send_message(
                        chat_id=os.getenv('TG_CHAT_ID'),
                        text=dedent(text)
                    )
            elif checking_result['status'] == 'timeout':
                timestamp = checking_result['timestamp_to_request']
        except requests.exceptions.HTTPError:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(3)
            continue


if __name__ == '__main__':
    main()
