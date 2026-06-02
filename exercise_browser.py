import streamlit as st
import pandas as pd

from api.services.exercise import *


# =====================================================
# EXERCISE CARD
# =====================================================

def render_exercise_card(exercise):

    with st.container(border=True):

        st.subheader(
            exercise["exercise_name"]
        )

        # =================================================
        # INFO ROW
        # =================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.info(
                f"Muscle: {exercise['internal_muscle_group']}"
            )

        with col2:

            st.info(
                f"Equipment: {exercise['equipment']}"
            )

        with col3:

            st.info(
                f"Level: {exercise['level']}"
            )

        # =================================================
        # SECOND ROW
        # =================================================

        col4, col5 = st.columns(2)

        with col4:

            st.info(
                f"Region: {exercise['internal_region']}"
            )

        with col5:

            st.info(
                f"Mechanic: {exercise['mechanic']}"
            )

        # =================================================
        # PRIMARY MUSCLES
        # =================================================

        st.markdown("### Primary Muscles")

        primary = exercise["primary_muscles"]

        if isinstance(primary, list):

            st.success(
                ", ".join(primary)
            )

        else:

            st.success(str(primary))

        # =================================================
        # SECONDARY MUSCLES
        # =================================================

        st.markdown("### Secondary Muscles")

        secondary = exercise["secondary_muscles"]

        if isinstance(secondary, list):

            st.info(
                ", ".join(secondary)
            )

        else:

            st.info(str(secondary))

        # =================================================
        # IMAGE PLACEHOLDER
        # =================================================

        st.info(
            "Exercise Image Coming Soon"
        )

        # =================================================
        # INSTRUCTIONS
        # =================================================

        with st.expander("📘 Instructions"):

            instructions = exercise["instructions"]

            if isinstance(instructions, list):

                for idx, step in enumerate(instructions):

                    st.markdown(
                        f"**Step {idx+1}:** {step}"
                    )

            else:

                st.write(instructions)

        # =================================================
        # ACTION BUTTON
        # =================================================

        st.button(

            f"Add {exercise['exercise_name']} To Workout",

            key=exercise["exercise_id"]
        )

        st.divider()


# =====================================================
# EXERCISE BROWSER
# =====================================================

def exercise_browser(exercise_df):

    st.header("🏋️ Exercise Browser")

    # =================================================
    # FILTERS
    # =================================================

    col1, col2, col3, col4 = st.columns(4)

    # -------------------------------------------------

    with col1:

        muscle_filter = st.selectbox(

            "Muscle Group",

            ["All"] +

            get_unique_muscle_groups(
                exercise_df
            )
        )

    # -------------------------------------------------

    with col2:

        equipment_filter = st.selectbox(

            "Equipment",

            ["All"] +

            get_unique_equipment(
                exercise_df
            )
        )

    # -------------------------------------------------

    with col3:

        level_filter = st.selectbox(

            "Level",

            ["All"] +

            get_unique_levels(
                exercise_df
            )
        )

    # -------------------------------------------------

    with col4:

        mechanic_filter = st.selectbox(

            "Mechanic",

            ["All"] +

            get_unique_mechanics(
                exercise_df
            )
        )

    # =================================================
    # SEARCH
    # =================================================

    search = st.text_input(
        "Search Exercise"
    )

    # =================================================
    # FILTER ENGINE
    # =================================================

    filtered_df = recommend_exercises(

        exercise_df,

        muscle_group=None
        if muscle_filter == "All"
        else muscle_filter,

        equipment=None
        if equipment_filter == "All"
        else equipment_filter,

        level=None
        if level_filter == "All"
        else level_filter,

        mechanic=None
        if mechanic_filter == "All"
        else mechanic_filter,

        limit=20
    )

    # =================================================
    # SEARCH FILTER
    # =================================================

    if search:

        filtered_df = filtered_df[

            filtered_df[
                "exercise_name"
            ]
            .str.lower()
            .str.contains(
                search.lower(),
                na=False
            )
        ]

    # =================================================
    # RESULTS
    # =================================================

    st.subheader(
        f"Exercises Found: {len(filtered_df)}"
    )

    # =================================================
    # EMPTY STATE
    # =================================================

    if filtered_df.empty:

        st.warning(
            "No Exercises Found"
        )

        return

    # =================================================
    # RENDER
    # =================================================

    for _, exercise in filtered_df.iterrows():

        render_exercise_card(exercise)