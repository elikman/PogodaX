import os
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

load_dotenv()

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not BOT_TOKEN or not WEATHER_API_KEY:
    logger.error("Необходимые токены не найдены в переменных окружения!")
    exit(1)

def get_weather(city: str) -> str:
    """Получение данных о погоде"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        
        return (
            f"🌍 Погода в городе {data['name']}:\n"
            f"🌡 Температура: {main['temp']}°C\n"
            f"🤔 Ощущается как: {main['feels_like']}°C\n"
            f"💧 Влажность: {main['humidity']}%\n"
            f"☁️ {weather['description'].capitalize()}"
        )
    
    except requests.Timeout:
        return "⚠️ Превышено время ожидания ответа от сервера погоды"
    except requests.RequestException as e:
        logger.error(f"Weather API error: {e}")
        return "❌ Ошибка при получении данных о погоде"
    except KeyError as e:
        logger.error(f"Error parsing weather data: {e}")
        return "❌ Ошибка при обработке данных о погоде"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот погоды.\n\n"
        "Просто напишите название города, и я покажу погоду!\n"
        "Например: Москва, Париж, Лондон"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        "🔍 Как пользоваться ботом:\n\n"
        "• Просто напишите название города\n"
        "• Или используйте команду /weather город\n\n"
        "📝 Примеры:\n"
        "• Москва\n"
        "• /weather Париж"
    )

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /weather"""
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите город после команды /weather")
        return

    city = ' '.join(context.args)
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    weather_info = get_weather(update.message.text)
    await update.message.reply_text(weather_info)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and hasattr(update, 'effective_message'):
        await update.effective_message.reply_text(
            "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."
        )

def main() -> None:
    """Основная функция"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("weather", weather_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        application.add_error_handler(error_handler)

        logger.info("Bot started")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == '__main__':
    main()