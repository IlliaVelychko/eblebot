import random
import logging
from storage import save_stats_decorator, load_stats
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Exception while handling an update: {context.error}")

# Initialize stats from file
stats = load_stats()

yellow_messages = [
    f"Ну все, @{{user}}, жовта в колекцію!",
    f"Думав, не дадуть? Жовта, @{{user}}!",
    f"Вчися відповідати за хуйню, @{{user}}!",
    f"@{{user}}, привітай жовту картку!",
    f"Це твій шлях до бану, @{{user}}!",
    f"Жовта картка і трохи ганьби, @{{user}}!",
    f"Ну це заслужено, @{{user}}. Жовта!",
    f"Йди нахуй з жовтою, @{{user}}!",
    f"Ну це вже край, жовта для тебе, @{{user}}!",
    f"Заслужив жовту, @{{user}}, і отримав!",
    f"Ще одна жовта на твоє ім'я, @{{user}}!",
    f"Не ховайся, жовта знайде, @{{user}}!",
    f"Жовта як символ твоєї тупості, @{{user}}!",
    f"Тримай жовту та подумай, @{{user}}!",
    f"Ось так в нас роблять, жовта для тебе, @{{user}}!",
    f"Це попередження, наступна буде червона, @{{user}}!",
    f"Це було боляче для нас, жовта тобі, @{{user}}!"
    f"Тримай жовту, нахуй, @{{user}}.",
    f"Ну, @{{user}}, за хуйню відповідати треба! Жовта тобі!",
    f"Що, блядь, @{{user}}? Жовта картка на місці!",
    f"Тримай картку, хулі. Їх же не жаліємо, @{{user}}.",
    f"@{{user}}, тепер в тебе є своя жовта хуйня.",
    f"Нахуй думати, якщо можна жовту отримати, так, @{{user}}?",
    f"Ну все, @{{user}}, ще трохи і буде бан, нахуй.",
    f"Піздець. Жовта для @{{user}}.",
    f"Скажемо дружно: 'За хуйню жовта, @{{user}}!'",
    f"Оце так хуйня, @{{user}}. Жовта для тебе!",
    f"Йобаний цирк! Жовта для @{{user}}!",
    f"Жовта на підході, @{{user}}!", 
    f"Думай, а не хуйню верзи, @{{user}}. Тримай жовту!",
    f"За таке треба карати — жовта, @{{user}}!",
    f"Молодець, @{{user}}, але жовта твоя.",
    f"Нахуя це робити? Тримай жовту, @{{user}}!",
    f"Оце так тупняк, @{{user}}. Жовта прийшла!",
    f"Слухай, @{{user}}, від жовтої тобі не сховатись!",
    f"@{{user}}, на тобі жовту за стараність!",
    f"Ну і навіщо це, @{{user}}? Жовта тут!",
    f"Жовта як доля для @{{user}}!",
    f"Ще трохи і червона, @{{user}}!",
    f"Жовта — твій подарунок, @{{user}}!",
    f"Від жовтої ще ніхто не помер, @{{user}}!",
    f"Що за хуйня, @{{user}}? Лови жовту!",
    f"Тримай, @{{user}}. Це заслужено — жовта!",
    f"Це не весело, @{{user}}. Жовта!",
    f"Йди нахуй, але з жовтою, @{{user}}!",
    f"@{{user}}, сам напросився. Жовта!",
    f"Купуй рамку для жовтої, @{{user}}!",
    f"Ганьба, @{{user}}. І жовта картка!",
    f"Лови свій заслужений штраф, @{{user}}!",
    f"Жовта як символ твоєї хуйні, @{{user}}!",
    f"Ну тепер ти точно в історії, @{{user}}. Жовта!",
    f"Тепер ти відомий своїми жовтими, @{{user}}!",
    f"Думай, що робиш, @{{user}}. Жовта!"
]

award_messages = [
    f"Хуяндос, @{{user}}! Грамота заслужена.",
    f"Оце так прорив, @{{user}}. Тримай нагороду!",
    f"Пиздець, @{{user}}, грамота твоя!",
    f"Браво, @{{user}}, всі аплодують!",
    f"@{{user}}, ти офіційно кращий. Грамота!",
    f"Це справжній прорив, @{{user}}, ти легенда!",
    f"@{{user}}, ти підкорив нас. Грамота заслужена!",
    f"Це було піздато, @{{user}}!",
    f"Ну хулі, ти топчик, @{{user}}. Грамота твоя!",
    f"@{{user}}, геній пиздєжа, це твоє визнання!",
    f"Гарна робота, @{{user}}! Грамота вже тут!",
    f"Оце талантище, @{{user}}. Грамота заслужена!",
    f"Йобаний талант, @{{user}}. Грамота в карму!",
    f"@{{user}}, ти легенда. Тримай нагороду!",
    f"Це твій момент, @{{user}}, грамота твоя!",
    f"Твої зусилля заслуговують на це, @{{user}}!",
    f"Тримай грамоту, @{{user}}, це було шикарно!"
    f"Ну тут без варіантів, @{{user}}. Єбать ти молодець, хуяндос!",
    f"@{{user}}, офіційно грамота 'Єбать ти молодець'. Піздатий результат!",
    f"Ну ти красавчик, @{{user}}. Хуй тобі, а не поразка!",
    f"Охуїти, @{{user}}! Грамота заслужена!",
    f"Ну хулі, @{{user}}. Тримай грамоту, бо ти піздатий!",
    f"Ніхуя собі, @{{user}}! Це твоя грамота!",
    f"@{{user}}, ти хуярив як треба. Грамота твоя!",
    f"Єбать ти молодець, @{{user}}. Тримай нагороду, нахуй!",
    f"Шикарно, @{{user}}! Піздато впорався!",
    f"Хуярь далі, @{{user}}! Грамота заслужена!",
    f"@{{user}}, ти топчик. Хуй хто краще зробить!",
    f"Це просто піздато, @{{user}}. Грамота твоя!",
    f"@{{user}}, ти йобнутий геній. Грамота!",
    f"Викатали хуярезультат! Браво, @{{user}}!",
    f"Ну тут без варіантів, @{{user}}. Піздато!",
    f"Хуїти, @{{user}}! Грамота вже в дорозі!",
    f"Ну ти пиздєц крутий, @{{user}}!",
    f"Шедеврально, @{{user}}! Грамота заслужена!",
    f"Йоб твою мать, це топ, @{{user}}!",
    f"@{{user}}, грамота за піздато виконану справу!",
    f"Покажи їм, хто тут бос, @{{user}}!",
    f"Піздатий хід, @{{user}}!",
    f"Ти тепер легенда, @{{user}}!",
    f"Йобаний в рот, @{{user}}, тримай нагороду!",
    f"Ну все, @{{user}}. Грамота тут!",
    f"Заради таких хуярять грамоти!",
    f"Ну це найкраще, @{{user}}!",
    f"Поклонімося генію, @{{user}}!",
    f"Ти топ нахуй, @{{user}}!",
    f"Всі підари заздрять, @{{user}}!",
    f"Ну це пизда, @{{user}}. Грамота!",
    f"Побільше б таких, як ти, @{{user}}!",
    f"Йди нахуй з грамотою, @{{user}}!",
    f"Справжній чемпіон, @{{user}}!"
]

kms_messages = [
    f"Ну шо, @{{user}}, вітаємо! Ти тепер КМС по піздєжу, йобаний підар!",
    f"@{{user}}, тепер ти офіційно піздабол номер один!",
    f"Кандидат у майстри спорту по піздєжу — @{{user}}!",
    f"Шляхетний титул піздєжа вручається тобі, @{{user}}!",
    f"@{{user}}, тебе точно перепиздити ніхто не зможе!",
    f"Твої словесні хуї перемагають всіх, @{{user}}!",
    f"@{{user}}, ти чемпіон по піздабольству, факт!",
    f"Ну ти і піздюх, @{{user}}! Грамота твоя!",
    f"Хуїш, але точно влучно, @{{user}}. КМС!",
    f"Ну все, @{{user}}, тепер офіційно ти головний хуяр!",
    f"@{{user}}, тобі тепер навіть заздрять підари!",
    f"Піздато! @{{user}}, твій талант неперевершений!",
    f"Ти такий піздєц, що аж піздато, @{{user}}!",
    f"Хуяндос, @{{user}}! КМС твій!",
    f"Ну це просто йобаний шедевр, @{{user}}!",
    f"Шлях до словесної хуїти пройдено, @{{user}}. КМС!",
    f"Хуїмба, @{{user}}! Легенда піздєжа!",
    f"Це була йобана магія слів, @{{user}}!",
    f"@{{user}}, тебе навіть хуйні не переможуть!",
    f"Ну ти пизда, @{{user}}. КМС твій!",
    f"Словесна йобана перлина, @{{user}}!",
    f"Підари в шоці, а ти — топ, @{{user}}!",
    f"Йди нахуй, але з КМС, @{{user}}!",
    f"Це піздато, факт, @{{user}}!",
    f"Ну все, тепер ти піздобол епічного рівня, @{{user}}!",
    f"Йобаний цирк, але влучний, @{{user}}!",
    f"КМС за геніальний піздєж твій, @{{user}}!",
    f"Тепер ти офіційний хуяр, @{{user}}!",
    f"Геніально, йобаний нахуй!",
    f"Це піздато і офіційно, @{{user}}! КМС!",
    f"Хуярь далі, але з КМСом, @{{user}}!",
    f"Ну тут без варіантів, ти топ хуяр!",
    f"Всі інші підари просто плачуть, @{{user}}!"
    f"Це офіційно, @{{user}}. КМС твій!",
    f"Хуяндос, @{{user}}, ти справжній піздабол!",
    f"@{{user}}, твої вміння вражають, КМС заслужений!",
    f"Йди нахуй, але з КМС, @{{user}}!",
    f"Це рівень топу, @{{user}}. КМС!",
    f"Тепер тебе знають всі, @{{user}}. КМС!",
    f"Ну це геніально, @{{user}}. Тримай КМС!",
    f"Оце талант, @{{user}}. КМС як нагорода!",
    f"Легендарно, @{{user}}. КМС!",
    f"Твої слова — це мистецтво, @{{user}}. КМС!",
    f"Браво, @{{user}}, ти заслужив!",
    f"Оце так піздєж, @{{user}}. КМС твій!",
    f"Ніхто так не може, як ти, @{{user}}. КМС!",
    f"Ну це рівень, @{{user}}, вітаємо з КМС!",
    f"@{{user}}, ти справжній майстер слова. КМС!",
    f"Це визнання, @{{user}}, КМС заслужений!",
    f"Ну що тут сказати, @{{user}}, ти піздато впорався!"
]

fuck_messages = [
    f"Та пішов ти нахуй @{{user}}",
    f"Та іди ти нахуй @{{user}}",
    f"@{{user}} іди нахуй",
]

who_asked_messages = [
    f"@{{user}} тебе хтось питав?",
    f"@{{user}} Не потрібних думок не висловлювати, а то жовта картка буде.",
]

reply_messages = [
    f"@{{user}} щоб ти ще сказав",
    f"@{{user}} Очевидних відповідей не давати, а то нахуй пошле.",
    f"@{{user}} Очевидних відповідей не давати, а то жовта картка буде.",
    f"@{{user}} Очевидних відповідей не давати!",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Привіт, це бот для роздачі жовтих карток, посилання нахуй, грамот та КМС!\n"
        "\nКоманди:\n"
        "/zhovta — видати жовту картку\n"
        "/hramota — видати грамоту\n"
        "/kms — присвоїти КМС\n"
        "/huy - послати нахуй.\n"
        "/putav - тебе хтось питав?\n"
        "/ckazav - щоб ти ще сказав.\n"
        "/remove_zhovta — зняти жовту картку\n"
        "/remove_hramota — зняти грамоту\n"
        "/remove_kms — зняти КМС\n"
        "/stats — показати статистику\n"
        "/all_stats - показати повну статистику\n"
        "/reset — обнулити всю статистику.\n\n"
        "Роби порядок або страждай від жовтих карток, хулі!"
    )
    await update.message.reply_text(message)

# Коли додаєш новий метод для відповіді по типу give_yellow або give_award
# перед async def, вище додавай @save_stats_decorator(stats), треба для того щоб дані бекапились.

@save_stats_decorator(stats)
async def give_yellow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)
    stats[user] = stats.get(user, {"yellow": 0, "awards": 0, "kms": 0})
    stats[user]["yellow"] += 1
    message = random.choice(yellow_messages).replace("{user}", user)
    await update.message.reply_text(message)

    with open("yellow.gif", "rb") as file:
        await update.message.reply_animation(animation=InputFile(file))

@save_stats_decorator(stats)
async def give_award(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)
    stats[user] = stats.get(user, {"yellow": 0, "awards": 0, "kms": 0})
    stats[user]["awards"] += 1
    message = random.choice(award_messages).replace("{user}", user)
    await update.message.reply_text(message)

    with open("gramota.jpg", "rb") as file:
        await update.message.reply_photo(photo=InputFile(file))

@save_stats_decorator(stats)
async def give_kms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)
    stats[user] = stats.get(user, {"yellow": 0, "awards": 0, "kms": 0})
    stats[user]["kms"] += 1
    message = random.choice(kms_messages).replace("{user}", user)
    await update.message.reply_text(message)

    with open("kms.jpg", "rb") as file:
        await update.message.reply_photo(photo=InputFile(file))

@save_stats_decorator(stats)
async def remove_yellow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)
    if stats.get(user, {}).get("yellow", 0) <= 0:
        await update.message.reply_text("Немає жовтої картки для зняття, нахуй.")
        return
    stats[user]["yellow"] -= 1
    await update.message.reply_text(f"Жовта картка знята у @{user}.")

@save_stats_decorator(stats)
async def remove_award(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)
    if stats.get(user, {}).get("awards", 0) <= 0:
        await update.message.reply_text("Немає грамоти для зняття.")
        return
    stats[user]["awards"] -= 1
    await update.message.reply_text(f"Грамота знята у @{user}.")

@save_stats_decorator(stats)
async def remove_kms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)
    if stats.get(user, {}).get("kms", 0) <= 0:
        await update.message.reply_text("Немає КМС для зняття.")
        return
    stats[user]["kms"] -= 1
    await update.message.reply_text(f"КМС знято у @{user}.")

@save_stats_decorator(stats)
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not stats:
        await update.message.reply_text("Статистика порожня.")
        return
    response = "Статистика:\n"
    for user, data in stats.items():
        response += f"@{user}:\n"
        response += f"🟡 Жовтих карток: {data['yellow']}\n"
        red_cards = data['yellow'] // 2
        if red_cards > 0:
            response += f"🔴 Червоних карток: {red_cards}\n"
        response += f"📜 Грамот: {data['awards']}\n"
        response += f"🏆 КМС: {data['kms']}\n\n"
    await update.message.reply_text(response)

@save_stats_decorator(stats)
async def reset_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats.clear()
    await update.message.reply_text("Статистика очищена.")

# Послати Нахуй
@save_stats_decorator(stats)
async def give_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)

    message = random.choice(fuck_messages).replace("{user}", user)
    await update.message.reply_text(message)

@save_stats_decorator(stats)
async def who_asked(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)

    message = random.choice(who_asked_messages).replace("{user}", user)
    await update.message.reply_text(message)

@save_stats_decorator(stats)
async def obious_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = update.message.reply_to_message.from_user if update.message.reply_to_message else update.message.from_user
    user = user_data.username if user_data.username else user_data.first_name or str(user_data.id)

    message = random.choice(reply_messages).replace("{user}", user)
    await update.message.reply_text(message)

@save_stats_decorator(stats)
async def all_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not stats:
        await update.message.reply_text("Статистика порожня.")
        return
    
    # Sort users by total awards descending
    sorted_users = sorted(stats.items(), 
                         key=lambda x: x[1]['yellow'] + x[1]['awards'] + x[1]['kms'],
                         reverse=True)
    
    response = "📊 Повна статистика для всіх користувачів:\n\n"
    for user, data in sorted_users:
        response += f"@{user}:\n"
        response += f"🟡 Жовтих карток: {data['yellow']}\n"
        red_cards = data['yellow'] // 2
        if red_cards > 0:
            response += f"🔴 Червоних карток: {red_cards}\n"
        response += f"📜 Грамот: {data['awards']}\n" 
        response += f"🏆 КМС: {data['kms']}\n\n"
    
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token("8005152106:AAF29-v3TguuPxmNWXcLgGIopgHs12LrQ0U").build()

    # Add error handler
    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("zhovta", give_yellow))
    app.add_handler(CommandHandler("hramota", give_award))
    app.add_handler(CommandHandler("kms", give_kms))
    app.add_handler(CommandHandler("remove_zhovta", remove_yellow))
    app.add_handler(CommandHandler("remove_hramota", remove_award))
    app.add_handler(CommandHandler("remove_kms", remove_kms))
    app.add_handler(CommandHandler("stats", show_stats))
    app.add_handler(CommandHandler("reset", reset_stats))
    app.add_handler(CommandHandler("huy", give_direction))
    app.add_handler(CommandHandler("putav", who_asked))
    app.add_handler(CommandHandler("ckazav", obious_reply))
    app.add_handler(CommandHandler("all_stats", all_stats))

    print("Єблот запущено!")
    app.run_polling()
