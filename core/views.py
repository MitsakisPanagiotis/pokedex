import random

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View, generic

from .models import Ability, Area, Encounter, Move, Pokemon, PokemonAbility, PokemonMove


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
    model = Move
    template_name = "move_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        move = context["move"]
        context["pokemon"] = PokemonMove.objects.select_related("pokemon").filter(move=move)
        return context


class AreaDetailsView(generic.detail.DetailView):
    model = Area
    template_name = "area_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area = context["area"]
        context["pokemon"] = Encounter.objects.select_related("pokemon").filter(area=area)
        return context


class AboutView(View):
    template_name = "about.html"

    def get(self, request):
        upper_bound = len(Pokemon.objects.all())
        return render(
            request,
            self.template_name,
            {"pokemon": Pokemon.objects.get(id=random.randint(1, upper_bound))},
        )


class ConfigView(View):
    def get(self, request):
        return JsonResponse(
            {"APPLICATION_ID": settings.APPLICATION_ID, "SEARCH_API_KEY": settings.SEARCH_API_KEY}
        )
