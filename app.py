import streamlit as st
import pandas as pd

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="B2B Payment Dashboard", layout="wide")

st.title("📊 B2B Payment Collection Dashboard")

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    df["Due_Date"] = pd.to_datetime(df["Due_Date"], errors='coerce')
    df["Payment_Date"] = pd.to_datetime(df["Payment_Date"], errors='coerce')
    df["Delay_Days"] = df["Delay_Days"].fillna(0)
    return df

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
status = st.sidebar.multiselect("Payment Status", df["Payment_Status"].unique(), default=df["Payment_Status"].unique())
client = st.sidebar.multiselect("Client", df["Client_Name"].unique(), default=df["Client_Name"].unique())

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Payment_Status"].isin(status)) &
    (df["Client_Name"].isin(client))
]

# -------------------------------
# KPI Metrics
# -------------------------------
total = len(filtered_df)
paid = len(filtered_df[filtered_df["Payment_Status"] == "Paid"])
pending = len(filtered_df[filtered_df["Payment_Status"] != "Paid"])
avg_delay = filtered_df["Delay_Days"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Invoices", total)
col2.metric("Paid Invoices", paid)
col3.metric("Pending Payments", pending)
col4.metric("Avg Delay Days", round(avg_delay, 2))

st.markdown("---")

# -------------------------------
# Charts
# -------------------------------

# Payments by Region
st.subheader("📍 Payments by Region")
region_data = filtered_df.groupby("Region")["Invoice_Amount"].sum()
st.bar_chart(region_data)

# Invoice Status Distribution
st.subheader("📌 Invoice Status Distribution")
status_data = filtered_df["Payment_Status"].value_counts()
st.bar_chart(status_data)

# Delay Trend
st.subheader("📈 Delay Trend Analysis")
trend = filtered_df.groupby(filtered_df["Due_Date"].dt.month)["Delay_Days"].mean()
st.line_chart(trend)

# Revenue Trend
st.subheader("💰 Revenue Collection Trend")
revenue = filtered_df.groupby("Due_Date")["Invoice_Amount"].sum()
st.line_chart(revenue)

# -------------------------------
# Top Delaying Clients
# -------------------------------
st.subheader("⚠️ Top Delaying Clients")
top_clients = filtered_df.groupby("Client_Name")["Delay_Days"].mean().sort_values(ascending=False).head(10)
st.bar_chart(top_clients)

# -------------------------------
# Data Table
# -------------------------------
st.subheader("📄 Full Data View")
st.dataframe(filtered_df)
