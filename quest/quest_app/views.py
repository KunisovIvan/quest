from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import View

from quest_app.form import CodesForm, AnswersForm
from quest_app.misc import level_up, check_time

from quest_app.models import Progress, Levels, FoundCodesForTeams, WriteData


class Home(View):
    """Отвечает за работу с данными на главной странице."""

    template_name = 'quest_app/index.html'
    form_codes = CodesForm
    form_answers = AnswersForm

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user

        progress, is_created = Progress.objects.get_or_create(user=user)
        level = Levels.objects.filter(number_of_level=progress.number_of_level).first()

        if progress.number_of_level > len(Levels.objects.all()):
            messages.success(request, ' Квест завершен!')
            user_logout(request)
            return redirect('login')

        hours, minutes, seconds = check_time(progress)

        if minutes > level.min_for_hint1 - 1 and not progress.is_published_hint1:
            progress.is_published_hint1 = True
            progress.save()
            return redirect('home')

        if minutes > level.min_for_hint2 - 1 and not progress.is_published_hint2:
            progress.is_published_hint2 = True
            progress.save()
            return redirect('home')

        if minutes > level.min_for_level_up - 1 or hours > 0:
            level_up(progress, level, user)
            messages.success(request, 'Вы прошли на новый уровень')
            return redirect('home')

        return render(request, self.template_name, {'level': level,
                                                    'form_codes': self.form_codes,
                                                    'form_answers': self.form_answers,
                                                    'spoiler_is_published': progress.is_published_spoiler,
                                                    "hint1_is_published": progress.is_published_hint1,
                                                    "hint2_is_published": progress.is_published_hint2,
                                                    "seconds": seconds,
                                                    "minutes": minutes,
                                                    "hours": hours,
                                                    "found_codes": progress.found_codes.all()})

    def post(self, request):

        user = request.user

        progress, is_created = Progress.objects.get_or_create(user=user)
        level = Levels.objects.filter(number_of_level=progress.number_of_level).first()

        form_answers = self.form_answers(data=request.POST)

        if form_answers.is_valid():
            answer = form_answers.cleaned_data['answers'].lower()

            WriteData.objects.create(user=user, data=answer)

            if answer in [x.answer for x in level.answers_for_level.all()]:
                messages.success(request, 'Верный ответ')
                progress.is_published_spoiler = True
                progress.save()
            else:
                messages.error(request, 'Неверный ответ')

            return redirect('home')

        form_codes = self.form_codes(data=request.POST)

        if form_codes.is_valid():
            code = form_codes.cleaned_data['codes'].lower()

            WriteData.objects.create(user=user, data=code)

            if code in [x.code for x in level.codes_for_level.all()]:

                if code in [x.found_code for x in progress.found_codes.all()]:
                    messages.success(request, 'Код уже был введен')
                else:
                    FoundCodesForTeams.objects.create(progress=progress, found_code=code)

                if len(level.codes_for_level.all()) == len(progress.found_codes.all()):
                    level_up(progress, level, user)
                    messages.success(request, 'Вы прошли на новый уровень')
                else:
                    messages.success(request, 'Найден код')

            else:
                messages.error(request, 'Неверный код')

            return redirect('home')

        return redirect('home')


class Register(View):
    """Отвечает за логику регистрации пользователя."""

    template_name = 'quest_app/register.html'
    form_class = UserCreationForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации!')
        return render(request, self.template_name, {'form': form})


class UserLogin(View):
    """Отвечает за логику авторизации пользователя."""

    template_name = 'quest_app/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


def user_logout(request):
    """Отвечает за логику разлогирования пользователя."""

    logout(request)
    return redirect('login')
