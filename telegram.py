import time
from telebot import TeleBot, types
# from telebot import telebot      
import logging
# from telebot import register_next_step_handler
import database.dbapi as dbapi
import database.models as  models
# import app
TOKEN = "6188095128:AAFQm2b0FCcEZF-VJquZ4vtiJFs5Cd8awcA"
bot = TeleBot(token=TOKEN)
# dp = Dispatcher(bot=bot)

PORT = 5432



@bot.message_handler(commands=['start'])
def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.first_name
    logging.info(f'{user_id=} {user_full_name=}, {time.asctime()}')
    bot.send_photo(user_id, "https://i.ytimg.com/vi/R-RbmqzRC9c/maxresdefault.jpg")
    bot.send_message(user_id, f"Добро пожаловать в чат бота-библиотеки, {user_full_name}!")


@bot.message_handler(commands=['add'])
def add_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название книги:")
    # bot.send_message(message.chat.id, "Введите название книги:")
    
    def add_author(message):
        title = message.text
        bot.send_message(message.chat.id, "Введите автора:")
        bot.register_next_step_handler(message, add_year, title=title)
    def add_year(message, title):
        author = message.text
        bot.send_message(message.chat.id, "Введите год издания:")
        bot.register_next_step_handler(message, add_book_to_db, title=title, author=author)
    def add_book_to_db(message, title, author):
        published = message.text
        try:
            db.add(title, author, published)
            bot.send_message(message.chat.id, f"Книга добавлена")
        except:
            bot.send_message(message.chat.id, "Ошибка при добавлении книги")
    bot.register_next_step_handler(message, add_author)

@bot.message_handler(commands=['delete'])
def delete_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название книги:")
    
    def delete_author(message):
        title = message.text
        bot.send_message(message.chat.id, "Введите автора:")
        bot.register_next_step_handler(message, delete_year, title=title)

    def delete_year(message, title):
        author = message.text
        bot.send_message(message.chat.id, "Введите год издания:")
        bot.register_next_step_handler(message, find_book, title=title, author=author)

    def find_book(message, title, author):
        published = message.text
        try:
            db.get_book(title, author, published)
            bot.send_message(message.chat.id, f"Найдена книга: {title}. Удаляем?")
            bot.register_next_step_handler(message, delete_book_from_db, title=title, author=author, published=published)
        except:
            bot.send_message(message.chat.id, "Книга не найдена")

    def delete_book_from_db(message, title, author, published):
        check = message.text
        if check == "Да":
                try:
                    if db.delete(title, author, published):
                        bot.send_message(message.chat.id, f"Книга удалена")
                    else:
                        bot.send_message(message.chat.id, "Невозможно удалить книгу 1")
                except:
                    bot.send_message(message.chat.id, "Невозможно удалить книгу 2")
        else:
            bot.send_message(message.chat.id, "Невозможно удалить книгу 3")
    bot.register_next_step_handler(message, delete_author)


@bot.message_handler(commands=['find'])
def find_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название книги:")
    
    def find_author(message):
        title = message.text
        bot.send_message(message.chat.id, "Введите автора:")
        bot.register_next_step_handler(message, find_year, title=title)

    def find_year(message, title):
        author = message.text
        bot.send_message(message.chat.id, "Введите год издания:")
        bot.register_next_step_handler(message, find_book, title=title, author=author)

    def find_book(message, title, author):
        published = message.text
        try:
            db.get_book(title, author, published)
            bot.send_message(message.chat.id, f"Найдена книга: {title} {author} {published}.")
        except:
            bot.send_message(message.chat.id, "Такой книги у нас нет")
    bot.register_next_step_handler(message, find_author)
    
@bot.message_handler(commands=['borrow'])
def borrow_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название книги:")

    def borrow_author(message):
        title = message.text
        bot.send_message(message.chat.id, "Введите автора:")
        bot.register_next_step_handler(message, borrow_year, title=title)
        print('->')

    def borrow_year(message, title):
        author = message.text
        bot.send_message(message.chat.id, "Введите год издания:")
        bot.register_next_step_handler(message, borrow_book, title=title, author=author)
        print('->>')

    def borrow_book(message, title, author):
        print('->>>')
        published = message.text
        try:
            book_id = db.get_book(title, author, published)
            bot.send_message(message.chat.id, f"Найдена книга: {title} {author} {published}. Берем?")
            bot.register_next_step_handler(message, borrow_book_1, book_id=book_id )
        except:
            print('->>>>')


    def borrow_book_1(message, book_id):
        print('-<')
        check = message.text
        if check == "Да":
            try:
                db.borrow(book_id, user_id)
                bot.send_message(message.chat.id, f"Вы взяли книгу")
            except:
                bot.send_message(message.chat.id, "Книгу сейчас невозможно взять 1")
        else:
            bot.send_message(message.chat.id, "Книгу сейчас невозможно взять 2")

    bot.register_next_step_handler(message, borrow_author)


@bot.message_handler(commands=['retrieve'])
def retrieve_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    # print('->')
    user_id = message.from_user.id
    print(user_id)
    # print('->>>')
    try:
        borrow_id = db.get_borrow(user_id)
        # print(borrow_id)
        infa_book = db.get_book_borrow(borrow_id)
        # print(infa_book)
        db.retrieve(borrow_id)
        bot.send_message(user_id, f"Вы вернули книгу {infa_book}")
        
    except:
        bot.send_message(message.chat.id, "Ошибка")

    
@bot.message_handler(commands=['list'])
def list_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    user_id = message.from_user.id
    try:
        bot.send_message(user_id, "Список книг:")
        lst = db.list_books()
        for b in lst:
            ud =''
            if b[3] != None:
                ud = ('(удалена)')
            bot.send_message(user_id, f'{b[0]}, {b[1]}, {b[2]} {ud};')
    except:
        bot.send_message(message.chat.id, "Нет книг")

@bot.message_handler(commands=['stats'])
def stats_handler(message: types.Message):
    db = dbapi.DatabaseConnector('biblabot', 'localhost', PORT)
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название книги:")

    def stats_author(message):
        title = message.text
        bot.send_message(message.chat.id, "Введите автора:")
        bot.register_next_step_handler(message, stats_year, title=title)

    def stats_year(message, title):
        author = message.text
        bot.send_message(message.chat.id, "Введите год издания:")
        bot.register_next_step_handler(message, stats_book, title=title, author=author)

    def stats_book(message, title, author):
        published = message.text
        try:
            book_id = db.get_book(title, author, published)
            bot.send_message(message.chat.id, f"Статистика доступна по адресу http://localhost:{PORT}/download/{book_id}")
        except:
            bot.send_message(message.chat.id, f"Нет такой книги")
            
    bot.register_next_step_handler(message, stats_author)
#print('=================БОТ ЗАПУЩЕН=================')
#bot.polling(none_stop=True)