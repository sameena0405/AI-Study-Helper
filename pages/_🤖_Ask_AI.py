import streamlit as st
from modules.qa_system import answer_question


st.set_page_config(
    page_title="Ask AI",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Page Header
# -----------------------------

st.title("🤖 Ask AI")
st.write("Your personal AI-powered study assistant.")

st.divider()


# -----------------------------
# Initialize Chat History
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -----------------------------
# Settings
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox(
        "📚 Select Subject",
        [
            "Python",
            "Machine Learning",
            "NLP",
            "Artificial Intelligence",
            "Deep Learning",
            "Data Science",
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


st.divider()


# -----------------------------
# Display Previous Messages
# -----------------------------

for message in st.session_state.chat_history:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    else:

        with st.chat_message("assistant"):
            st.write(message["content"])


# -----------------------------
# User Input
# -----------------------------

question = st.chat_input(
    "Ask something about your subject..."
)


# -----------------------------
# Ask AI
# -----------------------------

if question:

    # Display user question
    with st.chat_message("user"):
        st.write(question)

    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            answer = answer_question(
                question,
                topic,
                difficulty,
                st.session_state.chat_history
            )

        st.write(answer)


    # Save conversation
    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# -----------------------------
# Clear Conversation
# -----------------------------

st.divider()

if st.button("🗑️ Clear Conversation"):

    st.session_state.chat_history = []

    st.rerun()