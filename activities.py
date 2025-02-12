import streamlit as st

def activities_page():
    st.header("Your Activities")

    # Check if activities are in session state
    if 'activities' not in st.session_state:
        st.session_state['activities'] = []

    # Display the activities
    if st.session_state['activities']:
        st.write("## Your Scheduled Sessions")
        activities_list = st.session_state['activities']

        # Separate activities by role
        mentor_activities = [activity for activity in activities_list if activity['role'] == 'Mentor']
        mentee_activities = [activity for activity in activities_list if activity['role'] == 'Mentee']

        # Display tables
        if mentor_activities:
            st.write("### Mentorships You Are Offering")
            st.table(mentor_activities)

        if mentee_activities:
            st.write("### Mentorships You Are Seeking")
            st.table(mentee_activities)
    else:
        st.write("No activities scheduled yet.")

    st.write("## Refresh to Check for Updates")
    if st.button("Refresh"):
        st.rerun()
