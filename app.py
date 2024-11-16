import streamlit as st
import os
import PyPDF2
from groq import Groq
from dotenv import load_dotenv
from streamlit_extras.stylable_container import stylable_container

# Load and apply custom CSS from an external file
with open("app.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

# App title
st.markdown("### College Project", unsafe_allow_html=False)

# Function to load environment variables from .env file
def configure():
    load_dotenv()

configure()

# Navigation sidebar using stylable container
with stylable_container(
    key="navbar",
    css_styles="""div[data-testid="stDecoration"] { color: red; }"""
):
    side_bar = st.sidebar.selectbox("Navigate", ("Home", "About Us"))

# Home Page functionality
if side_bar == "Home":
    try:
        # File uploader for answer scripts
        uploadedfile = st.file_uploader("Upload your answer script")

        # Create a temporary directory for uploaded files
        temp_dir = "tempDir"
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        if uploadedfile:
            # Save the uploaded file to the temporary directory
            file_path = os.path.join(temp_dir, uploadedfile.name)
            with open(file_path, "wb") as f:
                f.write(uploadedfile.getbuffer())

            # Read and extract text from the uploaded PDF file
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = "".join(page.extract_text() for page in pdf_reader.pages)

            # Stylable container for text input area
            with stylable_container(
                key="input_area",
                css_styles="""color: yellow;"""
            ):
                # Maintain text input state across reruns
                if "input_text" not in st.session_state:
                    st.session_state.input_text = ""

                # Text input for user input
                inp = st.text_input("Input", value=st.session_state.input_text)

            # Clear data functionality
            if st.button("Clear data"):
                # Delete all files in the temporary directory
                for file_name in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, file_name))
                st.write("All files have been deleted.")
                
                # Reset the input field and rerun the app
                st.session_state.input_text = ""
                st.experimental_rerun()

            # If input is provided, send data to the Groq API
            if inp.strip():
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                completion = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=[
                        {"role": "user", "content": text},
                        {"role": "assistant", "content": inp},
                        {"role": "assistant", "content": "```string"}
                    ],
                    stop="```",
                )

                # Display the API response
                st.write(completion.choices[0].message.content)
    except Exception as e:
        # Handle errors gracefully
        st.error(f"An error occurred: {e}")

# About Us Page
elif side_bar == "About Us":
    st.write("This is the About Us section.")

# Add spacing at the end of the app for better layout
st.write("\n" * 6)
