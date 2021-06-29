from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pronos.models import Awayteam, Bet, Match, Userteam, UserteamMember
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import BetCreateForm, UserteamcreateForm, UserteamJoinform
from datetime import datetime
from django.utils import timezone
from django.core.paginator import Paginator

# Matchs index - liste all
class MatchListView(ListView):
    model = Awayteam
    template_name = 'pronos/match_index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'awayteams'

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        context['awayteams'] = Awayteam.objects.all().filter(match__done=False).order_by('-match__match_date')
        return context

    # paginate_by = 1


# Bet views
class BetListView(LoginRequiredMixin, ListView):
    model = Bet
    template_name = 'pronos/bet_index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'bets'
    paginate_by = 4

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@login_required
def BetCreateView(request):
    now = datetime.now()
    # bets = Bet.objects.filter(Bet.match).all()
    awayteams = Awayteam.objects.all()
    # awayteams = Awayteam.objects.filter(match=match).order_by('match_date')
    if request.method == 'POST':
        form = BetCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your prono has been created!')
            return redirect('bet-index')
    else:
        form = BetCreateForm()

    return render(request, 'pronos/bet_create.html', {'form': form, 'awayteams': awayteams, 'now': now })


class BetDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Bet
    def test_func(self):
        bet = self.get_object()
        if self.request.user == bet.user:
            return True
        return False


class BetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bet
    fields = ['match', 'hometeam', 'prono_hometeam', 'awayteam', 'prono_awayteam']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        bet = self.get_object()
        if self.request.user == bet.user:
            return True
        return False


class BetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bet
    success_url = "/"

    def test_func(self):
        bet = self.get_object()
        if self.request.user == bet.user:
            return True
        return False
        

# Userteam views
@login_required
def UserteamCreateView(request):
    userteams = Userteam.objects.all()
    if request.method == 'POST':
        form = UserteamcreateForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            form.save()
            messages.success(request, f'Your Team has been created!')
            userteam =  Userteam.objects.last()
            return redirect('userteam-detail', userteam.id)
    else:
        form = UserteamcreateForm()

    return render(request, 'pronos/userteam_create.html', {'form': form, 'userteams': userteams })


class UserteamDetailView(LoginRequiredMixin, DetailView):
    model = Userteam
    def get_context_data(self, **kwargs):
        context = super(UserteamDetailView, self).get_context_data(**kwargs)
        context['members'] = UserteamMember.objects.filter(userteam=self.get_object())
        return context

class UserteamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Userteam
    fields = ['name', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        userteam = self.get_object()
        if self.request.user == userteam.user:
            return True
        return False

class UserteamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Userteam
    success_url = "/"

    def test_func(self):
        userteam = self.get_object()
        if self.request.user == userteam.user:
            return True
        return False
        

@login_required
def UserteamJoinView(request):
    if request.method == 'POST':
        form = UserteamJoinform(request.POST)
        form.instance.user = request.user
        # form.instance.userteam = Userteam.name
        if form.is_valid():
            form.save()
            messages.success(request, f'Your a member of this Team!')
            userteam =  Userteam.objects.last()
            return redirect('userteam-detail', userteam.id)
    else:
        form = UserteamJoinform()

    return render(request, 'pronos/userteam_join.html', {'form': form})


# Scores views
