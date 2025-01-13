import streamlit as st
import pandas as pd

# Initialize timetable structure
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours = [f"{i}:00 - {i+1}:00" for i in range(8, 18)]  # Slots from 8 AM to 6 PM
classes = [f"Class {i}" for i in range(1, 21)]

# Initialize timetable in session state
if "timetable" not in st.session_state:
    st.session_state.timetable = pd.DataFrame(
        index=pd.MultiIndex.from_product([days, hours], names=["Day", "Hour"]),
        columns=classes,
    )

# Sidebar for input
st.sidebar.title("Class Timetable Input")
selected_day = st.sidebar.selectbox("Select Day", days)
selected_hour = st.sidebar.selectbox("Select Hour", hours)
selected_class = st.sidebar.selectbox("Select Class", classes)
subject = st.sidebar.text_input("Enter Subject Name", "")

# Update button to modify a specific cell
if st.sidebar.button("Update Timetable"):
    if subject.strip():
        # Update the specific cell
        st.session_state.timetable.loc[(selected_day, selected_hour), selected_class] = subject
        st.sidebar.success(f"Updated: {selected_day}, {selected_hour}, {selected_class} -> {subject}")
    else:
        st.sidebar.error("Subject name cannot be empty.")

# Display the timetable
st.title("Class Timetable")
selected_day_filter = st.selectbox("Filter by Day", ["All"] + days)

# Filter timetable by selected day
filtered_timetable = st.session_state.timetable.copy()
if selected_day_filter != "All":
    filtered_timetable = filtered_timetable.loc[selected_day_filter]

st.dataframe(filtered_timetable.fillna(""))

# Export timetable as CSV
csv_data = st.session_state.timetable.to_csv(index=True, encoding="utf-8")
st.download_button(
    label="Download Timetable as CSV",
    data=csv_data,
    file_name="timetable.csv",
    mime="text/csv",
)



