import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

def general_page():
    
    df = pd.read_csv("data/clustered_cuisines.csv").drop("Unnamed: 0", axis=1)
    def metric_show(n):
        if n>1000:
            return( str(str(round(n/1000,1))+"k") )
        else:
            return(str(n))
    def perc_show(n):
        return( str(str(round(n*100, 2))+"%") )
    def show_delta(metric, roun=2, df=df, dateCol="date"):
        df[dateCol] = pd.to_datetime(df[dateCol])
        sevendays = df[dateCol].max()-timedelta(days=7)
        fourteendays = sevendays - timedelta(days=7)
        prelastweek = df[(df[dateCol]>fourteendays)&(df[dateCol]<sevendays)][metric].sum()
        lastweek = df[(df[dateCol]>sevendays)][metric].sum()
        return(
            str(round(lastweek/prelastweek-1,roun))+"%"
        )

    
    st.title("General Metrics")
    st.write("See general information about your restaurant.")
    
    # ================ General Metrics ================ #
    n1, total_orders, accepted_orders, issues, completed_orders, n2  = st.columns(6)
    total_orders.metric(label="# of total orders", value=metric_show(df["requested_orders"].sum()), delta=show_delta("requested_orders", 3))
    issues.metric(label="# of issues in orders", value=metric_show(df["order_issues"].sum()), delta=show_delta("order_issues"), delta_color="inverse")
    accepted_orders.metric(label="# of accepted orders", value=metric_show(df["accepted_orders"].sum()), delta=show_delta("accepted_orders", 3))
    completed_orders.metric(label="# of completed orders", value=metric_show(df["completed_orders_ofo_state"].sum()), delta=show_delta("completed_orders_ofo_state", 3))
    

    n1, per_accepted, per_first, per_first_promo, returning, n2 = st.columns(6)
    per_accepted.metric(label="% of accepted orders", value=perc_show(df["accepted_orders"].sum()/df["requested_orders"].sum()))
    per_first.metric(label="% of first orders", value=perc_show(df["first_time_orders"].sum()/df["requested_orders"].sum()))
    per_first_promo.metric(label="% of first orders w/ promo", value=perc_show((df["first_time_orders_promo"].sum()/df["requested_orders"].sum())))
    returning.metric(label="% of returning orders", value=perc_show(df["returning_orders"].sum()/df["requested_orders"].sum()))

    n1, prep_time, rating, n2 = st.columns(4)
    prep_time.metric(label="Avg. Prep. Time", value=str(str(round(df["avg_prep_time"].mean()/60)))+" min.", delta=show_delta("avg_prep_time"), delta_color="inverse")
    rating.metric(label="Avg. Rating of meal", value=str(round(df["avg_rating"].mean(),2))+"/5.0", delta=show_delta("avg_rating"))

    st.markdown("<p align='right'>Note: Changes relative to previous week.</p>", True)
    
    # ================ Meals per time charts ================ #

    date_col, time_col = st.columns(2)

    orders_date = df.groupby("date").sum()[["completed_orders_ofo_state"]].rename(columns={"completed_orders_ofo_state":"# of orders"}).reset_index()
    fig = px.bar(orders_date, x="date", y="# of orders", title="Number of Completed Orders by Date")
    fig.update_traces(marker_color='darkred')
    fig.update_layout(
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    date_col.plotly_chart(fig)

    orders_hour = df.groupby("hour").sum()[["completed_orders_ofo_state"]].rename(columns={"completed_orders_ofo_state":"# of orders"}).reset_index()
    fig = px.bar(orders_hour, x="hour", y="# of orders", title="Number of Completed Orders by Time of the Day")
    fig.update_traces(marker_color='darkred')
    fig.update_layout(
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    time_col.plotly_chart(fig)

    # ================ Order Type Barchart ================ #

    barsum = (pd.DataFrame(df[["requested_orders", "accepted_orders", "completed_orders_ofo_state", "first_time_orders", 
        "first_time_orders_promo", "returning_orders", "returning_orders_promo", "order_issues"]].sum())
            .reset_index().rename(columns={"index": "Order Type", 0: "Number"})
            .replace("requested_orders", "Requested Orders").replace("accepted_orders", "Accepted Orders")
            .replace("completed_orders_ofo_state", "Completed Orders").replace("first_time_orders", "First Time Orders")
            .replace("first_time_orders_promo", "First Time Orders w/ Promo")
            .replace("returning_orders", "Returning Orders")
            .replace("returning_orders_promo", "Returning Orders w/ Promo")
            .replace("order_issues", "Order Issues"))
    fig = px.bar(barsum, x="Order Type", y="Number", title="Number of Orders by Order Type")
    fig.update_traces(marker_color='darkred')
    fig.update_layout(
        title={
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)



"""

    import plotly.figure_factory as ff
    import numpy as np

    # Add histogram data
    x1 = np.random.randn(200) - 2
    x2 = np.random.randn(200)
    x3 = np.random.randn(200) + 2

    # Group data together
    hist_data = [x1, x2, x3]

    group_labels = ['Group 1', 'Group 2', 'Group 3']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(
            hist_data, group_labels, bin_size=[.1, .25, .5])

    # Plot!
    st.plotly_chart(fig, use_container_width=True)

    import plotly.express as px
    fig = px.bar(df, x="")
    """ 