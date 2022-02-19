from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Levels(models.Model):
    """Уровень."""

    number_of_level = models.PositiveSmallIntegerField(verbose_name='Уровень №', default=1, unique=True)
    title = models.CharField(max_length=255, verbose_name='Название уровня')
    question = models.TextField(blank=True, verbose_name='Загадка на уровне')
    question_photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото для загадки')
    spoiler = models.TextField(blank=True, verbose_name='Спойлер')
    spoiler_photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото для спойлера')
    hint1 = models.CharField(max_length=255, verbose_name='Подсказка 1')
    hint2 = models.CharField(max_length=255, verbose_name='Подсказка 2')
    min_for_hint1 = models.PositiveSmallIntegerField(verbose_name='Минут до 1 подсказки', default=10)
    min_for_hint2 = models.PositiveSmallIntegerField(verbose_name='Минут до 2 подсказки', default=20)
    min_for_level_up = models.PositiveSmallIntegerField(verbose_name='Минут до конца уровня', default=60)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'


class CodesOnLevel(models.Model):
    """Коды на уровне."""

    level = models.ForeignKey(Levels, related_name='codes_for_level', verbose_name='Уровень', on_delete=models.CASCADE)
    code = models.CharField(max_length=255, verbose_name='Код на уровне')

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Код на уровне'
        verbose_name_plural = 'Коды на уровне'


class Answers(models.Model):
    """"Ответ на загадку."""

    level = models.ForeignKey(Levels, related_name='answers_for_level', verbose_name='Уровень',
                              on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, verbose_name='Ответ на загадку')

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = 'Ответ на загадку'
        verbose_name_plural = 'Ответы на загадки'


class Progress(models.Model):
    """Прогресс команды на уровне."""

    user = models.OneToOneField(User, related_name='progress_of_user', verbose_name='Пользователь',
                                on_delete=models.CASCADE)

    number_of_level = models.PositiveSmallIntegerField(verbose_name='Уровень №', default=1)

    is_published_spoiler = models.BooleanField(default=False, verbose_name='Показать ли спойлер')
    is_published_hint1 = models.BooleanField(default=False, verbose_name='Показать ли подсказку 1')
    is_published_hint2 = models.BooleanField(default=False, verbose_name='Показать ли подсказку 2')

    start_level_at = models.DateTimeField(default=timezone.now, verbose_name='Время старта уровня')

    def __str__(self):
        return f'Прогресс пользователя: {self.user}'

    class Meta:
        verbose_name = 'Прогресс команды'
        verbose_name_plural = 'Прогресс команды'


class FoundCodesForTeams(models.Model):
    """Найденные командой коды."""

    progress = models.ForeignKey(Progress, related_name='found_codes', verbose_name='Прогресс пользователя',
                                 on_delete=models.CASCADE)
    found_code = models.CharField(max_length=255, verbose_name='Найденный код')

    def __str__(self):
        return self.found_code

    class Meta:
        verbose_name = 'Найденный код'
        verbose_name_plural = 'Найденные коды'


class WriteData(models.Model):
    """Вводимые командой данные."""

    user = models.ForeignKey(User, related_name='write_data_for_user', verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    data = models.CharField(max_length=255, verbose_name='Вводимые данные')

    def __str__(self):
        return self.data

    class Meta:
        verbose_name = 'Вводимые данные'
        verbose_name_plural = 'Вводимые данные'


class Rating(models.Model):
    """Времена на уровнях."""

    level = models.ForeignKey(Levels, related_name='rating', verbose_name='Уровень', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='rating', verbose_name='Пользователь', on_delete=models.CASCADE)
    time = models.TimeField(verbose_name='Время прохождения уровня')
