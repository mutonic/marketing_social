from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import seaborn as sns

# Set page config
st.set_page_config(page_title="LinkedIn Analytics Dashboard", layout="wide")

# Function to load data
@st.cache_data
def load_data():
    try:
        metrics_df = pd.read_excel('./data/social_media.xlsx', sheet_name='Metrics')
        all_posts_df = pd.read_excel('./data/social_media.xlsx', sheet_name='All posts')
        
        # Strip column names of extra spaces
        metrics_df.columns = metrics_df.columns.str.strip()
        all_posts_df.columns = all_posts_df.columns.str.strip()
        
        # Convert date columns to datetime
        metrics_df['Date'] = pd.to_datetime(metrics_df['Date'], errors='coerce')
        all_posts_df['Created date'] = pd.to_datetime(all_posts_df['Created date'], errors='coerce')
        
        return metrics_df, all_posts_df
    except FileNotFoundError:
        st.error("Error: The file './data/social_media.xlsx' was not found.")
        return None, None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None

# Load data
metrics_df, all_posts_df = load_data()
if metrics_df is None or all_posts_df is None:
    st.stop()

# Sidebar filters
st.sidebar.title("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(metrics_df['Date'].min(), metrics_df['Date'].max()),
    min_value=metrics_df['Date'].min(),
    max_value=metrics_df['Date'].max()
)

content_filter = st.sidebar.radio(
    "Content Type",
    ["All", "Organic", "Sponsored"]
)

performance_filter = st.sidebar.radio(
    "Select Performance Category",
    ["All", "High Performer", "Moderate Performer", "Low Performer"]
)

# Main dashboard
st.title("LinkedIn AQS Analytics Dashboard")

# Top level metrics
st.header("Key Metrics Overview")
col1, col2, col3, col4 = st.columns(4)

# Filter metrics based on date range
mask = (metrics_df['Date'].dt.date >= date_range[0]) & (metrics_df['Date'].dt.date <= date_range[1])
filtered_metrics = metrics_df.loc[mask]

# Calculate metrics based on content filter
if content_filter == "Organic":
    impressions = filtered_metrics['Impressions (organic)'].sum()
    engagement_rate = filtered_metrics['Engagement rate (organic)'].mean()
    clicks = filtered_metrics['Clicks (organic)'].sum()
    reactions = filtered_metrics['Reactions (organic)'].sum()
elif content_filter == "Sponsored":
    impressions = filtered_metrics['Impressions (sponsored)'].sum()
    engagement_rate = filtered_metrics['Engagement rate (sponsored)'].mean()
    clicks = filtered_metrics['Clicks (sponsored)'].sum()
    reactions = filtered_metrics['Reactions (sponsored)'].sum()
else:
    impressions = filtered_metrics['Impressions (total)'].sum()
    engagement_rate = filtered_metrics['Engagement rate (total)'].mean()
    clicks = filtered_metrics['Clicks (total)'].sum()
    reactions = filtered_metrics['Reactions (total)'].sum()

with col1:
    st.metric("Total Impressions", f"{impressions:,}")
with col2:
    st.metric("Engagement Rate", f"{engagement_rate:.2f}%")
with col3:
    st.metric("Total Clicks", f"{clicks:,}")
with col4:
    st.metric("Total Reactions", f"{reactions:,}")

# Engagement metrics over time
st.subheader("Engagement Metrics Over Time")
metrics_choice = st.multiselect(
    'Select Metrics to Display',
    ['Impressions', 'Clicks', 'Reactions', 'Comments', 'Reposts'],
    default=['Impressions', 'Clicks']
)

fig_metrics = go.Figure()
for metric in metrics_choice:
    column_name = f"{metric} (total)"
    fig_metrics.add_trace(go.Scatter(
        x=filtered_metrics['Date'],
        y=filtered_metrics[column_name],
        name=metric,
        mode='lines'
    ))

fig_metrics.update_layout(
    title="Daily Engagement Metrics",
    xaxis_title="Date",
    yaxis_title="Count",
    hovermode='x unified'
)
st.plotly_chart(fig_metrics, use_container_width=True)

# Content Performance Analysis
st.header("Content Performance Analysis")

# Filter posts based on date range and content type
posts_mask = (all_posts_df['Created date'].dt.date >= date_range[0]) & (all_posts_df['Created date'].dt.date <= date_range[1])
filtered_posts = all_posts_df.loc[posts_mask].copy()

if content_filter != "All":
    filtered_posts = filtered_posts[filtered_posts['Post type'] == content_filter]

# Classify posts based on engagement metrics
def classify_post(row, q1, q2, q3):
    if row['Engagement rate'] >= q3:
        return "High Performer"
    elif row['Engagement rate'] >= q2:
        return "Moderate Performer"
    else:
        return "Low Performer"

# Calculate quantiles for classification
if not filtered_posts.empty and 'Engagement rate' in filtered_posts.columns:
    q1 = filtered_posts['Engagement rate'].quantile(0.25)
    q2 = filtered_posts['Engagement rate'].quantile(0.50)
    q3 = filtered_posts['Engagement rate'].quantile(0.75)
    filtered_posts['Performance Category'] = filtered_posts.apply(lambda row: classify_post(row, q1, q2, q3), axis=1)
else:
    st.warning("No data available for performance classification or 'Engagement rate' column is missing.")
    filtered_posts['Performance Category'] = "Unknown"

# Apply performance filter
if performance_filter != "All":
    filtered_posts = filtered_posts[filtered_posts['Performance Category'] == performance_filter]

# Display performance breakdown
st.subheader("Post Performance Classification")
performance_count = filtered_posts['Performance Category'].value_counts()
st.bar_chart(performance_count)

# Show top performing posts
st.subheader("Top Performing Posts by Category")
st.dataframe(
    filtered_posts[['Post title', 'Content Type', 'Created date', 'Impressions', 'Clicks', 'Engagement rate', 'Performance Category']]
)

# Visualization of clusters
st.subheader("NLP-Based Post Classification Visualization")
if not filtered_posts.empty and {'Impressions', 'Engagement rate'}.issubset(filtered_posts.columns):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=filtered_posts, x='Impressions', y='Engagement rate', hue='Performance Category', palette='viridis', ax=ax)
    ax.set_title("Post Clustering Based on Performance")
    st.pyplot(fig)
else:
    st.warning("Cannot generate visualization: Required columns ('Impressions', 'Engagement rate') are missing or dataset is empty.")