import streamlit as st


# ==========================================
# INITIALIZE USER DATA
# ==========================================

def initialize_user_data():

    if "quiz_results" not in st.session_state:
        st.session_state.quiz_results = []

    if "study_hours" not in st.session_state:
        st.session_state.study_hours = 0.0

    if "notes" not in st.session_state:
        st.session_state.notes = []


# ==========================================
# QUIZ RESULTS
# ==========================================

def save_quiz_result(score, total, accuracy):

    initialize_user_data()

    st.session_state.quiz_results.append({
        "score": score,
        "total": total,
        "accuracy": accuracy
    })


# ==========================================
# GET QUIZ RESULTS
# ==========================================

def get_quiz_results():

    initialize_user_data()

    return st.session_state.quiz_results


# ==========================================
# GET QUIZ STATISTICS
# ==========================================

def get_quiz_stats():

    results = get_quiz_results()

    if not results:
        return {
            "quiz_count": 0,
            "accuracy": 0
        }

    accuracies = [
        float(result.get("accuracy", 0))
        for result in results
    ]

    return {
        "quiz_count": len(results),
        "accuracy": sum(accuracies) / len(accuracies)
    }


# ==========================================
# NOTES
# ==========================================

def add_note(filename):

    initialize_user_data()

    if filename not in st.session_state.notes:
        st.session_state.notes.append(filename)


def get_notes_count():

    initialize_user_data()

    return len(st.session_state.notes)


# ==========================================
# STUDY HOURS
# ==========================================

def get_study_hours():

    initialize_user_data()

    return float(st.session_state.study_hours)


# ==========================================
# SAVE STUDY HOURS
# ==========================================

def save_study_hours(hours):

    initialize_user_data()

    st.session_state.study_hours = float(hours)


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def get_dashboard_stats():

    quiz_stats = get_quiz_stats()

    return {
        "notes": get_notes_count(),
        "quizzes": quiz_stats["quiz_count"],
        "accuracy": quiz_stats["accuracy"],
        "study_hours": get_study_hours()
    }