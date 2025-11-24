import os

import fitz  # PyMuPDF for handling PDF files
import google.generativeai as genai
import pytesseract  # OCR library to process images
from PIL import Image  # To open and handle images

# Specify the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Configure the Gemini API keys
os.environ["GEMINI_API_KEY_1"] = ""
os.environ["GEMINI_API_KEY_2"] = ""
genai.configure(api_key=os.environ[""])

# Models configuration
model_interaction = genai.GenerativeModel("gemini-1.5-flash")
model_identification = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_image(image_path):
    """Extracts text from the provided image path."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
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
        return text
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
        return ""

def identify_medication_from_text(text):
    """Identifies the most well-known medication name from extracted text using the second Gemini API."""
    prompt = f"Identify the most recognizable medication from the following text: {text}"
    response = model_identification.generate_content(prompt)
    return response.text.strip()

def get_drug_interactions(medications, pdf_text):
    """Generates drug interactions using the first Gemini API, with information from the PDF."""
    medication_list = ", ".join(medications)
    input_message = f"You are a Pharmacist with extensive knowledge of medications. Use the pdf book made available to you if needed to find about the meds. I am taking {medication_list}.provide potential interactions between these medications and foods, beverages, and other medications to avoid. Use the reference text as your primary source of information. Think of it as you are giving info about a avgerage human in the united States of America"
    
    # Generate the response using the first Gemini API
    response = model_interaction.generate_content(input_message)
    
    # Print formatted response
    print("Drug Interaction Information:")
    print(response.text)

def main():
    medications = []  # List to store all identified medications
    pdf_text = extract_text_from_pdf("thebook.pdf")  # Load PDF content

    while True:
        input_type = input("Would you like to add medications via 'text', 'image', 'pdf'? Type 'done' when finished: ").strip().lower()

        if input_type == "text":
            # Text-based medication input
            medication_names = input("Enter the names of the medications separated by commas: ").split(',')
            medications.extend([name.strip() for name in medication_names if name.strip()])

        elif input_type == "image":
            # Image-based medication input
            image_paths = input("Enter the paths to the images containing medication names, separated by commas: ").split(',')
            for image_path in image_paths:
                extracted_text = extract_text_from_image(image_path.strip())
                if extracted_text:
                    medication_name = identify_medication_from_text(extracted_text)
                    if medication_name:
                        medications.append(medication_name)

        elif input_type == "pdf":
            # PDF-based medication input
            medication_name = identify_medication_from_text(pdf_text)
            if medication_name:
                medications.append(medication_name)

        elif input_type == "done":
            break
        else:
            print("Invalid input type. Please enter 'text', 'image', 'pdf', or 'done'.")

    # Retrieve drug interactions for all identified medications, using PDF content as a reference
    if medications and pdf_text:
        get_drug_interactions(medications, pdf_text)
    else:
        print("No medications were provided or PDF content could not be loaded.")

if __name__ == "__main__":
    main()

