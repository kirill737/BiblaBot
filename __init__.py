import database.dbapi
import database.models

#__all__ =  ["dbapi", "models"]

from app import *
from telegram import *
import threading

class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run()

class TelegramThread(threading.Thread):
    def run(self) -> None:
        bot.polling(non_stop=True)
    
if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()

    telegram_thread = TelegramThread()
    telegram_thread.start()
