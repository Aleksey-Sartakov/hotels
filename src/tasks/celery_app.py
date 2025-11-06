from celery import Celery

from src.config import settings


def init_celery(celery_name, broker_host: str, broker_port: int, tasks_path: str, broker_type: str = None):
    broker = f"redis://{broker_host}:{broker_port}"

    if broker_type and broker_type == "rabbitmq":
        broker = ""

    return Celery(celery_name, broker=broker, include=[tasks_path])


celery_instance = init_celery(
    celery_name="hotels_background_task_manager",
    broker_host=settings.REDIS_HOST,
    broker_port=settings.REDIS_PORT,
    tasks_path="src.tasks.tasks"
)

celery_instance.conf.beat_schedule = {
    "luboe_nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5
    }
}
