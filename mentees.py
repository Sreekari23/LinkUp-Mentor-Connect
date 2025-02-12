import streamlit as st
from datetime import datetime, timedelta
from utils import create_event
from database import add_activity  # Import add_activity from database.py

def mentee_page():
    '''if st.session_state['role'] != 'mentee':
        st.error("You must be a mentee to access this page.")
        return'''

    st.header("Mentee Page")

    mentors = [
        {"name": "Dr. Smith", "expertise": "Machine Learning, AI"},
        {"name": "Ms. Johnson", "expertise": "Cybersecurity, Networks"},
        {"name": "Mr. Lee", "expertise": "Product Management, Agile"},
    ]

    if 'mentor_index' not in st.session_state:
        st.session_state.mentor_index = 0

    if 'selected_mentor' not in st.session_state:
        st.session_state.selected_mentor = None

    mentor_index = st.session_state.mentor_index

    if mentor_index < len(mentors):
        mentor = mentors[mentor_index]
        st.subheader(f"{mentor['name']}")
        st.write(f"Expertise: {mentor['expertise']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Skip", key=f"skip_mentor_{mentor_index}"):
                st.session_state.mentor_index += 1
                st.session_state.selected_mentor = None
        with col2:
            if st.button("✅ Connect", key=f"connect_mentor_{mentor_index}"):
                st.session_state.selected_mentor = mentor

    if st.session_state.selected_mentor:
        st.success(f"You are connecting with {st.session_state.selected_mentor['name']}!")

        date = st.date_input("Select a date for the mentorship session:")
        time = st.time_input("Select a time for the mentorship session:")

        if st.button("Schedule"):
            if date and time:
                start_time = datetime.combine(date, time)
                end_time = start_time + timedelta(hours=1)

                # Create a Google Calendar event using the imported create_event function
                event_link = create_event(
                    st.session_state['creds'],
                    summary=f"Mentorship Session with {st.session_state.selected_mentor['name']}",
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
                    "with_user": st.session_state.selected_mentor['name'],
                    "date": start_time.strftime("%Y-%m-%d"),
                    "time": start_time.strftime("%H:%M"),
                    "status": "Upcoming",
                    "role": "Mentee"
                }

                # Save activity to database
                add_activity(st.session_state['user_id'], "Session", st.session_state.selected_mentor['name'], 
                             start_time.strftime("%Y-%m-%d"), start_time.strftime("%H:%M"), "Upcoming", "Mentee")

                # Update session state
                st.session_state['activities'].append(new_activity)

                if st.button("Approve and Move to Next"):
                    st.session_state.mentor_index += 1
                    st.session_state.selected_mentor = None

            else:
                st.warning("Please select a date and time.")
    else:
        st.write("No more mentors available.")
