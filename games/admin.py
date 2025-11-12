from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'platform', 'status', 'rating', 'owner')
    list_filter = ('status', 'platform', 'owner')
    search_fields = ('title',)
