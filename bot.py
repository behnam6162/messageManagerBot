from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import psycopg2

api_id = 29560166
api_hash = "f456d2cbdd328a5fd1cfc8c380413372"

bot = Client("robot", api_id, api_hash)

with bot:
    try:
        ps = [p async for p in bot.get_chat_photos("me")]
        await bot.delete_profile_photos([p.file_id for p in ps])
        
        photos = ["640x640_BVARwpjT_2457589_1636761074725045718.jpeg", "irs01_s3old_10531478083423692807.jpg"]
        file = open("index.txt", "r")
        index = int(file.read())
        file.close()
        
        if index == 0:
            index = 1
        else:
            index = 0
            
        await bot.set_profile_photo(photo=photos[index])
        
        new_file = open("index.txt", "w")
        new_file.write(str(index))
        new_file.close()
        
    except:
        pass

def messageValidation(text):
    keywords = ['java', 'جاوا', 'python', 'پایتون', 'c#', 'csharp', 'سی شارپ', 'c++', 'سی پلاس پلاس',
                'fortran', 'js', 'javascript', 'جاوا اسکریپت', 'html', 'اچ تی ام ال', 'css', 'سی اس اس',
                'programming', 'برنامه نویسی', 'eclipse', 'اکلیپس', 'ایکلیپس', 'vscode', 'وی اس کد',
                'machine learning', 'یادگیری ماشین', 'quera', 'کویرا', 'کوئرا', 'web design', 'طراحی وب',
                'pascal', 'پاسکال', 'data structure', 'ساختمان داده', 'داده ساختار', 'algoritm design',
                'طراحی الگوریتم', 'الگوریتم', 'data base', 'database', 'پایگاه داده', 'دیتابیس', 'datamining',
                'داده کاوی', 'swing', 'javafx', 'شی گرایی', 'golang', 'go', 'زبان گو', 'زبان c',
                'زبان سی', 'زبان r', 'kotlin', 'کاتلین', 'android', 'اندروید', 'فرترن', 'فرتران', 'طراحی سایت',
                'react', 'vue', 'angular', 'react native', 'django', 'جنگو', 'پانداس', 'pandas', 'نامپای', 'numpy',
                'فلسک', 'flask', 'ری اکت', 'سی پلاس', 'c+', 'لیست پیوندی', 'link list', 'linked list', 'graph', 'گراف',
                'tkinter', 'پای کیوتی', 'pyqt', 'pygame', 'پای گیم', 'سوئینگ', 'اف ایکس', 'اف اکس', 'پشته', 'stack', 'آرایه'
                , 'ارایه', 'array', 'php', 'پی اچ پی', 'لاراول', 'laravel', 'matlab', 'متلب', 'مطلب', 'frontend', 'front end',
                'backend', 'back end', 'فرانت اند', 'بک اند', 'flowchart', 'algoritm', 'فلوچارت', 'sql', 'mysql', 'mongodb',
                'postgers', 'postgersql', 'ریاضی ۱', 'ریاضی 1'
                , 'فیزیک ۱', 'فیزیک 1', 'ریاضی', 'فیزیک', 'مبانی کامپیوتر', 'نرم افزار', 'جاوااسکریپت', 'cpp',
                'cp', 'فلاتر', 'flutter', '++c', '+c', '#c', 'کامپایلر', 'compiler', 'کدنویسی', 'کد نویسی', 'هوش مصنوعی']
    
    for keyword in keywords:
        if keyword in text:
            return keyword
    return None
    
async def messageManager(client, message):
    '''
    try:
        ps = [p async for p in bot.get_chat_photos("me")]
        await bot.delete_profile_photos([p.file_id for p in ps])
        
        photos = ["640x640_BVARwpjT_2457589_1636761074725045718.jpeg", "irs01_s3old_10531478083423692807.jpg"]
        file = open("index.txt", "r")
        index = int(file.read())
        file.close()
        
        if index == 0:
            index = 1
        else:
            index = 0

        await bot.set_profile_photo(photo=photos[index])

        new_file = open("index.txt", "w")
        new_file.write(str(index))
        new_file.close()
        
    except:
        pass
    '''
                        
    try:
        text = message.text.lower()
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

