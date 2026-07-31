import csv
from datetime import datetime
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Smart Expense Tracker", layout="centered")

st.title("💳 Smart Expense Tracker")
st.write("Apne daily kharchon ko yahan log karein aur track karein.")

# 1. Input Form
with st.form("expense_form"):
    item = st.text_input("Item Ka Naam (e.g. Lunch, Metro)")
    amount = st.number_input("Amount (Rs.)", min_value=1.0, step=10.0)
    category = st.selectbox(
        "Category", ["Food", "Transport", "Bills", "Shopping", "Other"]
    )

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if item.strip() != "":
            date = datetime.now().strftime("%Y-%m-%d")
            # CSV file mein data save karna
            with open("expenses.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([date, item, amount, category])
            st.success(f"✅ Save ho gaya: {item} - Rs. {amount}")
        else:
            st.warning("⚠️ Kripya item ka naam likhein!")

st.divider()

# 2. Display Data & Summary
st.header("📊 Expenses Summary")

try:
    # CSV file se data read karna
    df = pd.read_csv(
        "expenses.csv", names=["Date", "Item", "Amount", "Category"]
    )

    
      # History Table
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
total_spent = edited_df["Amount"].sum()
st.metric(label="Total Spent", value=f"Rs. {total_spent}")
edited_df.to_csv("expenses.csv", index=False, header=False)
except FileNotFoundError:
    st.info(
        "💡 Abhi tak koi data save nahi hua hai. Upar form bhar kar pehla expense add karein!"
    )
