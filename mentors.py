import streamlit as st
from datetime import datetime, timedelta
from utils import create_event
from database import add_activity  # Import add_activity from database.py

def mentor_page():
    '''if st.session_state['role'] != 'mentor':
        st.error("You must be a mentor to access this page.")
        return'''

    st.header("Mentor Page")

    mentees = [
        {"name": "Alice", "skills": "Python, Data Science"},
        {"name": "Bob", "skills": "Java, Backend Development"},
        {"name": "Carol", "skills": "UI/UX Design, Frontend Development"},
    ]

    if 'mentee_index' not in st.session_state:
        st.session_state.mentee_index = 0

    if 'selected_mentee' not in st.session_state:
        st.session_state.selected_mentee = None

    mentee_index = st.session_state.mentee_index

    if mentee_index < len(mentees):
        mentee = mentees[mentee_index]
        st.subheader(f"{mentee['name']}")
        st.write(f"Skills: {mentee['skills']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Skip", key=f"skip_{mentee_index}"):
                st.session_state.mentee_index += 1
                st.session_state.selected_mentee = None
        with col2:
            if st.button("✅ Connect", key=f"connect_{mentee_index}"):
                st.session_state.selected_mentee = mentee

    if st.session_state.selected_mentee:
        st.success(f"You are connecting with {st.session_state.selected_mentee['name']}!")

        date = st.date_input("Select a date for the mentorship session:")
        time = st.time_input("Select a time for the mentorship session:")

        if st.button("Schedule"):
            if date and time:
                start_time = datetime.combine(date, time)
                end_time = start_time + timedelta(hours=1)

                # Create a Google Calendar event using the imported create_event function
                event_link = create_event(
                    st.session_state['creds'],
                    summary=f"Mentorship Session with {st.session_state.selected_mentee['name']}",
                    description="A mentorship session.",
                    start_time=start_time,
                    end_time=end_time,
                    email=st.session_state['email']
                )

                if event_link:
                    st.markdown(f"[Join the Meeting]({event_link})")
                    st.success("A meeting link has been added to your calendar.")

                new_activity = {
                    "type": "Session",
                    "with_user": st.session_state.selected_mentee['name'],
                    "date": start_time.strftime("%Y-%m-%d"),
                    "time": start_time.strftime("%H:%M"),
                    "status": "Upcoming",
                    "role": "Mentor"
                }

                # Save activity to database
                add_activity(st.session_state['user_id'], "Session", st.session_state.selected_mentee['name'], 
                             start_time.strftime("%Y-%m-%d"), start_time.strftime("%H:%M"), "Upcoming", "Mentor")

                # Update session state
                st.session_state['activities'].append(new_activity)

                if st.button("Approve and Move to Next"):
                    st.session_state.mentee_index += 1
                    st.session_state.selected_mentee = None

            else:
                st.warning("Please select a date and time.")
    else:
        st.write("No more mentees available.")
