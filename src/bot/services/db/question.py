from usersupport.models import UserQuestion, TelegramUser
from asgiref.sync import sync_to_async


@sync_to_async
def select_question(user):
    question = UserQuestion.objects.filter(user=user, state="Открытый вопрос").first()
    return question


@sync_to_async
def select_question_by_id(user, pk):
    question = UserQuestion.objects.filter(user=user, pk=pk).first()
    return question


@sync_to_async
def add_question(user: TelegramUser, question):
    # try:
    user_question = UserQuestion(user=user, question=question).save()
    return user_question
    # except Exception:
    #     return select_question(user=user)


@sync_to_async
def add_history(user, pk, history):
    return UserQuestion.objects.filter(user=user, pk=pk).update(history=f"{history}")

@sync_to_async
def add_history2(user, pk, history2):
    return UserQuestion.objects.filter(user=user, pk=pk).update(history2=f"{history2}")

@sync_to_async
def update_state(user, pk):
    return UserQuestion.objects.filter(user=user, pk=pk).update(state="Вопрос закрыт")


@sync_to_async
def update_rate(user, pk, rate):
    return UserQuestion.objects.filter(user=user, pk=pk).update(rate=rate)


@sync_to_async
def update_feedback(user, pk, feedback):
    return UserQuestion.objects.filter(user=user, pk=pk).update(feedback=feedback)


@sync_to_async
def add_helper(user,pk, helper_id):
    return UserQuestion.objects.filter(user=user,pk=pk).update(helper_id=helper_id)


@sync_to_async
def add_mes_id(user, pk, mes_id):
    return UserQuestion.objects.filter(user=user, pk=pk).update(mes_id=mes_id)


@sync_to_async
def all_q(user):
    return UserQuestion.objects.filter(user=user, state="Вопрос закрыт").all()
