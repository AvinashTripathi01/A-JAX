# workout builder
from session_engine import *
from utils import *
from charts import *

# pages/2_Workout_Builder.py

import streamlit as st
import pandas as pd
from datetime import date

from exercise import *
from template_engine import *

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Workout Builder",

    layout="wide"
)

# =====================================================
# LOAD EXERCISES
# =====================================================

exercise_df = load_exercises()

# =====================================================
# SESSION STATE
# =====================================================

if "template_builder" not in st.session_state:

    st.session_state[
        "template_builder"
    ] = []

# =====================================================
# TITLE
# =====================================================

st.title("Workout Builder")

st.markdown("""

Create reusable workout templates for:
- Push Days
- Pull Days
- Leg Days
- Upper / Lower
- Specialization Programs

Templates only store:
- exercises
- sets
- reps

Weight is tracked during execution.

""")

# =====================================================
# TEMPLATE NAME
# =====================================================

template_name = st.text_input(

    "Workout Template Name",

    placeholder="Example: Push Day A"
)

# =====================================================
# FILTERS
# =====================================================

st.subheader("🔎 Exercise Filters")

col1, col2, col3, col4 = st.columns(4)

# -----------------------------------------------------

with col1:

    muscle_groups = sorted(

        exercise_df[
            "internal_muscle_group"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_muscle = st.selectbox(

        "Muscle Group",

        ["All"] + muscle_groups
    )

# -----------------------------------------------------

with col2:

    equipment_list = sorted(

        exercise_df[
            "equipment"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_equipment = st.selectbox(

        "Equipment",

        ["All"] + equipment_list
    )

# -----------------------------------------------------

with col3:

    levels = sorted(

        exercise_df[
            "level"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_level = st.selectbox(

        "Level",

        ["All"] + levels
    )

# -----------------------------------------------------

with col4:

    mechanics = sorted(

        exercise_df[
            "mechanic"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    selected_mechanic = st.selectbox(

        "Mechanic",

        ["All"] + mechanics
    )

# =====================================================
# SEARCH
# =====================================================

search_query = st.text_input(

    "Search Exercise",

    placeholder="Search exercise..."
)

# =====================================================
# FILTER DATAFRAME
# =====================================================

filtered_df = exercise_df.copy()

# -----------------------------------------------------

if selected_muscle != "All":

    filtered_df = filtered_df[

        filtered_df[
            "internal_muscle_group"
        ]
        ==
        selected_muscle
    ]

# -----------------------------------------------------

if selected_equipment != "All":

    filtered_df = filtered_df[

        filtered_df[
            "equipment"
        ]
        ==
        selected_equipment
    ]

# -----------------------------------------------------

if selected_level != "All":

    filtered_df = filtered_df[

        filtered_df[
            "level"
        ]
        ==
        selected_level
    ]

# -----------------------------------------------------

if selected_mechanic != "All":

    filtered_df = filtered_df[

        filtered_df[
            "mechanic"
        ]
        ==
        selected_mechanic
    ]

# -----------------------------------------------------

if search_query:

    filtered_df = filtered_df[

        filtered_df[
            "exercise_name"
        ]
        .str.contains(
            search_query,
            case=False,
            na=False
        )
    ]

# =====================================================
# EXERCISE SELECTOR
# =====================================================

st.divider()

st.subheader("➕ Add Exercise")

exercise_names = sorted(

    filtered_df[
        "exercise_name"
    ]
    .dropna()
    .unique()
    .tolist()
)

selected_exercise = st.selectbox(

    "Select Exercise",

    exercise_names
)

# =====================================================
# EXERCISE DETAILS
# =====================================================

exercise_details = get_exercise_details(

    exercise_df,

    selected_exercise
)

# =====================================================
# DISPLAY DETAILS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.info(
        f"Muscle Group: "
        f"{exercise_details['internal_muscle_group']}"
    )

    st.info(
        f"Region: "
        f"{exercise_details['internal_region']}"
    )

with col2:

    st.info(
        f"Equipment: "
        f"{exercise_details['equipment']}"
    )

    st.info(
        f"Mechanic: "
        f"{exercise_details['mechanic']}"
    )

with col3:

    st.info(
        f"Level: "
        f"{exercise_details['level']}"
    )

# =====================================================
# SETS / REPS
# =====================================================

col4, col5 = st.columns(2)

with col4:

    sets = st.number_input(

        "Sets",

        min_value=1,

        value=3
    )

with col5:

    reps = st.text_input(

        "Reps",

        value="10-12"
    )

# =====================================================
# ADD BUTTON
# =====================================================

if st.button("➕ Add To Workout"):

    new_exercise = {

        "Exercise": selected_exercise,

        "Muscle Group": exercise_details[
            "internal_muscle_group"
        ],

        "Region": exercise_details[
            "internal_region"
        ],

        "Equipment": exercise_details[
            "equipment"
        ],

        "Mechanic": exercise_details[
            "mechanic"
        ],

        "Level": exercise_details[
            "level"
        ],

        "Sets": sets,

        "Reps": reps
    }

    st.session_state[
        "template_builder"
    ].append(new_exercise)

    st.success(
        f"{selected_exercise} added!"
    )

# =====================================================
# CURRENT TEMPLATE
# =====================================================

st.divider()

st.header("📋 Current Workout")

template_data = st.session_state[
    "template_builder"
]

# =====================================================
# EMPTY STATE
# =====================================================

if len(template_data) == 0:

    st.warning(
        "No Exercises Added Yet"
    )

# =====================================================
# TEMPLATE TABLE
# =====================================================

else:

    template_df = pd.DataFrame(
        template_data
    )

    st.dataframe(

        template_df,

        use_container_width=True
    )

    # =================================================
    # REMOVE EXERCISE
    # =================================================

    remove_exercise = st.selectbox(

        "Remove Exercise",

        template_df["Exercise"].tolist()
    )

    if st.button("❌ Remove Selected Exercise"):

        st.session_state[
            "template_builder"
        ] = [

            ex for ex in template_data

            if ex["Exercise"]
            !=
            remove_exercise
        ]

        st.rerun()

# =====================================================
# SAVE TEMPLATE
# =====================================================

st.divider()

col6, col7 = st.columns(2)

with col6:

    if st.button("💾 Save / Update Workout Template"):

     if template_name == "":

        st.error(
            "Please Enter Template Name"
        )

    elif len(template_data) == 0:

        st.error(
            "Add Exercises First"
        )

    else:

        template_df = pd.DataFrame(
            template_data
        )

        save_template(

            template_name,

            template_df
        )

        st.success(
            f"{template_name} Saved!"
        )

# =====================================================
# CLEAR BUILDER
# =====================================================

with col7:

    if st.button("🗑️ Clear Workout"):

        st.session_state[
            "template_builder"
        ] = []

        st.rerun()

# =====================================================
# EXISTING TEMPLATES
# =====================================================

st.divider()

st.header("📚 Existing Templates")

template_names = get_template_names()

if len(template_names) == 0:

    st.info(
        "No Templates Found"
    )

else:

    selected_template = st.selectbox(

        "Saved Templates",

        template_names
    )

    preview_df = load_single_template(
        selected_template
    )

    st.dataframe(

        preview_df,

        use_container_width=True
    )
if len(template_names) > 0:

    load_template = st.selectbox(

        "Load Existing Template",

        template_names
    )

    if st.button("📂 Load Template Into Builder"):

        loaded_df = load_single_template(
            load_template
        )

        st.session_state[
            "template_builder"
        ] = loaded_df.to_dict("records")

        template_name = load_template

        st.success(
            f"{load_template} loaded!"
        )

        st.rerun()