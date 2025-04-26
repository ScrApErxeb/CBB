from pathlib import Path
from typing import Union
import textract
from PyPDF2 import PdfReader
import mammoth

def load_file(filepath: Union[str, Path]) -> str:
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    ext = filepath.suffix.lower()

    try:
        if ext == ".pdf":
            # Lecture des PDF avec PyPDF2
            reader = PdfReader(str(filepath))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        
        elif ext == ".docx":
            # Lecture des DOCX avec Mammoth
            with open(filepath, "rb") as docx_file:
                result = mammoth.extract_raw_text(docx_file)
            return result.value
        
        elif ext in [".txt", ".md"]:
            # Lecture des fichiers texte simples
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()

        else:
            # Autres formats => fallback textract
            text = textract.process(str(filepath))
            return text.decode('utf-8')

    except Exception as e:
        raise ValueError(f"Failed to extract text from {filepath.name}: {e}")
