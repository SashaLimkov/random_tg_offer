from usersupport.models import UserQuestion, TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_question(user):
    question = UserQuestion.objects.filter(user=user, state="Открытый вопрос").first()
    return question


@sync_to_async
def add_question(user: TelegramUser, question):
    # try:
    user_question = UserQuestion.objects.create(user=user, question=question)
    return user_question
    # except Exception:
    #     return select_question(user=user)


@sync_to_async
def add_history(user, history):
    return UserQuestion.objects.filter(user=user).update(history=f"{history}\n")


@sync_to_async
def add_helper(question, helper_id):
    return question.objects.update(helper_id=helper_id)


@sync_to_async
def add_mes_id(question, mes_id):
    return question.objects.update(mes_id=mes_id)
