# pages/3_Execute_Workout.py

import streamlit as st
import pandas as pd
from datetime import date
import os

from template_engine import *

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Execute Workout",

    layout="wide"
)

# =====================================================
# SESSION DIRECTORY
# =====================================================

SESSION_DIR = "data/sessions"

os.makedirs(
    SESSION_DIR,
    exist_ok=True
)

# =====================================================
# SESSION STATE
# =====================================================

if "active_workout" not in st.session_state:

    st.session_state[
        "active_workout"
    ] = None

# =====================================================
# TITLE
# =====================================================

st.title("Execute Workout")

st.markdown("""

Track real gym performance.

Templates contain:
- planned exercises
- planned sets/reps

Execution tracks:
- actual weight
- actual reps
- completion
- skipped exercises
- notes

""")

# =====================================================
# LOAD TEMPLATES
# =====================================================

template_names = get_template_names()

# =====================================================
# EMPTY STATE
# =====================================================

if len(template_names) == 0:

    st.warning(
        "No Workout Templates Found"
    )

    st.stop()

# =====================================================
# TEMPLATE SELECTOR
# =====================================================

selected_template = st.selectbox(

    "Select Workout Template",

    template_names
)

# =====================================================
# START WORKOUT
# =====================================================

if st.button("🚀 Start Workout Session"):

    template_df = load_single_template(
        selected_template
    )

    # =================================================
    # EXECUTION COLUMNS
    # =================================================

    template_df["Weight"] = 0.0

    template_df["Actual Reps"] = ""

    template_df["Completed"] = False

    template_df["Skipped"] = False

    template_df["Notes"] = ""

    st.session_state[
        "active_workout"
    ] = template_df

    st.success(
        f"{selected_template} session started!"
    )

# =====================================================
# ACTIVE SESSION
# =====================================================

if st.session_state[
    "active_workout"
] is not None:

    st.divider()

    st.header("🏋️ Active Workout")

    workout_df = st.session_state[
        "active_workout"
    ]

    # =================================================
    # EXERCISE LOOP
    # =================================================

    updated_rows = []

    for index, row in workout_df.iterrows():

        st.divider()

        st.subheader(
            row["Exercise"]
        )

        # =============================================
        # INFO
        # =============================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                f"Muscle: "
                f"{row['Muscle Group']}"
            )

        with col2:

            st.info(
                f"Sets: "
                f"{row['Sets']}"
            )

        with col3:

            st.info(
                f"Planned Reps: "
                f"{row['Reps']}"
            )

        # =============================================
        # EXECUTION INPUTS
        # =============================================

        col4, col5, col6 = st.columns(3)

        with col4:

            weight = st.number_input(

                f"Weight (kg) - {index}",

                min_value=0.0,

                value=float(row["Weight"])
            )

        with col5:

            actual_reps = st.text_input(

                f"Actual Reps - {index}",

                value=str(
                    row["Actual Reps"]
                )
            )

        with col6:

            completed = st.checkbox(

                f"Completed - {index}",

                value=bool(
                    row["Completed"]
                )
            )

        # =============================================
        # SKIP + NOTES
        # =============================================

        col7, col8 = st.columns(2)

        with col7:

            skipped = st.checkbox(

                f"Skipped - {index}",

                value=bool(
                    row["Skipped"]
                )
            )

        with col8:

            notes = st.text_input(

                f"Notes - {index}",

                value=str(
                    row["Notes"]
                )
            )

        # =============================================
        # UPDATE ROW
        # =============================================

        updated_row = row.copy()

        updated_row["Weight"] = weight

        updated_row["Actual Reps"] = actual_reps

        updated_row["Completed"] = completed

        updated_row["Skipped"] = skipped

        updated_row["Notes"] = notes

        updated_rows.append(
            updated_row
        )

    # =================================================
    # UPDATE STATE
    # =================================================

    updated_df = pd.DataFrame(
        updated_rows
    )

    st.session_state[
        "active_workout"
    ] = updated_df

    # =================================================
    # SAVE SESSION
    # =================================================

    st.divider()

    if st.button("💾 Save Workout Session"):

        session_date = str(
            date.today()
        )

        file_name = (

            f"{selected_template}"
            f"_{session_date}.csv"
        )

        save_path = (

            f"{SESSION_DIR}/"
            f"{file_name}"
        )

        updated_df.to_csv(

            save_path,

            index=False
        )

        st.success(
            "Workout Session Saved!"
        )

# =====================================================
# SESSION HISTORY
# =====================================================

st.divider()

st.header("🕘 Previous Sessions")

session_files = [

    file

    for file in os.listdir(
        SESSION_DIR
    )

    if file.endswith(".csv")
]

if len(session_files) == 0:

    st.info(
        "No Sessions Found"
    )

else:

    selected_session = st.selectbox(

        "Select Session",

        sorted(session_files)
    )

    session_df = pd.read_csv(

        f"{SESSION_DIR}/"
        f"{selected_session}"
    )

    st.dataframe(

        session_df,

        use_container_width=True
    )