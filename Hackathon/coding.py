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
    input_message = (
        f"You are a Pharmacist with extensive knowledge of meds. I am taking {medication_list}. "
        "Provide potential interactions between these medications and foods, beverages, and other medications to avoid."
    )

    # Generate the response using the first Gemini API
    response = model_interaction.generate_content(input_message)
    print("Drug Interaction Information:")
    print(response.text)

def main():
    # Step 1: Ask if the input is text or images
    input_type = input("Are you providing a text or images with medications? (Enter 'text' or 'image'): ").strip().lower()

    medications = []  # List to store identified medications

    if input_type == "text":
        # Step 2A: Text-based medication input
        medication_names = input("Enter the names of the medications separated by commas: ").split(',')
        medications = [name.strip() for name in medication_names if name.strip()]

        # Retrieve drug interactions for the list of medications
        get_drug_interactions(medications)

    elif input_type == "image":
        # Step 2B: Image-based medication input
        image_paths = input("Enter the paths to the images containing medication names, separated by commas: ").split(',')

        # Process each image and identify medications
        for image_path in image_paths:
            image_path = image_path.strip()
            if image_path:
                # Extract text from the image
                extracted_text = extract_text_from_image(image_path)
                
                if extracted_text:
                    # Identify the most recognizable medication from the extracted text
                    medication_name = identify_medication_from_text(extracted_text)
                    
                    # If a medication was identified, add it to the list
                    if medication_name:
                        medications.append(medication_name)
                    else:
                        print(f"No valid medication name identified from the image {image_path}. Please try with a clearer image.")
                else:
                    print(f"No text detected in the image {image_path}. Please try with a clearer image.")
        
        # Retrieve drug interactions for all identified medications
        if medications:
            get_drug_interactions(medications)
        else:
            print("No medications identified from the provided images.")

    else:
        print("Invalid input type. Please enter 'text' or 'image'.")

if __name__ == "__main__":
    main()
