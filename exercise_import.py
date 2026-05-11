import requests
import pandas as pd
import os
import time

# =====================================================
# CREATE DATA FOLDER
# =====================================================

os.makedirs("data", exist_ok=True)

# =====================================================
# API CONFIG
# =====================================================

BASE_URL = "https://oss.exercisedb.dev/api/v1/exercises"

# =====================================================
# STORAGE
# =====================================================

all_exercises = []

visited_cursors = set()

next_cursor = None

page_count = 1

MAX_EXERCISES = 1500

# =====================================================
# PAGINATION LOOP
# =====================================================

while True:

    print(f"\n📦 Fetching Page {page_count}...")

    try:

        # -------------------------------------------------
        # API REQUEST
        # -------------------------------------------------

        if next_cursor is None:

            response = requests.get(BASE_URL)

        else:

            response = requests.get(

                BASE_URL,

                params={
                    "cursor": next_cursor
                }
            )

        # -------------------------------------------------
        # STATUS CHECK
        # -------------------------------------------------

        print("Status:", response.status_code)

        if response.status_code != 200:

            print("❌ Request Failed")

            break

        # -------------------------------------------------
        # JSON RESPONSE
        # -------------------------------------------------

        data = response.json()

        # -------------------------------------------------
        # EXERCISES
        # -------------------------------------------------

        exercises = data.get("data", [])

        all_exercises.extend(exercises)

        print(
            f"✅ Exercises Collected: {len(all_exercises)}"
        )

        # -------------------------------------------------
        # SAFETY LIMIT
        # -------------------------------------------------

        if len(all_exercises) >= MAX_EXERCISES:

            print("\n⚠️ Safety Limit Reached")

            break

        # -------------------------------------------------
        # META
        # -------------------------------------------------

        meta = data.get("meta", {})

        has_next = meta.get("hasNextPage", False)

        next_cursor = meta.get("nextCursor")

        # -------------------------------------------------
        # REPEATED CURSOR PROTECTION
        # -------------------------------------------------

        if next_cursor in visited_cursors:

            print("\n⚠️ Repeated Cursor Detected")

            print("Stopping Pagination")

            break

        visited_cursors.add(next_cursor)

        # -------------------------------------------------
        # NO MORE PAGES
        # -------------------------------------------------

        if not has_next:

            print("\n✅ No More Pages")

            break

        # -------------------------------------------------
        # NEXT PAGE
        # -------------------------------------------------

        page_count += 1

        # -------------------------------------------------
        # SMALL DELAY
        # -------------------------------------------------

        time.sleep(1)

    except Exception as e:

        print("\n❌ ERROR OCCURRED")

        print(e)

        break

# =====================================================
# CLEAN DATA
# =====================================================

exercise_list = []

for exercise in all_exercises:

    exercise_list.append({

        "Exercise ID": exercise.get("exerciseId"),

        "Exercise Name": exercise.get("name"),

        "Body Part": ", ".join(
            exercise.get("bodyParts", [])
        ),

        "Target Muscle": ", ".join(
            exercise.get("targetMuscles", [])
        ),

        "Secondary Muscles": ", ".join(
            exercise.get("secondaryMuscles", [])
        ),

        "Equipment": ", ".join(
            exercise.get("equipments", [])
        ),

        "GIF URL": exercise.get("gifUrl")

    })

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame(exercise_list)

# =====================================================
# REMOVE DUPLICATES
# =====================================================

df.drop_duplicates(

    subset=["Exercise ID"],

    inplace=True
)

# =====================================================
# RESET INDEX
# =====================================================

df.reset_index(

    drop=True,

    inplace=True
)

# =====================================================
# SAVE CSV
# =====================================================

df.to_csv(

    "data/exercises.csv",

    index=False
)

# =====================================================
# SUCCESS
# =====================================================

print("\n✅ EXERCISES IMPORT COMPLETED")

print()

print("Total Unique Exercises:", len(df))

print()

print(df.head())