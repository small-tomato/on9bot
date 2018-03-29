# On9Bot (an annoying Cantonese Telegram bot) source code
# Uses Python 3 and the python-telegram-bot library, hosted on Heroku

from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import BadRequest
from time import sleep
from re import match
import psycopg2
import logging
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# conn = psycopg2.connect(host="ec2-23-21-121-220.compute-1.amazonaws.com",
#                         database="ddqe8lueaue1pl", user="fttveeezgekmvf",
#                         password="948fc928d48ed553c738617c8a906b5efc5b86e97ceb42cbbc55839a92057889")
# cur = conn.cursor()


def start(bot, update):
    if update.message.chat_id > 0:
        update.message.reply_markdown("你好，我係全Telegram最On9嘅bot。用 /help 睇點用。Zzz...\n\n"
                                      "I am only available in Cantonese for now since this bot is specifically "
                                      "designed to annoy members in a public Cantonese group [HK Duker](t.me/hkduker).",
                                      disable_web_page_preview=True)


def bot_help(bot, update):
    update.message.reply_markdown("[On9Bot所有功能](http://telegra.ph/On9Bot-Help-03-25)\n"
                                  "[Source code](https://www.codepile.net/pile/3aD3DPkD)")


def tag9js_text():
    text = '''一齊撳掣tag死[JS](tg://user?id=190726372)啦！限時15秒，現在開始！JS受死啦！
呢個群組個Enforcer好鬼煩，flood小小就會踢走你。你要注意下，五秒唔好撳個掣多過七次，否則你會被踢走。
萬一你撳掣太快，比Grey Wolf Enforcer踢走左去火星，你可以global search [HK Duker](t.me/hkduker) 即刻入返嚟繼續撳掣tag JS。
你可以隨時撳 /remove\_keyboard 整走個keyboard。'''
    return text


@run_async
def tag9js(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if update.message.chat_id == -1001295361187:
            js_info = bot.get_chat_member(-1001295361187, 190726372)
            if js_info.status != "creator":
                update.message.reply_markdown("一齊撳掣tag死[JS](tg://user?id=190726372)—— 吓？！JS唔")
            if js_info.user.username:
                update.message.reply_markdown(tag9js_text(),
                                              reply_markup=ReplyKeyboardMarkup([[js_info.user.name]]),
                                              disable_web_page_preview=True)
                sleep(15)
                update.message.reply_text("我已經整走咗個鍵盤啦。",
                                          reply_markup=ReplyKeyboardRemove(), quote=False)
            else:
                update.message.reply_text("你條死JS，del咗username？！豈有此理，等本大爺親自tag你啦！")
                for i in range(3):
                    update.message.reply_markdown("[JS](tg://user?id=190726372)上水啦！", quote=False)
                    sleep(2)
                update.message.reply_text("算啦，再tag JS我會攰死，今次放過你啦唉。", quote=False)
        elif update.message.chat_id < 0:
            update.message.reply_markdown("為咗減少對[JS](tg://user?id=190726372)嘅騷擾，呢個指令本群組用唔到㗎。")
        else:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("加入HK Duker", url="https://t.me/hkduker")]])
            update.message.reply_text("呢個指令只可以喺HK Duker用到，歡迎撳下面個掣入嚟HK Duker一齊tag死JS。",
                                      reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_text(e)


@run_async
def tag9(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if update.effective_user.id == 463998526 or (update.effective_user.id == 190726372 and
                                                     update.message.chat_id == -1001295361187):
            if update.message.chat_id > 0:
                update.message.reply_text("PM點tag9人姐？")
                return
            if update.message.reply_to_message:
                try:
                    if update.message.reply_to_message.from_user.id == 463998526:
                        update.message.reply_text("收皮啦tag我主人，唔幫你。")
                        return
                    if update.message.reply_to_message.from_user.id <= 0:
                        update.message.reply_text("唔知user id係咩就死開。Zzz...")
                        return
                    if update.message.reply_to_message.from_user.is_bot:
                        update.message.reply_text("Tag乜撚bot啊？")
                        return
                    user_info = bot.get_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
                    if user_info.user.username and user_info.status in ("administrator", "creator", "member"):
                        update.message.reply_markdown("限時十五秒，唔好tag得太過分。",
                                                      reply_markup=ReplyKeyboardMarkup([[user_info.user.name]]))
                        sleep(15)
                        update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
                    elif user_info.status in ("administrator", "creator", "member"):
                        update.message.reply_markdown("Tag唔到，佢無username。我tag一下lor。"
                                                      "[柒頭](tg://user?id={})。".format(user_info.user.id))
                    else:
                        raise BadRequest("¯\_(ツ)_/¯")
                except BadRequest:
                    update.message.reply_text("乜呢個群組有呢個人咩？定Telegram入面根本無呢個人？定係啲數字亂打嘅？Zzz...")
            else:
                try:
                    args = " ".join(args)
                    if args == "":
                        raise ValueError("¯\_(ツ)_/¯")
                    args = int(args)
                    if args == 463998526:
                        update.message.reply_text("收皮啦tag我主人，唔幫你。")
                        return
                    if args <= 0:
                        update.message.reply_text("唔知user id係咩就死開。Zzz...")
                        return
                except ValueError:
                    update.message.reply_text("打錯嘢喎。咁用先啱： /tag9 <user id>。 唔知user id係咩就死開。Zzz...")
                    return
                try:
                    user_info = bot.get_chat_member(update.message.chat_id, args)
                    if user_info.user.is_bot:
                        update.message.reply_text("Tag乜撚bot啊？")
                        return
                    if user_info.user.username and user_info.status in ("administrator", "creator", "member"):
                        update.message.reply_markdown("限時十五秒，唔好tag得太過分。",
                                                      reply_markup=ReplyKeyboardMarkup([[user_info.user.name]]))
                        sleep(15)
                        update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
                    elif user_info.status in ("administrator", "creator", "member"):
                        update.message.reply_markdown("Tag唔到，佢無username。我tag一下lor。"
                                                      "[柒頭](tg://user?id={})。".format(user_info.user.id))
                    else:
                        raise BadRequest("¯\_(ツ)_/¯")
                except BadRequest:
                    update.message.reply_text("乜呢個群組有呢個人咩？定Telegram入面根本無呢個人？定係啲數字亂打嘅？Zzz...")
        else:
            update.message.reply_text("唔好亂用Trainer Jono嘅指令，乖。")
    except Exception as e:
        update.message.reply_text(e)


# Ah, how boring it is after writing such a damn large function. raise BoredError("¯\_(ツ)_/¯")
# I wouldn't mind some drawings here, you know.
#   ____                       ____
#  |    \                     |    \                    |
#  |     \ ____ _____ ____    |     \ ____ ____ .  ____ |
#  |     | |  | | | | |  |    |     | |  | |  | | |___| |
#  |_____/ \_/\ | | | |  |    |_____/ \_/\ |  | | |___  |
#
#  _____ ____    ____
#    |  |       |                 |  /
#    |  |____   |____         ___ |/   ____
#    |      |       | |   |  |    |\  |____
# |__|  ____|   ____| |___|\ |___ | \ ____|


def remove_keyboard(bot, update):
    try:
        if update.message.chat_id < 0:
            update.message.reply_text("我已經整走咗個鍵盤啦（如有）。", reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text("我唔會整鍵盤比你撳，移乜除姐。")
    except Exception as e:
        update.message.reply_text(e)


# YOU ARE ADVISED TO IGNORE THE FOLLOWING OFFENSIVE WORDS.
# THESE WORDS ARE ONLY FOR DETECTING OFFENSIVE WORDS IN TELEGRAM MESSAGES
# AND NOT INSULTING USERS OR OTHER PEOPLE.


cn_swear_words = ("屌", "閪", "柒", "撚", "鳩", "𨳒", "屄", "𨶙", "𨳊", "㞗", "𨳍", "杘")
cn_swear_words_in_eng = ("diu", "dllm", "dnlm", "diuneinomo", "diuneilomo")
eng_swear_words = ("anus", "arse", "ass", "axwound", "bampot", "bastard", "beaner", "bitch", "blowjob", "bollocks",
                   "bollox", "boner", "butt", "camaltoe", "carpetmuncher", "chesticle", "chinc", "chink", "choad",
                   "chode", "clit", "cock", "coochie", "choochy", "coon", "cooter", "cracker", "cum", "cunnie",
                   "cunnilingus", "cunt", "dago", "damn", "deggo", "dick", "dike", "dildo", "doochbag", "dookie",
                   "douche", "dumb", "dyke", "fag", "fellatio", "feltch", "flamer", "fuck", "fidgepacker", "gay",
                   "goddamn", "goddamnit", "gooch", "gook", "gringo", "guido", "handjob", "hardon", "heeb", "hell",
                   "hoe", "homo", "honkey", "humping", "jagoff", "jap", "jerk", "jigaboo", "jizz", "junglebunny",
                   "kike", "kooch", "kootch", "kraut", "kunt", "kyke", "lesbian", "lesbo", "lezzie", "mick", "minge",
                   "muff", "munging", "negro", "nigaboo", "nigga", "nigger", "niglet", "nutsack", "paki", "panooch",
                   "pecker", "penis", "piss", "polesmoker", "pollock", "poon", "porchmonkey", "prick", "punanny",
                   "punta", "pussy", "pussies", "puto", "queef", "queer", "renob", "rimjob", "ruski", "schlong",
                   "scrote", "shit", "shiz", "skank", "skeet", "slut", "smeg", "snatch", "spic", "splooge", "spook",
                   "tard", "thot", "testicle", "tit", "twat", "vajj", "vag", "vajayjay", "vjayjay", "wank", "wetback",
                   "whore", "wop", "wtf", "fk", "asshole", "bullshit", "shitty", "asshole")


def cn_swear_word_detector():
    for cn_swear_word in cn_swear_words:
        if cn_swear_word in t:
            return True


def cn_swear_word_in_eng_detector():
    for cn_swear_word_in_eng in cn_swear_words_in_eng:
        for word in t:
            if word == cn_swear_word_in_eng:
                return True


def eng_swear_word_detector():
    for eng_swear_word in eng_swear_words:
        for word in t:
            if word == eng_swear_word:
                return True


def swear_word_detector(bot, update):
    try:
        global t
        t = update.message.text
        if cn_swear_word_detector():
            if update.message.chat_id < 0:
                update.message.reply_text("豈有此理，講粗口？！我最撚憎人講粗口，記你一次大過！")
                return
            else:
                update.message.reply_text("PM講粗口姐，我先懶得理你。Zzz...")
                return
        t = t.lower().split(" ")
        if cn_swear_word_in_eng_detector():
            if update.message.chat_id < 0:
                update.message.reply_text("廣東話粗口嘅英文縮寫我睇得明㗎，柒頭。我最撚憎人講粗口，記你一次大過！")
            else:
                update.message.reply_text("PM講粗口姐，我先懶得理你。Zzz...")
        elif eng_swear_word_detector():
            if update.message.chat_id < 0:
                update.message.reply_text("英文粗口我都明㗎，柒頭。我最撚憎人講粗口，記你一次大過！")
            else:
                update.message.reply_text("It's pm, I don't care if you swear, zzz.")
        else:
            return
    except Exception as e:
        update.message.reply_text(e)


def text_responses(bot, update):
    try:
        if update.message.new_chat_members:
            for on9user in update.message.new_chat_members:
                if on9user.id == 506548905:
                    update.message.reply_text("嘩，邊撚到嚟㗎？")
                    update.message.reply_text("大家好，我係全Telegram最On9嘅bot。用 /help 睇點用。")
                elif match(r'\d\d\d\d\d\d\d\d', on9user.first_name):
                    if match(r'\d\d\d\d\d\d\d\d', on9user.last_name):
                        update.message.reply_text("又係數字人？我屌！我ban 9數字人啦。")
                        bot.kick_chat_member(update.message.chat_id, on9user.id)
                elif on9user.is_bot:
                    update.message.reply_text("Zzz...哦？第個bot喎，乜水？")
                else:
                    update.message.reply_text("你好啊{}！歡迎嚟到{}陪我地一齊柒！".format(on9user.full_name,
                                                                           update.effective_chat.title))
            return
        elif update.message.left_chat_member:
            update.message.reply_text(update.message.left_chat_member.full_name + "離開左群組。")
            return
        y = update.message.from_user
        if match(r'\d\d\d\d\d\d\d\d', y.first_name):
            if match(r'\d\d\d\d\d\d\d\d', y.last_name):
                update.message.reply_text("又係數字人？我屌！我ban 9數字人啦。", quote=False)
                update.message.delete()
                bot.kick_chat_member(update.message.chat_id, update.message.from_user.id)
                return
        if update.message.pinned_message:
            if update.message.from_user.id == 463998526:
                update.message.reply_text("Trainer Jono pin嘢啊，係咪有人有意見？")
            else:
                update.message.reply_text("屌你老母咩 " + update.message.from_user.name + " ，pin嘢嘈醒全谷人。")
        if update.message.sticker:
            if update.message.sticker.set_name == "payize2" or update.message.sticker.set_name == "FPbabydukeredition":
                update.message.reply_text("屌你老母，Send乜撚bb啊，阻住個地球轉。")
        u = update.message.text.lower()
        if update.effective_user.id == 463998526:
            if u == "hello":
                update.message.reply_text("主人你好！")
            if u == "good dog":
                update.message.reply_text("屌你老母")
        if update.effective_user.id != 463998526 and update.effective_chat.type in ("group", "supergroup") and "@trainer_jono" in u:
            update.message.reply_text("Tag我主人jm9？")
        if "trainer jono is rubbish" in u:
            update.message.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg",
                                       caption="車娜 Jono is a wubbish. Tot肚ly wubbish. Dammit.")
        if "cough" in u:
            update.message.reply_text("Do you need some cough medicine?")
        if u == "js is very on9":
            update.message.reply_text("Your IQ is 500")
    except Exception as e:
        update.message.reply_text(e)


def echo(bot, update, args):
    args = " ".join(args)
    if update.message.reply_to_message:
        try:
            if args == "":
                if update.message.reply_to_message.text:
                    update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                              quote=False)
                    update.message.delete()
                    return
                else:
                    raise ValueError("¯\_(ツ)_/¯")
            else:
                update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
                update.message.delete()
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
        except BadRequest:
            update.message.reply_text("Markdown都唔識用？！睇左 /help 未？")
        except Exception as e:
            update.message.reply_text(e)
    else:
        try:
            if args == "":
                raise ValueError("¯\_(ツ)_/¯")
            update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
            update.message.delete()
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
        except Exception as e:
            update.message.reply_text(e)


def echo3(bot, update, args):
    args = " ".join(args)
    if update.message.reply_to_message:
        try:
            if args == "":
                if update.message.text:
                    for i in range(0, 3):
                        update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                              quote=False)
                    return
                else:
                    raise ValueError
            else:
                for i in range(0, 3):
                    update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
        except Exception as e:
            update.message.reply_text(e)
    else:
        try:
            if args == "":
                raise ValueError("¯\_(ツ)_/¯")
            for i in range(0, 3):
                update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
        except Exception as e:
            update.message.reply_text(e)


def get_id(bot, update):
    try:
        if update.message.reply_to_message:
            update.message.reply_markdown("佢嘅user id: ```{}```".format(update.message.reply_to_message.from_user.id))
        else:
            update.message.reply_markdown("呢個對話嘅chat id: ```{}```\n你嘅user id: ```{}```"
                                          .format(update.message.chat_id, update.effective_user.id))
    except Exception as e:
        update.message.reply_text(e)


def get_message_link(bot, update):
    try:
        if update.message.reply_to_message:
            group_info = bot.get_chat(update.message.chat_id)
            if group_info.type == "supergroup":
                if group_info.username:
                    update.message.reply_text("t.me/{}/{}".format(group_info.username,
                                                                  update.message.reply_to_message.message_id))
                else:
                    update.message.reply_text("Public supergroup先用得架柒頭。")
            else:
                update.message.reply_text("Public supergroup先用得架柒頭。")
        else:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
    except Exception as e:
        update.message.reply_text(e)


def get_audio_id(bot, update):
    try:
        if update.message.reply_to_message:
            if update.message.reply_to_message.audio:
                update.message.reply_markdown("File id for this audio file: ```{}```"
                                              .format(update.message.reply_to_message.audio.file_id))
            else:
                update.message.reply_text("唔係audio file(.mp3)就收皮啦。")
        else:
            update.message.reply_text("覆住個audio file(.mp3)嚟用啦大佬。")
    except Exception as e:
        update.message.reply_text(e)


def get_voice_id(bot, update):
    try:
        if update.message.reply_to_message:
            if update.message.reply_to_message.voice:
                update.message.reply_markdown("File id for this voice file: ```{}```"
                                              .format(update.message.reply_to_message.voice.file_id))
            else:
                update.message.reply_text("唔係voice file(.ogg)就收皮啦。")
        else:
            update.message.reply_text("覆住個voice file(.ogg)嚟用啦大佬。")
    except Exception as e:
        update.message.reply_text(e)


def ping(bot, update):
    try:
        update.message.reply_text("收到要屌你老母需時: 00:00.01\n999 MAX IN | 1 MAX OUT\n屌你老母需時︰00:00.01\n\n"
                                  "Sorry this took long to send but Telegram said I was too popular and wouldn't let me "
                                  "send messages for a bit...")
    except Exception as e:
        update.message.reply_text(e)


def poto(bot, update):
    try:
        update.message.reply_audio("CQADBQADOAADYv7JVYZTkCHv01_4Ag")
    except Exception as e:
        update.message.reply_text(e)


def beefball_christ(bot, update):
    try:
        update.message.reply_audio("CQADBQADHgADkXfRVcsnDoGOjnChAg")
    except Exception as e:
        update.message.reply_text(e)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    token = "506548905:AAFCkZ5SI9INLEb0fwRHRlEji4Or6s8B9DQ"
    name = "on9bot"
    port = os.environ.get('PORT')
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("tag9js", tag9js))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CommandHandler("link", get_message_link))
    dp.add_handler(CommandHandler("audio_id", get_audio_id))
    dp.add_handler(CommandHandler("voice_id", get_voice_id))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("x", poto))
    dp.add_handler(CommandHandler("y", beefball_christ))
    dp.add_handler(CommandHandler("tag9", tag9, pass_args=True))
    dp.add_handler(CommandHandler("r", echo, pass_args=True))
    dp.add_handler(CommandHandler("r3", echo3, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, swear_word_detector))
    dp.add_handler(MessageHandler(Filters.all, text_responses), group=1)
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=token, clean=True)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(name, token))
    updater.idle()


if __name__ == "__main__":
    main()
