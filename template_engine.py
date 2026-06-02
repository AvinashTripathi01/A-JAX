# template_engine.py

import pandas as pd
import os
from pandas.errors import EmptyDataError

# =====================================================
# TEMPLATE DIRECTORY
# =====================================================

TEMPLATE_DIR = "data/templates"

os.makedirs(
    TEMPLATE_DIR,
    exist_ok=True
)

# =====================================================
# DEFAULT TEMPLATE COLUMNS
# =====================================================

TEMPLATE_COLUMNS = [

    "exercise_name",

    "sets",

    "reps",

    "weight"
]

# =====================================================
# SAVE TEMPLATE
# =====================================================

def save_template(

    template_name,

    template_df
):

    file_path = (

        f"{TEMPLATE_DIR}/"
        f"{template_name}.csv"
    )

    # =========================================
    # ENSURE COLUMNS EXIST
    # =========================================

    for column in TEMPLATE_COLUMNS:

        if column not in template_df.columns:

            template_df[column] = ""

    # =========================================
    # SAVE CSV
    # =========================================

    template_df.to_csv(

        file_path,

        index=False
    )

# =====================================================
# CREATE TEMPLATE
# =====================================================

def create_template(

    template_name
):

    # =========================================
    # CREATE EMPTY TEMPLATE
    # WITH VALID COLUMNS
    # =========================================

    empty_df = pd.DataFrame(

        columns=TEMPLATE_COLUMNS
    )

    save_template(

        template_name,

        empty_df
    )

    return {

        "message":
            "Template created successfully",

        "template_name":
            template_name
    }

# =====================================================
# GET TEMPLATE NAMES
# =====================================================

def get_template_names():

    template_files = [

        file.replace(".csv", "")

        for file in os.listdir(
            TEMPLATE_DIR
        )

        if file.endswith(".csv")
    ]

    return sorted(template_files)

# =====================================================
# LOAD SINGLE TEMPLATE
# =====================================================

def load_single_template(
    template_name
):

    file_path = (

        f"{TEMPLATE_DIR}/"
        f"{template_name}.csv"
    )

    # =========================================
    # FILE DOES NOT EXIST
    # =========================================

    if not os.path.exists(file_path):

        return pd.DataFrame(
            columns=TEMPLATE_COLUMNS
        )

    # =========================================
    # FILE EXISTS
    # =========================================

    try:

        template_df = pd.read_csv(
            file_path
        )

        # =====================================
        # ENSURE COLUMNS EXIST
        # =====================================

        for column in TEMPLATE_COLUMNS:

            if column not in template_df.columns:

                template_df[column] = ""

        return template_df

    # =========================================
    # EMPTY OR CORRUPTED CSV
    # =========================================

    except EmptyDataError:

        empty_df = pd.DataFrame(
            columns=TEMPLATE_COLUMNS
        )

        save_template(

            template_name,

            empty_df
        )

        return empty_df

# =====================================================
# DELETE TEMPLATE
# =====================================================

def delete_template(
    template_name
):

    file_path = (

        f"{TEMPLATE_DIR}/"
        f"{template_name}.csv"
    )

    if os.path.exists(file_path):

        os.remove(file_path)

# =====================================================
# ADD EXERCISE TO TEMPLATE
# =====================================================

def add_exercise_to_template(

    template_name,

    exercise_data
):

    template_df = load_single_template(
        template_name
    )

    # =========================================
    # PREVENT DUPLICATES
    # =========================================

    if (

        "exercise_name" in template_df.columns

        and

        exercise_data["exercise_name"]
        in template_df["exercise_name"].values
    ):

        return {

            "message":
                "Exercise already exists",

            "data":
                template_df.to_dict(
                    orient="records"
                )
        }

    # =========================================
    # CREATE NEW ROW
    # =========================================

    new_row = {

        "exercise_name":
            exercise_data.get(
                "exercise_name",
                ""
            ),

        "sets":
            exercise_data.get(
                "sets",
                3
            ),

        "reps":
            exercise_data.get(
                "reps",
                "10"
            ),

        "weight":
            exercise_data.get(
                "weight",
                0
            )
    }

    new_row_df = pd.DataFrame(
        [new_row]
    )

    # =========================================
    # APPEND ROW
    # =========================================

    updated_df = pd.concat(

        [template_df, new_row_df],

        ignore_index=True
    )

    # =========================================
    # SAVE UPDATED TEMPLATE
    # =========================================

    save_template(

        template_name,

        updated_df
    )

    return {

        "message":
            "Exercise added successfully",

        "data":
            updated_df.to_dict(
                orient="records"
            )
    }

# =====================================================
# REMOVE EXERCISE FROM TEMPLATE
# =====================================================

def remove_exercise_from_template(

    template_name,

    exercise_name
):

    template_df = load_single_template(
        template_name
    )

    if template_df.empty:

        return template_df

    # =========================================
    # CLEAN INPUT
    # =========================================

    exercise_name = (
        str(exercise_name)
        .strip()
        .lower()
    )

    # =========================================
    # CLEAN CSV COLUMN
    # =========================================

    template_df["exercise_name"] = (
        template_df["exercise_name"]
        .astype(str)
        .str.strip()
    )

    # =========================================
    # REMOVE MATCHING ROW
    # =========================================

    updated_df = template_df[

        template_df[
            "exercise_name"
        ].str.lower() != exercise_name
    ]

    # =========================================
    # SAVE UPDATED TEMPLATE
    # =========================================

    save_template(

        template_name,

        updated_df
    )

    return updated_df

# =====================================================
# UPDATE EXERCISE IN TEMPLATE
# =====================================================

def update_exercise_in_template(

    template_name,

    exercise_name,

    updated_fields
):

    template_df = load_single_template(
        template_name
    )

    # =========================================
    # UPDATE FIELDS
    # =========================================

    for key, value in updated_fields.items():

        template_df.loc[

            template_df[
                "exercise_name"
            ] == exercise_name,

            key

        ] = value

    # =========================================
    # SAVE UPDATED DATA
    # =========================================

    save_template(

        template_name,

        template_df
    )

    return {

        "message":
            "Exercise updated successfully",

        "data":
            template_df.to_dict(
                orient="records"
            )
    }