from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Game
from .forms import GameForm, SimpleRegisterForm
from django.shortcuts import get_object_or_404



def register(request):
    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SimpleRegisterForm()
    return render(request, 'games/register.html', {'form': form})


def login_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'games/login.html', {'error': 'Invalid username or password'})
    return render(request, 'games/login.html')


def logout_handler(request):
    logout(request)
    return redirect('login')


@login_required
def profile(request):
    user_games = Game.objects.filter(owner=request.user)
    return render(request, 'games/profile.html', {'games': user_games})


@login_required
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'games/add_game.html', {'form': form})


@login_required
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, owner=request.user)
    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = GameForm(instance=game)
    return render(request, 'games/edit_game.html', {'form': form})

@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, owner=request.user)
    game.delete()
    return redirect('profile')

@login_required
def game_list(request):
    games = Game.objects.filter(owner=request.user)
    return render(request, 'games/game_list.html', {'games': games})

def home(request):
    return render(request, 'games/home.html')








