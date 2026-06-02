#analytics_engine.py
import pandas as pd
import os
from muscle_mapping import generate_muscle_map
from exercise_lookup import (
    get_exercise_metadata
)
MUSCLE_LOG_PATH = "data/muscle_volume_log.csv"
# =====================================================
# SESSION ANALYTICS
# =====================================================

def calculate_session_volume(session_df):

    session_df["set_volume"] = (

        session_df["actual_sets"]
        *
        session_df["actual_reps"]
        *
        session_df["weight"]

    )

    return round(
        session_df["set_volume"].sum(),
        2
    )

def calculate_completed_sets(session_df):

    completed = session_df[

        session_df["status"] == "completed"

    ]

    return int(
        completed["actual_sets"].sum()
    )

def calculate_total_reps(session_df):

    total_reps = (

        session_df["actual_sets"]
        *
        session_df["actual_reps"]

    ).sum()

    return int(total_reps)

def calculate_completion_percentage(session_df):

    total = len(session_df)

    if total == 0:

        return 0

    completed = len(

        session_df[
            session_df["status"] == "completed"
        ]

    )

    return round(
        (completed / total) * 100,
        2
    )

def calculate_average_weight(session_df):

    if len(session_df) == 0:

        return 0

    return round(
        session_df["weight"].mean(),
        2
    )

def calculate_workout_duration(

    start_time,
    end_time

):

    duration = (
        end_time - start_time
    ).total_seconds()

    return round(
        duration / 60,
        2
    )

def detect_prs(

    session_df,
    historical_df

):

    prs = []

    for _, row in session_df.iterrows():

        exercise = row["exercise_name"]

        current_weight = row["weight"]

        history = historical_df[

            historical_df["exercise_name"]
            == exercise

        ]

        if history.empty:

            prs.append(exercise)

            continue

        max_weight = history["weight"].max()

        if current_weight > max_weight:

            prs.append(exercise)

    return prs

# =====================================================
# WORKOUT DENSITY
# =====================================================

def calculate_workout_density(

    session_df
):

    # =========================================
    # TOTAL VOLUME
    # =========================================

    total_volume = calculate_session_volume(
        session_df
    )

    # =========================================
    # DURATION
    # =========================================

    duration = float(

        session_df.iloc[0][
            "duration_minutes"
        ]
    )

    # =========================================
    # AVOID DIVISION ERROR
    # =========================================

    if duration <= 0:

        return 0

    # =========================================
    # DENSITY
    # =========================================

    density = (

        total_volume / duration
    )

    return round(
        density,
        2
    )
# =====================================================
# WORKOUT VOLUME
# =====================================================

def calculate_volume(workout_df):

    workout_df["Volume"] = (

        workout_df["Sets"]
        * workout_df["Reps"]
        * workout_df["Weight (kg)"]

    )

    return workout_df


# =====================================================
# DAILY VOLUME
# =====================================================

def daily_volume(workout_df):

    daily = workout_df.groupby("Date")["Volume"].sum()

    return daily.reset_index()


# =====================================================
# MUSCLE VOLUME
# =====================================================

def muscle_volume(workout_df):

    muscle = workout_df.groupby(

        [
            "Muscle Group",
            "Region",
            "Target Muscles"
        ]

    )["Volume"].sum()

    return muscle.reset_index()


# =====================================================
# PROTEIN ADEQUACY
# =====================================================

def protein_adequacy(body_df):

    body_df["Protein Adequacy"] = (

        body_df["Protein"]
        / body_df["Weight"]

    )

    return body_df


# =====================================================
# CALORIE BALANCE
# =====================================================

def calorie_balance(body_df):

    body_df["Calorie Balance"] = (

        body_df["Calories Intake"]
        - body_df["Calories Burned"]

    )

    return body_df


# =====================================================
# STRENGTH INDEX
# =====================================================

def work_capacity_index(workout_df, body_df):

    daily = daily_volume(workout_df)

    merged = pd.merge(
        daily,
        body_df,
        on="Date",
        how="left"
    )

    merged["Work Capacity Index"] = (

        merged["Volume"]
        / merged["Weight"]

    )

    return merged


# =====================================================
# GROWTH SCORE
# =====================================================

def growth_score(body_df, capacity_df):

    merged = pd.merge(
        body_df,
        capacity_df[["Date", "Work Capacity Index"]],
        on="Date",
        how="left"
    )

    merged["Growth Score"] = (

        (merged["Protein Adequacy"] * 35)
        +

        (merged["Work Capacity Index"] * 0.05)
        +

        (
            (
                merged["Calories Intake"]
                - merged["Calories Burned"]
            ) * -0.01
        )

    )

    return merged

# =====================================================
# SAVE MUSCLE VOLUME LOG
# =====================================================

def save_muscle_volume_log(

    session_df,

    muscle_log_path=MUSCLE_LOG_PATH
):

    muscle_rows = []

    # =========================================
    # LOOP EXERCISES
    # =========================================

    for _, row in session_df.iterrows():

        # -------------------------------------
        # FETCH EXERCISE METADATA
        # -------------------------------------

        exercise = get_exercise_metadata(
    row["exercise_name"]
)
        if not exercise:

         continue
        # -------------------------------------
        # GENERATE MUSCLE MAP
        # -------------------------------------

        muscle_map = generate_muscle_map(
            exercise
        )

        # -------------------------------------
        # EXERCISE VOLUME
        # -------------------------------------

        exercise_volume = (

            row["actual_sets"]
            *
            row["actual_reps"]
            *
            row["weight"]

        )

        # -------------------------------------
        # ALLOCATE VOLUME
        # -------------------------------------

        for muscle, distribution in muscle_map.items():

            allocated_volume = (

                exercise_volume
                *
                distribution

            )

            muscle_rows.append({

                "date":
                    row["date"],

                "session_id":
                    row["session_id"],

                "exercise_name":
                    row["exercise_name"],

                "muscle":
                    muscle,

                "distribution":
                    distribution,

                "allocated_volume":
                    round(
                        allocated_volume,
                        2
                    )
            })

    # =========================================
    # CREATE DATAFRAME
    # =========================================

    muscle_df = pd.DataFrame(
        muscle_rows
    )

    # =========================================
    # LOAD EXISTING LOG
    # =========================================

    if os.path.exists(
        muscle_log_path
    ):

        existing_df = pd.read_csv(
            muscle_log_path
        )

    else:

        existing_df = pd.DataFrame()

    # =========================================
    # APPEND
    # =========================================

    final_df = pd.concat(

        [
            existing_df,
            muscle_df
        ],

        ignore_index=True
    )

    # =========================================
    # SAVE
    # =========================================

    final_df.to_csv(

        muscle_log_path,

        index=False
    )

    return muscle_df

# =====================================================
# SAVE SESSION TO WORKOUT LOG
# =====================================================

def save_session_to_workout_log(

    session_df,

    workout_log_path="data/Workout_Log.csv"
):

    # =========================================
    # CREATE VOLUME
    # =========================================

    session_df["volume"] = (

    session_df["actual_sets"]
    *

    session_df["actual_reps"]
    *

    session_df["weight"]

)
    
    session_df["workout_density"] = (

    calculate_workout_density(
        session_df
    )
)

    # =========================================
    # LOAD EXISTING LOG
    # =========================================

    if os.path.exists(
        workout_log_path
    ):

        existing_df = pd.read_csv(
            workout_log_path
        )

    else:

        existing_df = pd.DataFrame()

    # =========================================
    # APPEND SESSION
    # =========================================

    final_df = pd.concat(

        [
            existing_df,
            session_df
        ],

        ignore_index=True
    )

    # =========================================
    # SAVE
    # =========================================

    final_df.to_csv(

        workout_log_path,

        index=False
    )
    # =========================================
    # SAVE MUSCLE ANALYTICS
    # =========================================

    save_muscle_volume_log(
        session_df
    )
    return {

        "message":
            "Workout Logged Successfully"
    }