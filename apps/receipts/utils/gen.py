import os
import json
import easyocr
import numpy as np

from dotenv import load_dotenv
from pdf2image import convert_from_path
from google import genai
from receipt_manager.constant import get_prompt

load_dotenv()

class DocumentProcessor:
    def __init__(self, model_name: str, pdf_path: str):
        """
        Initializes the DocumentProcessor with the model name and PDF path.
        
        Args:
            model_name (str): The model to be used for generating content.
            pdf_path (str): The path to the PDF file to be processed.
        """
        self.model_name = model_name
        self.pdf_path = pdf_path
        self.reader = easyocr.Reader(['en'])

    def _extract_text_from_pdf(self) -> str:
        """
        Extracts text from the given PDF using OCR.
        
        Returns:
            str: Extracted text from the PDF. Returns an empty string if no text is found.
            
        Raises:
            ValueError: If no text is extracted from the PDF.
        """
        try:
            images = convert_from_path(self.pdf_path)
            extracted_text = ""

            for image in images:
                image_np = np.array(image)
                result = self.reader.readtext(image_np)
                extracted_text += "\n".join([line[1] for line in result])
                
            if not extracted_text:
                raise ValueError("No text extracted from the PDF.")
            
            return extracted_text
        except Exception as error:
            raise RuntimeError(f"Error during OCR extraction: {error}")

    def _process_text_with_model(self, extracted_text: str) -> dict:
        """
        Processes the extracted text using a model to generate structured content.
        
        Args:
            extracted_text (str): The raw text extracted from the PDF.
        
        Returns:
            dict: The structured data obtained from the model's response.
            
        Raises:
            json.JSONDecodeError: If the response cannot be parsed as JSON.
        """
        client = genai.Client(api_key=os.getenv('GENAI_API_KEY'))
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=get_prompt(extracted_text)
        )
        
        cleaned_text = response.text.strip('```json').strip('```')
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError as error:
            raise ValueError(f"Failed to parse JSON response: {error}")

    def process_pdf(self) -> dict:
        """
        Processes the PDF file by extracting text using OCR and then applying the model 
        to generate structured data.

        Returns:
            dict: The structured data obtained from the model's response.

        Raises:
            ValueError: If no text is extracted from the PDF.
            RuntimeError: If an error occurs during OCR extraction.
            ValueError: If the model response cannot be parsed as JSON.
        """
        extracted_text = self._extract_text_from_pdf()
        return self._process_text_with_model(extracted_text)
