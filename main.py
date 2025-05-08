import fitz  # PyMuPDF
from pydash import omit
from llm_generator import generate_campaign_content_with_rag, extract_text_from_pdf

def process_campaign(campaign_details, pdf_path):
    """Process the campaign, using extracted PDF content and generating the campaign plan."""
    
    # Pass the extracted pdf_text to the campaign generation function
    #if pdf_path:
        #print(f"🎯 PDF Content Extracted: \n\n{pdf_text[:500]}...")  # Show first 500 characters of PDF content
    pdf_text = extract_text_from_pdf(pdf_path)
    print(pdf_text)
    # Call the generation function with campaign details and the extracted pdf_text
    headline, body = generate_campaign_content_with_rag(omit(campaign_details, 'pdf_path'), pdf_text)
    return headline, body
    #else:
    #    print("No PDF content provided.")
    #    return None


if __name__ == "__main__":
    # Example campaign details with PDF path
    campaign_details = {
        'product': 'Smartphone Pro Max',
        'goal': 'Increase brand awareness',
        'audience': 'Tech enthusiasts',
        'budget': 5000,
        'platform': 'LinkedIn',
        'pdf_path': None  # No PDF provided
    }

    headline, body = process_campaign(campaign_details, campaign_details['pdf_path'])
