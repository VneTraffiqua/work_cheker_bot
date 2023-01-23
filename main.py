import time
import requests
import telegram
import os
from dotenv import load_dotenv


def get_lesson_verification(timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': 'Token 4985f388872e349d1d34ca76e8d9328665a9cf28'
    }
    params = {
        'timestamp': timestamp
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    bot = telegram.Bot(
        token=os.getenv('TELEGRAM_TOKEN')
    )
    timestamp = time.time()
    dvmn_request = get_lesson_verification(timestamp)
    while True:
        try:
            if dvmn_request['status'] == 'found':
                timestamp = dvmn_request['last_attempt_timestamp']
                if dvmn_request['new_attempts'][0]['is_negative']:
                    bot.send_message(
                        chat_id=os.getenv('TG_CHAT_ID'),
                        text=f'Преподаватель проверил работу! '
                             f'К сожалению, в работе нашлись ошибки! \n'
                             f'{dvmn_request["new_attempts"][0]["lesson_url"]}'
                    )
                else:
                    bot.send_message(
                        chat_id=os.getenv('CHAT_ID'),
                        text=f'Преподаватель проверил работу! '
                             f'Преподавателю все понравилось! '
                             f'Можете приступать к следующему уроку. \n'
                             f'{dvmn_request["new_attempts"][0]["lesson_url"]}'
                    )
            elif dvmn_request['status'] == 'timeout':
                timestamp = dvmn_request['timestamp_to_request']
            dvmn_request = get_lesson_verification(timestamp)
        except requests.exceptions.HTTPError:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(3)
            continue


if __name__ == '__main__':
    main()
