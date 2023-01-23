# Work_cheker_bot

Telegram bot to receive notifications about checking work on [Devman](https://dvmn.org/) 

## How to install?

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```pip install -r requirements.txt```

Recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html) for isolate the project

## Launch.

#### Added to `.env` file:
    'DVMN_TOKEN' - Devman token to work with the API
    `TELEGRAM_TOKEN` - telegram token to work with the API
    `TG_CHAT_ID` - ID of your chat. It can be obtained by sending a message to the @userinfobot bot

#### Run `main.py` to receive verification notifications in telegram:

```commandline
python main.py
```


