from django.contrib import admin
from characters.models import Character
from characters.models import Team
from characters.models import Position
from characters.models import Skills
from characters.models import Content
from characters.models import ContentType

# Register your models here.
@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'team', 'position']

@admin.register(Team)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Skills)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

@admin.register(Content)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "episode_name", "episode", "volume", "type"]

@admin.register(ContentType)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]