from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
import string

# Функция для номера телефона
def generate_random_phone_number():
    return "+79" + ''.join(random.choices(string.digits, k=9))

# Функция для почты с доменами Gmail и Mail.ru
def generate_random_email():
    email_domains = ["gmail.com", "mail.ru"]
    email_domain = random.choice(email_domains)
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + "@" + email_domain

# Функция для ФИО
def generate_random_name():
    first_names = ["Иван", "Алексей", "Максим", "Сергей", "Дмитрий", "Андрей","Вячеслав","Павел","Антон","Александр"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов","Акулов"]
    middle_names = ["Иванович", "Петрович", "Сидорович", "Кузнецович", "Смирнович","Вячеславович","Александрович","Павлович"]
    return f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(middle_names)}"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Это телеграм бот для пробива! После оплаты счета http://t.me/send?start=IVTokL9pnni5 вам выдадут команду, которая запустит пробив"
    )

# Команда /profile
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Подписка активна! Команды:\n/dnn для поиска по Telegram\n/dnn_num для поиска по номеру"
    )

# Команда /dnn
async def dnn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите имя пользователя (@ обязательно)"
    )
    context.user_data['awaiting_username'] = True

# Команда /dnn_num
async def dnn_num(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите номер (+7 или +375)"
    )
    context.user_data['awaiting_phone_number'] = True

# Обработка сообщения
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('awaiting_username', False):
        username = update.message.text
        if username.startswith('@'):
            random_phone_number = generate_random_phone_number()
            random_email = generate_random_email()
            random_name = generate_random_name()
            await update.message.reply_text(
                f"Вот номер телефона: {random_phone_number}\n"
                f"Вот почта: {random_email}\n"
                f"Вот ФИО: {random_name}"
            )
            context.user_data['awaiting_username'] = False
        else:
            await update.message.reply_text("Имя пользователя должно начинаться с @!")
    
    elif context.user_data.get('awaiting_phone_number', False):
        phone_number = update.message.text
        if phone_number.startswith('+7') or phone_number.startswith('+375'):
            random_email = generate_random_email()
            random_name = generate_random_name()
            await update.message.reply_text(
                f"Вот почта: {random_email}\n"
                f"Вот ФИО: {random_name}"
            )
            context.user_data['awaiting_phone_number'] = False
        else:
            await update.message.reply_text("Номер телефона должен начинаться с +7 или +375!")

# Основная функция
def main():
    application = Application.builder().token('7404642861:AAHIoI7SGQpzMrOPlUSE3gUAhf5xGCvD9VQ').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("dnn", dnn))
    application.add_handler(CommandHandler("dnn_num", dnn_num))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()