# template_engine.py

import pandas as pd
import os

# =====================================================
# TEMPLATE DIRECTORY
# =====================================================

TEMPLATE_DIR = "data/templates"

os.makedirs(
    TEMPLATE_DIR,
    exist_ok=True
)

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

    template_df.to_csv(

        file_path,

        index=False
    )

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

    if os.path.exists(file_path):

        return pd.read_csv(
            file_path
        )

    return pd.DataFrame()

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