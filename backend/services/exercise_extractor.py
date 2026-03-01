"""
Exercise Extractor Service
Extracts math exercises from images, PDFs, LaTeX, and text files
Uses OCR and parsing to identify mathematical problems
"""

import os
import logging
import re
from typing import Dict, Optional, List
from io import BytesIO
import json

logger = logging.getLogger(__name__)

# Initialize Mistral client for text extraction
api_key = os.environ.get("MISTRAL_API_KEY", "").strip()
if api_key:
    try:
        from mistralai import Mistral
        client = Mistral(api_key=api_key)
        logger.info("✓ Mistral client initialized for exercise extraction")
    except Exception as e:
        logger.error(f"✗ Failed to initialize Mistral client: {e}")
        client = None
else:
    client = None


async def extract_from_image(image_bytes: bytes, filename: str) -> Dict:
    """
    Extract math exercise from image using OCR with MathΣtral enhancement
    """
    try:
        logger.info(f"📸 Extracting text from image: {filename}")
        
        from PIL import Image
        import pytesseract
        
        # Open image
        image = Image.open(BytesIO(image_bytes))
        
        # Apply preprocessing for better OCR
        image = image.convert('L')  # Convert to grayscale
        
        # Use Tesseract OCR
        extracted_text = pytesseract.image_to_string(image)
        
        if not extracted_text.strip():
            logger.warning("⚠️ No text detected in image")
            return {
                "success": False,
                "error": "No math exercise found in image. Please ensure the image is clear and contains mathematical problems.",
                "mode": "error"
            }
        
        # Use MathΣtral to identify and structure the exercise
        if client:
            response = client.chat.complete(
                model="mathstral-7b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a mathematical text parser. Extract and structure math problems from scanned images or text."
                    },
                    {
                        "role": "user",
                        "content": f"""This text was extracted from a scanned math exercise image. 
Extract and clean the mathematical problem(s) from this text:

{extracted_text}

Respond with JSON:
{{
  "problems": ["Problem 1", "Problem 2"],
  "cleaned_text": "Clean, formatted version of the problem",
  "format": "image_ocr",
  "confidence": 0.8,
  "notes": "Any notes about image quality or ambiguities"
}}"""
                    }
                ]
            )
            
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["source_format"] = "image"
                result["filename"] = filename
                return result
        
        return {
            "problems": [extracted_text],
            "cleaned_text": extracted_text,
            "format": "image_ocr",
            "confidence": 0.7,
            "source_format": "image",
            "filename": filename
        }
    
    except Exception as e:
        logger.error(f"❌ Error extracting from image: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to extract text from image: {str(e)}",
            "mode": "error"
        }


async def extract_from_pdf(pdf_bytes: bytes, filename: str) -> Dict:
    """
    Extract math exercises from PDF using text extraction and OCR
    """
    try:
        logger.info(f"📄 Extracting text from PDF: {filename}")
        
        from pypdf import PdfReader
        from pdf2image import convert_from_bytes
        
        pdf_file = BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        
        extracted_text = ""
        
        # First try text extraction
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text.strip():
                extracted_text += f"\n--- Page {page_num + 1} ---\n{text}"
        
        # If text extraction didn't work well, use OCR on images
        if len(extracted_text.strip()) < 50:
            logger.info("📸 PDF text extraction minimal, using OCR on PDF images...")
            images = convert_from_bytes(pdf_bytes)
            import pytesseract
            from PIL import Image
            
            for idx, image in enumerate(images):
                image_gray = image.convert('L')
                text = pytesseract.image_to_string(image_gray)
                if text.strip():
                    extracted_text += f"\n--- Page {idx + 1} (OCR) ---\n{text}"
        
        if not extracted_text.strip():
            return {
                "success": False,
                "error": "No text found in PDF. Please ensure PDF contains text or clear images.",
                "mode": "error"
            }
        
        # Use MathΣtral to parse and structure
        if client:
            response = client.chat.complete(
                model="mathstral-7b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a mathematical text parser. Extract and structure math problems from PDF content."
                    },
                    {
                        "role": "user",
                        "content": f"""Extract math exercises from this PDF content:

{extracted_text[:2000]}

Respond with JSON:
{{
  "problems": ["Problem 1", "Problem 2"],
  "cleaned_text": "Clean version of the primary problem",
  "format": "pdf",
  "page_count": 1,
  "confidence": 0.85
}}"""
                    }
                ]
            )
            
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["source_format"] = "pdf"
                result["filename"] = filename
                result["full_text"] = extracted_text
                return result
        
        return {
            "problems": [extracted_text],
            "cleaned_text": extracted_text[:500],
            "format": "pdf",
            "source_format": "pdf",
            "filename": filename,
            "full_text": extracted_text
        }
    
    except Exception as e:
        logger.error(f"❌ Error extracting from PDF: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to extract from PDF: {str(e)}",
            "mode": "error"
        }


async def extract_from_latex(latex_text: str, filename: str = "exercise.tex") -> Dict:
    """
    Extract and parse math exercise from LaTeX format
    """
    try:
        logger.info("🔤 Parsing LaTeX exercise...")
        
        # Extract problem from LaTeX common structures
        patterns = {
            "problem": r"\\problem\{(.*?)\}",
            "textbf": r"\\textbf\{(.*?)\}",
            "equation": r"\$\$(.*?)\$\$",
            "inline_math": r"\$(.*?)\$",
            "section": r"\\(section|subsection|subsubsection)\{(.*?)\}",
        }
        
        extracted_content = ""
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, latex_text, re.DOTALL)
            if matches:
                if isinstance(matches[0], tuple):
                    for match in matches:
                        extracted_content += f"\n{match[1] if len(match) > 1 else match[0]}"
                else:
                    for match in matches:
                        extracted_content += f"\n{match}"
        
        # If no patterns matched, use the whole text
        if not extracted_content.strip():
            extracted_content = latex_text
        
        # Clean LaTeX formatting
        cleaned = re.sub(r'\\[a-zA-Z]+\{', '', extracted_content)
        cleaned = re.sub(r'\}', '', cleaned)
        cleaned = re.sub(r'\\\[|\\\]', '', cleaned)
        cleaned = re.sub(r'\$\$|\$', '', cleaned)
        
        if client:
            response = client.chat.complete(
                model="mathstral-7b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a LaTeX to plain text converter for math problems."
                    },
                    {
                        "role": "user",
                        "content": f"""Convert this LaTeX math exercise to clean plain text:

{extracted_content[:1000]}

Output as JSON:
{{
  "problems": ["The main problem"],
  "cleaned_text": "Plain text version",
  "has_equations": true,
  "format": "latex"
}}"""
                    }
                ]
            )
            
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["source_format"] = "latex"
                result["filename"] = filename
                result["original_latex"] = latex_text
                return result
        
        return {
            "problems": [cleaned],
            "cleaned_text": cleaned,
            "format": "latex",
            "source_format": "latex",
            "filename": filename,
            "original_latex": latex_text
        }
    
    except Exception as e:
        logger.error(f"❌ Error extracting from LaTeX: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to parse LaTeX: {str(e)}",
            "mode": "error"
        }


async def extract_from_text(text_content: str, filename: str = "exercise.txt") -> Dict:
    """
    Parse and structure math exercise from plain text
    """
    try:
        logger.info("📝 Parsing text exercise...")
        
        if not text_content.strip():
            return {
                "success": False,
                "error": "No text content provided",
                "mode": "error"
            }
        
        # Use MathΣtral to identify and structure problems
        if client:
            response = client.chat.complete(
                model="mathstral-7b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a math problem parser. Identify and structure mathematical exercises from text."
                    },
                    {
                        "role": "user",
                        "content": f"""Identify math problems in this text:

{text_content[:1000]}

Output as JSON:
{{
  "problems": ["Problem 1", "Problem 2"],
  "cleaned_text": "Main problem",
  "problem_count": 1,
  "format": "text"
}}"""
                    }
                ]
            )
            
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                result["source_format"] = "text"
                result["filename"] = filename
                return result
        
        return {
            "problems": [text_content],
            "cleaned_text": text_content,
            "format": "text",
            "source_format": "text",
            "filename": filename
        }
    
    except Exception as e:
        logger.error(f"❌ Error parsing text: {str(e)}")
        return {
            "success": False,
            "error": f"Failed to parse text: {str(e)}",
            "mode": "error"
        }


async def extract_exercise(
    file_bytes: bytes,
    filename: str,
    file_type: str
) -> Dict:
    """
    Main entry point: Extract exercise from any format
    file_type: 'image', 'pdf', 'latex', 'text'
    """
    logger.info(f"🔄 Extracting exercise from {file_type}: {filename}")
    
    if file_type == "image":
        return await extract_from_image(file_bytes, filename)
    elif file_type == "pdf":
        return await extract_from_pdf(file_bytes, filename)
    elif file_type == "latex":
        try:
            latex_text = file_bytes.decode('utf-8')
            return await extract_from_latex(latex_text, filename)
        except Exception as e:
            logger.error(f"Error decoding LaTeX: {e}")
            return {
                "success": False,
                "error": "Failed to decode LaTeX file",
                "mode": "error"
            }
    elif file_type == "text":
        try:
            text_content = file_bytes.decode('utf-8')
            return await extract_from_text(text_content, filename)
        except Exception as e:
            logger.error(f"Error decoding text: {e}")
            return {
                "success": False,
                "error": "Failed to decode text file",
                "mode": "error"
            }
    else:
        return {
            "success": False,
            "error": f"Unsupported file type: {file_type}",
            "mode": "error"
        }
