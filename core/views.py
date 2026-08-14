import random

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View, generic

from .models import Ability, Area, Move, Pokemon, PokemonAbility


class HomeView(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


class PokemonListView(generic.list.ListView):
    context_object_name = "pokemon_list"
    model = Pokemon
    template_name = "pokemon_list.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PokemonDetailsView(generic.detail.DetailView):
    context_object_name = "pokemon"
    model = Pokemon
    template_name = "pokemon_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pokemon = context["pokemon"]
        context["abilities"] = PokemonAbility.objects.select_related("ability").filter(
            pokemon=pokemon
        )
        return context


class AbilityDetailsView(generic.detail.DetailView):
    context_object_name = "ability"
    model = Ability
    template_name = "ability_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ability = context["ability"]
        context["pokemon"] = PokemonAbility.objects.select_related("pokemon").filter(
            ability=ability
        )
        return context


class MoveDetailsView(generic.detail.DetailView):
    context_object_name = "move"
    model = Move
    template_name = "move_details.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class AreaDetailsView(generic.detail.DetailView):
    context_object_name = "area"
    model = Area
    template_name = "area_details.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class AboutView(View):
    template_name = "about.html"

    def get(self, request):
        return render(
            request, self.template_name, {"pokemon": Pokemon.objects.get(id=random.randint(1, 386))}
        )


class ConfigView(View):
    def get(self, request):
        return JsonResponse(
            {"APPLICATION_ID": settings.APPLICATION_ID, "SEARCH_API_KEY": settings.SEARCH_API_KEY}
        )
