import pandas as pd
import streamlit as st

st.set_page_config(page_title="Expense Tracker", page_icon="💸")

# --- USER CREDENTIALS ---
USERS = {"hira": "hira123", "guest": "guest123"}

st.title("💸 Smart Expense Tracker")

# Sidebar me Login Details
st.sidebar.header("🔐 User Login")
user_input = (
    st.sidebar.text_input("Username", key="user_key").strip().lower()
)
pass_input = st.sidebar.text_input(
    "Password", type="password", key="pass_key"
)

# Login Verification
if user_input in USERS and USERS[user_input] == pass_input:
    st.sidebar.success(f"Welcome, {user_input.capitalize()}! 👋")

    # Har user ki alag CSV File
    user_file = f"expenses_{user_input}.csv"

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

    # --- DISPLAY & EDIT USER'S DATA ---
    st.header(f"📊 {user_input.capitalize()}'s Expenses Summary")

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
        st.info("💡 Aapka koi data save nahi hai. Pehla expense add karein!")

else:
    if user_input or pass_input:
        st.error("❌ Username ya Password galat hai!")
    else:
        st.info("👈 Left Sidebar me apna Username aur Password dalke login karein.")
