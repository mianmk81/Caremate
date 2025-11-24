import os

import google.generativeai as genai
import pytesseract  # OCR library to process images
from PIL import Image  # To open and handle images

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configure the first Gemini API key for interaction information
# Get API key from environment variable or set it here (DO NOT commit real keys)
os.environ["GEMINI_API_KEY_1"] = os.getenv("GEMINI_API_KEY_1", "")  # Replace with the first Gemini API key
genai.configure(api_key=os.environ["GEMINI_API_KEY_1"])

# Configure the second Gemini API key for medication identification
# Get API key from environment variable or set it here (DO NOT commit real keys)
os.environ["GEMINI_API_KEY_2"] = os.getenv("GEMINI_API_KEY_2", "")  # Replace with the second Gemini API key

# First Gemini model for interaction information
model_interaction = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
)

# Second Gemini model for medication identification from text
model_identification = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
    }
)

def extract_text_from_image(image_path):
    """Extracts text from the provided image path."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print("Extracted text from image:", text)
        return text
    except Exception as e:
        print(f"Error reading image: {e}")
        return ""

def identify_medication_from_text(text):
    """Uses the second Gemini API to identify the most well-known medication name from extracted text."""
    prompt = f"Identify the most recognizable medication from the following text: {text}"
    response = model_identification.generate_content(prompt)
    medication_name = response.text.strip()
    print(f"Identified medication from text: {medication_name}")
    return medication_name

def get_drug_interactions(medication):
    """Uses the first Gemini API to get drug interactions for a specific medication."""
    input_message = (
        f"You are a Pharmacist with extensive knowledge of meds. I am taking {medication}. Provide potential interactions between this medication and foods, beverages, and other medications to avoid."
    )

    # Generate the response using the first Gemini API
    response = model_interaction.generate_content(input_message)
    print("Drug Interaction Information:")
    print(response.text)

def main():
    # Step 1: Ask if the input is text or image
    input_type = input("Are you providing a text or an image with medications? (Enter 'text' or 'image'): ").strip().lower()

    if input_type == "text":
        # Step 2A: Text-based medication input
        medication_name = input("Enter the name of the medication: ").strip()
        
        # Directly retrieve drug interactions for the provided medication name
        get_drug_interactions(medication_name)

    elif input_type == "image":
        # Step 2B: Image-based medication input
        image_path = input("Enter the path to the image containing medication names: ").strip()
        
        # Extract text from the image
        extracted_text = extract_text_from_image(image_path)
        
        if extracted_text:
            # Use the second Gemini API to identify the most recognizable medication from the extracted text
            medication_name = identify_medication_from_text(extracted_text)
            
            # If a medication was identified, pass it to get interaction information
            if medication_name:
                # Now use the identified medication name in the get_drug_interactions function
                get_drug_interactions(medication_name)
            else:
                print("No valid medication name identified from the image. Please try with a clearer image.")
        else:
            print("No text detected in the image. Please try with a clearer image.")

    else:
        print("Invalid input type. Please enter 'text' or 'image'.")

if __name__ == "__main__":
    main()