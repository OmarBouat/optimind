import google.generativeai as genai
import streamlit as st


# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyCDgJM3jwy86gYUezKkU9AZmtjtxlafd94"

# Configure the API key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

# Function to generate text using Gemini API
def generate_text(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to generate a course roadmap
def generate_course_roadmap(dream_job):
    prompt = f"Give me just the name of the subjects for a roadmap for someone who wants to become a {dream_job}, from the easiest to the hardest subjects."
    roadmap_text = generate_text(prompt)
    return [subject.strip() for subject in roadmap_text.split("\n") if subject.strip()]  # Convert roadmap into a list of subjects

# Function to generate course content
def generate_course_content(subject):
    prompt = f"Provide an overview of the course content for {subject}."
    return generate_text(prompt)

# Function to generate an exam for a topic
def generate_exam(subject):
    prompt = f"Generate a 5-question exam with answers on the topic: {subject}."
    return generate_text(prompt)

# Streamlit app
def main():
    st.title("Oasis of wisdom")

    # Initialize session state variables
    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = None
    if "roadmap" not in st.session_state:
        st.session_state.roadmap = []

    # User input: Dream job
    dream_job = st.text_input("Enter your dream job:")

    # If no subject is selected, show the roadmap
    if st.session_state.selected_subject is None:
        if dream_job:
            if not st.session_state.roadmap:  # Generate roadmap only once
                st.session_state.roadmap = generate_course_roadmap(dream_job)

            st.write(f"### Course Roadmap for {dream_job}:")
            for subject in st.session_state.roadmap:
                if st.button(subject):  # Clicking a subject selects it
                    st.session_state.selected_subject = subject
                    st.rerun()

    # If a subject is selected, show course content and exam
    else:
        subject = st.session_state.selected_subject
        st.write(f"## {subject} Course Content")
        st.write(generate_course_content(subject))

        st.write("## Exam")
        st.write(generate_exam(subject))

        # Button to go back to the roadmap
        if st.button("Back to Roadmap"):
            st.session_state.selected_subject = None
            st.rerun()

# Run the Streamlit app
if __name__ == "__main__":
    main()
