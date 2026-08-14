from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    AbilityDetailsView,
    AboutView,
    AreaDetailsView,
    ConfigView,
    HomeView,
    MoveDetailsView,
    PokemonDetailsView,
    PokemonListView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("pokemon-list", PokemonListView.as_view(), name="pokemon_list"),
    path("pokemon/<slug:slug>", PokemonDetailsView.as_view(), name="pokemon_details"),
    path("ability/<slug:slug>", AbilityDetailsView.as_view(), name="ability_details"),
    path("move/<slug:slug>", MoveDetailsView.as_view(), name="move_details"),
    path("area/<slug:slug>", AreaDetailsView.as_view(), name="area_details"),
    path("about", AboutView.as_view(), name="about"),
    path("config", ConfigView.as_view(), name="config"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
