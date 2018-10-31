# bonbon-feeding-machine

## Prerequisites

* Python
* pip (`sudo apt install python-pip`)

## Usage

1. Create a directory with write permission to store photos and videos (e.g. `/tmp/bonbon`)

2. Create a directory with write permission to store servo commands (e.g. `/tmp/bonbon/commands`)

3. Create `configuration.txt` in the project root with the following content, modify the bot access token which can be retrieved or revoked from BotFather:

  ```
  [webcam]
  Path = /path/to/bonbon/photos/
  VideoLength = 15

  [telegram.bot]
  Token = random-bot-access-token
  SendTimeout = 20
  ```

4. Install all python modules with

  ```console
  $ pip install -r requirements.txt
  ```

5. After connected servo, run `set-device-permission.sh`

6. If in virtualenv, use `run.sh` to start Telegram bot and servo, otherwise

  for Telegram bot:

  ```console
  $ python main.py >> main.log
  ```

  for servo:

  ```console
  $ python servo.py >> servo.log
  ```

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
- [ ] Add credentials for telegram bot
- [ ] Adjust image brightness
- [ ] Non-continuous servo
- [ ] Better UART communication
- [ ] Better construction
