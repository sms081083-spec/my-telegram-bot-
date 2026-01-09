import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import feedparser  # Для RSS

# Твой токен (не меняй, если работает)
TOKEN = "7877790193:AAEBes5i7UR_dnZAmE9DTiL_yUAuC5dI2aA"

# Твой Telegram ID (узнай с /id, вставь сюда)
USER_ID = 753393124  # ←←← Замени на свой ID!

# Список RSS-фидов по регионам (только с доступными RSS)
RSS_FEEDS = [
    "https://www3.nhk.or.jp/nhkworld/en/news/rss.xml",  # NHK (Япония)
    "https://www.japantimes.co.jp/feed",  # Japan Times (Япония)
    "https://www.stuff.co.nz/rss",  # Stuff (Австралия/Новая Зеландия)
    "https://en.yna.co.kr/rss/news.xml",  # Yonhap (Южная Корея)
    "https://koreajoongangdaily.joins.com/rss",  # Korea JoongAng Daily (Южная Корея)
    "https://chosonsinbo.com/feed",  # Choson Sinbo (Северная Корея)
    "https://www.scmp.com/rss/91/feed",  # SCMP Hong Kong
    "https://hongkongfp.com/feed"  # HKFP (Гонконг)
]

# Расширенные ключевые слова (диаспора + эмиграционная политика)
KEYWORDS = [
    # Диаспора
    "Russian diaspora", "Ukrainian diaspora", "Russian community", "Ukrainian community",
    "русскоязычная диаспора", "украинская диаспора", "Russians in", "Ukrainians in",
    "Russian emigrants", "Ukrainian emigrants", "Russian speakers", "Ukrainian speakers",
    # Эмиграционная политика
    "immigration policy", "emigration policy", "visa changes", "migration laws",
    "refugee policy", "border control", "citizenship reforms", "work permits",
    "эмиграционная политика", "иммиграционная политика", "визовые изменения",
    "миграционные законы", "политика беженцев", "контроль границ", "реформы гражданства"
]

# Интервал проверки (1800 секунд = 30 минут)
INTERVAL = 1800

# Хранилище для последних новостей (чтобы не слать дубликаты)
last_news = set()

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! 👋 Я отслеживаю новости по диаспоре и эмиграционной политике. Напиши /news для проверки, или /id для твоего ID.")

@dp.message(Command("id"))
async def get_id(message: types.Message):
    await message.answer(f"Твой ID: {message.from_user.id} — вставь в код как USER_ID.")

@dp.message(Command("news"))
async def manual_news(message: types.Message):
    await send_news()

async def send_news():
    for rss_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries[:10]:  # Проверяем последние 10 новостей
                title = entry.title
                link = entry.link
                summary = entry.summary if 'summary' in entry else entry.description if 'description' in entry else ""

                # Уникальный ID новости
                news_id = f"{title}-{link}"

                if news_id in last_news:
                    continue  # Уже отправляли

                # Фильтр по ключевым словам
                if any(keyword.lower() in title.lower() or keyword.lower() in summary.lower() for keyword in KEYWORDS):
                    # Создаём TXT-файл
                    content = f"Заголовок: {title}\nСсылка: {link}\nОписание: {summary}"
                    file_name = "news_diaspora_policy.txt"
                    with open(file_name, "w", encoding="utf-8") as f:
                        f.write(content)

                    # Отправляем файл тебе
                    await bot.send_document(USER_ID, types.FSInputFile(file_name))
                    last_news.add(news_id)

        except Exception as e:
            logging.error(f"Ошибка с {rss_url}: {e}")

async def scheduler():
    while True:
        await send_news()
        await asyncio.sleep(INTERVAL)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот запущен и работает!")
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
