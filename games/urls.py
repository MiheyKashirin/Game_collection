from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.game_list, name='game_list'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_handler, name='login_handler'),
    path('logout/', views.logout_handler, name='logout_handler'),
    path('register/', views.register, name='register'),
    path('add/', views.add_game, name='add_game'),
    path('edit/<int:game_id>/', views.edit_game, name='edit_game'),
    path('delete/<int:game_id>/', views.delete_game, name='delete_game'),
]
