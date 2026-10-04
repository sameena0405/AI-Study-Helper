import streamlit as st

from modules.flashcard_generator import generate_flashcards
from utils.data_manager import get_notes, delete_note


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Flashcards",
    page_icon="🧠",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🧠 AI Flashcards")

st.write(
    "Turn your study material into smart revision "
    "flashcards using AI."
)

st.divider()


# ==========================================
# STUDY MATERIAL
# ==========================================

st.subheader("📚 Choose Your Study Material")

tab1, tab2 = st.tabs(
    [
        "📁 Saved Notes",
        "✍️ Enter Text"
    ]
)


# ==========================================
# SAVED NOTES
# ==========================================

with tab1:

    saved_notes = get_notes()

    if saved_notes:

        note_names = list(saved_notes.keys())

        selected_note = st.selectbox(
            "📚 Select a saved note",
            note_names
        )

        saved_text = saved_notes[selected_note]

        st.success(
            f"📄 Using: {selected_note}"
        )

        # ==================================
        # DELETE SELECTED NOTE
        # ==================================

        if st.button(
            "🗑️ Delete Selected Note",
            use_container_width=True
        ):

            delete_note(selected_note)

            # Clear generated flashcards if needed
            if "flashcards" in st.session_state:
                del st.session_state.flashcards

            st.success(
                f"✅ '{selected_note}' deleted successfully!"
            )

            st.rerun()

    else:

        st.info(
            "📭 No saved notes available. "
            "You can create notes from the Notes page "
            "or enter text manually."
        )

        saved_text = ""


# ==========================================
# ENTER TEXT
# ==========================================

with tab2:

    manual_text = st.text_area(
        "✍️ Enter your study material",
        height=250,
        placeholder=(
            "Paste or type your study material here..."
        )
    )

    st.caption(
        "You can paste text from textbooks, "
        "class notes, PDFs, websites, etc."
    )


# ==========================================
# SOURCE SELECTION
# ==========================================

source_choice = st.radio(
    "📌 Generate flashcards from:",
    [
        "📁 Saved Note",
        "✍️ Entered Text"
    ],
    horizontal=True
)


if source_choice == "📁 Saved Note":

    study_text = saved_text

else:

    study_text = manual_text


st.divider()


# ==========================================
# SETTINGS
# ==========================================

st.subheader("⚙️ Flashcard Settings")

col1, col2 = st.columns(2)


with col1:

    card_count = st.slider(
        "🔢 Number of Flashcards",
        min_value=3,
        max_value=15,
        value=5
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


# ==========================================
# GENERATE FLASHCARDS
# ==========================================

if st.button(
    "✨ Generate AI Flashcards",
    use_container_width=True,
    type="primary"
):

    if not study_text.strip():

        st.warning(
            "⚠️ Please select a saved note "
            "or enter some study material."
        )

    else:

        with st.spinner(
            "🤖 AI is creating your flashcards..."
        ):

            cards = generate_flashcards(
                study_text,
                card_count,
                difficulty
            )

        if not cards:

            st.error(
                "❌ Could not generate flashcards. "
                "Please check your Groq API configuration."
            )

        else:

            st.session_state.flashcards = cards
            st.session_state.flashcard_index = 0
            st.session_state.flashcard_known = 0
            st.session_state.flashcard_revision = 0
            st.session_state.show_answer = False

            st.success(
                f"🎉 {len(cards)} flashcards generated!"
            )


# ==========================================
# DISPLAY FLASHCARDS
# ==========================================

if "flashcards" in st.session_state:

    cards = st.session_state.flashcards

    index = st.session_state.flashcard_index

    completed = (
        st.session_state.flashcard_known
        + st.session_state.flashcard_revision
    )


    st.divider()

    st.subheader("🧠 Revision Cards")


    # ======================================
    # PROGRESS
    # ======================================

    st.progress(
        min(completed / len(cards), 1.0)
    )

    st.caption(
        f"Card {index + 1} of {len(cards)}"
    )


    # ======================================
    # QUESTION
    # ======================================

    card = cards[index]

    st.markdown(
        f"""
        <div style="
            padding: 35px;
            border-radius: 18px;
            border: 1px solid #555;
            text-align: center;
            margin: 20px 0;
        ">

        <h2>🧠 Question</h2>

        <h3>{card["question"]}</h3>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ======================================
    # REVEAL ANSWER
    # ======================================

    if not st.session_state.show_answer:

        if st.button(
            "🔄 Reveal Answer",
            use_container_width=True
        ):

            st.session_state.show_answer = True

            st.rerun()


    # ======================================
    # ANSWER
    # ======================================

    if st.session_state.show_answer:

        st.success(
            f"💡 **Answer:** {card['answer']}"
        )

        st.write("")

        col1, col2 = st.columns(2)


        with col1:

            if st.button(
                "✅ I Know",
                use_container_width=True
            ):

                st.session_state.flashcard_known += 1

                if index < len(cards) - 1:

                    st.session_state.flashcard_index += 1
                    st.session_state.show_answer = False

                    st.rerun()

                else:

                    st.session_state.flashcard_index = index


        with col2:

            if st.button(
                "❌ Need Revision",
                use_container_width=True
            ):

                st.session_state.flashcard_revision += 1

                if index < len(cards) - 1:

                    st.session_state.flashcard_index += 1
                    st.session_state.show_answer = False

                    st.rerun()


    # ======================================
    # SUMMARY
    # ======================================

    if completed >= len(cards):

        st.divider()

        st.subheader("🎯 Revision Summary")

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Total Cards",
                len(cards)
            )


        with col2:

            st.metric(
                "✅ I Know",
                st.session_state.flashcard_known
            )


        with col3:

            st.metric(
                "❌ Need Revision",
                st.session_state.flashcard_revision
            )


        st.divider()


        # ==================================
        # REVIEW AGAIN
        # ==================================

        if st.button(
            "🔁 Review Again",
            use_container_width=True
        ):

            st.session_state.flashcard_index = 0
            st.session_state.flashcard_known = 0
            st.session_state.flashcard_revision = 0
            st.session_state.show_answer = False

            st.rerun()