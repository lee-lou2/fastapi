from apps.backend.chatbot.question.tasks import *


@app.task
def health2():
    return {"message": "Live"}
