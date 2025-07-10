
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📒 IT Project Task Tracker System")

# Load or initialize task data
if "task_data" not in st.session_state:
    st.session_state.task_data = pd.DataFrame(columns=[
        "Task ID", "Task Description", "Owner", "Start Date", "End Date", "Status"
    ])

# Display task table
st.subheader("📌 Current Task Table")
st.dataframe(st.session_state.task_data, use_container_width=True)

# Add new task form
st.markdown("### ➕ Add New Task")
with st.form("add_task_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_id = st.text_input("Task ID")
        task_description = st.text_input("Task Description")
    with col2:
        owner = st.text_input("Owner")
        start_date = st.date_input("Start Date")
    with col3:
        end_date = st.date_input("End Date")
        status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
    submitted = st.form_submit_button("Add Task")
    if submitted:
        if not task_id or not task_description or not owner:
            st.warning("Please fill in all fields before adding a task.")
        else:
            new_task = pd.DataFrame([{
                "Task ID": task_id,
                "Task Description": task_description,
                "Owner": owner,
                "Start Date": start_date,
                "End Date": end_date,
                "Status": status
            }])
            st.session_state.task_data = pd.concat([st.session_state.task_data, new_task], ignore_index=True)
            st.success("Task added successfully.")

# Gantt chart
st.markdown("### 📊 Project Timeline (Gantt Chart)")
if not st.session_state.task_data.empty:
    df_chart = st.session_state.task_data.copy()
    df_chart["Start Date"] = pd.to_datetime(df_chart["Start Date"])
    df_chart["End Date"] = pd.to_datetime(df_chart["End Date"])
    fig = px.timeline(df_chart, x_start="Start Date", x_end="End Date", y="Task Description", color="Status")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

# Download updated data
st.markdown("### 📥 Download Updated File")
if not st.session_state.task_data.empty:
    csv = st.session_state.task_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV File", data=csv, file_name="updated_tasks.csv", mime="text/csv")
