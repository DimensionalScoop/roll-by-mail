from telegram import Bot
from telegram.ext import CommandHandler, ContextTypes, ApplicationBuilder
import logging

import parser
import fun

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

token_file = "token"
with open(token_file) as f:
    token = f.readline().replace("\n", "")
app = ApplicationBuilder().token(token).build()

async def start(update, context):
    await help(update, context)


async def hey(update, context):
    await update.message.reply_text("Heyya!!")


async def roll_dice(update, context):
    args = " ".join(context.args)
    answer = parser.handle_dice_command(args)
    await update.message.reply_markdown(answer)


async def roll_single_die(update, context):
    args = "d"+" ".join(context.args)
    answer = parser.handle_dice_command(args)
    await update.message.reply_markdown(answer)


async def roll_fate(update, context):
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
    await update.message.reply_markdown(answer)


async def roll_dsa(update, context):
    args = " ".join(context.args)
    answer = parser.handle_dice_command("dsa " + args)
    await update.message.reply_markdown(answer)


async def help(update, context):
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

    await update.message.reply_markdown(answer)


start_handler = CommandHandler("start", start)
app.add_handler(start_handler)
app.add_handler(CommandHandler("hey", hey))
app.add_handler(CommandHandler("roll", roll_dice))
app.add_handler(CommandHandler("r", roll_dice))
app.add_handler(CommandHandler("d", roll_single_die))
app.add_handler(CommandHandler("dsa", roll_dsa))
app.add_handler(CommandHandler("fate", roll_fate))
app.add_handler(CommandHandler("dF", roll_fate))
app.add_handler(CommandHandler("df", roll_fate))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("give_me_the_math", fun.give_me_the_math))

app.run_polling()
print("Started.")
