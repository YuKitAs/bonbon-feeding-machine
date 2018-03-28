import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


class TelegramBot:
    def __init__(self, token):
        self.updater = Updater(token)
        self.dispatcher = self.updater.dispatcher

    def start(self):
        logging.getLogger("TelegramBot").info("Starting telegram bot")
        self.updater.start_polling()
        self.updater.idle()

    def add_command_handler(self, command, callback):
        self.dispatcher.add_handler(CommandHandler(command, callback))
        return self

    def add_error_handler(self, callback):
        self.dispatcher.add_error_handler(callback)
        return self

    def add_default_message_handler(self, callback):
        self.dispatcher.add_handler(MessageHandler(Filters.text, callback))
        return self

    @staticmethod
    def with_token(token):
        return TelegramBot(token)
