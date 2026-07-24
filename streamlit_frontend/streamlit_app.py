import streamlit as st
import uuid

from auth import login, register
from api import stream_chat
# ---------------- Page Config ----------------

st.set_page_config(
    page_title="Customer Support AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CSS ----------------

try:
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )
except FileNotFoundError:
    pass

# ---------------- Session ----------------

defaults = {
    "logged_in": False,
    "show_signup": False,
    "token": "",
    "customer_email": "",
    "role": "",
    "messages": [],
    "thread_id": str(uuid.uuid4()),
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==========================================================
# LOGIN / SIGNUP
# ==========================================================

if not st.session_state.logged_in:

    # ---------------- LOGIN ----------------

    if not st.session_state.show_signup:

        st.title("🤖 Customer Support AI")
        st.caption("Powered by OpenAI GPT")

        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            try:

                with st.spinner("Logging in..."):

                    result = login(email, password)

                st.session_state.logged_in = True
                st.session_state.token = result["access_token"]
                st.session_state.customer_email = result["customer_email"]
                st.session_state.role = result["role"]

                st.rerun()

            except Exception as e:

                st.error(str(e))

        st.divider()

        st.write("Don't have an account?")

        if st.button(
            "Create Account",
            use_container_width=True
        ):
            st.session_state.show_signup = True
            st.rerun()

        role = st.session_state.role

        

    # ---------------- SIGNUP ----------------

    else:

        st.title("📝 Create Account")

        with st.form("signup_form", clear_on_submit=False):

            username = st.text_input("Username")

            signup_email = st.text_input("Email")

            signup_password = st.text_input(
                "Password",
                type="password",
            )

            product = st.text_input(
                "Product Name",
                placeholder="Enter the product/service name"
            )

            issue_description = st.text_area(
                "Issue Description"
            )

            signup_btn = st.form_submit_button(
                "Create Account"
            )

            if signup_btn:

                if not username.strip():
                    st.warning("Please enter your username.")

                elif not signup_email.strip():
                    st.warning("Please enter your email.")

                elif not signup_password.strip():
                    st.warning("Please enter your password.")

                elif not product.strip():
                    st.warning("Please enter the product name.")

                elif not issue_description.strip():
                    st.warning("Please describe your issue.")

                else:
                    try:
                        register(
                            username,
                            signup_email,
                            signup_password,
                            product,
                            issue_description,
                        )

                        st.success("✅ Account created successfully!")

                    except Exception as e:
                        st.error(str(e))

        if st.button(
            "⬅ Back to Login",
            use_container_width=True
        ):

            st.session_state.show_signup = False
            st.rerun()

# ==========================================================
# CHAT PAGE
# ==========================================================

else:

    

    # ---------------- Sidebar ----------------

    with st.sidebar:

        st.title("🤖 Customer AI")

        st.success(
            f"👤 {st.session_state.customer_email}"
        )

        st.info(
            f"Role : {st.session_state.role.upper()}"
        )

        st.divider()

        if st.button("➕ New Chat"):

            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())

            st.rerun()

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.session_state.show_signup = False
            st.session_state.token = ""
            st.session_state.customer_email = ""
            st.session_state.role = ""
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())

            st.rerun()

    # ---------------- Chat ----------------

    st.title("💬 AI Customer Support Assistant")

    st.caption(
        "Ask about tickets, documentation, or operational requests."
    )

    # Previous Messages

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input(
        "Type your message..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            placeholder = st.empty()

            full_response = ""

            try:

                with st.spinner(
                    "🤖 AI is thinking..."
                ):

                    response = stream_chat(
                        prompt,
                        st.session_state.thread_id,
                        st.session_state.token,
                    )

                    for chunk in response.iter_content(
                        chunk_size=1024,
                        decode_unicode=True,
                    ):

                        if chunk:

                            full_response += chunk

                            placeholder.markdown(
                                full_response + "▌"
                            )

                placeholder.markdown(full_response)

            except Exception as e:

                full_response = f"❌ {e}"

                placeholder.error(full_response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
            }
        )