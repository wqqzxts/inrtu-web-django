from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from characters.models import Character
from django.views.generic import TemplateView

# Create your views here.
class ShowCharactersView(TemplateView):
    template_name = "characters/show_characters.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['characters'] = Character.objects.all()

        return context