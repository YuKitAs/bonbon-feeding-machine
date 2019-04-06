import logging
import subprocess
import sys
import time
from configparser import ConfigParser

import os
from emoji import emojize
from telegram import ReplyKeyboardRemove
from telegram.ext import run_async

import webcam
from telegram_bot import TelegramBot

logging.basicConfig(stream=sys.stdout, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)

config = ConfigParser()
config.read("configuration.txt")

WEBCAM_PATH = config["webcam"]["Path"]
WEBCAM_DEFAULT_VIDEO_LENGTH = int(config["webcam"]["VideoLength"])

TELEGRAM_BOT_TOKEN = config["telegram.bot"]["Token"]
TELEGRAM_BOT_SEND_TIMEOUT = int(config["telegram.bot"]["SendTimeout"])


@run_async
def handle_start(_bot, update):
    update.message.reply_text(emojize(
        """
Hello Bonbon master! What do you want to do?
1. /takephoto :camera:
2. /recordvideo :video_camera:
3. /feed :lollipop:
4. /forwardservo :fast_forward:
5. /backwardservo :rewind:
        """.strip()), reply_markup=ReplyKeyboardRemove())


@run_async
def handle_take_photo(bot, update):
    logging.getLogger("handle_take_photo").info("Taking photo")

    image_path = webcam.capture_image(WEBCAM_PATH)

    logging.getLogger("handle_take_photo").info("Sending photo stored at '%s'" % image_path)

    bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, "rb"), timeout=TELEGRAM_BOT_SEND_TIMEOUT)

    logging.getLogger("handle_take_photo").info("Photo sent")


@run_async
def handle_record_video(bot, update):
    logging.getLogger("handle_record_video").info("Recording video")

    update.message.reply_text("Recording video... Please wait a minute.")

    video_path = webcam.capture_video(WEBCAM_PATH, WEBCAM_DEFAULT_VIDEO_LENGTH)

    logging.getLogger("handle_record_video").info("Sending video stored at '%s'" % video_path)

    bot.send_document(chat_id=update.message.chat_id, document=open(video_path, "rb"),
                      timeout=TELEGRAM_BOT_SEND_TIMEOUT)

    logging.getLogger("handle_record_video").info("Video sent")


@run_async
def handle_feed(_bot, _update):
    logging.getLogger("handle_feed").info("Rotating feeding machine")

    command_file_path = os.path.join('/tmp/bonbon/commands', 'feed_%s' % str(int(time.time())))
    with open(command_file_path, 'a'):
        pass

    logging.getLogger("handle_feed").info("Command file wrote: %s" % command_file_path)


@run_async
def handle_forward_servo(_bot, _update):
    logging.getLogger("handle_forward_servo").info("Rotating servo forwards")

    command_file_path = os.path.join('/tmp/bonbon/commands', 'forward_%s' % str(int(time.time())))
    with open(command_file_path, 'a'):
        pass

    logging.getLogger("handle_forward_servo").info("Command file wrote: %s" % command_file_path)


@run_async
def handle_backward_servo(_bot, _update):
    logging.getLogger("handle_backward_servo").info("Rotating servo backwards")

    command_file_path = os.path.join('/tmp/bonbon/commands', 'backward_%s' % str(int(time.time())))
    with open(command_file_path, 'a'):
        pass

    logging.getLogger("handle_backward_servo").info("Command file wrote: %s" % command_file_path)


@run_async
def handle_reset_servo(_bot, _update):
    logging.getLogger("handle_reset_servo").info("Resetting servo")

    command_file_path = os.path.join('/tmp/bonbon/commands', 'reset_%s' % str(int(time.time())))
    with open(command_file_path, 'a'):
        pass

    logging.getLogger("handle_reset_servo").info("Command file wrote: %s" % command_file_path)


@run_async
def handle_default_message(_bot, update):
    update.message.reply_text("Bonbon loves you ~")
    time.sleep(5)
    update.message.reply_text(emojize(":yellow_heart:"))


def handle_error(_bot, update, error):
    error_message = "An error has occurred: %s" % error

    if update:
        update.message.reply_text(error_message)

    logging.getLogger("handle_error").error(error_message)


@run_async
def handle_view_log(_bot, update):
    result = ""
    result += subprocess.run(['tail', 'servo.log'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    result += "=================\n"
    result += subprocess.run(['tail', 'main.log'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    update.message.reply_text(result)


def main():
    TelegramBot.with_token(TELEGRAM_BOT_TOKEN) \
        .add_command_handler("start", handle_start) \
        .add_command_handler("takephoto", handle_take_photo) \
        .add_command_handler("recordvideo", handle_record_video) \
        .add_command_handler("feed", handle_feed) \
        .add_command_handler("forwardservo", handle_forward_servo) \
        .add_command_handler("backwardservo", handle_backward_servo) \
        .add_command_handler("resetservo", handle_reset_servo) \
        .add_command_handler("viewlog", handle_view_log) \
        .add_default_message_handler(handle_default_message) \
        .add_error_handler(handle_error) \
        .start()


if __name__ == "__main__":
    main()
