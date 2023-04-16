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

#### example:

````
TELEGRAM_TOKEN=1234567890:AAH6I2jaaaZZZ7PCtJaEPm5B-dM-******
TG_CHAT_ID=1234567890
DVMN_TOKEN=4985f388872e349d1d34ca76e8d8989899a9cf28
TELEGRAM_LOGGER_TOKEN=1234567890:AAH6I2jaaaAAB7PCtJaEPm5B-dM-******
````

#### Run `main.py` to receive verification notifications in telegram:

```commandline
python main.py
```

## Build Using Docker

#### Added to `.env` file:
    'DVMN_TOKEN' - Devman token to work with the API
    `TELEGRAM_TOKEN` - telegram token to work with the API
    `TG_CHAT_ID` - ID of your chat. It can be obtained by sending a message to the @userinfobot bot

###### example:

````
TELEGRAM_TOKEN=1234567890:AAH6I2jaaaZZZ7PCtJaEPm5B-dM-******
TG_CHAT_ID=1234567890
DVMN_TOKEN=4985f388872e349d1d34ca76e8d8989899a9cf28
TELEGRAM_LOGGER_TOKEN=1234567890:AAH6I2jaaaAAB7PCtJaEPm5B-dM-******
````

#### Build the image

`docker build -t work_cheker_bot .`


#### Create the container and run:

`docker run -dit work_cheker_bot `


