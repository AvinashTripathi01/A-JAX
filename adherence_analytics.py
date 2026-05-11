import pandas as pd


# =====================================================
# ADHERENCE SCORE
# =====================================================


def calculate_adherence(session_df):

    if session_df.empty:

        return 0

    total_exercises = len(session_df)

    completed = len(

        session_df[
            session_df["status"] == "completed"
        ]
    )

    adherence = (
        completed / total_exercises
    ) * 100

    return round(adherence, 2)


# =====================================================
# SKIPPED EXERCISES
# =====================================================


def skipped_exercises(session_df):

    skipped_df = session_df[
        session_df["status"] == "skipped"
    ]

    return skipped_df


# =====================================================
# REPLACED EXERCISES
# =====================================================


def replaced_exercises(session_df):

    replaced_df = session_df[
        session_df["status"] == "replaced"
    ]

    return replaced_df


# =====================================================
# COMPLETED EXERCISES
# =====================================================


def completed_exercises(session_df):

    completed_df = session_df[
        session_df["status"] == "completed"
    ]

    return completed_df