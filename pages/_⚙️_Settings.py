import streamlit as st

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings")
st.write("Customize your study experience.")

st.divider()

name = st.text_input(
    "👤 Student Name",
    value=st.session_state.get(
        "student_name",
        "Student"
    )
)

difficulty = st.selectbox(
    "🎯 Default Difficulty",
    ["Easy", "Medium", "Hard"],
    index=["Easy", "Medium", "Hard"].index(
        st.session_state.get(
            "difficulty",
            "Medium"
        )
    )
)

questions = st.slider(
    "📝 Questions Per Quiz",
    1,
    20,
    st.session_state.get(
        "questions",
        5
    )
)

study_goal = st.slider(
    "⏱️ Daily Study Goal (hours)",
    1,
    12,
    st.session_state.get(
        "study_goal",
        2
    )
)

st.divider()

if st.button(
    "💾 Save Settings",
    use_container_width=True
):
    st.session_state["student_name"] = name
    st.session_state["difficulty"] = difficulty
    st.session_state["questions"] = questions
    st.session_state["study_goal"] = study_goal

    st.success(
        "Settings saved successfully! 🎉"
    )