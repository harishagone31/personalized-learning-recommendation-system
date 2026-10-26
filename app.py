import streamlit as st

st.set_page_config(
    page_title="Personalized Learning System",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Personalized Learning Recommendation System")
st.write("Get a learning plan designed for your needs!")

st.divider()

name = st.text_input("Enter your name")

subject = st.selectbox(
    "Choose your subject",
    ["Python", "Java", "Data Structures", "Artificial Intelligence"]
)

level = st.selectbox(
    "Choose your learning level",
    ["Beginner", "Intermediate", "Advanced"]
)

goal = st.selectbox(
    "What do you want to improve?",
    ["Theory", "Coding Practice", "Projects"]
)

if st.button("Generate My Learning Plan"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    else:
        st.subheader("Your Personalized Learning Plan")
        st.write("**Student:**", name)
        st.write("**Subject:**", subject)
        st.write("**Level:**", level)
        st.write("**Learning Goal:**", goal)

        st.subheader("📖 Subject Recommendation")

        if subject == "Python":
            st.write("Practice Python programs and learn its basic concepts.")
        elif subject == "Java":
            st.write("Study Java syntax and practice object-oriented programming.")
        elif subject == "Data Structures":
            st.write("Practice arrays, stacks, queues, linked lists, and trees.")
        else:
            st.write("Learn AI concepts and explore beginner-friendly AI projects.")

        st.subheader("🎯 Your Learning Steps")

        if level == "Beginner":
            st.write("Start with basic concepts and simple examples.")
        elif level == "Intermediate":
            st.write("Solve intermediate exercises and small problems.")
        else:
            st.write("Work on advanced problems and challenging projects.")

        if goal == "Theory":
            st.write("**Activity:** Read notes and summarize important concepts.")
        elif goal == "Coding Practice":
            st.write("**Activity:** Solve coding exercises regularly.")
        else:
            st.write("**Activity:** Build a small project using your chosen subject.")

        st.success("Your learning plan is ready! Keep practicing! 🎉")