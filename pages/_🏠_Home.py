import streamlit as st

from utils.data_manager import get_dashboard_stats


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)


# ==========================================
# GET DASHBOARD DATA
# ==========================================

stats = get_dashboard_stats()

notes_count = stats["notes"]
quiz_count = stats["quizzes"]
accuracy = stats["accuracy"]
study_hours = stats["study_hours"]


# ==========================================
# HEADER
# ==========================================

st.title("🏠 Welcome to AI-Powered Study Helper 👋")

st.write(
    "This platform helps you summarize notes, "
    "generate quizzes, create flashcards and "
    "organize your study schedule."
)

st.divider()


# ==========================================
# STATISTICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📚 Notes",
        notes_count
    )


with col2:

    st.metric(
        "📝 Quizzes",
        quiz_count
    )


with col3:

    st.metric(
        "🎯 Accuracy",
        f"{accuracy:.0f}%"
    )


with col4:

    st.metric(
        "⏱️ Study Hours",
        f"{study_hours:.1f}"
    )


st.divider()


# ==========================================
# AVAILABLE FEATURES
# ==========================================

st.header("✨ Available Features")


col1, col2 = st.columns(2)


with col1:

    st.markdown("### 🤖 Ask AI")

    st.write(
        "Ask questions about your study material."
    )


    st.markdown("### 📄 Notes")

    st.write(
        "Upload and manage your notes."
    )


    st.markdown("### ✨ Summarizer")

    st.write(
        "Generate concise summaries."
    )


    st.markdown("### 📝 Quiz")

    st.write(
        "Practice using AI-generated quizzes."
    )


with col2:

    st.markdown("### 🧠 Flashcards")

    st.write(
        "Create revision flashcards."
    )


    st.markdown("### 📅 Study Planner")

    st.write(
        "Plan your study sessions."
    )


    st.markdown("### 📊 Progress")

    st.write(
        "Analyze your learning progress."
    )


st.divider()


st.info(
    "👈 Select a feature from the sidebar to get started!"
)