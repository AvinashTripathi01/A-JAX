#workout.py
import pandas as pd

from template_engine import (
    save_template,
    get_template_names,
    load_single_template,
    delete_template,
    add_exercise_to_template,
)

from session_engine import (
    create_session_from_template,
    load_sessions,
)

# =====================================================
# CREATE TEMPLATE
# =====================================================

def create_template(

    template_name,

    exercises
):

    rows = []

    for exercise in exercises:

        rows.append({

            "template_name":
                template_name,

            "exercise_name":
                exercise.get(
                    "exercise_name"
                ),

            "sets":
                exercise.get(
                    "sets",
                    3
                ),

            "reps":
                exercise.get(
                    "reps",
                    "10"
                )
        })

    template_df = pd.DataFrame(rows)

    save_template(

        template_name,

        template_df
    )

    return {

        "message":
            "Template Created",

        "template_name":
            template_name,

        "exercise_count":
            len(rows)
    }

# =====================================================
# GET ALL TEMPLATE NAMES
# =====================================================

def get_templates():

    return get_template_names()

# =====================================================
# GET SINGLE TEMPLATE
# =====================================================

def get_template(

    template_name
):

    df = load_single_template(
        template_name
    )

    return df.to_dict(
        orient="records"
    )

# =====================================================
# REMOVE TEMPLATE
# =====================================================

def remove_template(

    template_name
):

    delete_template(
        template_name
    )

    return {

        "message":
            "Template Deleted"
    }

# =====================================================
# CREATE WORKOUT SESSION
# =====================================================

def create_session(

    template_name
):

    template_df = load_single_template(
        template_name
    )

    if template_df.empty:

        return {

            "error":
                "Template Not Found"
        }

    session_id = create_session_from_template(
        template_name, template_df
    )

    return {

        "message":
            "Workout Session Created",

        "session_id":
            session_id
    }

# =====================================================
# LOAD ALL SESSIONS
# =====================================================

def get_sessions():

    df = load_sessions()

    return df.to_dict(
        orient="records"
    )
