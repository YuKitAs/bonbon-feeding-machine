from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import configparser
import time
import cv2
import servo

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('configuration.txt')

TOKEN = config['telegram.bot']['Token']
PATH = config['photo']['Path']


def start(bot, update):
    update.message.reply_text(
        "Hello Bonbon master! Enter /takephoto to check how Bonbon is doing." +
        " Enter /controlservo to rotate the feeding machine.")


def capture_image(bot, update):
    image = "{}bonbon-{}.png".format(PATH, time.strftime("%Y%m%d%H%M%S", time.localtime()))

    capture = cv2.VideoCapture(0)

    _, frame = capture.read()
    cv2.imwrite(image, frame)

    capture.release()
    cv2.destroyAllWindows()

    bot.send_photo(chat_id=update.message.chat_id, photo=open(image, "rb"))


def control_servo(bot, update):
    servo.send_servo_signal()


def auto_reply(bot, update):
    update.message.reply_text("Bonbon loves you <3")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("takephoto", capture_image))
    dispatcher.add_handler(CommandHandler("controlservo", control_servo))

    dispatcher.add_handler(MessageHandler(Filters.text, auto_reply))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
