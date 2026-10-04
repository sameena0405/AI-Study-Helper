import streamlit as st
from datetime import date, timedelta

from modules.study_planner import create_study_plan


st.set_page_config(
    page_title="Study Planner",
    page_icon="📅",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("📅 Study Planner")

st.write(
    "Create a personalized study schedule "
    "based on your subjects, priorities and available time."
)

st.divider()


# ==========================================
# PLANNER SETTINGS
# ==========================================

st.subheader("⚙️ Plan Your Study")

col1, col2, col3 = st.columns(3)

with col1:

    start_date = st.date_input(
        "📅 Start Date",
        value=date.today()
    )

with col2:

    days = st.number_input(
        "🗓️ Study Duration (Days)",
        min_value=1,
        max_value=30,
        value=7
    )

with col3:

    daily_hours = st.number_input(
        "⏱️ Daily Study Hours",
        min_value=1.0,
        max_value=12.0,
        value=3.0,
        step=0.5
    )


st.divider()


# ==========================================
# SUBJECTS
# ==========================================

st.subheader("📚 Your Subjects")

st.caption(
    "Add the subjects you want to study "
    "and set their priority."
)


if "subjects" not in st.session_state:

    st.session_state.subjects = [
        {
            "name": "",
            "priority": "High"
        }
    ]


for i in range(
    len(st.session_state.subjects)
):

    col1, col2, col3 = st.columns(
        [5, 2, 1]
    )

    with col1:

        st.session_state.subjects[i]["name"] = (
            st.text_input(
                f"Subject {i + 1}",
                value=st.session_state.subjects[i]["name"],
                placeholder="Example: Machine Learning",
                key=f"subject_{i}"
            )
        )

    with col2:

        st.session_state.subjects[i]["priority"] = (
            st.selectbox(
                "Priority",
                [
                    "High",
                    "Medium",
                    "Low"
                ],
                index=[
                    "High",
                    "Medium",
                    "Low"
                ].index(
                    st.session_state.subjects[i]["priority"]
                ),
                key=f"priority_{i}"
            )
        )

    with col3:

        if len(st.session_state.subjects) > 1:

            if st.button(
                "🗑️",
                key=f"delete_{i}"
            ):

                st.session_state.subjects.pop(i)

                st.rerun()


st.write("")


col1, col2 = st.columns(2)

with col1:

    if st.button(
        "➕ Add Subject",
        use_container_width=True
    ):

        st.session_state.subjects.append(
            {
                "name": "",
                "priority": "Medium"
            }
        )

        st.rerun()


with col2:

    generate = st.button(
        "✨ Generate Study Plan",
        use_container_width=True,
        type="primary"
    )


# ==========================================
# GENERATE PLAN
# ==========================================

if generate:

    valid_subjects = [
        subject
        for subject in st.session_state.subjects
        if subject["name"].strip()
    ]

    if not valid_subjects:

        st.warning(
            "Please add at least one subject."
        )

    else:

        plan = create_study_plan(
            valid_subjects,
            start_date,
            days,
            daily_hours
        )

        st.session_state.study_plan = plan
        st.session_state.plan_start = start_date
        st.session_state.plan_days = days
        st.session_state.plan_hours = daily_hours


# ==========================================
# DISPLAY PLAN
# ==========================================

if "study_plan" in st.session_state:

    plan = st.session_state.study_plan

    st.divider()

    st.subheader("📋 Your Personalized Study Plan")

    # --------------------------------------
    # SUMMARY
    # --------------------------------------

    total_hours = (
        st.session_state.plan_days
        * st.session_state.plan_hours
    )

    study_days = st.session_state.plan_days

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📅 Study Days",
            study_days
        )

    with col2:

        st.metric(
            "⏱️ Daily Hours",
            f"{st.session_state.plan_hours:.1f} h"
        )

    with col3:

        st.metric(
            "📚 Total Hours",
            f"{total_hours:.1f} h"
        )

    with col4:

        st.metric(
            "🎯 Subjects",
            len(
                [
                    s
                    for s in st.session_state.subjects
                    if s["name"].strip()
                ]
            )
        )


    st.divider()


    # --------------------------------------
    # DAILY SCHEDULE
    # --------------------------------------

    for day in plan:

        current_date = day["date"]

        date_text = current_date.strftime(
            "%A, %d %B %Y"
        )

        st.markdown(
            f"### 📅 Day {day['day']} — {date_text}"
        )

        st.caption(
            f"Total study time: "
            f"{day['total_hours']:.1f} hours"
        )


        if not day["sessions"]:

            st.info(
                "No study sessions planned."
            )

            continue


        for session in day["sessions"]:

            if session["priority"] == "High":

                priority_icon = "🔥"

            elif session["priority"] == "Medium":

                priority_icon = "🟡"

            else:

                priority_icon = "🟢"


            col1, col2, col3 = st.columns(
                [5, 2, 2]
            )

            with col1:

                st.markdown(
                    f"**📚 {session['subject']}**"
                )

            with col2:

                st.markdown(
                    f"{priority_icon} "
                    f"{session['priority']}"
                )

            with col3:

                st.markdown(
                    f"⏱️ {session['hours']:.1f} hr"
                )


        st.divider()


    # --------------------------------------
    # STUDY TIPS
    # --------------------------------------

    st.subheader("💡 Study Strategy")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "🧠 **Active Recall**\n\n"
            "After each session, close your notes "
            "and recall the important concepts."
        )

    with col2:

        st.info(
            "🔄 **Revision**\n\n"
            "Spend the last 15–20 minutes of your "
            "study day reviewing what you learned."
        )


    st.divider()

    st.success(
        "🎯 Your study plan is ready. "
        "Follow each session and track your progress "
        "from the Progress page."
    )