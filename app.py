import streamlit as st

from utils.data_manager import get_dashboard_stats


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Study Helper",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# DASHBOARD DATA
# ==========================================

stats = get_dashboard_stats()


notes_count = stats["notes"]

quiz_count = stats["quizzes"]

accuracy = stats["accuracy"]

study_hours = stats["study_hours"]


# ==========================================
# HEADER
# ==========================================

st.title("📚 AI-Powered Study Helper")

st.subheader(
    "Learn smarter. Study better. Achieve more. 🚀"
)

st.write(
    "Welcome to your personalized study assistant. "
    "Use the tools in the sidebar to learn, "
    "practice and track your progress."
)

st.divider()


# ==========================================
# DASHBOARD METRICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📄 Notes",
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
# STUDY TOOLS
# ==========================================

st.header("🚀 Study Tools")


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 🤖 Ask AI")

    st.write(
        "Ask questions about your study topics."
    )


with col2:

    st.markdown("### ✨ Summarizer")

    st.write(
        "Convert long notes into concise summaries."
    )


with col3:

    st.markdown("### 📝 Quiz Generator")

    st.write(
        "Generate AI-powered practice questions."
    )


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 🧠 Flashcards")

    st.write(
        "Create quick revision flashcards."
    )


with col2:

    st.markdown("### 📅 Study Planner")

    st.write(
        "Create a personalized study schedule."
    )


with col3:

    st.markdown("### 📊 Progress")

    st.write(
        "Track your learning performance."
    )


st.divider()


# ==========================================
# GET STARTED
# ==========================================

st.info(
    "👈 Select a feature from the sidebar to get started!"
)