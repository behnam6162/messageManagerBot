from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import psycopg2

api_id = 29560166
api_hash = "f456d2cbdd328a5fd1cfc8c380413372"

bot = Client("robot", api_id, api_hash)

def get_connection():
    try:
        return psycopg2.connect(
            database = "ddo4b2kv76leb4",
            user = "ijzvxvtnrwroqe",
            password = "48527b554637ce08eb55912a5c3e6aadf99460edd9584fe6699a14bc98318426",
            host = "ec2-54-82-205-3.compute-1.amazonaws.com",
            port = 5432,
        )
    except:
        return False

def getKeywords():
    conn = get_connection()
    if conn:
        curs = conn.cursor()
        curs.execute("SELECT * FROM sc.kw")
        keywords = [item[1] for item in curs.fetchall()]
        conn.close()
        return keywords
    else:
        return []

def showKeywords():
    keywords = getKeywords()
    message = "\n".join(keywords)
    return message

def insertKeyword(keyword):
    conn = get_connection()
    if conn:
        curs = conn.cursor()
        curs.execute("INSERT INTO sc.kw (name) VALUES (%s)", [keyword])
        conn.commit()
        conn.close()
    
def addKeyWord(keyword):
    keywords = getKeywords()
    if keyword not in keywords:
        insertKeyword(keyword)
        return True
    else:
        return False

def delete(keyword):
    conn = get_connection()
    if conn:
        curs = conn.cursor()
        curs.execute("DELETE FROM sc.kw WHERE name = %s", [keyword])
        conn.commit()
        conn.close()
    
def delKeyWord(keyword):
    keywords = getKeywords()
    if keyword in keywords:
        delete(keyword)
        return True
    else:
        return False

def messageValidation(text):
    keywords = getKeywords()
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None
    
async def messageManager(client, message):
    try:
        text = message.text.lower()

        if str(message.chat.type) == "ChatType.PRIVATE":
            if text.startswith("add"):
                try:
                    keyword = text[3:].strip()
                    if addKeyWord(keyword):
                        await bot.send_message(message.chat.id, "کلمه کلیدی با موفقیت اضافه شد")
                    else:
                        await bot.send_message(message.chat.id, "این کلمه قبلا افزوده شده است")
                except:
                    pass
                
            elif text.startswith("del"):
                try:
                    keyword = text[3:].strip()
                    if delKeyWord(keyword):
                        await bot.send_message(message.chat.id, "کلمه کلیدی با موفقیت حذف شد")
                    else:
                        await bot.send_message(message.chat.id, "این کلمه در لیست کلمات وجود ندارد")
                except:
                    pass
                
            elif text.startswith("show"):
                await bot.send_message(message.chat.id, showKeywords())
    
        else:
            kw = messageValidation(text)
            if kw is not None and len(text) <= 300:
                msg = "کلید: " + kw + "\n\n" + "متن پيام:" + "\n\n" + text
                
                if str(message.chat.type) == "ChatType.CHANNEL":                    
                    try:
                        await message.forward(-1001462419183)
                    except:
                        if str(message.chat.username) != "None":
                            msg += "\n\n" + "لينک کانال: " + "\n\n" + "@" + str(message.chat.username)
                            msg += "\n\n" + "لينک پيام: " + "\n\n" + "https://t.me/%s/%s" % (str(message.chat.username), str(message.id))
                            
                        await bot.send_message(-1001462419183, msg)

                elif str(message.chat.type) == "ChatType.SUPERGROUP":
                    if str(message.chat.username) != "None":
                        msg += "\n\n" + "لينک گروه:" + "\n\n" + "@" + str(message.chat.username)
                        msg += "\n\n" + "لينک پيام:" + "\n\n" + "https://t.me/%s/%s" % (str(message.chat.username), str(message.id))
                        
                        if hasattr(message, "from_user"):
                            msg += "\n\n" + "آیدی کاربر:" + "\n\n" + "@" + str(message.from_user.username)
                                                        
                        await bot.send_message(-1001462419183, msg)
                    else:
                        try:
                            await message.forward(-1001462419183)
                        except:
                            await bot.send_message(-1001462419183, msg)

    except:
        pass

messageManagerHandler = MessageHandler(messageManager)
bot.add_handler(messageManagerHandler)

bot.run()

