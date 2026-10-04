import streamlit as st

from utils.supabase_client import supabase


# ---------------- USER ----------------

def get_current_user_id():
    return st.session_state.get("user_id")


# ---------------- QUIZ ----------------

def save_quiz_result(score, total, accuracy):
    user_id = get_current_user_id()

    if user_id is None:
        return

    supabase.table("quiz_results").insert({
        "user_id": str(user_id),
        "score": int(score),
        "total": int(total),
        "accuracy": float(accuracy)
    }).execute()


def get_quiz_results():
    user_id = get_current_user_id()

    if user_id is None:
        return []

    response = (
        supabase
        .table("quiz_results")
        .select("score,total,accuracy")
        .eq("user_id", str(user_id))
        .order("id")
        .execute()
    )

    return response.data or []


def get_quiz_stats():
    results = get_quiz_results()

    if not results:
        return {
            "quiz_count": 0,
            "accuracy": 0
        }

    accuracies = [
        float(result["accuracy"])
        for result in results
    ]

    return {
        "quiz_count": len(results),
        "accuracy": round(
            sum(accuracies) / len(accuracies),
            2
        )
    }


# ---------------- NOTES ----------------

def save_note(filename, content):
    user_id = get_current_user_id()

    if user_id is None:
        return

    existing = (
        supabase
        .table("notes")
        .select("id")
        .eq("user_id", str(user_id))
        .eq("filename", filename)
        .execute()
    )

    if existing.data:

        supabase.table("notes").update({
            "content": content
        }).eq(
            "id",
            existing.data[0]["id"]
        ).execute()

    else:

        supabase.table("notes").insert({
            "user_id": str(user_id),
            "filename": filename,
            "content": content
        }).execute()


def get_notes():
    user_id = get_current_user_id()

    if user_id is None:
        return {}

    response = (
        supabase
        .table("notes")
        .select("filename,content")
        .eq("user_id", str(user_id))
        .order("id")
        .execute()
    )

    return {
        row["filename"]: row["content"]
        for row in (response.data or [])
    }


def delete_note(filename):
    user_id = get_current_user_id()

    if user_id is None:
        return

    (
        supabase
        .table("notes")
        .delete()
        .eq("user_id", str(user_id))
        .eq("filename", filename)
        .execute()
    )


def get_notes_count():
    user_id = get_current_user_id()

    if user_id is None:
        return 0

    response = (
        supabase
        .table("notes")
        .select("id")
        .eq("user_id", str(user_id))
        .execute()
    )

    return len(response.data or [])


# ---------------- STUDY HOURS ----------------

def save_study_hours(hours):
    user_id = get_current_user_id()

    if user_id is None:
        return

    existing = (
        supabase
        .table("study_hours")
        .select("user_id")
        .eq("user_id", str(user_id))
        .execute()
    )

    if existing.data:

        supabase.table("study_hours").update({
            "hours": float(hours)
        }).eq(
            "user_id",
            str(user_id)
        ).execute()

    else:

        supabase.table("study_hours").insert({
            "user_id": str(user_id),
            "hours": float(hours)
        }).execute()


def get_study_hours():
    user_id = get_current_user_id()

    if user_id is None:
        return 0

    response = (
        supabase
        .table("study_hours")
        .select("hours")
        .eq("user_id", str(user_id))
        .execute()
    )

    if response.data:
        return float(response.data[0]["hours"])

    return 0


# ---------------- DASHBOARD ----------------

def get_dashboard_stats():

    quiz_stats = get_quiz_stats()

    return {
        "notes": get_notes_count(),
        "quizzes": quiz_stats["quiz_count"],
        "accuracy": quiz_stats["accuracy"],
        "study_hours": get_study_hours()
    }