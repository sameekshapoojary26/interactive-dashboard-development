import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Business Analytics Dashboard",
                   page_icon="📊", layout="wide")

st.title("📊 Interactive Business Intelligence Dashboard")
st.markdown("Revenue, Customer and Business Performance Analytics")

# Generate sample business data
np.random.seed(42)
n = 500

df = pd.DataFrame({
    "Date": pd.date_range("2026-01-01", periods=n, freq="D"),
    "Region": np.random.choice(
        ["North", "South", "East", "West"], n),
    "Category": np.random.choice(
        ["Electronics", "Fashion", "Food", "Home"], n),
    "Revenue": np.random.randint(500, 10000, n),
    "Users": np.random.randint(10, 200, n),
    "Churn": np.random.choice([0, 1], n, p=[0.85, 0.15])
})

# Sidebar filters
st.sidebar.header("Dashboard Filters")

regions = st.sidebar.multiselect(
    "Select Region", df["Region"].unique(),
    default=list(df["Region"].unique()))

categories = st.sidebar.multiselect(
    "Select Category", df["Category"].unique(),
    default=list(df["Category"].unique()))

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["Date"].min().date(), df["Date"].max().date()])

if len(date_range) == 2:
    filtered = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories)) &
        (df["Date"].dt.date >= date_range[0]) &
        (df["Date"].dt.date <= date_range[1])
    ]
else:
    filtered = df[
        (df["Region"].isin(regions)) &
        (df["Category"].isin(categories))
    ]

if filtered.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# KPI Cards
revenue = filtered["Revenue"].sum()
users = filtered["Users"].sum()
churn = filtered["Churn"].mean() * 100
ticket = filtered["Revenue"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{revenue:,.0f}")
c2.metric("Active Users", f"{users:,}")
c3.metric("Churn Rate", f"{churn:.2f}%")
c4.metric("Average Ticket Size", f"₹{ticket:,.2f}")

st.divider()

# Dashboard pages
page = st.selectbox(
    "Choose Dashboard Page",
    ["Overview", "Revenue Analysis", "Customer Analysis"]
)

if page == "Overview":
    st.subheader("Business Overview")

    fig = px.line(
        filtered, x="Date", y="Revenue",
        title="Revenue Trend", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        filtered.groupby("Region", as_index=False)["Revenue"].sum(),
        x="Region", y="Revenue",
        title="Revenue by Region")
    st.plotly_chart(fig2, use_container_width=True)

elif page == "Revenue Analysis":
    st.subheader("Revenue Analysis")

    fig = px.bar(
        filtered.groupby("Category", as_index=False)["Revenue"].sum(),
        x="Category", y="Revenue",
        color="Category", title="Revenue by Category")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.area(
        filtered, x="Date", y="Revenue",
        title="Daily Revenue")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Customer Analysis":
    st.subheader("Customer Analysis")

    fig = px.pie(
        filtered, names="Region",
        title="Regional Distribution")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(
        filtered, x="Users", color="Category",
        title="User Distribution")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered Dataset")
st.dataframe(filtered, use_container_width=True)

st.success("Interactive Dashboard Successfully Generated!")
