import streamlit as st
import plotly.graph_objects as go

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


# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("📊 My Progress")

st.write(
    "Track your learning performance "
    "and quiz results."
)

st.divider()


# -----------------------------
# GET DATA
# -----------------------------

quiz_results = get_quiz_results()
quiz_stats = get_quiz_stats()
notes_count = get_notes_count()
study_hours = get_study_hours()


quiz_count = quiz_stats["quiz_count"]
accuracy = quiz_stats["accuracy"]


# -----------------------------
# SUMMARY CARDS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📝 Quizzes Completed",
        quiz_count
    )

with col2:
    st.metric(
        "🎯 Average Accuracy",
        f"{accuracy:.0f}%"
    )

with col3:
    st.metric(
        "📚 Notes",
        notes_count
    )

with col4:
    st.metric(
        "⏱️ Study Hours",
        f"{study_hours:.1f}"
    )


st.divider()


# -----------------------------
# QUIZ PERFORMANCE
# -----------------------------

st.subheader("🎯 Quiz Performance")


if quiz_results:

    quiz_numbers = list(
        range(1, len(quiz_results) + 1)
    )

    accuracies = [
        float(result.get("accuracy", 0))
        for result in quiz_results
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=quiz_numbers,
            y=accuracies,
            mode="lines+markers",
            name="Accuracy"
        )
    )

    fig.update_layout(
        title="Quiz Accuracy",
        xaxis_title="Quiz Number",
        yaxis_title="Accuracy (%)",
        yaxis=dict(
            range=[0, 100]
        ),
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


else:

    st.info(
        "📭 No quiz results yet. "
        "Complete a quiz to see your progress."
    )


st.divider()


# -----------------------------
# QUIZ HISTORY
# -----------------------------

st.subheader("📋 Quiz History")


if quiz_results:

    for i, result in enumerate(
        reversed(quiz_results),
        start=1
    ):

        score = result.get(
            "score",
            0
        )

        total = result.get(
            "total",
            0
        )

        result_accuracy = float(
            result.get(
                "accuracy",
                0
            )
        )

        st.write(
            f"**Quiz {len(quiz_results) - i + 1}**"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Score",
                f"{score}/{total}"
            )

        with col2:
            st.metric(
                "Accuracy",
                f"{result_accuracy:.0f}%"
            )

        with col3:

            if result_accuracy >= 80:
                st.success("Excellent 🌟")

            elif result_accuracy >= 60:
                st.info("Good 👍")

            else:
                st.warning("Needs Practice 📚")

        st.divider()


else:

    st.info(
        "Complete your first quiz to create "
        "your quiz history."
    )


# -----------------------------
# STUDY SUMMARY
# -----------------------------

st.subheader("📈 Study Summary")

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"📚 You currently have "
        f"**{notes_count}** saved notes."
    )

with col2:

    st.info(
        f"⏱️ Your recorded study time is "
        f"**{study_hours:.1f} hours**."
    )