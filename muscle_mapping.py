# =====================================================
# muscle_mapping.py
# Central Muscle Intelligence Engine
# =====================================================

from collections import defaultdict


# =====================================================
# MECHANIC WEIGHTS
# =====================================================

MECHANIC_DISTRIBUTION = {

    "isolation": {
        "primary": 0.85,
        "secondary": 0.15
    },

    "compound": {
        "primary": 0.60,
        "secondary": 0.40
    },

    "static": {
        "primary": 0.70,
        "secondary": 0.30
    }
}


# =====================================================
# NORMALIZE MUSCLE NAMES
# =====================================================

MUSCLE_NORMALIZATION = {

    "chest": "chest",
    "pectorals": "chest",

    "lats": "lats",
    "latissimus dorsi": "lats",

    "middle back": "middle_back",
    "lower back": "lower_back",

    "traps": "traps",

    "shoulders": "shoulders",
    "delts": "shoulders",

    "biceps": "biceps",
    "triceps": "triceps",

    "forearms": "forearms",

    "quadriceps": "quads",
    "quads": "quads",

    "hamstrings": "hamstrings",

    "glutes": "glutes",

    "calves": "calves",

    "abdominals": "abs",
    "abs": "abs",

    "obliques": "obliques",

    "adductors": "adductors",
    "abductors": "abductors"
}


# =====================================================
# NORMALIZE SINGLE MUSCLE
# =====================================================

def normalize_muscle(muscle):

    if not muscle:

        return None

    muscle = (

        str(muscle)
        .lower()
        .strip()
    )

    # =====================================
    # REMOVE BAD CHARACTERS
    # =====================================

    muscle = muscle.replace(
        "-",
        " "
    )

    muscle = muscle.replace(
        "_",
        " "
    )

    muscle = " ".join(
        muscle.split()
    )

    normalized = MUSCLE_NORMALIZATION.get(
        muscle,
        muscle
    )

    return normalized


# =====================================================
# APPLY NAME-BASED MODIFIERS
# =====================================================

def apply_name_modifiers(
    exercise_name,
    muscle_map
):

    name = exercise_name.lower()

    # ---------------------------------------------
    # INCLINE PRESS
    # ---------------------------------------------

    if "incline" in name:

        if "chest" in muscle_map:

            muscle_map["upper_chest"] = (
                muscle_map["chest"] * 0.25
            )

            muscle_map["chest"] *= 0.75

    # ---------------------------------------------
    # HAMMER CURL
    # ---------------------------------------------

    if "hammer" in name:

        muscle_map["brachialis"] = 0.15
        muscle_map["forearms"] = 0.10

        if "biceps" in muscle_map:

            muscle_map["biceps"] *= 0.75

    # ---------------------------------------------
    # WIDE GRIP
    # ---------------------------------------------

    if "wide" in name:

        if "lats" in muscle_map:

            muscle_map["upper_back"] = 0.10

    return muscle_map


# =====================================================
# NORMALIZE FINAL DISTRIBUTION
# =====================================================

def normalize_distribution(muscle_map):

    # =====================================
    # REMOVE INVALID VALUES
    # =====================================

    muscle_map = {

        k: v

        for k, v in muscle_map.items()

        if v > 0
    }

    total = sum(
        muscle_map.values()
    )

    if total == 0:

        return muscle_map

    for muscle in muscle_map:

        muscle_map[muscle] = round(

            muscle_map[muscle] / total,

            4
        )

    return dict(muscle_map)


# =====================================================
# GENERATE MUSCLE MAP
# =====================================================

def generate_muscle_map(exercise):

    primary_muscles = exercise.get(
        "primaryMuscles",
        []
    )

    secondary_muscles = exercise.get(
        "secondaryMuscles",
        []
    )

    mechanic = exercise.get(
        "mechanic",
        "compound"
    )

    exercise_name = exercise.get(
        "name",
        ""
    )

    distribution = MECHANIC_DISTRIBUTION.get(

        mechanic,

        MECHANIC_DISTRIBUTION["compound"]
    )

    primary_weight = distribution["primary"]

    secondary_weight = distribution["secondary"]

    muscle_map = defaultdict(float)

    # =================================================
    # PRIMARY MUSCLES
    # =================================================

    if primary_muscles:

        primary_share = (

            primary_weight
            /
            len(primary_muscles)
        )

        for muscle in primary_muscles:

            normalized = normalize_muscle(
                muscle
            )

            if normalized:

                muscle_map[normalized] += (
                    primary_share
                )

    # =================================================
    # SECONDARY MUSCLES
    # =================================================

    if secondary_muscles:

        secondary_share = (

            secondary_weight
            /
            len(secondary_muscles)
        )

        for muscle in secondary_muscles:

            normalized = normalize_muscle(
                muscle
            )

            if normalized:

                muscle_map[normalized] += (
                    secondary_share
                )

    # =================================================
    # APPLY MODIFIERS
    # =================================================

    muscle_map = apply_name_modifiers(

        exercise_name,

        muscle_map
    )

    # =================================================
    # NORMALIZE FINAL OUTPUT
    # =================================================

    muscle_map = normalize_distribution(
        muscle_map
    )

    # =================================================
    # REMOVE INVALID MUSCLES
    # =================================================

    cleaned_map = {}

    for muscle, value in muscle_map.items():

        if muscle and value > 0:

            cleaned_map[muscle] = value

    return cleaned_map