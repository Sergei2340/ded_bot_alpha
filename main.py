from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

import config

openai.api_key = config.OPENAI_API_KEY


def generate_story():
    character = "пожилой мужчина"

    prompt = f"{character} рассказывает:"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=4097 - len(prompt) - 5,
        temperature=0.7,
        n=1,
        stop=None,
    )

    story = response.choices[0].text.strip()
    return story


async def generate_and_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    story = generate_story()
    await update.message.reply_text(story)


app = ApplicationBuilder().token(config.TG_TOKEN).build()

app.add_handler(CommandHandler("hello", generate_and_reply))

app.run_polling()
