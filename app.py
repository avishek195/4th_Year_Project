import streamlit as st
import os
import PyPDF2
from groq import Groq
from dotenv import load_dotenv
from streamlit_extras.stylable_container import stylable_container

with open("app.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>",unsafe_allow_html=True)

st.markdown("""### Collage project """,unsafe_allow_html=False)
def configure():
    load_dotenv()

configure()

with stylable_container(
    key="navbar",
    css_styles="""
      div[data-testid="stDecoration"]{
        color:red
      }
    """
):
    side_bar = st.sidebar.selectbox(
        "Navigate",
        ("Home","About us")
    )

if side_bar == "Home":
    try:
        uploadedfile = st.file_uploader("Upload your answer script")

        if not os.path.exists("tempDir"):
            os.mkdir("tempDir")


        with open(os.path.join("tempDir", uploadedfile.name), "wb") as f:
            f.write(uploadedfile.getbuffer())
        
        with open(os.path.join("tempDir", uploadedfile.name), "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            

        with stylable_container(
            key="input_area",
            css_styles="""
                 color: yellow;
            """
        ):
            inp = st.text_input("input")
            # print(inp)
        if inp != "":
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "user",
                        "content": text
                    },
                    {
                        "role": "assistant",
                        "content": inp
                    },
                    {
                        "role": "assistant",
                        "content": "```string"
                    }
                ],
                stop="```",
            )

            # print(completion.choices[0].message.content)
            
            st.write(completion.choices[0].message.content)
        with stylable_container(
            key="del_btn",
            css_styles="""
            
            """
        ):
            del_btn = st.button("Delete your data button")
        if del_btn:
            for d in os.listdir("tempDir")[:]:
                os.remove(os.path.join("tempDir",d))
                st.write("")
    except:
        pass
elif side_bar == "About us":
    st.write(""" this is About us""")

st.write("\n")
st.write("\n") 
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
