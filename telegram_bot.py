from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import configparser
import webcam
import servo
from emoji import emojize

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('configuration.txt')

TOKEN = config['telegram.bot']['Token']
PATH = config['photo']['Path']

VIDEO, SERVO = range(2)


def start(_bot, update):
    update.message.reply_text(
        "Hello Bonbon master! What do you want to do?\n"
        + emojize("1. /takephoto :camera:\n")
        + emojize("2. /recordvideo :video_camera:\n")
        + emojize("3. /controlservo :lollipop:"), reply_markup=ReplyKeyboardRemove())


def take_photo(bot, update):
    image = webcam.capture_image(PATH)

    bot.send_photo(chat_id=update.message.chat_id, photo=open(image, "rb"))


def set_length(_bot, update):
    update.message.reply_text("How long should the video be? Please enter a number of seconds (MAX = 30). \n/cancel",
                              reply_markup=ReplyKeyboardRemove())

    return VIDEO


def record_video(bot, update):
    length = update.message.text
    if 0 < int(length) <= 30:
        update.message.reply_text("Recording video... Please wait a minute.")
        video = webcam.capture_video(PATH, int(length))
        bot.send_document(chat_id=update.message.chat_id, document=open(video, "rb"), timeout=1000)
    else:
        update.message.reply_text("Invalid number. No video recorded.")

    return ConversationHandler.END


def confirm_video(_bot, update):
    reply_keyboard = [["Yes", "No"]]

    update.message.reply_text("Do you want to record the behavior of servo? \n/cancel",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                               one_time_keyboard=True))

    return SERVO


def control_servo(bot, update):
    if update.message.text == "Yes":
        update.message.reply_text("Rotating servo and recording...", reply_markup=ReplyKeyboardRemove())
        # servo.send_servo_signal()
        video = webcam.capture_video(PATH, 5)
        bot.send_document(chat_id=update.message.chat_id, document=open(video, "rb"), timeout=1000)
    elif update.message.text == "No":
        update.message.reply_text("Rotating servo...", reply_markup=ReplyKeyboardRemove())
        # servo.send_servo_signal()

    return ConversationHandler.END


def cancel_conv(_bot, update):
    update.message.reply_text("Action canceled.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def auto_reply(_bot, update):
    update.message.reply_text("Bonbon loves you <3")


def error(_bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_handler(CommandHandler("takephoto", take_photo))

    video_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('recordvideo', set_length)],

        states={
            VIDEO: [MessageHandler(Filters.text, record_video)]
        },

        fallbacks=[CommandHandler('cancel', cancel_conv)]
    )

    dispatcher.add_handler(video_conv_handler)

    servo_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('controlservo', confirm_video)],

        states={
            SERVO: [MessageHandler(Filters.text, control_servo)]
        },

        fallbacks=[CommandHandler('cancel', cancel_conv)]
    )

    dispatcher.add_handler(servo_conv_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, auto_reply))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
