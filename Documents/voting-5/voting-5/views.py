from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .models import Poll, Vote
from .forms import PollForm, PollEditForm, VoteForm, LoginForm, RegisterForm


class PollListView(ListView):
    model = Poll
    context_object_name = 'polls'
    template_name = 'voting/list.html'
    paginate_by = 10

    def _user_voted(self, request, poll):
        if request.user.is_authenticated:
            return Vote.objects.filter(poll=poll, user=request.user).exists()
        voted_ids = request.session.get('voted_polls', [])
        return poll.pk in [int(x) for x in voted_ids if str(x).isdigit()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        poll_list_data = []
        for poll in context['object_list']:
            voted = self._user_voted(self.request, poll)
            if voted:
                total = poll.get_total_votes()
                choices_with_counts = []
                for c in poll.choices.all():
                    count = c.get_votes_count()
                    percent = (count / total * 100) if total else 0
                    percent_css = f'{percent:.1f}'
                    choices_with_counts.append((c, count, percent, percent_css))
                poll_list_data.append({
                    'poll': poll,
                    'voted': True,
                    'choices_with_counts': choices_with_counts,
                    'total_votes': total,
                })
            else:
                poll_list_data.append({
                    'poll': poll,
                    'voted': False,
                    'form': VoteForm(poll),
                })
        context['poll_list_data'] = poll_list_data
        return context


def poll_detail(request, pk):
    return redirect('app:poll_list')


def poll_results(request, pk):
    return redirect('app:poll_list')


def vote_submit(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    voted = False
    if request.user.is_authenticated:
        voted = Vote.objects.filter(poll=poll, user=request.user).exists()
    else:
        voted_ids = request.session.get('voted_polls', [])
        voted = pk in [int(x) for x in voted_ids if str(x).isdigit()]
    if voted:
        messages.info(request, 'Вы уже голосовали в этом опросе.')
        return redirect('app:poll_list')
    if request.method != 'POST':
        return redirect('app:poll_list')
    form = VoteForm(poll, request.POST)
    if form.is_valid():
        choice = form.cleaned_data['choice']
        Vote.objects.create(
            poll=poll,
            choice=choice,
            user=request.user if request.user.is_authenticated else None
        )
        if not request.user.is_authenticated:
            session_voted = request.session.get('voted_polls', [])
            if pk not in session_voted:
                session_voted.append(pk)
                request.session['voted_polls'] = session_voted
        messages.success(request, 'Ваш голос учтён.')
    else:
        messages.error(request, 'Выберите вариант ответа.')
    return redirect('app:poll_list')


@login_required
def poll_create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            form.save(created_by=request.user)
            messages.success(request, 'Опрос создан.')
            return redirect('app:poll_list')
    else:
        form = PollForm()
    return render(request, 'voting/create.html', {'form': form})


@login_required
def poll_edit(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user != poll.created_by:
        messages.error(request, 'Редактировать может только автор опроса.')
        return redirect('app:poll_list')
    if request.method == 'POST':
        form = PollEditForm(poll, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Опрос сохранён.')
            return redirect('app:poll_list')
    else:
        form = PollEditForm(poll)
    return render(request, 'voting/edit.html', {'poll': poll, 'form': form})


class AuthLoginView(LoginView):
    template_name = 'voting/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True


class AuthLogoutView(LogoutView):
    next_page = reverse_lazy('app:poll_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('app:poll_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно. Добро пожаловать!')
            return redirect('app:poll_list')
    else:
        form = RegisterForm()
    return render(request, 'voting/register.html', {'form': form})
