from django.core.exceptions import ValidationError
from django.db import models


class DamageClass(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=8, unique=True)
    slug = models.SlugField(max_length=8, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "damage_class"

    def __str__(self) -> str:
        return f"{self.name}"


class Generation(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Ability(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=16, unique=True)
    slug = models.SlugField(max_length=16, unique=True)
    effect = models.TextField()
    description = models.TextField()
    generation = models.ForeignKey(Generation, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Effect(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=16, unique=True)
    slug = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Region(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=6, unique=True)
    slug = models.SlugField(max_length=6, unique=True)
    generation = models.ForeignKey(Generation, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Location(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=37, unique=True)
    slug = models.SlugField(max_length=37, unique=True)
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Area(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=48, unique=True)
    slug = models.CharField(max_length=48, unique=True)
    location = models.ForeignKey(Location, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Type(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=8, unique=True)
    slug = models.SlugField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Move(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    type = models.ForeignKey(Type, on_delete=models.RESTRICT)
    accuracy = models.PositiveSmallIntegerField(null=True)
    power = models.PositiveSmallIntegerField(null=True)
    effect = models.ForeignKey(Effect, on_delete=models.RESTRICT)
    description = models.TextField()
    effect_chance = models.PositiveSmallIntegerField(null=True)
    pp = models.PositiveSmallIntegerField()
    generation = models.ForeignKey(Generation, on_delete=models.RESTRICT)
    damage_class = models.ForeignKey(DamageClass, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"


class Species(models.Model):
    name = models.CharField(max_length=12, unique=True)
    slug = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Pokemon(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    sprite = models.ImageField(upload_to="sprites/")
    artwork = models.ImageField(upload_to="official-artwork/")
    name = models.CharField(max_length=15, unique=True)
    slug = models.SlugField(max_length=16, unique=True)
    generation = models.ForeignKey(Generation, on_delete=models.RESTRICT)
    type_1 = models.ForeignKey(
        Type,
        on_delete=models.RESTRICT,
        related_name="primary_type",
        related_query_name="primary_type",
    )
    type_2 = models.ForeignKey(
        Type,
        default=None,
        null=True,
        on_delete=models.RESTRICT,
        related_name="secondary_type",
        related_query_name="secondary_type",
    )
    species = models.ForeignKey(Species, on_delete=models.RESTRICT)
    hp = models.PositiveSmallIntegerField()
    attack = models.PositiveSmallIntegerField()
    defense = models.PositiveSmallIntegerField()
    special_attack = models.PositiveSmallIntegerField()
    special_defense = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()
    height = models.DecimalField(max_digits=3, decimal_places=1)
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    description = models.TextField()
    moves = models.ManyToManyField(Move, through="PokemonMove")
    abilities = models.ManyToManyField(Ability, through="PokemonAbility")
    areas = models.ManyToManyField(Area, through="Encounter")
    legendary = models.BooleanField(default=False)
    mythical = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def clean(self) -> None:
        if self.is_legendary and self.is_mythical:
            raise ValidationError("A Pokémon cannot be both legendary and mythical.")


class Encounter(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.RESTRICT)
    area = models.ForeignKey(Area, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.pokemon_id}: {self.area_id}"


class PokemonAbility(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.RESTRICT)
    ability = models.ForeignKey(Ability, on_delete=models.RESTRICT)
    is_hidden = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pokemon_abilities"

    def __str__(self) -> str:
        return f"Pokemon {self.pokemon_id}: {self.ability_id}"


class PokemonMove(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.RESTRICT)
    move = models.ForeignKey(Move, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pokemon_moves"

    def __str__(self) -> str:
        return f"Pokemon {self.pokemon_id}: {self.move_id}"
