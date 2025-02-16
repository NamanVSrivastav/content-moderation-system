from celery import Celery
from app.services.moderation_service import ModerationService
from app.utils.retry import retry_with_backoff

app = Celery("moderation_tasks", broker="redis://redis:6379/0")

@app.task(bind=True)
@retry_with_backoff(retries=3)
def process_moderation_task(self, text: str):
    service = ModerationService()
    return service.moderate_text(text)