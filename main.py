import time
import requests
import telegram
import os
from dotenv import load_dotenv
from textwrap import dedent
import logging
from hendlers import LogsHandler


logger = logging.getLogger('TgLogger')


def main():
    timestamp = time.time()
    load_dotenv()
    tg_token = os.getenv('TELEGRAM_TOKEN')
    tg_logger_token = os.getenv('TELEGRAM_LOGGER_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    bot = telegram.Bot(
        token=tg_token
    )
    logger.setLevel(logging.DEBUG)
    logger.addHandler(LogsHandler(tg_logger_token, tg_chat_id))
    logger.debug('Бот запущен')
    while True:
        try:
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
            if checking_result['status'] == 'found':
                timestamp = checking_result['last_attempt_timestamp']
                if checking_result['new_attempts'][0]['is_negative']:
                    text = f'''
                        Преподаватель проверил работу!
                        К сожалению, в работе нашлись ошибки!
                        {checking_result["new_attempts"][0]["lesson_url"]}
                        '''

                    bot.send_message(
                        chat_id=tg_chat_id,
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
        except requests.exceptions.ConnectionError as err:
            logger.debug('Бот упал с ошибкой')
            logger.exception(err)
            time.sleep(3)
            continue


if __name__ == '__main__':
    main()
