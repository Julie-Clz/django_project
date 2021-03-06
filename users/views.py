from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from pronos.models import Match, Userteam, UserteamMember, Bet
from django.db.models import Sum, Count, Q


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ton compte a bien été crée. Connecte-toi maintenant!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    userteams =  Userteam.objects.filter(user=request.user).all()
    members =  UserteamMember.objects.filter(user=request.user).all()
    points = Bet.objects.filter(user=request.user).aggregate(sum_point=Sum('point')).get('sum_point')
    bets_finish = Bet.objects.filter(user=request.user).filter(match__done=True).count()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Ton compte a bien été modifié!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'userteams': userteams,
        'members': members,
        'points': points,
        'bets_finish': bets_finish,
    }

    return render(request, 'users/profile.html', context)


@login_required
def statistiques(request):
    # userteams =  Userteam.objects.filter(user=request.user).all()
    members =  UserteamMember.objects.filter(user=request.user).all()
    points = Bet.objects.filter(user=request.user).aggregate(sum_point=Sum('point')).get('sum_point')
    # bets = Bet.objects.filter(user=request.user).order_by('match__match_date').all()
    # finish_bets = Bet.objects.filter(user=request.user).filter(match__done=True).order_by('-match__match_date').all()
    # bets_num = Bet.objects.filter(user=request.user).count()
    points_max = Bet.objects.filter(user=request.user).count() * 3
    matchs = Match.objects.filter(done=True).count()
    user_points = Bet.objects.filter(user=request.user).values('user__username').annotate(points=Sum('point')).annotate(pronos=Count('match')).annotate(bons=Count('point', filter=Q(point=1))).annotate(exacts=Count('point', filter=Q(point=3))).order_by('-points')
    pronostat = round(((Bet.objects.filter(user=request.user).count()) / matchs) * 100)
    bonstat = round(((Bet.objects.filter(user=request.user, point=1).count()) / (Bet.objects.filter(user=request.user).count())) * 100)
    exactstat = round(((Bet.objects.filter(user=request.user, point=3).count()) / (Bet.objects.filter(user=request.user).count())) * 100)
    pointstat = round((points / points_max) * 100)
    pointstats = round((points / (matchs * 3)) * 100)

    context = {
        # 'userteams': userteams,
        'members': members,
        # 'points_max': points_max,
        'points': points,
        # 'bets_num': bets_num,
        # 'finish_bets': finish_bets,
        # 'bets': bets,
        'matchs': matchs,
        'user_points': user_points,
        'pronostat': pronostat,
        'exactstat': exactstat,
        'bonstat': bonstat,
        'pointstat': pointstat,
        'pointstats': pointstats,
    }

    return render(request, 'users/user_stats.html', context)
