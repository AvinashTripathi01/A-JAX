import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# DAILY VOLUME TREND
# =====================================================

def plot_volume_trend(daily_df):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        daily_df["Date"],
        daily_df["Volume"],
        marker="o"
    )

    ax.set_title("Daily Volume Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# =====================================================
# STRENGTH TREND
# =====================================================

def plot_strength_trend(strength_df):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        strength_df["Date"],
        strength_df["Strength Index"],
        marker="o"
    )

    ax.set_title("Strength Index Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Strength Index")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# =====================================================
# WEEKLY WORKLOAD
# =====================================================

def plot_weekly_workload(daily_df):

    daily_df["Date"] = pd.to_datetime(daily_df["Date"])

    daily_df["Week"] = (
        daily_df["Date"]
        .dt.isocalendar()
        .week
    )

    weekly = (
        daily_df
        .groupby("Week")["Volume"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(
        weekly["Week"].astype(str),
        weekly["Volume"]
    )

    ax.set_title("Weekly Workload")
    ax.set_xlabel("Week")
    ax.set_ylabel("Total Volume")

    plt.tight_layout()

    return fig


# =====================================================
# MUSCLE DISTRIBUTION
# =====================================================

def plot_muscle_distribution(muscle_df):

    grouped = (
        muscle_df
        .groupby("Muscle Group")["Volume"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.pie(
        grouped["Volume"],
        labels=grouped["Muscle Group"],
        autopct="%1.1f%%"
    )

    ax.set_title("Muscle Distribution")

    return fig


# =====================================================
# MUSCLE IMBALANCE
# =====================================================

def plot_muscle_imbalance(muscle_df):

    grouped = (
        muscle_df
        .groupby("Target Muscles")["Volume"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        grouped["Target Muscles"],
        grouped["Volume"]
    )

    ax.set_title("Muscle Imbalance")
    ax.set_xlabel("Muscles")
    ax.set_ylabel("Volume")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# =====================================================
# WEIGHT TREND
# =====================================================

def plot_weight_trend(body_df):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        body_df["Date"],
        body_df["Weight"],
        marker="o"
    )

    ax.set_title("Weight Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Weight (kg)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# =====================================================
# CALORIES TREND
# =====================================================

def plot_calorie_trend(body_df):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        body_df["Date"],
        body_df["Calories Intake"],
        marker="o",
        label="Calories Intake"
    )

    ax.plot(
        body_df["Date"],
        body_df["Calories Burned"],
        marker="o",
        label="Calories Burned"
    )

    ax.set_title("Calories Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Calories")

    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# =====================================================
# PROTEIN TREND
# =====================================================

def plot_protein_trend(body_df):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        body_df["Date"],
        body_df["Protein"],
        marker="o"
    )

    ax.set_title("Protein Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Protein (g)")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig


# =====================================================
# GROWTH SCORE TREND
# =====================================================

def plot_growth_score(growth_df):

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        growth_df["Date"],
        growth_df["Growth Score"],
        marker="o"
    )

    ax.set_title("Growth Score Trend")
    ax.set_xlabel("Date")
    ax.set_ylabel("Growth Score")

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig