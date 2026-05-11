# =====================================================
# exercise.py
# JSON-Based Exercise Intelligence Engine
# =====================================================

import json
import pandas as pd
import os


# =====================================================
# FILE PATH
# =====================================================

EXERCISE_FILE = "data/exercises.json"


# =====================================================
# INTERNAL MUSCLE MAPPING
# =====================================================

MUSCLE_MAPPING = {

    # =================================================
    # CHEST
    # =================================================

    "chest": {
        "muscle_group": "Chest",
        "region": "Middle Chest"
    },

    "pectorals": {
        "muscle_group": "Chest",
        "region": "Middle Chest"
    },

    "upper chest": {
        "muscle_group": "Chest",
        "region": "Upper Chest"
    },

    "lower chest": {
        "muscle_group": "Chest",
        "region": "Lower Chest"
    },

    "pecs": {
        "muscle_group": "Chest",
        "region": "Middle Chest"
    },

    # =================================================
    # BACK
    # =================================================

    "lats": {
        "muscle_group": "Back",
        "region": "Upper Back"
    },

    "latissimus dorsi": {
        "muscle_group": "Back",
        "region": "Upper Back"
    },

    "middle back": {
        "muscle_group": "Back",
        "region": "Middle Back"
    },

    "lower back": {
        "muscle_group": "Back",
        "region": "Lower Back"
    },

    "spine": {
        "muscle_group": "Back",
        "region": "Lower Back"
    },

    "traps": {
        "muscle_group": "Back",
        "region": "Upper Traps"
    },

    "trapezius": {
        "muscle_group": "Back",
        "region": "Upper Traps"
    },

    "rhomboids": {
        "muscle_group": "Back",
        "region": "Middle Back"
    },

    # =================================================
    # SHOULDERS
    # =================================================

    "delts": {
        "muscle_group": "Shoulders",
        "region": "Side Delt"
    },

    "shoulders": {
        "muscle_group": "Shoulders",
        "region": "Front Delt"
    },

    "front delts": {
        "muscle_group": "Shoulders",
        "region": "Front Delt"
    },

    "side delts": {
        "muscle_group": "Shoulders",
        "region": "Side Delt"
    },

    "rear delts": {
        "muscle_group": "Shoulders",
        "region": "Rear Delt"
    },

    # =================================================
    # BICEPS
    # =================================================

    "biceps": {
        "muscle_group": "Biceps",
        "region": "Biceps"
    },

    "brachialis": {
        "muscle_group": "Biceps",
        "region": "Brachialis"
    },

    "brachioradialis": {
        "muscle_group": "Forearms",
        "region": "Forearms"
    },

    # =================================================
    # TRICEPS
    # =================================================

    "triceps": {
        "muscle_group": "Triceps",
        "region": "Triceps"
    },

    # =================================================
    # FOREARMS
    # =================================================

    "forearms": {
        "muscle_group": "Forearms",
        "region": "Forearms"
    },

    # =================================================
    # LEGS
    # =================================================

    "quadriceps": {
        "muscle_group": "Legs",
        "region": "Quadriceps"
    },

    "quads": {
        "muscle_group": "Legs",
        "region": "Quadriceps"
    },

    "hamstrings": {
        "muscle_group": "Legs",
        "region": "Hamstrings"
    },

    "glutes": {
        "muscle_group": "Legs",
        "region": "Glutes"
    },

    "gluteus maximus": {
        "muscle_group": "Legs",
        "region": "Glutes"
    },

    "calves": {
        "muscle_group": "Legs",
        "region": "Calves"
    },

    "adductors": {
        "muscle_group": "Legs",
        "region": "Inner Thigh"
    },

    "abductors": {
        "muscle_group": "Legs",
        "region": "Outer Thigh"
    },

    # =================================================
    # CORE
    # =================================================

    "abdominals": {
        "muscle_group": "Core",
        "region": "Abs"
    },

    "abs": {
        "muscle_group": "Core",
        "region": "Abs"
    },

    "obliques": {
        "muscle_group": "Core",
        "region": "Obliques"
    },

    "hip flexors": {
        "muscle_group": "Core",
        "region": "Hip Flexors"
    },

    # =================================================
    # FULL BODY
    # =================================================

    "full body": {
        "muscle_group": "Full Body",
        "region": "Full Body"
    }
}

# =====================================================
# LOAD EXERCISES JSON
# =====================================================

def load_exercises():

    if not os.path.exists(EXERCISE_FILE):

        return pd.DataFrame()

    with open(EXERCISE_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    exercise_list = []

    for exercise in data:

        primary_muscles = exercise.get(
            "primaryMuscles",
            []
        )

        secondary_muscles = exercise.get(
            "secondaryMuscles",
            []
        )

        # ---------------------------------------------
        # INTERNAL MAPPING
        # ---------------------------------------------

        internal_group = "Unknown"

        internal_region = "Unknown"

        if len(primary_muscles) > 0:

            primary = primary_muscles[0].lower()

            mapping = MUSCLE_MAPPING.get(primary)

            if mapping:

                internal_group = mapping[
                    "muscle_group"
                ]

                internal_region = mapping[
                    "region"
                ]

        # ---------------------------------------------
        # NORMALIZED STRUCTURE
        # ---------------------------------------------

        exercise_list.append({

            "exercise_id":
                exercise.get("id"),

            "exercise_name":
                exercise.get("name"),

            "force":
                exercise.get("force"),

            "level":
                exercise.get("level"),

            "mechanic":
                exercise.get("mechanic"),

            "equipment":
                exercise.get("equipment"),

            "primary_muscles":
                primary_muscles,

            "secondary_muscles":
                secondary_muscles,

            "category":
                exercise.get("category"),

            "instructions":
                exercise.get("instructions", []),

            "images":
                exercise.get("images", []),

            "internal_muscle_group":
                internal_group,

            "internal_region":
                internal_region
        })

    df = pd.DataFrame(exercise_list)

    return df


# =====================================================
# SEARCH EXERCISES
# =====================================================

def search_exercises(df, keyword):

    if df.empty:

        return df

    keyword = keyword.lower()

    return df[

        df["exercise_name"]
        .str.lower()
        .str.contains(keyword, na=False)
    ]


# =====================================================
# FILTER BY MUSCLE GROUP
# =====================================================

def filter_by_muscle_group(df, muscle_group):

    if df.empty:

        return df

    return df[

        df["internal_muscle_group"]
        .str.lower() == muscle_group.lower()
    ]


# =====================================================
# FILTER BY REGION
# =====================================================

def filter_by_region(df, region):

    if df.empty:

        return df

    return df[

        df["internal_region"]
        .str.lower() == region.lower()
    ]


# =====================================================
# FILTER BY EQUIPMENT
# =====================================================

def filter_by_equipment(df, equipment):

    if df.empty:

        return df

    return df[

        df["equipment"]
        .fillna("")
        .str.lower()
        .str.contains(equipment.lower())
    ]


# =====================================================
# FILTER BY LEVEL
# =====================================================

def filter_by_level(df, level):

    if df.empty:

        return df

    return df[

        df["level"]
        .fillna("")
        .str.lower() == level.lower()
    ]


# =====================================================
# FILTER BY MECHANIC
# =====================================================

def filter_by_mechanic(df, mechanic):

    if df.empty:

        return df

    return df[

        df["mechanic"]
        .fillna("")
        .str.lower() == mechanic.lower()
    ]


# =====================================================
# RECOMMEND EXERCISES
# =====================================================

def recommend_exercises(

    exercise_df,

    muscle_group=None,

    equipment=None,

    level=None,

    mechanic=None,

    limit=20
):

    # ============================================
    # COPY DATAFRAME
    # ============================================

    filtered_df = exercise_df.copy()

    # ============================================
    # MUSCLE GROUP FILTER
    # ============================================

    if muscle_group:

        filtered_df = filtered_df[

            filtered_df[
                "internal_muscle_group"
            ]
            .str.lower()
            ==
            muscle_group.lower()
        ]

    # ============================================
    # EQUIPMENT FILTER
    # ============================================

    if equipment:

        filtered_df = filtered_df[

            filtered_df[
                "equipment"
            ]
            .str.lower()
            ==
            equipment.lower()
        ]

    # ============================================
    # LEVEL FILTER
    # ============================================

    if level:

        filtered_df = filtered_df[

            filtered_df[
                "level"
            ]
            .str.lower()
            ==
            level.lower()
        ]

    # ============================================
    # MECHANIC FILTER
    # ============================================

    if mechanic:

        filtered_df = filtered_df[

            filtered_df[
                "mechanic"
            ]
            .str.lower()
            ==
            mechanic.lower()
        ]

    # ============================================
    # LIMIT RESULTS
    # ============================================

    filtered_df = filtered_df.head(limit)

    # ============================================
    # RETURN
    # ============================================

    return filtered_df


# =====================================================
# GET UNIQUE VALUES
# =====================================================

def get_unique_muscle_groups(df):

    return sorted(

        df["internal_muscle_group"]
        .dropna()
        .unique()
        .tolist()
    )


def get_unique_regions(df):

    return sorted(

        df["internal_region"]
        .dropna()
        .unique()
        .tolist()
    )


def get_unique_levels(df):

    return sorted(

        df["level"]
        .dropna()
        .unique()
        .tolist()
    )


def get_unique_mechanics(df):

    return sorted(

        df["mechanic"]
        .dropna()
        .unique()
        .tolist()
    )


def get_unique_equipment(df):

    return sorted(

        df["equipment"]
        .dropna()
        .unique()
        .tolist()
    )


# =====================================================
# GET EXERCISE DETAILS
# =====================================================

def get_exercise_details(df, exercise_name):

    filtered = df[

        df["exercise_name"]
        == exercise_name
    ]

    if filtered.empty:

        return None

    return filtered.iloc[0].to_dict()


# =====================================================
# QUICK TEST
# =====================================================

if __name__ == "__main__":

    df = load_exercises()

    print()

    print("Total Exercises:", len(df))

    print()

    print(df.head())

    print()

    chest_exercises = recommend_exercises(

        df,

        muscle_group="Core",

        limit=5
    )

    print(chest_exercises[
        [
            "exercise_name",
            "equipment",
            "mechanic",
            "level"
        ]
    ])