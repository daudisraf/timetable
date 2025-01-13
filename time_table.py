import streamlit as st
import pandas as pd

# Initialize a blank timetable
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
hours = [f"{i}:00 - {i+1}:00" for i in range(8, 18)]  # Slots from 8 AM to 6 PM
classes = [f"DK {i}" for i in range(1, 21)]

timetable = pd.DataFrame(index=pd.MultiIndex.from_product([days, hours], names=["Day", "Hour"]),
                         columns=classes)

# Sidebar title
st.sidebar.title("Class Timetable Input")
st.sidebar.write("Select a day, hour, class, and enter the subject.")

# Sidebar inputs
selected_day = st.sidebar.selectbox("Select Day", days)
selected_hour = st.sidebar.selectbox("Select Hour", hours)
selected_class = st.sidebar.selectbox("Select Class", classes)
subject = st.sidebar.text_input("Enter Subject Name", "")

if st.sidebar.button("Update Timetable"):
    if subject.strip():
        timetable.loc[(selected_day, selected_hour), selected_class] = subject
        st.sidebar.success(f"Updated: {selected_day}, {selected_hour}, {
                           selected_class} -> {subject}")
    else:
        st.sidebar.error("Subject name cannot be empty.")

# Display the timetable
st.title("Class Timetable")
selected_day_filter = st.selectbox("Filter by Day", ["All"] + days)
filtered_timetable = timetable.copy()

if selected_day_filter != "All":
    filtered_timetable = timetable.loc[selected_day_filter]

st.dataframe(filtered_timetable.fillna(""))

# Export to CSV with a download button
if st.button("Export Timetable to CSV"):
    # Save the filtered timetable to a CSV file in memory
    filtered_csv = filtered_timetable.to_csv(index=True, encoding='utf-8')
    st.download_button(
        label="Download Timetable as CSV",
        data=filtered_csv,
        file_name="timetable.csv",
        mime="text/csv",
    )
    st.success("Timetable is ready for download.")


