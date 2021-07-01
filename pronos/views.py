from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from pronos.models import Awayteam, Bet, Match, Userteam, UserteamMember
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import BetCreateForm, UserteamcreateForm, UserteamJoinform
from datetime import datetime



# Matchs index - liste all
class MatchListView(ListView):
    model = Awayteam
    template_name = 'pronos/match_index.html' # <app>/<model>_<viewtype>.html
    # context_object_name = 'awayteams'
    # paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        context['awayteams'] = Awayteam.objects.all().filter(match__done=False).order_by('-match__match_date')
        context['doneawayteams'] = Awayteam.objects.all().filter(match__done=True).order_by('-match__match_date')
        return context

class MatchDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Match

    def test_func(self):
        if self.request.user.username == 'julie':
            return True
        return False

class MatchUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    pass
    model = Match
    fields = ['goal_hometeam', 'goal_awayteam', 'done']

    def test_func(self):
        if self.request.user.username == 'julie':
            return True
        return False

    def post(self, request, pk):
        match = self.object = self.get_object()
        form = self.get_form()
        if not form.is_valid():
            return super().form_invalid(form)
        form.save()
        done = match.done
        match_id = match.id
        home_score = match.goal_hometeam
        away_score = match.goal_awayteam
        if done == True:
            bets = Bet.objects.filter(match=match_id)
            for bet in bets:
                if home_score == bet.prono_hometeam and away_score == bet.prono_awayteam:
                    bet.point = 3
                    bet.save()
                elif home_score < away_score and bet.prono_hometeam < bet.prono_awayteam:
                    bet.point = 1
                    bet.save()
                elif home_score > away_score and bet.prono_hometeam > bet.prono_awayteam:
                    bet.point = 1
                    bet.save()
                elif home_score == away_score and bet.prono_hometeam == bet.prono_awayteam:
                    bet.point = 1
                    bet.save()
                else:
                    bet.point = 0
                    bet.save()
            return HttpResponse('Point Successfully Updated!')
        else:
            bets = Bet.objects.filter(match=match_id)
            for bet in bets:
                bet.point = 0
                bet.save()
            return HttpResponse('Point Successfully RAZ!')


# Bet views
class BetListView(LoginRequiredMixin, ListView):
    model = Bet
    template_name = 'pronos/bet_index.html' # <app>/<model>_<viewtype>.html
    # context_object_name = 'bets'
    paginate_by = 4

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super(BetListView, self).get_context_data(**kwargs)
        context['bets'] = Bet.objects.all().filter(match__done=False).order_by('-match__match_date')
        context['donebets'] = Bet.objects.all().filter(match__done=True).order_by('-match__match_date')
        return context


@login_required
def BetCreateView(request):
    now = datetime.now()
    bets = Bet.objects.all()
    awayteams = Awayteam.objects.all().filter(match__done=False).order_by('match__match_date')
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
    fields = ['prono_hometeam', 'prono_awayteam']
    success_url = "/index/"

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
    success_url = "/index/"

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
    
    def test_func(self):
        userteam = self.get_object()
        if self.request.user == userteam.user:
            return True
        return False


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
    success_url = "/profile/"

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
