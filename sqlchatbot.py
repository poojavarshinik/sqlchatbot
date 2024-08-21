import os
os.system('pip install google-generativeai')
os.system('pip install google-api_core')
import time
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Set the API key environment variable
os.environ["GEMINI_API_KEY"] = "AIzaSyA0Jx5lovrPEfz7_4_fLFwP4vttlOuRmXc"  # Replace with your actual API key

# Configure the Google AI API with the API key from the environment variable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    try:
        file = genai.upload_file(path, mime_type=mime_type)
        return file
    except exceptions.GoogleAPIError as e:
        st.error(f"An error occurred while uploading the file: {e}")
        raise

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    for name in (file.name for file in files):
        try:
            file = genai.get_file(name)
            while file.state.name == "PROCESSING":
                time.sleep(10)
                file = genai.get_file(name)
            if file.state.name != "ACTIVE":
                raise Exception(f"File {file.name} failed to process")
        except exceptions.GoogleAPIError as e:
            st.error(f"An error occurred while checking file status: {e}")
            raise

def main():
    st.title("SQL Query Generator Chatbot")
    st.write("This chatbot generates SQL queries based on your natural language input.")

    # Path to the file to be uploaded
    file_path = "SAMPLEE.csv"  # Update with the correct path

    # Upload file to Gemini
   
    try:
        files = [upload_to_gemini(file_path, mime_type="text/csv")]
       
    except Exception as e:
        st.error(f"Failed to upload file: {e}")
        return

    # Wait for the file to be active
   
    try:
        wait_for_files_active(files)
       
    except Exception as e:
        st.error(f"Failed to wait for file: {e}")
        return

    # Create the model with your generation configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You will be provided with natural language input and a schema for a table in a database. Your task is to construct an SQL query that retrieves the relevant data from the original table based on the input.\nAnalyze the given natural language input to identify the required data and its context.\nMatch the values or attributes mentioned in the natural language input to the corresponding columns in the original table schema. If an exact match for column names or values cannot be found, identify and use the most relevant matching columns and values based on context and similarity. If exact matches are not available, look for columns or values that are contextually similar or relevant. Make sure the query you give has values that belong to the original table.",
    )

    # Start a chat session with files included in the history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    files[0],
                    "I need companies in England that belong to the following industries: Educational Training Providers, Accounting, Steel Manufacturers, Business Management Consultants, Textile Merchants And Agents, Mobile App Development/Software Companies with employees ranging between 10 and 200.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```sql\nSELECT *\nFROM SAMPLEE\nWHERE country = 'England' AND\n      (sub_industry = 'Educational Training Providers' OR sub_industry = 'Accounting' OR sub_industry = 'Steel Manufacturers' OR sub_industry = 'Business Management Consultants' OR sub_industry = 'Textile Merchants And Agents' OR sub_industry = 'Mobile App Development/Software Companies') AND\n      employee_range BETWEEN '10 to 19' AND '200 to 499';\n```",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "Companies with industries related to housebuilder developers, property developers, construction, and builders.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```sql\nSELECT *\nFROM SAMPLEE\nWHERE industry IN ('Housebuilder Developer', 'Property Developer', 'Construction', 'Builder');\n```",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "I need restaurant and food industries in England with an employee range within 500 and 1000.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```sql\nSELECT *\nFROM SAMPLEE\nWHERE country = 'England'\n  AND (\n    sub_industry LIKE '%Restaurant%'\n    OR sub_industry LIKE '%Food%'\n    OR industry LIKE '%Food and Beverage%'\n  )\n  AND employee_range BETWEEN '500 to 999';\n```",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "I need accounting and advertising industries that have their head office in England.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```sql\nSELECT *\nFROM SAMPLEE\nWHERE head_office_country = 'England'\n  AND (\n    sub_industry = 'Accounting'\n    OR sub_industry LIKE '%Advertising%'\n    OR industry = 'Accounting'\n    OR industry = 'Advertising Services'\n  );\n```",
                ],
            },
            {
                "role": "user",
                "parts": [
                    "Companies that have SIC codes 4191 and 4128.",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```sql\nSELECT *\nFROM SAMPLEE\nWHERE SIC_CODE IN ('4191', '4128');\n```",
                ],
            },
        ]
    )

    # Input from user
    user_input = st.text_input("Enter your query:")

    if user_input:
        # Send the user's input to the model
        try:
            response = chat_session.send_message(user_input)
            st.write("Generated SQL Query:")
            st.code(response.text, language="sql")
        except Exception as e:
            st.error(f"Failed to get response from model: {e}")

if __name__ == "__main__":
    main()
