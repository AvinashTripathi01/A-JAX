#main.py
from fastapi import (
    FastAPI,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from api.routes.analytics_routes import (
    router as analytics_router
)
from api.services.exercise import (

    load_exercises,

    search_exercises,

    filter_by_muscle_group,

    filter_by_equipment,

    filter_by_level,

    filter_by_mechanic,

    recommend_exercises,
)

from api.services.workout import (

    create_template,

    get_templates,

    get_template,

    remove_template,

    create_session,

    get_sessions,
)

from template_engine import (

    add_exercise_to_template,

    remove_exercise_from_template,

    update_exercise_in_template,
)

from session_engine import (

    get_session,

    update_session_exercise,

    complete_session,

    load_sessions,
)

app = FastAPI()
app.include_router(
    analytics_router
)
# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# =====================================================
# ROOT
# =====================================================

@app.get("/")
def home():

    return {

        "message": "A-JAX Backend Running"
    }

# =====================================================
# DASHBOARD TEST
# =====================================================

@app.get("/dashboard")
def dashboard_data():

    return {

        "streak": 12,

        "weekly_volume": "24.8k",

        "sessions": 4,

        "pr": "102.5kg Bench Press"
    }

# =====================================================
# ALL EXERCISES
# =====================================================

@app.get("/exercises")
def get_exercises():

    df = load_exercises()

    return df.to_dict(
        orient="records"
    )

# =====================================================
# SEARCH EXERCISES
# =====================================================

@app.get("/exercises/search")
def search(query: str):

    df = load_exercises()

    results = search_exercises(
        df,
        query
    )

    return results.to_dict(
        orient="records"
    )

# =====================================================
# FILTER BY MUSCLE GROUP
# =====================================================

@app.get("/exercises/muscle/{muscle_group}")
def muscle_filter(muscle_group: str):

    df = load_exercises()

    results = filter_by_muscle_group(
        df,
        muscle_group
    )

    return results.to_dict(
        orient="records"
    )

# =====================================================
# FILTER BY EQUIPMENT
# =====================================================

@app.get("/exercises/equipment/{equipment}")
def equipment_filter(equipment: str):

    df = load_exercises()

    results = filter_by_equipment(
        df,
        equipment
    )

    return results.to_dict(
        orient="records"
    )

# =====================================================
# FILTER BY LEVEL
# =====================================================

@app.get("/exercises/level/{level}")
def level_filter(level: str):

    df = load_exercises()

    results = filter_by_level(
        df,
        level
    )

    return results.to_dict(
        orient="records"
    )

# =====================================================
# FILTER BY MECHANIC
# =====================================================

@app.get("/exercises/mechanic/{mechanic}")
def mechanic_filter(mechanic: str):

    df = load_exercises()

    results = filter_by_mechanic(
        df,
        mechanic
    )

    return results.to_dict(
        orient="records"
    )

# =====================================================
# RECOMMEND EXERCISES
# =====================================================

@app.get("/recommend")
def recommend(

    muscle_group: str = None,

    equipment: str = None,

    level: str = None,

    mechanic: str = None,

    limit: int = 20
):

    df = load_exercises()

    results = recommend_exercises(

        df,

        muscle_group=muscle_group,

        equipment=equipment,

        level=level,

        mechanic=mechanic,

        limit=limit
    )

    return results.to_dict(
        orient="records"
    )

# =====================================================
# GET ALL TEMPLATES
# =====================================================

@app.get("/templates")
def fetch_templates():

    return get_templates()

# =====================================================
# GET SINGLE TEMPLATE
# =====================================================

@app.get("/templates/{template_name}")
def fetch_template(
    template_name: str
):

    return get_template(
        template_name
    )

# =====================================================
# CREATE TEMPLATE
# =====================================================

@app.post("/templates")
def create_new_template(
    payload: dict
):

    template_name = payload.get(
        "template_name"
    )

    exercises = payload.get(
        "exercises",
        []
    )

    return create_template(

        template_name,

        exercises
    )

# =====================================================
# DELETE TEMPLATE
# =====================================================

@app.delete("/templates/{template_name}")
def delete_template_route(
    template_name: str
):

    return remove_template(
        template_name
    )

# =====================================================
# CREATE WORKOUT SESSION
# =====================================================

@app.post("/sessions/create")
def create_workout_session(
    payload: dict
):

    template_name = payload.get(
        "template_name"
    )

    return create_session(
        template_name
    )

# =====================================================
# GET ALL SESSIONS
# =====================================================

@app.get("/sessions")
def fetch_sessions():

    return get_sessions()

# =====================================================
# GET SINGLE SESSION
# =====================================================

@app.get("/sessions/{session_id}")
def fetch_single_session(

    session_id: str
):

    return get_session(
        session_id
    )

# =====================================================
# UPDATE SESSION EXERCISE
# =====================================================

@app.put(
    "/sessions/{session_id}/exercise/{exercise_name:path}"
)
def update_session_exercise_route(

    session_id: str,

    exercise_name: str,

    payload: dict
):

    return update_session_exercise(

        session_id,

        exercise_name,

        payload
    )

# =====================================================
# COMPLETE SESSION
# =====================================================

@app.post(
    "/sessions/{session_id}/complete"
)
def complete_session_route(

    session_id: str
):

    return complete_session(
        session_id
    )

# =====================================================
# ADD EXERCISE TO TEMPLATE
# =====================================================

@app.post("/templates/{template_name}/exercise")
def add_exercise_route(

    template_name: str,

    payload: dict
):

    return add_exercise_to_template(

        template_name,

        payload
    )

# =====================================================
# REMOVE EXERCISE FROM TEMPLATE
# =====================================================

@app.delete(
    "/templates/{template_name}/exercise/{exercise_name:path}"
)
def remove_exercise_route(

    template_name: str,

    exercise_name: str
):

    updated_df = remove_exercise_from_template(

        template_name,

        exercise_name
    )

    return updated_df.to_dict(
        orient="records"
    )

# =====================================================
# UPDATE EXERCISE IN TEMPLATE
# =====================================================

@app.put(
    "/templates/{template_name}/exercise/{exercise_name:path}"
)
def update_exercise_route(

    template_name: str,

    exercise_name: str,

    payload: dict
):

    updated_df = update_exercise_in_template(

        template_name,

        exercise_name,

        payload
    )

    return updated_df.to_dict(
        orient="records"
    )
# =====================================================
# GET WORKOUT SESSION
# =====================================================

@app.get("/workout-session/{session_id}")
def get_workout_session(

    session_id: str
):

    session = get_session(
        session_id
    )

    if len(session) == 0:

        raise HTTPException(

            status_code=404,

            detail="Session not found"
        )

    return session

# =====================================================
# LOAD WORKOUT SESSION
# =====================================================

@app.get(
    "/workout-session/{session_id}"
)
def load_workout_session(
    session_id: str
):

    from session_engine import (
        load_single_session
    )

    return load_single_session(
        session_id
    )
# ========================================
# UPDATE SESSION EXERCISE
# ========================================

@app.put(
    "/sessions/{session_id}/exercise/{exercise_name}"
)
def update_session_exercise(

    session_id: str,

    exercise_name: str,

    updates: dict
):

    import pandas as pd

    session_file = (
        f"data/sessions/{session_id}.csv"
    )

    df = pd.read_csv(
        session_file
    )

    # FIND EXERCISE ROW

    mask = (

        df[
            "exercise_name"
        ] == exercise_name
    )

    # UPDATE VALUES

    if "actual_sets" in updates:

        df.loc[
            mask,
            "actual_sets"
        ] = updates[
            "actual_sets"
        ]

    if "actual_reps" in updates:

        df.loc[
            mask,
            "actual_reps"
        ] = updates[
            "actual_reps"
        ]

    if "weight" in updates:

        df.loc[
            mask,
            "weight"
        ] = updates[
            "weight"
        ]

    if "completed" in updates:

        df.loc[
            mask,
            "completed"
        ] = updates[
            "completed"
        ]

    # SAVE CSV

    df.to_csv(
        session_file,
        index=False
    )

    return {

        "message":
        "Session updated"
    }
