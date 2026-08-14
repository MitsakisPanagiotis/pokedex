from django.contrib import admin

from .models import (
    Ability,
    Area,
    DamageClass,
    Effect,
    Encounter,
    Generation,
    Location,
    Move,
    Pokemon,
    PokemonAbility,
    PokemonMove,
    Region,
    Type,
)

admin.site.register(Ability)
admin.site.register(Area)
admin.site.register(DamageClass)
admin.site.register(Effect)
admin.site.register(Encounter)
admin.site.register(Generation)
admin.site.register(Location)
admin.site.register(Move)
admin.site.register(Pokemon)
admin.site.register(PokemonAbility)
admin.site.register(PokemonMove)
admin.site.register(Region)
admin.site.register(Type)
