import os

import fitz  # PyMuPDF for handling PDF files
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
    model_name="gemini-1.5-flash",
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
    model_name="gemini-1.5-flash",
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
        print(f"Extracted text from image {image_path}: {text}")
        return text
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return ""

def extract_text_from_pdf(pdf_path):
    """Extracts text from the provided PDF path."""
    try:
        text = ""
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
        print(f"Extracted text from PDF {pdf_path}: {text}")
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def identify_medication_from_text(text):
    """Uses the second Gemini API to identify the most well-known medication name from extracted text."""
    prompt = f"Identify the most recognizable medication from the following text: {text}"
    response = model_identification.generate_content(prompt)
    medication_name = response.text.strip()
    print(f"Identified medication from text: {medication_name}")
    return medication_name

def get_drug_interactions(medications):
    """Uses the first Gemini API to get drug interactions for a list of medications."""
    medication_list = ", ".join(medications)
    input_message = f"You are a Pharmacist with extensive knowledge of meds. I am taking {medication_list}.use the pdf knowledge and give us a general overview, Provide potential interactions between these medications and foods, beverages, and other medications to avoid."
    

    # Generate the response using the first Gemini API
    response = model_interaction.generate_content(input_message)
    print("Drug Interaction Information:")
    print(response.text)

def main():
    medications = []  # List to store all identified medications

    while True:
        # Ask if the user wants to add medications via text, image, pdf, or if they are done
        input_type = input("Would you like to add medications via 'text', 'image', 'pdf'? Type 'done' when finished: ").strip().lower()

        if input_type == "text":
            # Text-based medication input
            medication_names = input("Enter the names of the medications separated by commas: ").split(',')
            medications.extend([name.strip() for name in medication_names if name.strip()])

        elif input_type == "image":
            # Image-based medication input
            image_paths = input("Enter the paths to the images containing medication names, separated by commas: ").split(',')
            for image_path in image_paths:
                image_path = image_path.strip()
                if image_path:
                    # Extract text from the image
                    extracted_text = extract_text_from_image(image_path)
                    
                    if extracted_text:
                        # Use the second Gemini API to identify the most recognizable medication from the extracted text
                        medication_name = identify_medication_from_text(extracted_text)
                        
                        # If a medication was identified, add it to the list
                        if medication_name:
                            medications.append(medication_name)
                        else:
                            print(f"No valid medication name identified from the image {image_path}. Please try with a clearer image.")
                    else:
                        print(f"No text detected in the image {image_path}. Please try with a clearer image.")

        elif input_type == "pdf":
            # PDF-based medication input
            pdf_path = "./thebook.pdf"  # Hardcoded for the same directory
            extracted_text = extract_text_from_pdf(pdf_path)
            
            if extracted_text:
                # Use the second Gemini API to identify the most recognizable medication from the extracted text
                medication_name = identify_medication_from_text(extracted_text)
                
                # If a medication was identified, add it to the list
                if medication_name:
                    medications.append(medication_name)
                else:
                    print(f"No valid medication name identified from the PDF {pdf_path}. Please try with a clearer PDF.")
            else:
                print(f"No text detected in the PDF {pdf_path}. Please try with a clearer PDF.")

        elif input_type == "done":
            # Exit the loop and show results
            break

        else:
            print("Invalid input type. Please enter 'text', 'image', 'pdf', or 'done'.")

    # Once all inputs are collected, retrieve drug interactions for all identified medications
    if medications:
        get_drug_interactions(medications)
    else:
        print("No medications were provided.")

if __name__ == "__main__":
    main()
