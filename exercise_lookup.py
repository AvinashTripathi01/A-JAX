import json
import os


# =====================================================
# EXERCISE DATABASE PATH
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

EXERCISE_DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "exercises.json"
)


# =====================================================
# LOAD EXERCISE DATABASE
# =====================================================

def load_exercise_database():

    if not os.path.exists(
        EXERCISE_DB_PATH
    ):

        return []

    with open(

        EXERCISE_DB_PATH,

        "r",

        encoding="utf-8"

    ) as file:

        exercises = json.load(file)

    return exercises


# =====================================================
# NORMALIZE EXERCISE NAME
# =====================================================

def normalize_exercise_name(name):

    return (

        str(name)
        .lower()
        .strip()
    )


# =====================================================
# CREATE EXERCISE INDEX
# =====================================================

EXERCISE_INDEX = {}

exercise_database = load_exercise_database()

for exercise in exercise_database:

    exercise_name = normalize_exercise_name(

        exercise.get(
            "name",
            ""
        )
    )

    EXERCISE_INDEX[
        exercise_name
    ] = exercise


# =====================================================
# LOOKUP EXERCISE
# =====================================================

def get_exercise_metadata(

    exercise_name
):

    normalized_name = normalize_exercise_name(

        exercise_name
    )

    return EXERCISE_INDEX.get(

        normalized_name,

        {}
    )