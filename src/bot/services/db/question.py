from usersupport.models import UserQuestion, TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_question(user_id):
    question = UserQuestion.objects.filter(user_id=user_id, state="Открытый вопрос").first()
    return question


@sync_to_async
def add_question(user_id, question):
    try:
        user_question = UserQuestion(
            user_id=user_id,
            question=question
        ).save()
        return user_question
    except Exception:
        return select_question(user_id=user_id)


@sync_to_async
def add_history(question: UserQuestion, history):
    return question.objects.update(history=f"-{history}\n")


@sync_to_async
def add_helper(question, helper_id):
    return question.objects.update(helper_id=helper_id)


@sync_to_async
def add_mes_id(question, mes_id):
    return question.objects.update(mes_id=mes_id)
