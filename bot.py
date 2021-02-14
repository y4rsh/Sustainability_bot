import logging
import config
from aiogram import Bot, Dispatcher, executor, types
import keyboards as kb
import pandas as pd

API_TOKEN = config.token

products_info = pd.read_csv("prods.csv")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """

    """
    await message.reply("Привет! Я - састейнометр, и я помогаю людям следить за экологичностью их потребительской корзины.\n\n", reply_markup=kb.inline_knowledge)


# @dp.message_handler(commands=["tracker"])
# async def tracker(message: types.Message):
#     """
#     eco-food-tracker
#     """
#     # if user_id not in DataBase:
#     #     ask his name
#     #     add user to DataBase
#     # else:
#     await message.reply("Выбери категорию продукта", reply_markup=kb.inline_categories)


@dp.callback_query_handler(lambda c: c.data == "know1")
async def prod_categories(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id, kb.inline_vegetables)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Категории продуктов:", reply_markup=kb.inline_categories)


@dp.callback_query_handler(lambda c: c.data == "know2")
async def full_list(callback_query: types.CallbackQuery):
    """
    Функция выводит полный список продуктов и ресурсозатрат.

    """
    text = "Полный список затрат ресурсов на кг продукта. \n"
    for i in range(products_info.shape[0]):
        text += products_info.loc[i][0]+": CO2:"+str(products_info.loc[i][1])+", вода: "+str(products_info.loc[i][2])+", земля: "+str(products_info.loc[i][3])+"\n"
    text += "\n\n В виде таблицы: https://docs.google.com/document/d/1pKOrF7iYl-YG5ETcUzPZlmtgFEqw7VoOQIILj2MLF44/edit"
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=text)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Чтобы вернуться назад, отправь команду /start ")


@dp.callback_query_handler(lambda c: c.data == "know3")
async def about_sust(callback_query: types.CallbackQuery):
    """
    ЗДЕСЬ БОЛЬШЕ О SUSTAINABILITY И ССЫЛКИ НА ТЕКСТЫ

    """
    text = """Продовольственная безопасность - ситуация, которой все люди в каждый момент времени имеют физические, экономические и социальные возможности для получения доступа к достаточному количеству безопасной и питательной пищи, необходимой для ведения активной и здоровой жизни.
    
Продовольственная система - это все элементы и любая деятельность, которые связаны с производством, переработкой, распределением, приготовлением или потреблением еды, а также социально-экономические и экологические последствия этой деятельности.

Устойчивая продовольственная система (sustainable food system) - такая продовольственная система, которая обеспечивает продовольственную безопасность и достаточное питание для всех людей таким образом, что экономическим, социальным и экологическим основам для обеспечения продовольственной безопасности будущих поколений ничего не угрожает.

Экологический след от производства продуктов питания состоит из четырех компонентов: углеродный след, затраты водных ресурсов, затраты земельных ресурсов, воздействие на биоразнообразие. Устойчивую цену мы получаем, комбинируя показатели затрат этих ресурсов (за исключением воздействия на биоразнообразие).

Углеродный след - количество парниковых газов, производимых за жизненный цикл продукта, в кг. Затраты водных ресурсов - общий объем пресной воды, который напрямую или косвенно используется для производства продукта. Использование земельных ресурсов  - поверхность земли, используемая для производства продуктов питания. Влияние на биоразнообразие оценивается на основе количества лесов, которое было вырублено ради новых сельхозугодий, количества видов в Красной книге, которым угрожает исчезновение из-за развития сельского хозяйства, а также трофического индекса для оценки разнообразия морских ресурсов.

Подборный пример на коровках и помидорках: 
https://docs.google.com/document/d/1GVyynFJomLUKDFQxhws36IVLN7h7uzCJadQq4d-dIdM/edit?usp=sharing)

Методолгия расчета: 
https://docs.google.com/document/d/1q_v2HTJuUUeVIrFprHYu1nXe-dl5op8kEVwVge148o0/edit
    """
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=text)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Чтобы вернуться назад, отправь команду /start ")


@dp.callback_query_handler(lambda c: c.data[:3] == "cat")
async def veg(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data[-1] == "1":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Выбери нужный продукт из списка.",
                               reply_markup=kb.inline_fruits)
    elif callback_query.data[-1] == "2":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Выбери нужный продукт из списка.",
                               reply_markup=kb.inline_vegetables)
    elif callback_query.data[-1] == "3":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Выбери нужный продукт из списка.",
                               reply_markup=kb.inline_grain)
    elif callback_query.data[-1] == "4":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Выбери нужный продукт из списка.",
                               reply_markup=kb.inline_meat)
    elif callback_query.data[-1] == "7":
        await bot.send_message(chat_id=callback_query.from_user.id, text="Выбери нужный продукт из списка.",
                               reply_markup=kb.inline_drinks)

def calculator(product:str):
    return product+" "+str(2**10)

@dp.callback_query_handler(lambda c: c.data[:5] == "calc ")
async def veg(callback_query: types.CallbackQuery):
    """
    СЧИТАЕМ ЭКО-ЦЕНУ
    :param callback_query:
    :return:
    """
    product = callback_query.data[5:]
    water = products_info[products_info["Name"] == product].iloc[0][2]
    land = products_info[products_info["Name"] == product].iloc[0][3]
    co2 = products_info[products_info["Name"] == product].iloc[0][1]
    sust_price = products_info[products_info["Name"] == product].iloc[0][4]
    text = "{}, расходы на кг продукта: \n Расходы водных ресурсов: {} л \n Расходы земных ресурсов: {} кв.м \n Расходы СО2: {} кг \n Устойчивая цена: {}".format(product, water, land, co2, sust_price)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=callback_query.from_user.id, text=text)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)