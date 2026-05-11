import streamlit as st
import pandas as pd


# =====================================================
# WORKOUT EXECUTOR PAGE
# =====================================================


def workout_executor(session_df):

    st.header("🏋️ Workout Execution")

    if session_df.empty:

        st.warning(
            "No Active Workout Session"
        )

        return

    # =================================================
    # LOOP EXERCISES
    # =================================================

    for idx, row in session_df.iterrows():

        with st.container(border=True):

            st.subheader(
                row["exercise_name"]
            )

            col1, col2, col3 = st.columns(3)

            # -----------------------------------------
            # SETS
            # -----------------------------------------

            with col1:

                actual_sets = st.number_input(

                    "Sets",

                    min_value=0,

                    value=int(
                        row["actual_sets"]
                    ),

                    key=f"sets_{idx}"
                )

            # -----------------------------------------
            # REPS
            # -----------------------------------------

            with col2:

                actual_reps = st.text_input(

                    "Reps",

                    value=str(
                        row["actual_reps"]
                    ),

                    key=f"reps_{idx}"
                )

            # -----------------------------------------
            # WEIGHT
            # -----------------------------------------

            with col3:

                weight = st.number_input(

                    "Weight",

                    min_value=0.0,

                    value=float(
                        row["weight"]
                    ),

                    key=f"weight_{idx}"
                )

            # -----------------------------------------
            # STATUS
            # -----------------------------------------

            status = st.selectbox(

                "Workout Status",

                [
                    "completed",
                    "skipped",
                    "replaced"
                ],

                key=f"status_{idx}"
            )

            # -----------------------------------------
            # NOTES
            # -----------------------------------------

            notes = st.text_area(

                "Notes",

                key=f"notes_{idx}"
            )

            st.divider()

    # =================================================
    # SAVE BUTTON
    # =================================================

    st.button(
        "💾 Save Executed Workout"
    )