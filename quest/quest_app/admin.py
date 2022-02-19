from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Levels, CodesOnLevel, Answers, Progress, FoundCodesForTeams, WriteData, Rating


class CodesOnLevelInline(admin.TabularInline):
    """Выводить inline модель CodesOnLevel"""

    model = CodesOnLevel
    extra = 0


class AnswersInline(admin.TabularInline):
    """Выводить inline модель Answers"""

    model = Answers
    extra = 0


class RatingInline(admin.TabularInline):
    """Выводить inline модель Rating"""

    model = Rating
    extra = 0

    readonly_fields = ('get_number_of_level', )

    fieldsets = (
        (None, {'fields': ('get_number_of_level', 'level', 'time', )}),)

    def has_add_permission(self, request, obj=None) -> bool:
        """Запрещено добавлять экземпляры модели."""

        return False

    def get_number_of_level(self, obj) -> str:
        """Возвращает номер уровня."""

        return f'Уровень №{obj.level.number_of_level}'

    get_number_of_level.short_description = 'Уровень №'


class ProgressInline(admin.TabularInline):
    """Выводить inline модель Progress"""

    model = Progress
    extra = 0
    readonly_fields = ('get_found_codes_for_teams', )
    fieldsets = (
        (None, {
            'fields': ('number_of_level', 'is_published_spoiler', 'is_published_hint1', 'is_published_hint2',
                       'start_level_at', 'get_found_codes_for_teams')
        }),
    )

    def has_add_permission(self, request, obj=None) -> bool:
        """Запрещено добавлять экземпляры модели."""

        return False

    def get_found_codes_for_teams(self, obj) -> str:
        """Возвращает найденные на уровне коды."""

        return ', '.join(x.found_code for x in FoundCodesForTeams.objects.filter(progress=obj))

    get_found_codes_for_teams.short_description = 'Найденые коды'

class LevelsAdmin(admin.ModelAdmin):
    """Выводить модель Levels"""

    list_display = ['number_of_level', 'title']
    inlines = [AnswersInline, CodesOnLevelInline]


class UserAdmin(BaseUserAdmin):
    """Выводить модель User"""

    list_display = ['id', 'username']
    readonly_fields = ('get_write_data', )
    fieldsets = (
        (None, {
            'fields': ('username', 'get_write_data')
        }),
    )
    inlines = [ProgressInline, RatingInline]

    def get_write_data(self, obj):
        """Возвращает все, что писал пользователь."""

        return ', '.join(x.data for x in WriteData.objects.filter(user=obj))


admin.site.register(Levels, LevelsAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
