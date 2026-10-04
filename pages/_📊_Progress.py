import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_manager import (
    get_quiz_results,
    get_quiz_stats,
    get_notes_count,
    get_study_hours
)


st.set_page_config(
    page_title="Progress",
    page_icon="📊",
    layout="wide"
)


st.title("📊 My Progress")
st.write(
    "Track your quizzes, accuracy, notes and study hours."
)

st.divider()


# -----------------------------
# GET DATA
# -----------------------------

quiz_results = get_quiz_results()

quiz_stats = get_quiz_stats()

notes_count = get_notes_count()

study_hours = get_study_hours()


# -----------------------------
# SUMMARY CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📄 Notes",
        notes_count
    )


with col2:

    st.metric(
        "📝 Quizzes",
        quiz_stats["quiz_count"]
    )


with col3:

    st.metric(
        "🎯 Average Accuracy",
        f"{quiz_stats['accuracy']:.1f}%"
    )


with col4:

    st.metric(
        "⏱️ Study Hours",
        f"{study_hours:.1f}"
    )


st.divider()


# -----------------------------
# ACCURACY GRAPH
# -----------------------------

st.subheader("📈 Quiz Accuracy")


if quiz_results:

    graph_data = []

    for i, result in enumerate(
        quiz_results,
        start=1
    ):

        graph_data.append({
            "Quiz": f"Quiz {i}",
            "Accuracy": float(
                result.get("accuracy", 0)
            )
        })


    df = pd.DataFrame(graph_data)


    fig = px.line(
        df,
        x="Quiz",
        y="Accuracy",
        markers=True,
        title="Quiz Accuracy Progress"
    )


    fig.update_layout(
        yaxis_title="Accuracy (%)",
        xaxis_title="Quiz",
        yaxis=dict(
            range=[0, 100]
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "📊 Complete at least one quiz "
        "to see your accuracy graph."
    )


st.divider()


# -----------------------------
# QUIZ HISTORY
# -----------------------------

st.subheader("📋 Quiz History")


if quiz_results:

    history_data = []

    for i, result in enumerate(
        quiz_results,
        start=1
    ):

        history_data.append({
            "Quiz": f"Quiz {i}",
            "Score": f"{result.get('score', 0)}/"
                     f"{result.get('total', 0)}",
            "Accuracy": f"{float(result.get('accuracy', 0)):.1f}%"
        })


    history_df = pd.DataFrame(
        history_data
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "📭 No quiz attempts yet."
    )


st.divider()


# -----------------------------
# STUDY SUMMARY
# -----------------------------

st.subheader("📚 Study Summary")

col1, col2 = st.columns(2)


with col1:

    st.write(
        f"📄 **Total Notes:** {notes_count}"
    )

    st.write(
        f"📝 **Total Quizzes:** "
        f"{quiz_stats['quiz_count']}"
    )


with col2:

    st.write(
        f"🎯 **Average Accuracy:** "
        f"{quiz_stats['accuracy']:.1f}%"
    )

    st.write(
        f"⏱️ **Study Hours:** "
        f"{study_hours:.1f}"
    )