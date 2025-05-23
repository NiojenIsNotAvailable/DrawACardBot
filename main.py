from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random
import os
TOKEN = os.getenv("TOKEN")

BOT_USERNAME: Final = '@DrawACardBot'

# Статична повна колода
suits = {
    'Hearts': '♥️',
    'Diamonds': '♦️',
    'Spades': '♠️',
    'Clubs': '♣️'
}
ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
FULL_DECK = [f'{rank} {suits[suit]}' for suit in suits for rank in ranks] + ['Joker (Red)', 'Joker (Black)']

# Змінна активної колоди
active_deck = []

# /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Мяв")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Мурмявмурміумяв:\n/battle — почати бій\n/draw — витягнути карту\n/end — завершити бій")

# /battle
async def battle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_deck
    active_deck = FULL_DECK.copy()
    random.shuffle(active_deck)
    await update.message.reply_text("FIGHT! (Колода готова 🃏)")

# /draw
async def draw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_deck

    if not active_deck:
        await update.message.reply_text("Бій не почався. Юз /battle")
        return

    drawn_card = active_deck.pop()
    user_name = update.message.from_user.username
    await update.message.reply_text(f'@{user_name} витягує карту: {drawn_card}')

    if 'Joker' in drawn_card:
        active_deck = FULL_DECK.copy()
        random.shuffle(active_deck)
        await update.message.reply_text("🎉 ДЖОКЕР ХЕЛЛЙЕААХХ! +1 бенні, і +2 до всіх кидків (Колода відновлена).")

# /end
async def end_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global active_deck
    active_deck = []
    await update.message.reply_text("Бій завершено. Колода очищена.")

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}') 

# main
if __name__ == '__main__':
    print("Starting...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('battle', battle_command))
    app.add_handler(CommandHandler('draw', draw_command))
    app.add_handler(CommandHandler('end', end_command))

    app.add_error_handler(error)
    print("Polling...")
    app.run_polling(poll_interval=3)
