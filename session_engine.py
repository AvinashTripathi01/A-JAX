import pandas as pd
import os
from datetime import datetime


# =====================================================
# FILE PATH
# =====================================================

SESSION_FILE = "data/workout_sessions.csv"


# =====================================================
# CREATE FILE IF NOT EXISTS
# =====================================================


def initialize_sessions():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(SESSION_FILE):

        df = pd.DataFrame(columns=[

            "session_id",
            "date",
            "template_name",
            "exercise_name",
            "planned_sets",
            "planned_reps",
            "actual_sets",
            "actual_reps",
            "weight",
            "status",
            "notes"
        ])

        df.to_csv(SESSION_FILE, index=False)


# =====================================================
# LOAD SESSIONS
# =====================================================


def load_sessions():

    initialize_sessions()

    return pd.read_csv(SESSION_FILE)


# =====================================================
# CREATE SESSION FROM TEMPLATE
# =====================================================


def create_session_from_template(template_df):

    session_id = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    session_rows = []

    for _, row in template_df.iterrows():

        session_rows.append({

            "session_id": session_id,

            "date": datetime.now().strftime(
                "%Y-%m-%d"
            ),

            "template_name": row[
                "template_name"
            ],

            "exercise_name": row[
                "exercise_name"
            ],

            "planned_sets": row[
                "sets"
            ],

            "planned_reps": row[
                "reps"
            ],

            "actual_sets": row[
                "sets"
            ],

            "actual_reps": row[
                "reps"
            ],

            "weight": 0,

            "status": "planned",

            "notes": ""
        })

    session_df = pd.DataFrame(session_rows)

    existing_df = load_sessions()

    final_df = pd.concat([
        existing_df,
        session_df
    ], ignore_index=True)

    final_df.to_csv(
        SESSION_FILE,
        index=False
    )

    return session_id