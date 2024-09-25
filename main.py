from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import random

TOKEN: Final = '8196092610:AAEXThNcDT2KnxFUiwKR0RXJD7VZGm39CYw'
BOT_USERNAME: Final = '@DrawACardBot'

# Deck of 54 cards including jokers
deck_of_cards = [
    'Ace of Hearts', '2 of Hearts', '3 of Hearts', '4 of Hearts', '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts',
    'Ace of Diamonds', '2 of Diamonds', '3 of Diamonds', '4 of Diamonds', '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', 'King of Diamonds',
    'Ace of Spades', '2 of Spades', '3 of Spades', '4 of Spades', '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades',
    'Ace of Clubs', '2 of Clubs', '3 of Clubs', '4 of Clubs', '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs', 'King of Clubs',
    'Joker (Red)', 'Joker (Black)'
]

# /start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Мяв')

# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Мур')

# /draw command handler
async def draw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.username  # Get user's username
    drawn_card = random.choice(deck_of_cards)  # Randomly select a card from the deck
    response = f'@{user_name} {drawn_card}'  # Format response
    await update.message.reply_text(response)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')              

if __name__ == '__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('draw', draw_command))

    # errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
