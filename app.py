import streamlit as st
import os
import time
import re
import json
from prompt_updated import input_prompt_template
import langchain_huggingface
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Hugging Face API key from environment variables
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Set up the model configuration for text generation
def generate_response_from_llm(input_text):
    #mistral llm
    repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
    #repo_id = "tiiuae/Falcon3-7B-Instruct"
    model_kwargs = {"token": HUGGINGFACEHUB_API_TOKEN}
    llm = HuggingFaceEndpoint(repo_id=repo_id, temperature=0.5, model_kwargs=model_kwargs)
    # Generate content based on the input text
    time.sleep(5)
    output = llm.invoke(input_text)
    # Return the generated text
    return output

# Streamlit app
# Initialize Streamlit app
#st.title("ATS Score check for Resume")
#st.markdown('<style>h1{color: orange; text-align: center;}</style>', unsafe_allow_html=True)

#st.title("ATS Score check for Resume")
html_temp = """
<div style="background-color:#43766C;padding:6px">
<h2 style="color:white;text-align:center;">ATS Score check for Resume App </h2>
</div>
"""
st.markdown(html_temp,unsafe_allow_html=True)

# Create two columns for side-by-side layout
col1, col2 = st.columns([1, 1])

# Job Description in first column
with col1:
    job_description = st.text_area("Paste the Job Description", height=300)

# Resume in second column
with col2:
    data_from_resume = st.text_area("Paste the Resume Here", height=300)

# job_description = st.text_area("Paste the Job Description",height=200)
# data_from_resume = st.text_area("Paste the Resume Here",height=200)
#uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Please upload a PDF or DOCX file")

submit_button = st.button("Submit")

if submit_button:
    if job_description is not None:
        if data_from_resume is not None:
            response_text  = generate_response_from_llm(input_prompt_template.format(data_from_resume=data_from_resume, job_description=job_description))
            #print(response_text)
            # Parse the response if it's a JSON string (as a precaution)
            try:
                response_dict = json.loads(response_text)  # Converts the string to a dictionary
            except json.JSONDecodeError as e:
                st.error(f"Error parsing JSON: {e}")
                response_dict = {}


            #st.subheader("ATS Evaluation Result:")

            html_temp1 = """
            <div style="background-color:#76453B ;padding:6px">
            <h2 style="color:white;text-align:center;">ATS Evaluation Result </h2>
            </div>
            """
            st.markdown(html_temp1,unsafe_allow_html=True)

            # Now, display the content correctly

            # Display ATS Score
            html_temp2 = """
                <div style="background-color:#B19470; padding:6px; width:704px; margin:auto;">
                <h3 style="color:white;text-align:center; font-size:20px;">ATS Score</h3>
                </div>
            """
            st.markdown(html_temp2, unsafe_allow_html=True)
            #st.subheader("ATS Score")
            st.write(response_dict.get("ATS Score", "N/A"))

            # Display Summary/Career Objective
            html_temp2 = """
                <div style="background-color:#B19470; padding:6px; width:704px; margin:auto;">
                <h3 style="color:white;text-align:center; font-size:20px;">Summary/Career Objective</h3>
                </div>
            """
            st.markdown(html_temp2, unsafe_allow_html=True)
            #st.subheader("Summary/Career Objective")
            st.write(response_dict.get("Summary/Career Objective", "N/A"))

            # Display Missing Keywords
            #st.subheader("Missing Keywords")
            html_temp2 = """
                <div style="background-color:#B19470; padding:6px; width:704px; margin:auto;">
                <h3 style="color:white;text-align:center; font-size:20px;">Missing Keywords</h3>
                </div>
            """
            st.markdown(html_temp2, unsafe_allow_html=True)
            missing_keywords = response_dict.get("Missing Keywords", [])
            st.write(", ".join(missing_keywords) if missing_keywords else "No missing keywords")

            # st.write(response_text)
            # #st.write(f'{{\n"Job Description Match": "{match_percentage}%",\n"Missing Keywords": "",\n"Candidate Summary": "",\n"Experience": ""\n}}')

            # # Display message based on Job Description Match percentage
            # if match_percentage >= 80:
            #     st.text("Move forward with hiring")
            # else:
            #     st.text("Not a Match")

