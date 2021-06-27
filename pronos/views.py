from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pronos.models import Awayteam, Match, Bet
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import BetCreateForm




class MatchListView(ListView):
    model = Awayteam
    awayteams = Awayteam.objects.all()
    template_name = 'pronos/match_index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'awayteams'
    paginate_by = 4


class BetListView(LoginRequiredMixin, ListView):
    model = Bet
    template_name = 'pronos/bet_index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'bets'
    paginate_by = 4

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@login_required
def BetCreateView(request):
    awayteams = Awayteam.objects.all()
    if request.method == 'POST':
        form = BetCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your prono has been created!')
            return redirect('bet-index')
    else:
        form = BetCreateForm()

    return render(request, 'pronos/bet_create.html', {'form': form, 'awayteams': awayteams })

class BetDetailView(DetailView):
    model = Bet

class BetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bet
    fields = ['match', 'hometeam', 'awayteam', 'prono_hometeam', 'prono_awayteam']

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
