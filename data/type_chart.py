
TYPE_CHART = {

    # ---------- Normal ----------
    ("normal", "rock"): 0.5,
    ("normal", "ghost"): 0.0,
    ("normal", "steel"): 0.5,

    # ---------- Fire ----------
    ("fire", "grass"): 2.0,
    ("fire", "ice"): 2.0,
    ("fire", "bug"): 2.0,
    ("fire", "steel"): 2.0,
    ("fire", "fire"): 0.5,
    ("fire", "water"): 0.5,
    ("fire", "rock"): 0.5,
    ("fire", "dragon"): 0.5,

    # ---------- Water ----------
    ("water", "fire"): 2.0,
    ("water", "ground"): 2.0,
    ("water", "rock"): 2.0,
    ("water", "water"): 0.5,
    ("water", "grass"): 0.5,
    ("water", "dragon"): 0.5,

    # ---------- Electric ----------
    ("electric", "water"): 2.0,
    ("electric", "flying"): 2.0,
    ("electric", "electric"): 0.5,
    ("electric", "grass"): 0.5,
    ("electric", "dragon"): 0.5,
    ("electric", "ground"): 0.0,

    # ---------- Grass ----------
    ("grass", "water"): 2.0,
    ("grass", "ground"): 2.0,
    ("grass", "rock"): 2.0,
    ("grass", "fire"): 0.5,
    ("grass", "grass"): 0.5,
    ("grass", "poison"): 0.5,
    ("grass", "flying"): 0.5,
    ("grass", "bug"): 0.5,
    ("grass", "dragon"): 0.5,
    ("grass", "steel"): 0.5,

    # ---------- Ice ----------
    ("ice", "grass"): 2.0,
    ("ice", "ground"): 2.0,
    ("ice", "flying"): 2.0,
    ("ice", "dragon"): 2.0,
    ("ice", "fire"): 0.5,
    ("ice", "water"): 0.5,
    ("ice", "ice"): 0.5,
    ("ice", "steel"): 0.5,

    # ---------- Fighting ----------
    ("fighting", "normal"): 2.0,
    ("fighting", "ice"): 2.0,
    ("fighting", "rock"): 2.0,
    ("fighting", "dark"): 2.0,
    ("fighting", "steel"): 2.0,
    ("fighting", "poison"): 0.5,
    ("fighting", "flying"): 0.5,
    ("fighting", "psychic"): 0.5,
    ("fighting", "bug"): 0.5,
    ("fighting", "fairy"): 0.5,
    ("fighting", "ghost"): 0.0,

    # ---------- Poison ----------
    ("poison", "grass"): 2.0,
    ("poison", "fairy"): 2.0,
    ("poison", "poison"): 0.5,
    ("poison", "ground"): 0.5,
    ("poison", "rock"): 0.5,
    ("poison", "ghost"): 0.5,
    ("poison", "steel"): 0.0,

    # ---------- Ground ----------
    ("ground", "fire"): 2.0,
    ("ground", "electric"): 2.0,
    ("ground", "poison"): 2.0,
    ("ground", "rock"): 2.0,
    ("ground", "steel"): 2.0,
    ("ground", "grass"): 0.5,
    ("ground", "bug"): 0.5,
    ("ground", "flying"): 0.0,
}


def type_multiplier(move_type, defender_types):
    mult = 1.0

    for t in defender_types:
        mult *= TYPE_CHART.get(
            (move_type.lower(), t.lower()),
            1.0,
        )

    return mult


print("✅ type_chart.py v2 Ready")

# ---------- Flying ----------
TYPE_CHART.update({
    ("flying", "grass"): 2.0,
    ("flying", "fighting"): 2.0,
    ("flying", "bug"): 2.0,
    ("flying", "electric"): 0.5,
    ("flying", "rock"): 0.5,
    ("flying", "steel"): 0.5,
})

# ---------- Psychic ----------
TYPE_CHART.update({
    ("psychic", "fighting"): 2.0,
    ("psychic", "poison"): 2.0,
    ("psychic", "psychic"): 0.5,
    ("psychic", "steel"): 0.5,
    ("psychic", "dark"): 0.0,
})

# ---------- Bug ----------
TYPE_CHART.update({
    ("bug", "grass"): 2.0,
    ("bug", "psychic"): 2.0,
    ("bug", "dark"): 2.0,
    ("bug", "fire"): 0.5,
    ("bug", "fighting"): 0.5,
    ("bug", "poison"): 0.5,
    ("bug", "flying"): 0.5,
    ("bug", "ghost"): 0.5,
    ("bug", "steel"): 0.5,
    ("bug", "fairy"): 0.5,
})

# ---------- Rock ----------
TYPE_CHART.update({
    ("rock", "fire"): 2.0,
    ("rock", "ice"): 2.0,
    ("rock", "flying"): 2.0,
    ("rock", "bug"): 2.0,
    ("rock", "fighting"): 0.5,
    ("rock", "ground"): 0.5,
    ("rock", "steel"): 0.5,
})

# ---------- Ghost ----------
TYPE_CHART.update({
    ("ghost", "psychic"): 2.0,
    ("ghost", "ghost"): 2.0,
    ("ghost", "dark"): 0.5,
    ("ghost", "normal"): 0.0,
})

# ---------- Dragon ----------
TYPE_CHART.update({
    ("dragon", "dragon"): 2.0,
    ("dragon", "steel"): 0.5,
    ("dragon", "fairy"): 0.0,
})

# ---------- Dark ----------
TYPE_CHART.update({
    ("dark", "psychic"): 2.0,
    ("dark", "ghost"): 2.0,
    ("dark", "fighting"): 0.5,
    ("dark", "dark"): 0.5,
    ("dark", "fairy"): 0.5,
})

# ---------- Steel ----------
TYPE_CHART.update({
    ("steel", "ice"): 2.0,
    ("steel", "rock"): 2.0,
    ("steel", "fairy"): 2.0,
    ("steel", "fire"): 0.5,
    ("steel", "water"): 0.5,
    ("steel", "electric"): 0.5,
    ("steel", "steel"): 0.5,
})

# ---------- Fairy ----------
TYPE_CHART.update({
    ("fairy", "fighting"): 2.0,
    ("fairy", "dragon"): 2.0,
    ("fairy", "dark"): 2.0,
    ("fairy", "fire"): 0.5,
    ("fairy", "poison"): 0.5,
    ("fairy", "steel"): 0.5,
})

print("✅ type_chart.py v3 Ready")
