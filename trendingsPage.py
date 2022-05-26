import streamlit as st
import pandas as pd
from datetime import timedelta
def trending_page():
    df = pd.read_csv("data/clustered_cuisines.csv").drop("Unnamed: 0", axis=1)
    st.title("Trending Products")
    st.write("See below which of your products have been trending.")
    # ================ Top Products Table ================ #
    st.header("Top Products Sold")
    st.table(df.sort_values("completed_orders_ofo_state", ascending=False)[["name", "completed_orders_ofo_state"]]
                .head(10).reset_index().drop("index",axis=1)
                .rename(columns={"name": "Product sold", "completed_orders_ofo_state": "Completed Orders"}))

    # ================ Trending Items ================ #

    st.header("Items trending recently:")
    trending_type = st.selectbox("Select period type", ["Last Week", "Last Month"])
    
    df["date"] = pd.to_datetime(df['date'])
    last_week = df["date"].max()-timedelta(days=7)
    last_month = df["date"].max()-timedelta(days=30)

    if trending_type=="Last Week":
        st.table(df[df["date"]>=last_week].sort_values(
            "completed_orders_ofo_state", ascending=False
            ).head(10)[["name", "completed_orders_ofo_state"]].reset_index().drop("index",axis=1)
            .rename(columns={"name": "Product sold", "completed_orders_ofo_state": "Completed Orders"}))    
    elif trending_type=="Last Month":
        st.table(df[df["date"]>=last_month].sort_values(
            "completed_orders_ofo_state", ascending=False
            ).head(10)[["name", "completed_orders_ofo_state"]].reset_index().drop("index",axis=1)
            .rename(columns={"name": "Product sold", "completed_orders_ofo_state": "Completed Orders"}))    

    # ================ Aggregate View by Time ================ #

    # === By time of day === # 
    st.header("Aggregate view of top items by time")
    st.subheader("By time of day")

    df["daytime"] = (df["hour"].replace(list(range(0,7)), "Morning")
    .replace(list(range(7,11)), "Breakfast")
    .replace(list(range(11,15)), "Lunch")
    .replace(list(range(15,18)), "Afternoon Snack")
    .replace(list(range(18,24)), "Dinner")
    )

    hour = st.selectbox("Select a day time:", ["Morning", "Breakfast", "Lunch", "Afternoon Snack", "Dinner"])

    daytime = (df[df["daytime"]==hour].sort_values("completed_orders_ofo_state", ascending=False)
    .head(10)[["name", "completed_orders_ofo_state"]].reset_index().drop("index",axis=1)
    .rename(columns={"name": "Product sold", "completed_orders_ofo_state": "Completed Orders"})).drop_duplicates()

    st.table(daytime)

    # === By day of week === # 
    st.subheader("By day of week")
    df["weekday"] = df["date"].dt.day_name()

    dayofweek = st.selectbox("Select a day of the week:", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

    weekday = (df[df["weekday"]==dayofweek].sort_values("completed_orders_ofo_state", ascending=False)
    .head(10)[["name", "completed_orders_ofo_state"]].reset_index().drop("index",axis=1)
    .rename(columns={"name": "Product sold", "completed_orders_ofo_state": "Completed Orders"})).drop_duplicates()

    st.table(weekday)