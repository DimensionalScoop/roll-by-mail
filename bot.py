import telegram.ext as tele
from telegram.ext import CommandHandler
import telegram
import logging
import time

import parser
import fun

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

token_file = "token"
with open(token_file) as f:
    token = f.readline().replace("\n", "")
updater = tele.Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def hey(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Heyya!!")


def roll_dice(update, context):
    chat_id = update.effective_chat.id
    args = " ".join(context.args)
    answer = parser.handle_dice_command(args)
    context.bot.send_message(chat_id=chat_id, text=answer,parse_mode="MARKDOWN")


def roll_single_die(update, context):
    chat_id = update.effective_chat.id
    args = "d"+" ".join(context.args)
    answer = parser.handle_dice_command(args)
    context.bot.send_message(chat_id=chat_id, text=answer,parse_mode="MARKDOWN")


def roll_fate(update, context):
    chat_id = update.effective_chat.id
    args = " ".join(context.args)

    complete_args = "dF "
    try:
        args = int(args)
        if args < 0:
            complete_args += str(args)
        else:
            complete_args += "+" + str(args)
    except ValueError:
        complete_args += args
    answer = parser.handle_dice_command(complete_args)
    context.bot.send_message(chat_id=chat_id, text=answer,parse_mode="MARKDOWN")


def roll_dsa(update, context):
    chat_id = update.effective_chat.id
    args = " ".join(context.args)
    answer = parser.handle_dice_command("dsa " + args)
    context.bot.send_message(chat_id=chat_id, text=answer,parse_mode="MARKDOWN")


def help(update, context):
    chat_id = update.effective_chat.id

    answer = """
A dice rolling bot by @elayn
------------------------------------
`/roll`, `/r`
roll dice
E.g.: `/r 2d20+3` rolls two d20 and adds three

`/d`
roll a single die
E.g.: `/d 10` rolls a d10

`/dsa`, `/r dsa`
roll a DSA check
E.g.: `/dsa` rolls `3d20`

`/fate`, `/dF`, `/r dF`
roll a Fate check
E.g.: `/fate +2` rolls four fudge dice and adds two
    """

    context.bot.send_message(chat_id=chat_id, text=answer,parse_mode="MARKDOWN")


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CommandHandler("hey", hey))
dispatcher.add_handler(CommandHandler("roll", roll_dice))
dispatcher.add_handler(CommandHandler("r", roll_dice))
dispatcher.add_handler(CommandHandler("d", roll_single_die))
dispatcher.add_handler(CommandHandler("dsa", roll_dsa))
dispatcher.add_handler(CommandHandler("fate", roll_fate))
dispatcher.add_handler(CommandHandler("dF", roll_fate))
dispatcher.add_handler(CommandHandler("df", roll_fate))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(CommandHandler("give_me_the_math", fun.give_me_the_math))

updater.start_polling()
print("Started.")

while True:
    time.sleep(1)
