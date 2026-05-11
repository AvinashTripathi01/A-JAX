# app.py

import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(

    page_title="A-JAX",

    page_icon="⚡",

    layout="wide",

    initial_sidebar_state="expanded"
)

# =====================================================
# HOME PAGE
# =====================================================

st.title("A-JAX")

st.caption(
    "AI-Powered Fitness Operating System"
)

# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""

# AI-Powered Fitness Operating System

Build workouts.  
Execute training sessions.  
Track progression.  
Analyze performance.  

""")

# =====================================================
# CORE SYSTEMS
# =====================================================

st.divider()

st.header("Core Systems")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏗️ Workout Builder")

    st.write(
        "Create reusable training templates."
    )

    st.subheader("🏋️ Exercise Browser")

    st.write(
        "Explore 873+ exercises with intelligent filtering."
    )

    st.subheader("⚖️ Body Tracking")

    st.write(
        "Track weight, calories, protein and recovery."
    )

with col2:

    st.subheader("🔥 Workout Execution")

    st.write(
        "Track actual gym performance in real-time."
    )

    st.subheader("📈 Analytics")

    st.write(
        "Monitor volume, strength, recovery and growth."
    )

    st.subheader("📚 Template Library")

    st.write(
        "Manage Push/Pull/Legs and custom workout splits."
    )

# =====================================================
# QUICK STATS
# =====================================================

st.divider()

st.header("Quick Stats")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Workout Templates",
        "0"
    )

with col2:

    st.metric(
        "Exercises",
        "873"
    )

with col3:

    st.metric(
        "Workout Sessions",
        "0"
    )

with col4:

    st.metric(
        "Growth Score",
        "0"
    )

# =====================================================
# GETTING STARTED
# =====================================================

st.divider()

st.info(
    "Use the built-in Streamlit sidebar navigation to move between pages."
)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "A-JAX v1 MVP — Intelligent Fitness Operating System"
)