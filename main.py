from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
import random
import os

# Токен з .env або середовища
TOKEN = os.getenv("TOKEN")
BOT_USERNAME: Final = '@DrawACardBot'

# Дозволені команди
ALLOWED_COMMANDS = {'start', 'help', 'battle', 'draw', 'end'}

# Колода
suits = {
    'Hearts': '♥️',
    'Diamonds': '♦️',
    'Spades': '♠️',
    'Clubs': '♣️'
}
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
FULL_DECK = [f'{rank} {suits[suit]}' for suit in suits for rank in ranks] + ['Joker (Red)', 'Joker (Black)']
active_deck = []

# Перевірка, чи команда наша
def is_our_command(update: Update) -> str | None:
    text = update.message.text or ""
    if not text.startswith('/'):
        return None
    parts = text[1:].split('@')
    command = parts[0].split()[0]

    if command not in ALLOWED_COMMANDS:
        return None

    if len(parts) == 2 and parts[1].lower() != BOT_USERNAME[1:].lower():
        return None

    return command

# Командні функції
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Мяв")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Мурмявмурміумяв:\n"
        "/battle — почати бій\n"
        "/draw — витягнути карту\n"
        "/end — завершити бій"
    )

async def battle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_deck
    active_deck = FULL_DECK.copy()
    random.shuffle(active_deck)
    await update.message.reply_text("FIGHT! (Колода готова 🃏)")

async def draw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_deck

    if not active_deck:
        await update.message.reply_text("Бій не почався. Юз /battle")
        return

    drawn_card = active_deck.pop()
    user_name = update.message.from_user.username or "Гравець"
    await update.message.reply_text(f'@{user_name} витягує карту: {drawn_card}')

    if 'Joker' in drawn_card:
        active_deck = FULL_DECK.copy()
        random.shuffle(active_deck)
        await update.message.reply_text("🎉 ДЖОКЕР ХЕЛЛЙЕААХХ! +1 бенні, і +2 до всіх кидків (Колода відновлена).")

async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_deck
    active_deck = []
    await update.message.reply_text("Бій завершено. Колода очищена.")

# Основний хендлер усіх текстових команд
async def handle_text_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = is_our_command(update)
    if not command:
        return  # чужа команда або неприпустима — ігнор

    if command == "start":
        await start_command(update, context)
    elif command == "help":
        await help_command(update, context)
    elif command == "battle":
        await battle_command(update, context)
    elif command == "draw":
        await draw_command(update, context)
    elif command == "end":
        await end_command(update, context)

# Обробка помилок
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Запуск
if __name__ == '__main__':
    print("Starting...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/'), handle_text_command))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
