import re
from operator import is_none

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify

from core.models import (
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
    Species,
    Type,
)

from ...pokeapi.api_client import PokeAPI


class Command(BaseCommand):
    help = "Seed the database with data by providing the generation."

    def add_arguments(self, parser):
        parser.add_argument("--generation", type=int)

    def handle(self, *args, **options):
        api = PokeAPI()
        self.seed_generation(api, options["generation"])

    def seed_generation(self, api, gen):
        match gen:
            case 1:
                data = api.get("generation_i")
            case 2:
                data = api.get("generation_ii")
            case 3:
                data = api.get("generation_iii")
            case 4:
                data = api.get("generation_iv")
            case 5:
                data = api.get("generation_v")
            case 6:
                data = api.get("generation_vi")
            case 7:
                data = api.get("generation_vii")
            case 8:
                data = api.get("generation_viii")
            case 9:
                data = api.get("generation_ix")
            case _:
                raise CommandError("Unknown input. Enter a generation from 1 to 9.")

        i = 0
        size = len(data["results"])
        area_pattern = re.compile(r"^\w+\s\d+|^\w+\s\w+\s\(\w?\d+\w\)")
        location_pattern = re.compile(r"^\w+\s\d+")
        for result in data["results"]:
            i += 1
            self.stdout.write(f"{i}/{size}")
            resources = api.get_json(result["url"])
            species_data = api.get_json(resources["species"]["url"])
            encounter_data = api.get_json(resources["location_area_encounters"])

            areas = []
            for area in encounter_data:
                if not Area.objects.filter(
                    id=int(area["location_area"]["url"].split("/")[-2])
                ).exists():
                    area_data = api.get_json(area["location_area"]["url"])

                    area_name = ""
                    area_slug = ""
                    if len(area_data["names"]) != 0:
                        for name in area_data["names"]:
                            if name["language"]["name"] == "en":
                                if not re.search(area_pattern, name["name"]):
                                    area_name = name["name"]
                                    area_slug = slugify(area_name)
                                    break
                                else:
                                    area_name = area_data["name"].replace("-", " ").title()
                                    area_slug = slugify(area_name)
                                    break
                    else:
                        area_name = area_data["name"].replace("-", " ").title()
                        area_slug = slugify(area_name)

                    if not Location.objects.filter(
                        id=int(area_data["location"]["url"].split("/")[-2])
                    ).exists():
                        location_data = api.get_json(area_data["location"]["url"])

                        location_name = ""
                        location_slug = ""
                        if len(location_data["names"]) != 0:
                            for name_2 in location_data["names"]:
                                if name_2["language"]["name"] == "en":
                                    if (
                                        re.search(location_pattern, name_2["name"])
                                        or name_2["name"] == "Altering Cave"
                                        or name_2["name"] == "Mirage Island"
                                        or name_2["name"] == "Royal Avenue"
                                        or name_2["name"] == "Safari Zone"
                                        or name_2["name"] == "Victory Road"
                                    ):
                                        location_name = (
                                            location_data["name"].replace("-", " ").title()
                                        )
                                        location_slug = slugify(location_name)
                                        break
                                    else:
                                        location_name = name_2["name"]
                                        location_slug = slugify(location_name)
                                        break

                        else:
                            location_name = location_data["name"].replace("-", " ").title()
                            location_slug = location_data["name"]

                        if not Region.objects.filter(
                            id=int(location_data["region"]["url"].split("/")[-2])
                        ).exists():
                            region_data = api.get_json(location_data["region"]["url"])

                            region_name = ""
                            region_slug = ""
                            for name_3 in region_data["names"]:
                                if name_3["language"]["name"] == "en":
                                    region_name = name_3["name"]
                                    region_slug = slugify(region_name)
                                    break

                            if is_none(region_data["main_generation"]):
                                continue

                            if not Generation.objects.filter(
                                id=int(region_data["main_generation"]["url"].split("/")[-2])
                            ).exists():
                                generation_data = api.get_json(
                                    region_data["main_generation"]["url"]
                                )

                                generation_name = ""
                                generation_slug = ""
                                for name_4 in generation_data["names"]:
                                    if name_4["language"]["name"] == "en":
                                        generation_name = name_4["name"]
                                        generation_slug = slugify(generation_name)
                                        break

                                Generation.objects.create(
                                    id=generation_data["id"],
                                    name=generation_name,
                                    slug=generation_slug,
                                )

                            Region.objects.create(
                                id=region_data["id"],
                                name=region_name,
                                slug=region_slug,
                                generation=Generation.objects.get(
                                    id=int(region_data["main_generation"]["url"].split("/")[-2])
                                ),
                            )

                        Location.objects.create(
                            id=location_data["id"],
                            name=location_name,
                            slug=location_slug,
                            region=Region.objects.get(
                                id=int(location_data["region"]["url"].split("/")[-2])
                            ),
                        )

                    Area.objects.create(
                        id=area_data["id"],
                        name=area_name,
                        slug=area_slug,
                        location=Location.objects.get(
                            id=int(area_data["location"]["url"].split("/")[-2])
                        ),
                    )
                    areas.append(Area.objects.get(id=area_data["id"]))

            pokemon_name = ""
            pokemon_slug = ""
            for name_5 in species_data["names"]:
                if name_5["language"]["name"] == "en":
                    pokemon_name = name_5["name"]

                    if "♀" or "♂" in name_5:
                        pokemon_slug = species_data["name"]
                    else:
                        pokemon_slug = slugify(pokemon_name)
                    break

            species_name = ""
            species_slug = ""
            for obj in species_data["genera"]:
                if obj["language"]["name"] == "en":
                    species_name = obj["genus"].replace("Pokémon", "").strip()
                    species_slug = slugify(species_name)
                    break

            if not Species.objects.filter(name=species_name).exists():
                Species.objects.create(name=species_name, slug=species_slug)

            entries = [
                entry["flavor_text"]
                for entry in species_data["flavor_text_entries"]
                if entry["language"]["name"] == "en"
            ]

            types = []
            for type_1 in resources["types"]:
                type_data = api.get_json(type_1["type"]["url"])

                if not Type.objects.filter(id=type_data["id"]).exists():
                    type_name = ""
                    type_slug = ""

                    for name_6 in type_data["names"]:
                        if name_6["language"]["name"] == "en":
                            type_name = name_6["name"]
                            type_slug = slugify(type_name)
                            break

                    Type.objects.create(
                        id=type_data["id"],
                        name=type_name,
                        slug=type_slug,
                    )

                types.append(Type.objects.get(id=type_data["id"]))

            hp = 0
            attack = 0
            defense = 0
            special_attack = 0
            special_defense = 0
            speed = 0
            is_legendary = False
            is_mythical = False
            for stat in resources["stats"]:
                if stat["stat"]["name"] == "hp":
                    hp = stat["base_stat"]

                if stat["stat"]["name"] == "attack":
                    attack = stat["base_stat"]

                if stat["stat"]["name"] == "defense":
                    defense = stat["base_stat"]

                if stat["stat"]["name"] == "special-attack":
                    special_attack = stat["base_stat"]

                if stat["stat"]["name"] == "special-defense":
                    special_defense = stat["base_stat"]

                if stat["stat"]["name"] == "speed":
                    speed = stat["base_stat"]

            if species_data["is_legendary"]:
                is_legendary = True

            if species_data["is_mythical"]:
                is_mythical = True

            image_file = ContentFile(api.get_image(resources["sprites"]["front_default"]))
            filename = f"{pokemon_name.lower()}.png"

            artwork_file = ContentFile(
                api.get_image(resources["sprites"]["other"]["official-artwork"]["front_default"])
            )
            filename_2 = f"{pokemon_name.lower()}.png"

            if not Pokemon.objects.filter(id=resources["id"]).exists():
                pokemon = Pokemon.objects.create(
                    id=species_data["id"],
                    name=pokemon_name,
                    slug=pokemon_slug,
                    generation=Generation.objects.get(
                        id=int(species_data["generation"]["url"].split("/")[-2])
                    ),
                    type_1=types[0],
                    type_2=types[1] if len(types) == 2 else None,
                    species=Species.objects.get(name=species_name),
                    description=re.sub(r"\s+", " ", entries[-1]),
                    height=resources["height"] / 10,
                    weight=resources["weight"] / 10,
                    hp=hp,
                    attack=attack,
                    defense=defense,
                    special_attack=special_attack,
                    special_defense=special_defense,
                    speed=speed,
                    legendary=is_legendary,
                    mythical=is_mythical,
                )

                if not default_storage.exists(f"sprites/{filename}"):
                    pokemon.sprite.save(filename, image_file)
                    pokemon.save()

                if not default_storage.exists(f"artwork/{filename_2}"):
                    pokemon.artwork.save(filename_2, artwork_file)
                    pokemon.save()

            abilities = []
            for ability in resources["abilities"]:
                if not Ability.objects.filter(
                    id=int(ability["ability"]["url"].split("/")[-2])
                ).exists():
                    ability_data = api.get_json(ability["ability"]["url"])

                    ability_name = ""
                    ability_slug = ""
                    for name_7 in ability_data["names"]:
                        if name_7["language"]["name"] == "en":
                            ability_name = name_7["name"]
                            ability_slug = slugify(ability_name)
                            break

                    effect = ""
                    for entry in ability_data["effect_entries"]:
                        if entry["language"]["name"] == "en":
                            effect = re.sub(r"\s+", " ", entry["effect"])
                            break

                    descriptions = [
                        description["flavor_text"]
                        for description in ability_data["flavor_text_entries"]
                        if description["language"]["name"] == "en"
                    ]

                    try:
                        generation = Generation.objects.get(
                            id=int(ability_data["generation"]["url"].split("/")[-2])
                        )
                    except Generation.DoesNotExist:
                        gen_data = api.get_json(ability_data["generation"]["url"])

                        generation_name = ""
                        generation_slug = ""
                        for name_8 in gen_data["names"]:
                            if name_8["language"]["name"] == "en":
                                generation_name = name_8["name"]
                                generation_slug = slugify(generation_name)
                                break

                        generation = Generation.objects.create(
                            id=gen_data["id"],
                            name=generation_name,
                            slug=generation_slug,
                        )

                    Ability.objects.create(
                        id=ability_data["id"],
                        name=ability_name,
                        slug=ability_slug,
                        effect=effect,
                        description=re.sub(r"\s+", " ", descriptions[-1]),
                        generation=generation,
                    )

                abilities.append(
                    Ability.objects.get(id=int(ability["ability"]["url"].split("/")[-2]))
                )

            moves = []
            for move in resources["moves"]:
                if not Move.objects.filter(id=int(move["move"]["url"].split("/")[-2])).exists():
                    move_data = api.get_json(move["move"]["url"])

                    if is_none(move_data["meta"]):
                        continue

                    move_name = ""
                    move_slug = ""
                    for name_9 in move_data["names"]:
                        if name_9["language"]["name"] == "en":
                            move_name = name_9["name"]
                            move_slug = slugify(move_name)
                            break

                    move_descriptions = [
                        move_description["flavor_text"]
                        for move_description in move_data["flavor_text_entries"]
                        if move_description["language"]["name"] == "en"
                    ]

                    if not Effect.objects.filter(
                        id=int(move_data["meta"]["ailment"]["url"].split("/")[-2])
                    ).exists():
                        effect_data = api.get_json(move_data["meta"]["ailment"]["url"])

                        effect_name = ""
                        effect_slug = ""
                        for name_10 in effect_data["names"]:
                            if name_10["language"]["name"] == "en":
                                if name_10["name"] != "????" and name_10["name"] != "none":
                                    effect_name = name_10["name"]
                                    effect_slug = slugify(effect_name)
                                    break
                                else:
                                    effect_name = effect_data["name"].title()
                                    effect_slug = slugify(effect_name)
                                    break

                        Effect.objects.create(
                            id=effect_data["id"],
                            name=effect_name,
                            slug=effect_slug,
                        )

                    if not DamageClass.objects.filter(
                        id=int(move_data["damage_class"]["url"].split("/")[-2])
                    ).exists():
                        damage_class_data = api.get_json(move_data["damage_class"]["url"])

                        damage_class_name = ""
                        damage_class_slug = ""
                        for name_11 in damage_class_data["names"]:
                            if name_11["language"]["name"] == "en":
                                damage_class_name = name_11["name"]
                                damage_class_slug = slugify(damage_class_name)
                                break

                        description_ = ""
                        for description_2 in damage_class_data["descriptions"]:
                            if description_2["language"]["name"] == "en":
                                description_ = description_2["description"]
                                break

                        DamageClass.objects.create(
                            id=damage_class_data["id"],
                            name=damage_class_name,
                            slug=damage_class_slug,
                            description=description_,
                        )

                    try:
                        type_2 = Type.objects.get(id=int(move_data["type"]["url"].split("/")[-2]))
                    except Type.DoesNotExist:
                        type_data_ = api.get_json(move_data["type"]["url"])

                        type_name = ""
                        type_slug = ""
                        for name_12 in type_data_["names"]:
                            if name_12["language"]["name"] == "en":
                                type_name = name_12["name"]
                                type_slug = slugify(type_name)
                                break

                        type_2 = Type.objects.create(
                            id=type_data_["id"],
                            name=type_name,
                            slug=type_slug,
                        )

                    try:
                        generation_2 = Generation.objects.get(
                            id=int(move_data["generation"]["url"].split("/")[-2])
                        )
                    except Generation.DoesNotExist:
                        gen_data_ = api.get_json(move_data["generation"]["url"])

                        generation_name = ""
                        generation_slug = ""
                        for name_13 in gen_data_["names"]:
                            if name_13["language"]["name"] == "en":
                                generation_name = name_13["name"]
                                generation_slug = slugify(generation_name)
                                break

                        generation_2 = Generation.objects.create(
                            id=gen_data_["id"],
                            name=generation_name,
                            slug=generation_slug,
                        )

                    Move.objects.create(
                        id=move_data["id"],
                        name=move_name,
                        slug=move_slug,
                        type=type_2,
                        accuracy=move_data["accuracy"],
                        power=move_data["power"],
                        effect=Effect.objects.get(
                            id=int(move_data["meta"]["ailment"]["url"].split("/")[-2])
                        ),
                        effect_chance=move_data["effect_chance"],
                        description=re.sub(r"\s+", " ", move_descriptions[-1]),
                        pp=move_data["pp"],
                        generation=generation_2,
                        damage_class=DamageClass.objects.get(
                            id=int(move_data["damage_class"]["url"].split("/")[-2])
                        ),
                    )

                moves.append(Move.objects.get(id=int(move["move"]["url"].split("/")[-2])))

            pokemon = Pokemon.objects.get(id=resources["id"])

            for move in moves:
                PokemonMove.objects.create(pokemon=pokemon, move=move)

            for j, ability in enumerate(abilities):
                PokemonAbility.objects.create(
                    pokemon=pokemon,
                    ability=ability,
                    is_hidden=resources["abilities"][j]["is_hidden"],
                )

            for area in areas:
                Encounter.objects.create(pokemon=pokemon, area=area)

        self.stdout.write(self.style.SUCCESS("Database was populated with the data."))
