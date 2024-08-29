import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key for Google Generative AI
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# Initialize the model for generating text
model = genai.GenerativeModel('gemini-pro')

# Function to generate content using the LLM model
def get_gemini_response(question):
    response = model.generate_content(question)
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
        print(f"Error fetching the website content: {e}")
        return None

# Function to extract relevant information from the website
def extract_relevant_info(soup):
    # Example: Extracting all paragraph texts
    paragraphs = soup.find_all('p')
    content = [p.text for p in paragraphs]
    return content

# Main function to interact with the chatbot
def chatbot_console():
    print("Welcome to the Gemini Chatbot. Type 'exit' to quit.")
    url = input("Please enter the website URL: ")
    
    # Fetch and parse website content
    soup = fetch_website_content(url)
    
    if soup:
        # Extract relevant information
        extracted_info = extract_relevant_info(soup)
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            # Optionally, you can use the extracted info in the prompt
            prompt = f"Based on the website data: {' '.join(extracted_info[:100])}, {user_input}"
            
            response = get_gemini_response(prompt)
            print("Bot:", response)

# Run the chatbot
if __name__ == "__main__":
    chatbot_console()