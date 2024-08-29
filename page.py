import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# Initialize the model for generating text
model = genai.GenerativeModel('gemini-pro')

# Function to generate content using the LLM model
def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    # Extract and return the main text response
    return response.candidates[0].content.parts[0].text

# Function to fetch and parse website content
def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching the website content: {e}")
        return None

# Function to extract relevant information from the website
def extract_relevant_info(soup):
    # Example: Extracting all paragraph texts
    paragraphs = soup.find_all('p')
    content = [p.text for p in paragraphs]
    return content

# Streamlit app
st.set_page_config(page_title='AI Chatbot')

# Header
st.title('Relinns Technologies Assignment')

# Input fields for URL and text
url = st.text_input('Enter the website URL:')
user_input = st.text_area('Enter your query:')

# Button to get response
if st.button('Get Response'):
    if url and user_input:
        # Fetch and parse website content
        soup = fetch_website_content(url)
        
        if soup:
            # Extract relevant information
            extracted_info = extract_relevant_info(soup)
            prompt = f"Based on the website data: {' '.join(extracted_info[:100])}, {user_input}"
            
            # Get the response from the model
            response = get_gemini_response(prompt)
            
            # Display the response with formatting
            st.subheader('Response from the AI:')
            
            # Format the output using Markdown for bold and color
            formatted_response = (
                f"**Input URL:** {url}\n\n"
                f"**User Query:** {user_input}\n\n"
                f"**AI Response:**\n"
                f"<span style='color:blue'>{response}</span>"
            )
            
            st.markdown(formatted_response, unsafe_allow_html=True)
        else:
            st.error("Failed to fetch or parse the website content.")
    else:
        st.error("Please provide both URL and query.")
