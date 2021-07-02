from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from pronos.models import Userteam, UserteamMember, Bet
from django.db.models import Sum


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
    bets_num = Bet.objects.filter(user=request.user).count()
    bets_finish = Bet.objects.filter(user=request.user).filter(match__done=True).count()
    points_max = bets_num * 3
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
        'points_max': points_max,
        'points': points,
        'bets_num': bets_num,
        'bets_finish': bets_finish,
    }

    return render(request, 'users/profile.html', context)


@login_required
def statistiques(request):
    userteams =  Userteam.objects.filter(user=request.user).all()
    members =  UserteamMember.objects.filter(user=request.user).all()
    points = Bet.objects.filter(user=request.user).aggregate(sum_point=Sum('point')).get('sum_point')
    bets = Bet.objects.filter(user=request.user).all()
    bets_num = Bet.objects.filter(user=request.user).count()
    bets_finish = Bet.objects.filter(user=request.user).filter(match__done=True).count()
    points_max = bets_num * 3
    
    context = {
        'userteams': userteams,
        'members': members,
        'points_max': points_max,
        'points': points,
        'bets_num': bets_num,
        'bets_finish': bets_finish,
        'bets': bets,
    }

    return render(request, 'users/user_stats.html', context)
