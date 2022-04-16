import re


async def is_phone_number_valid(number: str):
    pattern = r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$"
    res = re.fullmatch(pattern, number)
    return True if res else False


# @dp.message_handler(regexp=)
# async def check_number(message: types.Message):
#     id = message.from_user.id
#
#     r = requests.get('https://api.nutritionscience.pro/api/v1/users/tgbot', params={'phone': "89867178660"})
#
#     select_type = cur.execute('SELECT firstname FROM data WHERE number = ?', (message.text,)).fetchone()
#     type = str(select_type[0])
#
#     result = dict(r.json())
#     await bot.delete_message(message.from_user.id, message.message_id)
#     if result['user'] == True and result['is_active'] == False:
#         await bot.send_message(id, "Учетная запись неактивна, либо не приобретен курс. Отправить вопрос невозможно",
#                                reply_markup=kb.main)
#     if result['user'] == True and result['is_active'] == True:
#         if type == 'ученик':
#             await bot.send_message(id, "Вы успешно авторизовались", reply_markup=kb.ask)
#         if type == 'куратор':
#             await bot.send_message(id, "Вы успешно авторизовались", reply_markup=kb.mainkur)
#         if type == 'наставник':
#             await bot.send_message(id, "Вы успешно авторизовались", reply_markup=kb.mainknast)
#     if result['user'] == False and result['is_active'] == False:
#         await bot.send_message(id, "Авторизация невозможна.", reply_markup=kb.main)
