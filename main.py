import telebot
from telebot import types

TOKEN = '5639992265:AAFMRsoa_xuZ1rBW8g5bd7VE7303dFrDkNE'
bot = telebot.TeleBot(TOKEN)

info_message = "Я умею выполнять команды:\n"
info_message += "1) GetStat - получить статистику по чату (число пользователей и админов)\n"
info_message += "2) Ban *username* - забанить в этом чате пользователя с именем username\n"
info_message += "3) Unban *username* - разбанить в этом чате пользователя с именем username\n"
info_message += "4) MakeAdmin *username* - сделать админом в этом чате пользователя с именем username\n"
info_message += "5) LeaveChat - удалить меня из чата\n"
info_message += "Ну что, начнем?"

users = {}
cur_chat_id = None


def after_ban(user_name):
    try:
      cur_user_id = users[user_name]
      print(user_name, cur_user_id)
      bot.ban_chat_member(cur_chat_id, cur_user_id)
      bot.send_message(cur_chat_id, "Забанил")
    except:
      bot.send_message(cur_chat_id, "Не получилось забанить. Проверьте, что у меня есть нужные права, и что вы правильно ввели username. Возможно я не знаю этого пользователя")

def after_unban(user_name):
    try:
      cur_user_id = users[user_name]
      bot.unban_chat_member(cur_chat_id, cur_user_id)
      bot.send_message(cur_chat_id, "Разбанил")
    except:
      bot.send_message(cur_chat_id, "Не получилось разбанить. Проверьте, что у меня есть нужные права, и что вы правильно ввели username. Возможно пользователь не в бане")

def after_admin(user_name):
    try:
      cur_user_id = users[user_name]
      bot.promote_chat_member(cur_chat_id, cur_user_id, True, True, True)
      bot.send_message(cur_chat_id, "Добавил админа")
    except:
      bot.send_message(cur_chat_id, "Что-то не пошло. Пожалуйста, проверьте что указанный пользователь не является админом. Если не является, то я не знаю этого пользователя")


stat_icon = "https://png.pngtree.com/png-vector/20190223/ourlarge/pngtree-stats-glyph-black-icon-png-image_691602.jpg"
ban_icon = "https://static6.depositphotos.com/1003559/644/i/600/depositphotos_6448250-stock-photo-skull-with-crossed-bones.jpg"
unban_icon = "https://cdn-icons-png.flaticon.com/512/56/56748.png"
make_admin_icon = "https://i.pinimg.com/236x/de/32/b5/de32b5b5fa1339e7f02a442b737c2828.jpg"
leave_chat_icon = "https://cdn-icons-png.flaticon.com/512/258/258149.png"


@bot.inline_handler(lambda query: query.query[:7] == "GetStat")
def query_text(query):
    r = types.InlineQueryResultArticle(
        id='1', title="Статистика",
        description="---",
        input_message_content=types.InputTextMessageContent(message_text=query.query),
        thumb_url=stat_icon, thumb_width=48, thumb_height=48)

    bot.answer_inline_query(query.id, [r], cache_time=2147483646)

@bot.inline_handler(lambda query: query.query[:3] == "Ban")
def query_text(query):
    r = types.InlineQueryResultArticle(
        id='1', title="Забанить",
        description="Имя?",
        input_message_content=types.InputTextMessageContent(message_text=query.query),
        thumb_url=ban_icon, thumb_width=48, thumb_height=48)

    bot.answer_inline_query(query.id, [r], cache_time=2147483646)

@bot.inline_handler(lambda query: query.query[:5] == "Unban")
def query_text(query):
    r = types.InlineQueryResultArticle(
        id='1', title="Разбанить",
        description="Имя?",
        input_message_content=types.InputTextMessageContent(message_text=query.query),
        thumb_url=unban_icon, thumb_width=48, thumb_height=48)

    bot.answer_inline_query(query.id, [r], cache_time=2147483646)

@bot.inline_handler(lambda query: query.query[:9] == "MakeAdmin")
def query_text(query):
    r = types.InlineQueryResultArticle(
        id='1', title="Сделать админом",
        description="Имя?",
        input_message_content=types.InputTextMessageContent(message_text=query.query),
        thumb_url=make_admin_icon, thumb_width=48, thumb_height=48)

    bot.answer_inline_query(query.id, [r], cache_time=2147483646)

@bot.inline_handler(lambda query: query.query[:9] == "LeaveChat")
def query_text(query):
    r = types.InlineQueryResultArticle(
        id='1', title="Удалить бота",
        description="---",
        input_message_content=types.InputTextMessageContent(message_text=query.query),
        thumb_url=leave_chat_icon, thumb_width=48, thumb_height=48)

    bot.answer_inline_query(query.id, [r], cache_time=2147483646)


@bot.message_handler(content_types=["new_chat_members"])
def handler_new_member(message):
    global cur_chat_id
    if cur_chat_id is None:
        cur_chat_id = message.chat.id
    
    bot.send_message(cur_chat_id, "Давно тебя не было в уличных гонках! Заходи!")
    bot.send_message(cur_chat_id, info_message)
    username = message.new_chat_members[0].username
    if username is None:
        userneme = message.new_chat_members[0].first_name + message.new_chat_members[0].last_name
    users[username] = message.new_chat_members[0].id


@bot.message_handler(content_types=["text"])
def first(message):
    global cur_chat_id
    if cur_chat_id is None:
        cur_chat_id = message.chat.id
        
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name + message.from_user.last_name
    users[username] = message.from_user.id
    print(message.from_user.id, username)

    data = message.text.split()
    try:
      if data[0] == "GetStat":
          bot.send_message(cur_chat_id, "Число пользователей в этом чате: " + str(bot.get_chat_member_count(cur_chat_id)) + '\n' + "Число админов в чате: " + str(len(bot.get_chat_administrators(cur_chat_id))))
      elif data[0] == "Ban":
          after_ban(data[1])
      elif data[0] == "Unban":
          after_unban(data[1])
      elif data[0] == "MakeAdmin":
          after_admin(data[1])
      elif data[0] == "LeaveChat":
          bot.send_message(cur_chat_id, "Я сделал все что мог... Я ухожу...")
          bot.leave_chat(cur_chat_id)
    except:
        bot.send_message(cur_chat_id, "Пожалуйста, укажите аргументы правильно")

bot.polling(none_stop=True, interval=0)
