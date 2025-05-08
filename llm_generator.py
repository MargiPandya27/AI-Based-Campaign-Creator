import os
import fitz  # PyMuPDF
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY not set in .env file")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')


def extract_text_from_pdf(filepath):
    """Extract text from the provided PDF file."""
    try:
        doc = fitz.open(filepath)  # Open the PDF
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # Get each page
            text += page.get_text()  # Extract text from the page
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""  # Return empty string if error occurs


def generate_campaign_content_with_rag(campaign_details, pdf_text=""):
    """Generate LinkedIn ad content based on campaign details and optional PDF content."""
    prompt = f"""
    You are a LinkedIn marketing expert tasked with creating a highly customized ad campaign for the brand "{campaign_details['product']}". 

    Based on the campaign brief below and the PDF material if provided, write compelling ad copy, suggest a creative hook, and provide targeting parameters tailored for LinkedIn advertising. Make sure the ad copy reflects the brand's unique value and does NOT include placeholders like [Brand Name], [Link to Website]. Include appropriate hashtags.
    {pdf_text[:6000]}  # Only include the first 6000 characters of the PDF text

    Campaign Brief:
    - Product: {campaign_details['product']}
    - Goal: {campaign_details['goal']}
    - Target Audience: {campaign_details['audience']}
    - Budget: {campaign_details['budget']}
    - Platform: {campaign_details['platform']}

    Please format your response EXACTLY as follows:

    HEADLINE: [Your catchy headline here]
    BODY: [Your persuasive ad body text here]

    Use a professional, engaging tone suitable for LinkedIn audiences."""

    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # Improved parsing of the response to extract the headline and body
        headline = ""
        body = ""

        # Split the response into lines and search for 'HEADLINE' and 'BODY' labels
        for line in content.split('\n'):
            if line.startswith("HEADLINE:"):
                headline = line.split("HEADLINE:")[1].strip()
            elif line.startswith("BODY:"):
                body = line.split("BODY:")[1].strip()

        # If the headline or body are empty, return default content
        if not headline or not body:
            headline = "Engaging Headline for Your Campaign"
            body = f"Check out {campaign_details['product']}! Here's why it's a must-have: {campaign_details['goal']}"

        return headline, body

    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return "Error generating headline", "Error generating body"
