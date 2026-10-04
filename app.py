import streamlit as st

from utils.auth import (
    create_users_table,
    register_user,
    login_user
)


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Study Helper",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# DATABASE
# ==========================================

create_users_table()


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "username" not in st.session_state:
    st.session_state["username"] = None


# ==========================================
# LOGIN SCREEN
# ==========================================

if not st.session_state["logged_in"]:

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "<h1 style='text-align:center;'>📚 AI Study Helper</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Your personalized AI-powered study assistant"
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        tab1, tab2 = st.tabs(
            ["🔑 Login", "🆕 Create Account"]
        )

        # ==================================
        # LOGIN
        # ==================================

        with tab1:

            st.subheader("Welcome Back!")

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "🔑 Login",
                use_container_width=True
            ):

                if not username.strip():

                    st.warning(
                        "Please enter your username."
                    )

                elif not password:

                    st.warning(
                        "Please enter your password."
                    )

                else:

                    user = login_user(
                        username,
                        password
                    )

                    if user:

                        # Store complete login session
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = str(user[0])
                        st.session_state["username"] = str(user[1])

                        st.success(
                            f"✅ Login successful! Welcome {user[1]}"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "❌ Invalid username or password."
                        )


        # ==================================
        # CREATE ACCOUNT
        # ==================================

        with tab2:

            st.subheader("Create Your Account")

            new_username = st.text_input(
                "Username",
                key="register_username"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="register_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password"
            )

            if st.button(
                "🆕 Create Account",
                use_container_width=True
            ):

                if not new_username.strip():

                    st.warning(
                        "Please enter a username."
                    )

                elif not new_password:

                    st.warning(
                        "Please enter a password."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "❌ Passwords do not match."
                    )

                else:

                    created = register_user(
                        new_username,
                        new_password
                    )

                    if created:

                        st.success(
                            "✅ Account created successfully!"
                        )

                        st.info(
                            "Go to the Login tab and login."
                        )

                    else:

                        st.error(
                            "❌ Username already exists."
                        )

    st.stop()


# ==========================================
# LOGGED-IN USER
# ==========================================

st.title(
    f"👋 Welcome, {st.session_state['username']}!"
)

st.write(
    "You are successfully logged in to AI Study Helper."
)

st.info(
    "Use the sidebar to open your study tools."
)


# ==========================================
# SESSION INFORMATION
# ==========================================

with st.sidebar:

    st.success(
        f"👤 {st.session_state['username']}"
    )

    st.caption(
        f"User ID: {st.session_state['user_id']}"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["username"] = None

        st.rerun()