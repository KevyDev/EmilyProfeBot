import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, constants
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
# from dotenv import load_dotenv

async def start(update, context):
    await update.message.reply_text(
        text=f"¡Hola, {update.effective_user.first_name}! 👋 Mi nombre es Emily y soy profesora de Español. Podría ayudarte a mejorar tus redacciones. ¡Más te vale tener buena ortografía! 😤",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💻 Desarrollado por KevyDev", url="https://kevydev.github.io/portfolio/")],])
    )
    await update.message.reply_text("Dale, envíame un texto y te lo corrijo. Aprovecha que por ahora es gratis je, je, je. 😼")

async def review(update, context):
    text = update.message.text
    data = {"language": "es", "text": text}
    response = requests.post("https://api.languagetoolplus.com/v2/check", data=data)
    if response.status_code == 200:
        matches = response.json()["matches"]
        i = 1
        indications = "No se encontró ningún error. ¡Muy bien! 😋"
        if len(matches) > 0:
            indications = f'¡Se ha encontrado un posible error! 😡\n\n' if len(matches) == 1 else f'¡Se han encontrado {len(matches)} posibles errores! 😡😡😡\n\n'
            for match in matches:
                if i > 1:
                    indications += "\n\n---------------------------------------------\n\n"
                indications += f'*{i}. {match["message"]}*\n\n_{match["sentence"]}_'
                if len(match["replacements"]) > 0:
                    indications += "\n\nAlternativas:"
                    for replacement in match["replacements"]:
                        indications += f'\n*{replacement["value"]}*'
                i += 1
        await update.message.reply_text(
            text=indications,
            reply_to_message_id=update.message.message_id,
            parse_mode=constants.ParseMode.MARKDOWN
        )
    else:
        await update.message.reply_text(
            text="Tuve un problema revisando el texto. Vuelve a enviarlo en otra ocasión. 😕",
            reply_to_message_id=update.message.message_id
        )

def main():
    # load_dotenv()
    app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, review))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()