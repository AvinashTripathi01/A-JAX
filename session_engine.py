#session_engine.py
import pandas as pd
import os

from datetime import datetime


# =====================================================
# BASE PATHS
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

SESSION_DIR = os.path.join(
    DATA_DIR,
    "sessions"
)

# =====================================================
# CREATE SESSIONS FOLDER
# =====================================================

os.makedirs(

    SESSION_DIR,

    exist_ok=True
)


# =====================================================
# CREATE SESSION FROM TEMPLATE
# =====================================================

def create_session_from_template(

    template_name,

    template_df
):

    # =========================================
    # GENERATE UNIQUE SESSION ID
    # =========================================

    session_id = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    # =========================================
    # SESSION START TIME
    # =========================================

    session_start_time = datetime.now()

    # =========================================
    # BUILD SESSION ROWS
    # =========================================

    session_rows = []

    for _, row in template_df.iterrows():

        session_rows.append({

            "session_id": session_id,

            "date": datetime.now().strftime(
                "%Y-%m-%d"
            ),

            "template_name": template_name,

            # =====================================
            # SESSION METADATA
            # =====================================

            "start_time": session_start_time.isoformat(),

            "end_time": "",

            "duration_minutes": 0,

            # =====================================
            # EXERCISE DATA
            # =====================================

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

            "completed": False,

            "status": "planned",

            "notes": "",

            "rest_timer": 90
        })

    # =========================================
    # CREATE SESSION DATAFRAME
    # =========================================

    session_df = pd.DataFrame(
        session_rows
    )

    # =========================================
    # FIX NaN VALUES
    # =========================================

    session_df = session_df.fillna("")

    # =========================================
    # SAVE SESSION FILE
    # =========================================

    session_file = os.path.join(

        SESSION_DIR,

        f"{session_id}.csv"
    )

    session_df.to_csv(

        session_file,

        index=False
    )

    # =========================================
    # RETURN SESSION ID
    # =========================================

    return session_id


# =====================================================
# LOAD SINGLE SESSION
# =====================================================

def get_session(

    session_id
):

    session_file = os.path.join(

        SESSION_DIR,

        f"{session_id}.csv"
    )

    # =========================================
    # CHECK FILE EXISTS
    # =========================================

    if not os.path.exists(
        session_file
    ):

        return []

    # =========================================
    # LOAD SESSION
    # =========================================

    df = pd.read_csv(
        session_file
    )

    # =========================================
    # FIX NaN VALUES
    # =========================================

    df = df.fillna("")

    # =========================================
    # SAFE RECORDS
    # =========================================

    records = df.to_dict(
        orient="records"
    )

    # =========================================
    # CLEAN INVALID VALUES
    # =========================================

    for row in records:

        for key, value in row.items():

            if pd.isna(value):

                row[key] = ""

    return records


# =====================================================
# UPDATE SESSION EXERCISE
# =====================================================

def update_session_exercise(

    session_id,

    exercise_name,

    updated_fields
):

    session_file = os.path.join(

        SESSION_DIR,

        f"{session_id}.csv"
    )

    # =========================================
    # CHECK FILE EXISTS
    # =========================================

    if not os.path.exists(
        session_file
    ):

        return {

            "message":
                "Session Not Found"
        }

    # =========================================
    # LOAD SESSION
    # =========================================

    df = pd.read_csv(
        session_file
    )

    # =========================================
    # FIND EXERCISE
    # =========================================

    mask = (

        df["exercise_name"]

        ==

        exercise_name
    )

    # =========================================
    # UPDATE FIELDS
    # =========================================

    for key, value in updated_fields.items():

        if key in df.columns:

            df.loc[
                mask,
                key
            ] = value

    # =========================================
    # FIX NaN VALUES
    # =========================================

    df = df.fillna("")

    # =========================================
    # SAVE SESSION
    # =========================================

    df.to_csv(

        session_file,

        index=False
    )

    return {

        "message":
            "Session Exercise Updated"
    }


# =====================================================
# COMPLETE SESSION
# =====================================================

def complete_session(

    session_id
):

    session_file = os.path.join(

        SESSION_DIR,

        f"{session_id}.csv"
    )

    # =========================================
    # CHECK FILE EXISTS
    # =========================================

    if not os.path.exists(
        session_file
    ):

        return {

            "message":
                "Session Not Found"
        }

    # =========================================
    # LOAD SESSION
    # =========================================

    df = pd.read_csv(
        session_file
    )

    # =========================================
    # END TIME
    # =========================================

    end_time = datetime.now()

    # =========================================
    # START TIME
    # =========================================

    start_time = datetime.fromisoformat(

        str(
            df.iloc[0]["start_time"]
        )
    )

    # =========================================
    # DURATION
    # =========================================

    duration_minutes = (

        end_time - start_time

    ).total_seconds() / 60

    # =========================================
    # MARK COMPLETED
    # =========================================

    df["status"] = "completed"

    df["completed"] = True

    # =========================================
    # SAVE METADATA
    # =========================================

    df["end_time"] = end_time.isoformat()

    df["duration_minutes"] = round(

        duration_minutes,

        2
    )

    # =========================================
    # FIX NaN VALUES
    # =========================================

    df = df.fillna("")

    # =========================================
    # SAVE SESSION
    # =========================================

    df.to_csv(

        session_file,

        index=False
    )

    # =========================================
    # SAVE TO ANALYTICS LOG
    # =========================================

    from analytics_engine import (

        save_session_to_workout_log
    )

    completed_session_df = df[

        df["session_id"] == session_id

    ]

    save_session_to_workout_log(

        completed_session_df
    )

    # =========================================
    # RETURN
    # =========================================

    return {

        "message":
            "Workout Completed",

        "duration_minutes":
            round(duration_minutes, 2)
    }


# =====================================================
# LOAD ALL SESSIONS
# =====================================================

def load_sessions():

    sessions = []

    for file in os.listdir(

        SESSION_DIR
    ):

        if file.endswith(".csv"):

            sessions.append(file)

    return sessions

# =====================================================
# LOAD SINGLE SESSION
# =====================================================

def load_single_session(
    session_id
):

    import pandas as pd

    session_path = (
        f"sessions/{session_id}.csv"
    )

    df = pd.read_csv(
        session_path
    )

    return df.to_dict(
        orient="records"
    )

