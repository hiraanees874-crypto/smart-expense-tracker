import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

# --- 1. USER AUTHENTICATION CONFIGURATION ---
# Plain passwords match karne ke liye direct config
credentials = {
    "usernames": {
        "hira": {
            "name": "Hira Anees",
            "password": "hira123",
        },
        "guest": {
            "name": "Guest User",
            "password": "guest123",
        },
    }
}

# Create authenticator object
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="expense_tracker_cookie",
    key="auth_key_12345",
    cookie_expiry_days=30,
)

# Custom Login logic (bina library mismatch error ke)
st.title("🔐 Login Page")

with st.form("login_form"):
    username_input = st.text_input("Username").strip().lower()
    password_input = st.text_input("Password", type="password")
    submit_login = st.form_submit_button("Login")

    if submit_login:
        users = credentials["usernames"]
        if (
            username_input in users
            and users[username_input]["password"] == password_input
        ):
            st.session_state["authentication_status"] = True
            st.session_state["username"] = username_input
            st.session_state["name"] = users[username_input]["name"]
            st.rerun()
        else:
            st.session_state["authentication_status"] = False
            st.error("Username/password galat hai!")

# Accessing login status
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")
name = st.session_state.get("name")

# --- 2. LOGGED IN USER SECTION ---
if authentication_status:

    st.sidebar.write(f"Logged in as: **{name}**")
    if st.sidebar.button("Logout"):
        st.session_state["authentication_status"] = None
        st.session_state["username"] = None
        st.session_state["name"] = None
        st.rerun()

    # Har user ke liye ALAG CSV File ka naam
    user_file = f"expenses_{username}.csv"

    st.title(f"💸 Smart Expense Tracker - ({name})")

    # --- EXPENSE INPUT FORM ---
    with st.form("expense_form"):
        date = st.date_input("Date")
        item = st.text_input("Item Name")
        amount = st.number_input("Amount (Rs.)", min_value=0.0, step=10.0)
        category = st.selectbox(
            "Category", ["Food", "Transport", "Bills", "Shopping", "Other"]
        )
        submit = st.form_submit_button("Add Expense")

        if submit:
            if item.strip() != "":
                new_data = pd.DataFrame(
                    [[date, item, amount, category]],
                    columns=["Date", "Item", "Amount", "Category"],
                )
                try:
                    existing_df = pd.read_csv(
                        user_file,
                        names=["Date", "Item", "Amount", "Category"],
                    )
                    updated_df = pd.concat(
                        [existing_df, new_data], ignore_index=True
                    )
                except FileNotFoundError:
                    updated_df = new_data

                updated_df.to_csv(user_file, index=False, header=False)
                st.success("Expense Add Ho Gaya!")
                st.rerun()
            else:
                st.warning("Kripya item ka naam likhein!")

    st.divider()

    # --- DISPLAY & EDIT USER'S OWN DATA ---
    st.header("📊 Your Expenses Summary")

    try:
        df = pd.read_csv(
            user_file, names=["Date", "Item", "Amount", "Category"]
        )

        edited_df = st.data_editor(
            df, num_rows="dynamic", use_container_width=True
        )

        total_spent = edited_df["Amount"].sum()
        st.metric(label="Total Spent", value=f"Rs. {total_spent}")

        edited_df.to_csv(user_file, index=False, header=False)

    except FileNotFoundError:
        st.info(
            "💡 Aapka koi data save nahi hai. Upar se pehla expense add karein!"
        )
