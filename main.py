import streamlit as st
import pandas as pd
from datetime import timedelta
import numpy as np


df = pd.read_csv("data/clustered_cuisines.csv").drop("Unnamed: 0", axis=1)

def general_page():
    st.title("General Metrics")
    st.write("See general information about your restaurant.")
    
    # ================ General Metrics ================ #
    total_orders, accepted_orders, issues, completed_orders  = st.columns(4)
    total_orders.metric(label="# of total orders", value=df["requested_orders"].sum())
    issues.metric(label="# of issues in orders", value=df["order_issues"].sum())
    accepted_orders.metric(label="# of total accepted orders", value=df["accepted_orders"].sum())
    completed_orders.metric(label="# of completed orders", value=df["completed_orders_ofo_state"].sum())
    
    per_accepted, per_first, per_first_promo, returning = st.columns(4)
    per_accepted.metric(label="% of accepted orders", value=round((df["accepted_orders"].sum()/df["requested_orders"].sum())*100, 1))
    per_first.metric(label="% of first orders", value=round((df["first_time_orders"].sum()/df["requested_orders"].sum())*100,1))
    per_first_promo.metric(label="% of first orders w/ promo", value=round((df["first_time_orders_promo"].sum()/df["requested_orders"].sum())*100,1))
    returning.metric(label="% of returning orders", value=round((df["returning_orders"].sum()/df["requested_orders"].sum())*100,1))

    prep_time, rating = st.columns(2)
    prep_time.metric(label="Avg. Prep. Time (in min.)", value=round(df["avg_prep_time"].mean()/60))
    rating.metric(label="Avg. Rating of meal (out of 5)", value=round(df["avg_rating"].mean(),2))

    
    # ================ Meals per time charts ================ #

    orders_date = df.groupby("date").sum()[["completed_orders_ofo_state"]].rename(columns={"completed_orders_ofo_state":"orders_num"})
    st.header("Completed orders over time:")
    st.area_chart(orders_date)

    orders_hour = df.groupby("hour").sum()[["completed_orders_ofo_state"]].rename(columns={"completed_orders_ofo_state":"# or orders"})
    st.header("Completed orders by time of the day:")
    st.bar_chart(orders_hour)
    

def trending_page():
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


def cuisine_page():
    st.title("Cuisines Analysis")
    st.write("Using an Artificial Intelligence solution, we have been able to group your different products by cuisine. Below you can see how your products are trending based on these cuisine types.")

    df["Cuisine"] = (df["cuisine_clustered"]
    .replace("rice", "Accompaniment").replace("ramen", "Ramen").replace("salad", "Salad")
    .replace("pita", "Breakfast").replace("chees", "Accompaniment").replace("breakfast burrito", "Mexican")
    .replace("chicken", "Chicken").replace("wing", "Chicken").replace("bottl", "Drinks")
    .replace("burrito", "Mexican").replace("breakfast", "Breakfast").replace("extra ranch sauc", "Salad")
    .replace("curri", "Mexican").replace("egg", "Breakfast").replace("chicken fri", "Chicken")
    .replace("fri", "Accompaniment").replace("cheesesteak", "Sandwich").replace("taco", "Mexican")
    .replace("chip", "Snacks").replace("toast", "Breakfast").replace("chees mac", "Italian")
    .replace("roll", "Accompaniment").replace("the", np.nan).replace("chees egg sausag", "Breakfast")
    .replace("your", np.nan).replace("veget", "Vegetarian").replace("af", np.nan)
    .replace("noodl", "Ramen").replace("hot", np.nan).replace("chees grill", "Breakfast")
    .replace("plate", np.nan).replace("chicken wing", "Chicken").replace("chees fri", "Accompaniment")
    .replace("bread", "Breakfast").replace("lamb", "Meat").replace("garlic parmesan", "Salad")
    .replace("bacon", "Breakfast").replace("quesadilla", "Mexican").replace("curri red", "Mexican")
    .replace("meat", "Meat") 
    )

    st.header("Top Trending Cuisines")

    trending_cuisines = (df.groupby("Cuisine").sum()[["completed_orders_ofo_state"]]
    .rename(columns={"completed_orders_ofo_state": "Completed Orders"})
    .sort_values("Completed Orders", ascending=False)).reset_index()
    trending_cuisines["Avg. Rating"] = df.groupby("Cuisine").mean().reset_index()["avg_rating"]
    st.table(trending_cuisines)

    st.header("Analysis by cuisine")

    cuisine = st.selectbox("Select cuisine to see analysis:", ['Accompaniment', 'Breakfast', 'Chicken', 'Drinks', 'Italian',
       'Meat', 'Mexican', 'Ramen', 'Salad', 'Sandwich', 'Snacks',
       'Vegetarian'])

    items, orders, stars = st.columns(3)
    items.metric(label="% of representation among all products", value=round(len(df[df["Cuisine"]==cuisine].groupby("name")) / len(df.groupby("name"))*100))
    orders.metric(label="# of total orders", value=df[df["Cuisine"]==cuisine]["completed_orders_ofo_state"].sum())
    stars.metric(label="Avg. Rating of this cuisine", value=round(df[df["Cuisine"]==cuisine]["avg_rating"].mean(),2))

    st.header("Top Products in this Cuisine:")
    top_items_cui = (df[df["Cuisine"]==cuisine].groupby("name").sum().sort_values("completed_orders_ofo_state", 
                                                                                ascending=False)
        [["completed_orders_ofo_state"]].head(10).reset_index()
    .rename(columns={"name":"Product Sold", "completed_orders_ofo_state":"Completed Orders"}))
    st.table(top_items_cui)


# ================ Sidebar ================ #
st.sidebar.image("data/logo.png")
st.sidebar.title("Restaurant Dashboard")
page_selection = st.sidebar.selectbox("Select page view:", ["General Metrics", "Trending Products", "Cuisines Page"])

if page_selection == "General Metrics":
    general_page()
elif page_selection == "Trending Products":
    trending_page()
elif page_selection == "Cuisines Page":
    cuisine_page()


