from datetime import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from quest_app.models import Rating, Progress, Levels


def level_up(progress: Progress, level: Levels, user: User) -> None:
    """Переводит пользователя на новый уровень.
    Сбрасывает прогресс и найденные коды на уровне.
    Записывает время на уровне в Rating."""

    progress.found_codes.all().delete()

    time = timezone.now() - progress.start_level_at
    time = datetime.min + time
    Rating.objects.create(level=level, user=user, time=time.time())

    progress.number_of_level += 1
    progress.is_published_hint1 = False
    progress.is_published_hint2 = False
    progress.is_published_spoiler = False
    progress.start_level_at = timezone.now()
    progress.save()


def check_time(progress: Progress) -> tuple:
    """Возвращает время, которое прошло от начала уровня. Возвращаем в виде tuple для секундомера в шаблоне"""

    result_time = timezone.now() - progress.start_level_at

    seconds = result_time.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return hours, minutes, seconds
