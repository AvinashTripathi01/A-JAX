# analytics_routes.py
from fastapi import APIRouter

import pandas as pd

import os


router = APIRouter()


# =====================================================
# FILE PATHS
# FIX 3: WORKOUT_LOG now points to master_log.csv
# (old Workout_Log.csv is no longer written to after
#  the master_log architecture change)
# FIX 5: Absolute paths so the file resolves correctly
# regardless of where uvicorn is launched from
# =====================================================

BASE_DIR    = os.path.dirname(
    os.path.abspath(__file__)
)

# Walk up to project root (api/routes/ → api/ → root)
PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..")
)

WORKOUT_LOG = os.path.join(
    PROJECT_ROOT, "data", "master_log.csv"
)

MUSCLE_LOG  = os.path.join(
    PROJECT_ROOT, "data", "muscle_volume_log.csv"
)


# =====================================================
# LOAD DATA
# =====================================================

def load_csv(path):

    if not os.path.exists(path):

        return pd.DataFrame()

    return pd.read_csv(path)


# =====================================================
# OVERVIEW ANALYTICS
# FIX 2: Removed read of work_capacity_index column
# (it does not exist in the CSV).
# avg_work_capacity now computed as total_volume /
# total_sets — a valid proxy for work per set.
# =====================================================

@router.get("/analytics/overview")

def analytics_overview():

    workout_df = load_csv(
        WORKOUT_LOG
    )

    if workout_df.empty:

        return {
            "total_workouts":    0,
            "total_volume":      0,
            "avg_work_capacity": 0,
            "total_sets":        0,
        }

    total_workouts = int(
        workout_df["session_id"].nunique()
    )

    total_volume = float(
        workout_df["volume"].sum()
    )

    total_sets = int(
        workout_df["actual_sets"].sum()
    )

    # FIX 2: compute from columns that actually exist
    avg_work_capacity = round(
        total_volume / total_sets
        if total_sets > 0
        else 0,
        2
    )

    return {

        "total_workouts":
            total_workouts,

        "total_volume":
            round(total_volume, 2),

        "avg_work_capacity":
            avg_work_capacity,

        "total_sets":
            total_sets,
    }


# =====================================================
# MUSCLE ANALYTICS
# FIX 1: Added percentage field that frontend expects.
# analytics.tsx calls item.percentage.toFixed(1) —
# without this field the entire loadAnalytics() call
# crashes inside the shared try/catch, which is why
# ALL three sections render empty, not just muscles.
# =====================================================

@router.get("/analytics/muscles")

def muscle_analytics():

    muscle_df = load_csv(
        MUSCLE_LOG
    )

    if muscle_df.empty:

        return []

    grouped = muscle_df.groupby(

        "muscle"

    )["allocated_volume"].sum()

    grouped = grouped.sort_values(
        ascending=False
    )

    # FIX 1: calculate total for percentage
    total = grouped.sum()

    response = []

    for muscle, volume in grouped.items():

        response.append({

            "muscle":
                muscle,

            "volume":
                round(float(volume), 2),

            # FIX 1: percentage field the frontend needs
            "percentage":
                round(
                    (float(volume) / float(total)) * 100,
                    2
                ) if total > 0 else 0,
        })

    return response


# =====================================================
# WEEKLY VOLUME
# No logic changes — this was correct.
# Benefts from FIX 3 (reads master_log now) and
# FIX 5 (absolute path) automatically.
# =====================================================

@router.get("/analytics/weekly-volume")

def weekly_volume():

    workout_df = load_csv(
        WORKOUT_LOG
    )

    if workout_df.empty:

        return []

    workout_df["date"] = pd.to_datetime(
        workout_df["date"]
    )

    workout_df["week"] = (
        workout_df["date"]
        .dt.isocalendar()
        .week
    )

    grouped = workout_df.groupby(
        "week"
    )["volume"].sum()

    response = []

    for week, volume in grouped.items():

        response.append({

            "week":
                int(week),

            "volume":
                round(float(volume), 2),
        })

    return response


# =====================================================
# DASHBOARD PAYLOAD
# FIX 4a: weekly_volume serialised as flat number
#   array so the SVG chart in analytics.tsx can map
#   directly: volumeData.map((v: number) => ...)
#   Previously returned [{week, volume}] objects,
#   causing 120 - v = NaN and a blank chart.
# FIX 4b: strength_trend added as empty array so the
#   frontend doesn't get undefined — blank chart is
#   better than a JS crash.
# =====================================================

@router.get("/analytics/dashboard")

def dashboard_analytics():

    overview = analytics_overview()

    muscles  = muscle_analytics()

    weekly   = weekly_volume()

    # FIX 4a: flatten to plain numbers for SVG polyline
    weekly_volume_flat = [
        item["volume"] for item in weekly
    ]

    return {

        "overview":
            overview,

        "muscles":
            muscles,

        # FIX 4a: flat array, not array of objects
        "weekly_volume":
            weekly_volume_flat,

        # FIX 4b: field must exist so frontend doesn't crash
        "strength_trend":
            [],
    }