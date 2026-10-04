import streamlit as st
from pathlib import Path

from utils.file_handler import (
    extract_text,
    save_note,
    get_saved_notes
)


st.set_page_config(
    page_title="My Notes",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("📄 My Notes")

st.write(
    "Upload, create, view and manage your study notes."
)

st.divider()


# -----------------------------
# UPLOAD / WRITE TABS
# -----------------------------

tab1, tab2 = st.tabs(
    [
        "📥 Upload Notes",
        "✍️ Write Notes"
    ]
)


# ==================================================
# UPLOAD NOTES
# ==================================================

with tab1:

    uploaded_file = st.file_uploader(
        "📂 Upload your study material",
        type=["pdf", "docx", "txt"],
        help="Supported formats: PDF, DOCX and TXT"
    )

    if uploaded_file:

        st.success(
            f"📄 {uploaded_file.name} uploaded successfully!"
        )

        if st.button(
            "📖 Extract & Save Notes",
            use_container_width=True
        ):

            with st.spinner(
                "🔍 Extracting text from your notes..."
            ):

                text = extract_text(
                    uploaded_file
                )

            if text.strip():

                filename = (
                    Path(
                        uploaded_file.name
                    ).stem
                    + ".txt"
                )

                save_note(
                    filename,
                    text
                )

                st.success(
                    "✅ Notes extracted and saved successfully!"
                )

                st.subheader(
                    "📖 Extracted Text"
                )

                st.text_area(
                    "Extracted content",
                    text,
                    height=300
                )

            else:

                st.error(
                    "❌ No readable text was found in this file."
                )

                st.info(
                    "If your PDF contains scanned images, "
                    "OCR will be needed to extract the text."
                )


# ==================================================
# WRITE NOTES
# ==================================================

with tab2:

    note_title = st.text_input(
        "📝 Note Title",
        placeholder="Example: Machine Learning Unit 1"
    )

    note_content = st.text_area(
        "Write your notes",
        height=300,
        placeholder="Type your study notes here..."
    )

    if st.button(
        "💾 Save Notes",
        use_container_width=True
    ):

        if not note_title.strip():

            st.warning(
                "⚠️ Please enter a note title."
            )

        elif not note_content.strip():

            st.warning(
                "⚠️ Please write some notes."
            )

        else:

            filename = (
                note_title.strip()
                .replace(" ", "_")
                + ".txt"
            )

            save_note(
                filename,
                note_content
            )

            st.success(
                "✅ Notes saved successfully!"
            )


# ==================================================
# SAVED NOTES
# ==================================================

st.divider()

st.subheader("📚 Saved Notes")

saved_notes = get_saved_notes()


if saved_notes:

    for note in saved_notes:

        col1, col2 = st.columns(
            [6, 1]
        )

        with col1:

            st.markdown(
                f"📄 **{note.name}**"
            )

        with col2:

            delete = st.button(
                "🗑️ Delete",
                key=f"delete_{note.name}",
                use_container_width=True
            )

        if delete:

            try:

                note.unlink()

                st.success(
                    f"🗑️ '{note.name}' deleted successfully!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Could not delete the note: {e}"
                )


        with st.expander(
            "👁️ View Note"
        ):

            try:

                with open(
                    note,
                    "r",
                    encoding="utf-8"
                ) as file:

                    content = file.read()

                st.text_area(
                    "Note content",
                    content,
                    height=200,
                    key=f"note_{note.name}"
                )

            except Exception:

                st.error(
                    "❌ Unable to read this note."
                )


else:

    st.info(
        "📭 No saved notes yet. "
        "Upload or create a note to get started."
    )