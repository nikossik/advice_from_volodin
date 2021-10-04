import telebot
import sqlite3

import config
import messages
import function


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id, messages.bot_messages['help'])


@bot.message_handler(commands=['start'])
def bot_start(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data(
            id INTEGER,
            file_name_csv STRING,
            now_index INTEGER
        )
        """
    )
    connect.commit()

    cursor.execute(f"SELECT id FROM user_data WHERE id = {message.chat.id}")
    data = cursor.fetchone()

    if data is None:
        user_id = message.chat.id
        name = function.shuffle()
        cursor.execute("INSERT INTO user_data VALUES(?,?,?);", [user_id, name, 0])
        connect.commit()
        connect.close()

    sticker = open('img/book_sticker.webp', 'rb')
    bot.send_animation(message.chat.id, sticker)
    bot.send_message(message.chat.id, messages.bot_messages['start_message'])


@bot.message_handler(content_types=['text'])
def text_handler(message):
    try:
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT file_name_csv FROM user_data WHERE id = {message.chat.id}")
        file_name = cursor.fetchone()[0]

        connect.close()
        connect = sqlite3.connect('users.db')
        cursor = connect.cursor()
        cursor.execute(f"SELECT now_index FROM user_data WHERE id = {message.chat.id}")
        now_index = cursor.fetchone()[0]

        res = function.give_advice(file_name, now_index)

        bot.send_message(message.chat.id, res)

        cursor.execute('UPDATE user_data SET now_index=? WHERE id=?', (now_index+1, message.chat.id))
        connect.commit()
        connect.close()
    except:
        print('Соря')


if __name__ == "__main__":
    print('bot started!')
    bot.polling(none_stop=config.NONE_STOP)