import streamlit as st

from modules.quiz_generator import generate_quiz
from utils.data_manager import save_quiz_result


st.set_page_config(
    page_title="Quiz Generator",
    page_icon="📝",
    layout="wide"
)


st.title("📝 AI Quiz Generator")

st.write(
    "Choose a topic and let AI create a personalized quiz."
)

st.divider()


# -----------------------------
# Quiz Settings
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    subject = st.selectbox(
        "📚 Select Subject",
        [
            "Python",
            "Machine Learning",
            "Artificial Intelligence",
            "NLP",
            "Deep Learning",
            "Data Science",
            "Computer Networks",
            "Database Management",
            "General"
        ]
    )


with col2:

    difficulty = st.selectbox(
        "🎯 Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )


topic = st.text_input(
    "📖 Enter Quiz Topic",
    placeholder="Example: Supervised Learning"
)


num_questions = st.slider(
    "🔢 Number of Questions",
    min_value=1,
    max_value=10,
    value=5
)


# -----------------------------
# Clear old quiz when settings change
# -----------------------------

settings = (
    subject,
    difficulty,
    topic,
    num_questions
)

if "quiz_settings" not in st.session_state:

    st.session_state.quiz_settings = settings

elif st.session_state.quiz_settings != settings:

    st.session_state.pop("quiz", None)
    st.session_state.pop("quiz_submitted", None)

    st.session_state.quiz_settings = settings


st.divider()


# -----------------------------
# Generate Quiz
# -----------------------------

if st.button(
    "✨ Generate AI Quiz",
    use_container_width=True
):

    if not topic.strip():

        st.warning(
            "Please enter a quiz topic first."
        )

    else:

        with st.spinner(
            f"🤖 Generating {num_questions} questions..."
        ):

            quiz = generate_quiz(
    subject,
    topic,
    difficulty,
    num_questions
)

        if len(quiz) < num_questions:

            st.error(
                f"Only {len(quiz)} questions were generated. "
                "Please click Generate AI Quiz again."
            )

            st.session_state.pop("quiz", None)

        else:

            st.session_state.quiz = quiz

            st.session_state.quiz_topic = topic

            st.session_state.quiz_difficulty = difficulty

            st.session_state.quiz_submitted = False

            st.success(
                f"🎉 {num_questions} questions generated!"
            )


# -----------------------------
# Display Quiz ONLY after generation
# -----------------------------

if "quiz" in st.session_state:

    quiz = st.session_state.quiz

    st.divider()

    st.subheader(
        f"🧠 {st.session_state.quiz_topic}"
    )

    st.caption(
        f"Difficulty: "
        f"{st.session_state.quiz_difficulty} | "
        f"Questions: {len(quiz)}"
    )

    answers = {}

    for i, q in enumerate(quiz):

        st.markdown(
            f"### Q{i + 1}. {q['question']}"
        )

        answers[i] = st.radio(
            "Choose your answer:",
            q["options"],
            key=f"quiz_{i}"
        )

        st.divider()


    # -----------------------------
    # Submit Quiz
    # -----------------------------

    if st.button(
        "✅ Submit Quiz",
        use_container_width=True
    ):

        score = 0

        for i, q in enumerate(quiz):

            if answers[i] == q["answer"]:
                score += 1


        accuracy = (
            score / len(quiz)
        ) * 100


        save_quiz_result(
            score,
            len(quiz),
            accuracy
        )


        st.session_state.quiz_submitted = True


        st.divider()

        st.subheader("🎯 Your Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Score",
                f"{score}/{len(quiz)}"
            )

        with col2:

            st.metric(
                "Accuracy",
                f"{accuracy:.0f}%"
            )


        st.divider()

        st.subheader("📖 Answer Review")

        for i, q in enumerate(quiz):

            if answers[i] == q["answer"]:

                st.success(
                    f"Q{i + 1} — Correct ✅"
                )

            else:

                st.error(
                    f"Q{i + 1} — Incorrect ❌"
                )

                st.write(
                    f"Correct answer: **{q['answer']}**"
                )