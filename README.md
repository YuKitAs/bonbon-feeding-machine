# bonbon-feeding-machine

## Prerequisites

* Python Virtualenv (see [note](https://github.com/YuKitAs/tech-note/blob/master/programming-language/python/setup-virtual-environment.md))

## Usage

1. Create a directory with write permission to store photos and videos, and a directory with write permission to store servo commands as sub-directory, for example:

    ```console
    $ mkdir -p /path/to/bonbon/commands
    ```

2. Create `configuration.txt` in the project root with custom values as follows:
    
    ```
    [webcam]
    Path = /path/to/bonbon/
    VideoLength = 15
    
    [telegram.bot]
    Token = random-bot-access-token
    ChatId = [whitelisted-chat-id-1, whitelisted-chat-id-2]
    SendTimeout = 20
    ```
    
    The bot access token which can be retrieved or revoked from BotFather. 
    
    The individual chat id can be retrieved with `update.message.chat_id`, or just send a random message and then check logs for `handle_default_message`.


3. Activate virtualenv, install all Python modules with pip (`sudo apt install python-pip`):

    ```console
    $ pip install -r requirements.txt
    ```

4. After connected servo, run `set-device-permission.sh`

5. Execute `run.sh` to start Telegram bot and servo in the background (remember to check if the processes `main.py` and `servo.py` are already running)

6. The hidden Telegram bot command `/viewlog` can be used to list recent logs

## Worklog

### v1.0

- [x] Capture image with webcam and save to disk
- [x] Send image from disk with telegram bot
- [x] Servo control
- [x] Implement remote control by mobile phone
- [x] Assemble and test

### v2.0

- [X] Record video and save to disk
- [X] Add an option for sending video
- [X] Add an option for viewing logs
- [X] Add credentials for telegram bot
- [ ] Adjust image brightness
- [ ] Non-continuous servo
- [ ] Better UART communication
- [ ] Better construction
