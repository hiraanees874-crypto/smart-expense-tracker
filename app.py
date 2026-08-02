import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth

# --- 1. USER AUTHENTICATION CONFIGURATION ---
# Yahan aap naye users aur passwords add kar sakte hain
names = ["Hira Anees", "Guest User"]
usernames = ["hira", "guest"]

# Hashed passwords (Example passwords: 'hira123' aur 'guest123')
# Streamlit-authenticator requires plain passwords to be hashed
passwords = ["hira123", "guest123"]
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0],
        },
        usernames[1]: {
            "name": names[1],
            "password": hashed_passwords[1],
        },
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "expense_tracker_cookie",
    "auth_key_12345",
    cookie_expiry_days=30,
)

# Login Widget
name, authentication_status, username = authenticator.login("Login", "main")

# --- 2. LOGIN CHECK ---
if authentication_status == False:
    st.error("Username/password galat hai!")
elif authentication_status == None:
    st.warning("Kripya apna Username aur Password dalein.")
elif authentication_status:

    # --- LOGGED IN USER SECTION ---
    authenticator.logout("Logout", "sidebar")
    st.write(f"### Welcome, *{name}*! 👋")

    # Har user ke liye ALAG CSV File ka naam
    user_file = f"expenses_{username}.csv"

    st.title("💸 Smart Expense Tracker")

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
                    # Purana data read karke naya add karein
                    existing_df = pd.read_csv(
                        user_file,
                        names=["Date", "Item", "Amount", "Category"],
                    )
                    updated_df = pd.concat(
                        [existing_df, new_data], ignore_index=True
                    )
                except FileNotFoundError:
                    updated_df = new_data

                # User ki specific CSV me save karein
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

        # Editable Table
        edited_df = st.data_editor(
            df, num_rows="dynamic", use_container_width=True
        )

        # Total Calculation
        total_spent = edited_df["Amount"].sum()
        st.metric(label="Total Spent", value=f"Rs. {total_spent}")

        # Delete / Edit Sync
        edited_df.to_csv(user_file, index=False, header=False)

    except FileNotFoundError:
        st.info("💡 Aapka koi data save nahi hai. Upar se pehla expense add karein!")
