import pandas as pd

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

def strength_index(workout_df, body_df):

    daily = daily_volume(workout_df)

    merged = pd.merge(
        daily,
        body_df,
        on="Date",
        how="left"
    )

    merged["Strength Index"] = (

        merged["Volume"]
        / merged["Weight"]

    )

    return merged


# =====================================================
# GROWTH SCORE
# =====================================================

def growth_score(body_df, strength_df):

    merged = pd.merge(
        body_df,
        strength_df[["Date", "Strength Index"]],
        on="Date",
        how="left"
    )

    merged["Growth Score"] = (

        (merged["Protein Adequacy"] * 35)
        +

        (merged["Strength Index"] * 0.05)
        +

        (
            (
                merged["Calories Intake"]
                - merged["Calories Burned"]
            ) * -0.01
        )

    )

    return merged