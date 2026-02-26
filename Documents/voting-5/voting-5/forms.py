from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Poll, Choice


class PollForm(forms.ModelForm):
    choice1 = forms.CharField(label='Вариант 1', max_length=255, required=True)
    choice2 = forms.CharField(label='Вариант 2', max_length=255, required=True)
    choice3 = forms.CharField(label='Вариант 3', max_length=255, required=False)

    class Meta:
        model = Poll
        fields = ['question']
        labels = {'question': 'Вопрос опроса'}

    def save(self, commit=True, created_by=None):
        poll = super().save(commit=False)
        if created_by is not None:
            poll.created_by = created_by
        if commit:
            poll.save()
            for i, key in enumerate(['choice1', 'choice2', 'choice3'], start=1):
                text = self.cleaned_data.get(key)
                if text and text.strip():
                    Choice.objects.create(poll=poll, text=text.strip())
        return poll


class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect
    )

    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = poll.choices.all()


class PollEditForm(forms.Form):
    question = forms.CharField(label='Вопрос опроса', max_length=255)

    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll = poll
        self.fields['question'].initial = poll.question
        for i, choice in enumerate(poll.choices.order_by('id'), start=1):
            name = f'choice_{choice.pk}'
            self.fields[name] = forms.CharField(
                label=f'Вариант {i}',
                max_length=255,
                initial=choice.text,
                required=True
            )

    @property
    def choice_fields(self):
        return [self[f] for f in self.fields if f.startswith('choice_')]

    def save(self):
        self.poll.question = self.cleaned_data['question']
        self.poll.save()
        for key, value in self.cleaned_data.items():
            if key.startswith('choice_') and value:
                pk = key.replace('choice_', '')
                if pk.isdigit():
                    Choice.objects.filter(pk=int(pk), poll=self.poll).update(text=value.strip())
        return self.poll


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput
    )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
