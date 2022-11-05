from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import sqlite3

api_id = 29560166
api_hash = "f456d2cbdd328a5fd1cfc8c380413372"

bot = Client("robot", api_id, api_hash)

def getKeywords():
    connection_obj = sqlite3.connect('db.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT * FROM Keywords")
    keywords = [item[1] for item in cursor_obj.fetchall()]
    connection_obj.close()
    return keywords

async def showKeywords():
    keywords = getKeywords()
    message = "   ".join(keywords)
    await bot.send_message(-1001462419183, message)

def insertKeyword(keyword):
    connection_obj = sqlite3.connect('db.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("INSERT INTO Keywords (name) VALUES (?)", [keyword])
    connection_obj.commit()
    connection_obj.close()
    
def addKeyWord(keyword):
    keywords = getKeywords()
    if keyword.lower() not in keywords:
        insertKeyword(keyword)

def delete(keyword):
    connection_obj = sqlite3.connect('db.db')
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM Keywords WHERE name = ?", [keyword])
    connection_obj.commit()
    connection_obj.close()
    
def delKeyWord(keyword):
    keywords = getKeywords()
    if keyword.lower() in keywords:
        delete(keyword)

def messageValiddation(text):
    keywords = getKeywords()
    for keyword in keywords:
        if keyword in text:
            return True
    return False
    
async def messageManager(client, message):
    text = message.text

    try:
        if message.chat.id == 229812662:
            if text.startswith("addKeyword"):
                try:
                    keyword = text.split()[1]
                    addKeyWord(keyword)
                except:
                    pass
                
            elif text.startswith("delKeyword"):
                try:
                    keyword = text.split()[1]
                    delKeyWord(keyword)
                except:
                    pass
                
            elif text.startswith("showKeyword"):
                await showKeywords()
                
        else:
            if str(message.chat.type) == "ChatType.CHANNEL":
                if messageValiddation(text.lower()):
                    msg = "متن پيام:" + "\n\n" + text
                    
                    if str(message.chat.username) != "None":
                        msg += "\n\n" + "لينک کانال: " + "\n\n" + "@" + str(message.chat.username)
                        msg += "\n\n" + "لينک پيام: " + "\n\n" + "https://t.me/%s/%s" % (str(message.chat.username), str(message.id))
                        
                    await bot.send_message(-1001462419183, msg)
                    
            elif str(message.chat.type) == "ChatType.SUPERGROUP":
                if len(text) <= 150 and messageValiddation(text.lower()):
                    msg = "متن پيام:" + "\n\n" + text
                    
                    if str(message.chat.username) != "None":
                        msg += "\n\n" + "لينک گروه:" + "\n\n" + "@" + str(message.chat.username)
                        msg += "\n\n" + "لينک پيام:" + "\n\n" + "https://t.me/%s/%s" % (str(message.chat.username), str(message.id))

                    if str(message.from_user.username) != "None":
                        msg += "\n\n" + "آيدي کاربر:" + "\n\n" + "@" + str(message.from_user.username)

                    await bot.send_message(-1001462419183, msg)
    except:
        pass

messageManagerHandler = MessageHandler(messageManager)
bot.add_handler(messageManagerHandler)

bot.run()

