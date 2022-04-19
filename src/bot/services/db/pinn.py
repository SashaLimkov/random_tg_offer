from usersupport.models import UserQuestion, PinnedMessage
from asgiref.sync import sync_to_async


@sync_to_async
def select_pinned_message(question):
    question = PinnedMessage.objects.filter(question=question).first()
    return question


@sync_to_async
def add_pinned_message(question: UserQuestion, kur, nast):
    try:
        user_question = PinnedMessage(
            question=question, kurators_chat=kur, mentors_chat=nast
        ).save()
        return user_question
    except Exception:
        return select_pinned_message(question=question)
