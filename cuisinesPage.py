import streamlit as st
import pandas as pd
import numpy as np

def cuisine_page():
    df = pd.read_csv("data/clustered_cuisines.csv").drop("Unnamed: 0", axis=1)
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
