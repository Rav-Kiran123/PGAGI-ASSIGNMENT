from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
import streamlit as st
import os
from dotenv import load_dotenv
from deep_translator import GoogleTranslator  

# Load environment variables
load_dotenv()

# Initialize Google Gemini via LangChain (using ChatGoogleGenerativeAI)
google_genai = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-latest",  # Ensure you are using the correct Gemini model identifier
    google_api_key=os.getenv('GOOGLE_API_KEY'),
    temperature=0  # Optional: Adjust for more or less creativity in responses
)

# Streamlit App
def main():
    st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon=":robot_face:", layout="wide")

    # Custom CSS for UI Enhancements
    st.markdown("""
    <style>
    .header {text-align: center; font-size: 40px; font-weight: bold; color: #4CAF50;}
    .button {background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px;}
    .chat-box {border: 1px solid #ddd; padding: 10px; border-radius: 5px; background-color: #f9f9f9;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="header">TalentScout Hiring Assistant</p>', unsafe_allow_html=True)

    # Language Selection
    language = st.selectbox("Choose your preferred language:", ["English", "Spanish", "French", "German", "Italian"])
    
    # Collect basic information from the candidate
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    years_of_experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
    desired_position = st.text_input("Desired Position(s)")
    location = st.text_input("Current Location")
    
    # Ask for Tech Stack
    tech_stack = st.text_area("Tech Stack (e.g., Python, Django, SQL)")

    if st.button("Submit", key="submit_button"):
        if not name or not email or not phone or not tech_stack:
            st.error("Please fill in all required fields.")
        else:
            st.write("Thank you for providing your information!")
            # Store the candidate's information in the session state for later use
            st.session_state.candidate_info = {
                "name": name,
                "email": email,
                "phone": phone,
                "years_of_experience": years_of_experience,
                "desired_position": desired_position,
                "location": location,
                "tech_stack": tech_stack
            }

            # Send the collected data to Google Gemini via LangChain for question generation
            tech_questions = generate_technical_questions(tech_stack)

            if tech_questions:
                st.write("Based on your tech stack, here are some technical questions:")
                for idx, question in enumerate(tech_questions, 1):
                    st.write(f"{idx}. {question}")
            else:
                st.error("Could not generate questions. Please make sure your tech stack is clearly specified.")

            # Translate response to the selected language
            translate_and_respond(language)

# Function to generate technical questions based on tech stack using Google Gemini via LangChain
def generate_technical_questions(tech_stack):
    try:
        prompt = f"Generate 3-5 concise technical interview questions for assessing proficiency in: {tech_stack}. No explanations, just the questions."
        response = google_genai.invoke(prompt)  # Invoke model
        
        # Extract text from AIMessage object
        generated_text = response.content  # This correctly accesses the message content

        # Split the response into separate questions
        generated_questions = response.content.strip().split("\n")

        return generated_questions

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to translate and respond in the selected language using deep-translator
def translate_and_respond(language):
    # Initialize Google Translate API (deep-translator)
    user_message = f"Thank you for your tech stack. Your answers will help us assess your skills."
    
    if language != "English":
        try:
            translated_text = GoogleTranslator(source='auto', target=language.lower()).translate(user_message)
            st.write(f"Translated message: {translated_text}")
        except Exception as e:
            st.error(f"Error in translation: {e}")
    else:
        st.write(user_message)

if __name__ == "__main__":
    # Initialize session state to store candidate info
    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}

    main()


