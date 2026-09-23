import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    LabeledPrice,
    PreCheckoutQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# ГЛАВНАЯ КЛАВИАТУРА
# =========================

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 Магазин"),
            KeyboardButton(text="🆓 Бесплатный проект"),
        ],
        [
            KeyboardButton(text="🔨 Собрать проект"),
            KeyboardButton(text="📦 Мои проекты"),
        ],
        [
            KeyboardButton(text="🆘 Поддержка"),
            KeyboardButton(text="🛠 Инструменты"),
        ],
        [
            KeyboardButton(text="🤝 Партнерка"),
        ],
    ],
    resize_keyboard=True
)


# =========================
# /START
# =========================

@dp.message(CommandStart())
async def start(message: Message):
    name = message.from_user.first_name or "клиент"

    text = (
        f"🙂 {name}, привет!\n\n"
        "Собираю готовый мобильный проект Black Russia под твой сервер: "
        "своё название, свои цвета, своя иконка, свой APK.\n\n"
        "💸 От 399 ₽   🕓 Сборка ~10 минут   ✅ Всё автоматически\n\n"
        "Мод, база данных и приложение ставятся на твой сервер без тебя — "
        "нужно только ответить на вопросы бота.\n\n"
        "Выбери раздел в меню под строкой ввода."
    )

    await message.answer(text, reply_markup=main_keyboard)


# =========================
# МАГАЗИН
# =========================

@dp.message(F.text == "🛒 Магазин")
async def shop(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 BLACK RUSSIA PRO",
                    callback_data="br_pro"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢 Реклама",
                    callback_data="advertising"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="main_menu"
                )
            ],
        ]
    )

    text = (
        "🪙 МАГАЗИН LILHEAD\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Готовый проект Black Russia под твой сервер: "
        "своё название, свои цвета, своя иконка, свой APK.\n\n"
        "Мод, база и приложение ставятся на сервер сами — "
        "ты только отвечаешь на вопросы бота. "
        "Сборка занимает ~10 минут.\n\n"
        "🔓 Оплата — ₽ или Telegram Stars. "
        "Доступ открывается сразу после оплаты."
    )

    await message.answer(text, reply_markup=keyboard)


# =========================
# BLACK RUSSIA PRO
# =========================

@dp.callback_query(F.data == "br_pro")
async def black_russia_pro(callback):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Оплатить 399 ₽",
                    url="https://t.me/liIhead"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌟 Telegram Stars 320",
                    callback_data="stars_info"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="main_menu"
                )
            ],
        ]
    )

    text = (
        "📦 BLACK RUSSIA PRO\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "399 ₽   ⭐️ 320   🕓 сборка ~10 минут\n\n"
        "Готовый мод с упором на тюнинг и визуал. "
        "Ставится на твой сервер целиком: мод, база данных и приложение.\n\n"
        "Что внутри\n"
        "• Стайлинг, тех-центр и шиномонтаж — тюнинг сохраняется\n"
        "• Радиальное меню, GPS-метки и зелёные зоны как в Black Russia\n"
        "• Кейсы, ревард-система, автосалоны с выбором цвета\n"
        "• Донат и инвентарь работают полностью\n\n"
        "Проект остаётся твоим\n"
        "• Название, цвета, иконка и ID приложения — под тебя\n"
        "• APK не конфликтует с другими проектами на телефоне игрока\n"
        "• Авторство полностью твоё\n"
        "• Выйдет обновление мода — обновлю твою копию бесплатно\n\n"
        "🔓 Доступ откроется сразу после оплаты."
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )

    await callback.answer()


# =========================
# STARS
# =========================

@dp.callback_query(F.data == "stars_info")
async def stars_info(callback):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌟 Заплатить 320 ⭐",
                    callback_data="pay_stars"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="br_pro"
                )
            ]
        ]
    )

    text = (
        "🌟 ОПЛАТА TELEGRAM STARS\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Доработанный мод BLACK RUSSIA PRO "
        "с уклоном в тюнинг и визуал, "
        "полной кастомизацией и готовностью к запуску.\n\n"
        "Стоимость: ⭐️ 320 Stars\n\n"
        "После нажатия кнопки Telegram откроет "
        "официальную форму оплаты."
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard
    )

    await callback.answer()


# =========================
# СОЗДАНИЕ INVOICE
# =========================

@dp.callback_query(F.data == "pay_stars")
async def pay_stars(callback):

    prices = [
        LabeledPrice(
            label="BLACK RUSSIA PRO",
            amount=320
        )
    ]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title="BLACK RUSSIA PRO",
        description=(
            "Доработанный мод BLACK RUSSIA PRO "
            "с кастомизацией и готовностью к запуску."
        ),
        payload=f"black_russia_pro:{callback.from_user.id}",
        currency="XTR",
        prices=prices,
        provider_token=""
    )

    await callback.answer()


# =========================
# PRE-CHECKOUT
# =========================

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):

    await query.answer(ok=True)


# =========================
# УСПЕШНАЯ ОПЛАТА
# =========================

@dp.message(F.successful_payment)
async def successful_payment(message: Message):

    payment = message.successful_payment

    await message.answer(
        "✅ ОПЛАТА УСПЕШНА!\n\n"
        "Спасибо за покупку BLACK RUSSIA PRO.\n\n"
        f"🧾 ID платежа:\n"
        f"{payment.telegram_payment_charge_id}\n\n"
        "📦 Покупка зарегистрирована.\n"
        "🔨 Следующий этап — настройка проекта и сборка.\n\n"
        "Мы продолжим автоматически."
    )


# =========================
# БЕСПЛАТНЫЙ ПРОЕКТ
# =========================

@dp.message(F.text == "🆓 Бесплатный проект")
async def free_project(message: Message):

    await message.answer(
        "🆓 БЕСПЛАТНЫЙ ПРОЕКТ\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Здесь будут доступны бесплатные проекты."
    )


# =========================
# СОБРАТЬ ПРОЕКТ
# =========================

@dp.message(F.text == "🔨 Собрать проект")
async def build_project(message: Message):

    await message.answer(
        "🔨 СОБРАТЬ ПРОЕКТ\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Здесь будет автоматическая сборка проекта.\n\n"
        "Ты отправляешь файлы → бот задаёт вопросы → "
        "собирает проект → выдаёт готовый результат."
    )


# =========================
# МОИ ПРОЕКТЫ
# =========================

@dp.message(F.text == "📦 Мои проекты")
async def my_projects(message: Message):

    await message.answer(
        "📦 МОИ ПРОЕКТЫ\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "У тебя пока нет проектов."
    )


# =========================
# ПОДДЕРЖКА
# =========================

@dp.message(F.text == "🆘 Поддержка")
async def support(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать в поддержку",
                    url="https://t.me/liIhead"
                )
            ]
        ]
    )

    await message.answer(
        "🆘 ПОДДЕРЖКА\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Если у тебя возникли вопросы или проблемы, "
        "напиши в поддержку.",
        reply_markup=keyboard
    )


# =========================
# ИНСТРУМЕНТЫ
# =========================

@dp.message(F.text == "🛠 Инструменты")
async def tools_menu(message: Message):

    await message.answer(
        "🛠 ИНСТРУМЕНТЫ\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Раздел инструментов пока находится в разработке."
    )


# =========================
# ПАРТНЕРКА
# =========================

@dp.message(F.text == "🤝 Партнерка")
async def partner(message: Message):

    await message.answer(
        "🤝 ПАРТНЕРКА\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "Партнёрская программа будет подключена позже."
    )


# =========================
# ГЛАВНОЕ МЕНЮ
# =========================

@dp.callback_query(F.data == "main_menu")
async def main_menu(callback):

    name = callback.from_user.first_name or "клиент"

    text = (
        f"🙂 {name}, привет!\n\n"
        "Собираю готовый мобильный проект Black Russia "
        "под твой сервер: своё название, свои цвета, "
        "своя иконка, свой APK.\n\n"
        "💸 От 399 ₽   🕓 Сборка ~10 минут   ✅ Всё автоматически\n\n"
        "Выбери раздел в меню под строкой ввода."
    )

    await callback.message.delete()

    await callback.message.answer(
        text,
        reply_markup=main_keyboard
    )

    await callback.answer()


# =========================
# ЗАПУСК
# =========================

async def main():
    print("LILHEAD BOT запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
