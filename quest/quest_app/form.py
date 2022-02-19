from django import forms


class CodesForm(forms.Form):
    codes = forms.CharField(label='', widget=forms.TextInput())


class AnswersForm(forms.Form):
    answers = forms.CharField(label='', widget=forms.TextInput())
