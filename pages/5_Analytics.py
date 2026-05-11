# pages/5_Analytics.py

import streamlit as st
import pandas as pd
import os

from utils import *
from charts import *

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="Analytics",

    layout="wide"
)

# =====================================================
# TITLE
# =====================================================

st.title("Analytics Dashboard")

st.markdown("""

Analyze:
- training volume
- muscle balance
- strength progression
- calorie trends
- protein intake
- growth score

""")

# =====================================================
# FILE PATHS
# =====================================================

WORKOUT_FILE = "data/Workout_Log.csv"

BODY_FILE = "data/Body_Log.csv"

# =====================================================
# LOAD WORKOUT DATA
# =====================================================

if os.path.exists(WORKOUT_FILE):

    workout_df = pd.read_csv(
        WORKOUT_FILE
    )

else:

    workout_df = pd.DataFrame()

# =====================================================
# LOAD BODY DATA
# =====================================================

if os.path.exists(BODY_FILE):

    body_df = pd.read_csv(
        BODY_FILE
    )

else:

    body_df = pd.DataFrame()

# =====================================================
# EMPTY STATE
# =====================================================

if workout_df.empty and body_df.empty:

    st.warning(
        "No Analytics Data Found"
    )

    st.stop()

# =====================================================
# DATE FILTER
# =====================================================

st.divider()

st.header("📅 Date Filter")

all_dates = []

# -----------------------------------------------------

if not workout_df.empty:

    workout_df["Date"] = pd.to_datetime(
        workout_df["Date"]
    )

    all_dates.extend(
        workout_df["Date"].tolist()
    )

# -----------------------------------------------------

if not body_df.empty:

    body_df["Date"] = pd.to_datetime(
        body_df["Date"]
    )

    all_dates.extend(
        body_df["Date"].tolist()
    )

# -----------------------------------------------------

min_date = min(all_dates)

max_date = max(all_dates)

start_date, end_date = st.date_input(

    "Select Date Range",

    value=(min_date, max_date)
)

# =====================================================
# FILTER WORKOUT DATA
# =====================================================

if not workout_df.empty:

    workout_df = workout_df[

        (workout_df["Date"] >= pd.to_datetime(start_date))
        &
        (workout_df["Date"] <= pd.to_datetime(end_date))
    ]

# =====================================================
# FILTER BODY DATA
# =====================================================

if not body_df.empty:

    body_df = body_df[

        (body_df["Date"] >= pd.to_datetime(start_date))
        &
        (body_df["Date"] <= pd.to_datetime(end_date))
    ]

# =====================================================
# ANALYTICS PROCESSING
# =====================================================

if not workout_df.empty:

    workout_df = calculate_volume(
        workout_df
    )

    daily_df = daily_volume(
        workout_df
    )

    muscle_df = muscle_volume(
        workout_df
    )

else:

    daily_df = pd.DataFrame()

    muscle_df = pd.DataFrame()

# -----------------------------------------------------

if not body_df.empty:

    body_df = protein_adequacy(
        body_df
    )

    body_df = calorie_balance(
        body_df
    )

# -----------------------------------------------------

if not workout_df.empty and not body_df.empty:

    strength_df = strength_index(

        workout_df,

        body_df
    )

    growth_df = growth_score(

        body_df,

        strength_df
    )

else:

    strength_df = pd.DataFrame()

    growth_df = pd.DataFrame()

# =====================================================
# KPI SECTION
# =====================================================

st.divider()

st.header("🏆 Performance Overview")

# =====================================================
# KPI CALCULATIONS
# =====================================================

if not daily_df.empty:

    total_volume = int(
        daily_df["Volume"].sum()
    )

else:

    total_volume = 0

# -----------------------------------------------------

if not workout_df.empty:

    total_exercises = len(
        workout_df
    )

    unique_exercises = workout_df[
        "Exercise"
    ].nunique()

else:

    total_exercises = 0

    unique_exercises = 0

# -----------------------------------------------------

if not growth_df.empty:

    latest_growth = growth_df.iloc[-1]

    latest_growth_score = round(

        latest_growth[
            "Growth Score"
        ],

        2
    )

else:

    latest_growth_score = 0

# -----------------------------------------------------

if not strength_df.empty:

    latest_strength = strength_df.iloc[-1]

    latest_strength_index = round(

        latest_strength[
            "Strength Index"
        ],

        2
    )

else:

    latest_strength_index = 0

# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Total Volume",

        f"{total_volume:,}"
    )

with col2:

    st.metric(

        "Workout Entries",

        total_exercises
    )

with col3:

    st.metric(

        "Strength Index",

        latest_strength_index
    )

with col4:

    st.metric(

        "Growth Score",

        latest_growth_score
    )

# =====================================================
# PERFORMANCE ANALYTICS
# =====================================================

st.divider()

st.header("🏋️ Performance Analytics")

col5, col6 = st.columns(2)

# -----------------------------------------------------

with col5:

    if not daily_df.empty:

        st.subheader(
            "Daily Volume Trend"
        )

        fig = plot_volume_trend(
            daily_df
        )

        st.pyplot(fig)

# -----------------------------------------------------

with col6:

    if not strength_df.empty:

        st.subheader(
            "Strength Trend"
        )

        fig = plot_strength_trend(
            strength_df
        )

        st.pyplot(fig)

# =====================================================
# WEEKLY WORKLOAD
# =====================================================

if not daily_df.empty:

    st.subheader(
        "Weekly Workload"
    )

    fig = plot_weekly_workload(
        daily_df
    )

    st.pyplot(fig)

# =====================================================
# MUSCLE ANALYTICS
# =====================================================

st.divider()

st.header("💪 Muscle Analytics")

col7, col8 = st.columns(2)

# -----------------------------------------------------

with col7:

    if not muscle_df.empty:

        st.subheader(
            "Muscle Distribution"
        )

        fig = plot_muscle_distribution(
            muscle_df
        )

        st.pyplot(fig)

# -----------------------------------------------------

with col8:

    if not muscle_df.empty:

        st.subheader(
            "Muscle Imbalance"
        )

        fig = plot_muscle_imbalance(
            muscle_df
        )

        st.pyplot(fig)

# =====================================================
# BODY ANALYTICS
# =====================================================

st.divider()

st.header("⚖️ Body Analytics")

col9, col10 = st.columns(2)

# -----------------------------------------------------

with col9:

    if not body_df.empty:

        st.subheader(
            "Weight Trend"
        )

        fig = plot_weight_trend(
            body_df
        )

        st.pyplot(fig)

# -----------------------------------------------------

with col10:

    if not body_df.empty:

        st.subheader(
            "Calories Trend"
        )

        fig = plot_calorie_trend(
            body_df
        )

        st.pyplot(fig)

# =====================================================
# PROTEIN + GROWTH
# =====================================================

col11, col12 = st.columns(2)

# -----------------------------------------------------

with col11:

    if not body_df.empty:

        st.subheader(
            "Protein Trend"
        )

        fig = plot_protein_trend(
            body_df
        )

        st.pyplot(fig)

# -----------------------------------------------------

with col12:

    if not growth_df.empty:

        st.subheader(
            "Growth Score Trend"
        )

        fig = plot_growth_score(
            growth_df
        )

        st.pyplot(fig)

# =====================================================
# RAW DATA
# =====================================================

st.divider()

with st.expander("📁 Workout Data"):

    if not workout_df.empty:

        st.dataframe(

            workout_df,

            use_container_width=True
        )

# -----------------------------------------------------

with st.expander("📁 Body Data"):

    if not body_df.empty:

        st.dataframe(

            body_df,

            use_container_width=True
        )