import streamlit as st
from modules.summarizer import summarize_text

st.set_page_config(
    page_title="Summarizer",
    page_icon="✨",
    layout="wide"
)

st.title("✨ AI Note Summarizer")
st.write("Convert long study material into concise summaries.")

st.divider()

text = st.text_area(
    "Paste your study notes here",
    height=300,
    placeholder="Paste your notes here..."
)

length = st.selectbox(
    "Summary Length",
    ["Short", "Medium", "Detailed"]
)

if st.button("✨ Generate Summary", use_container_width=True):

    if text.strip():

        with st.spinner("Generating summary..."):

            summary = summarize_text(text, length)

        st.subheader("📌 Summary")

        st.success(summary)

    else:
        st.warning("Please enter some notes first.")