from pathlib import Path
import mammoth
import PyPDF2
import textract

from app.vector.qdrant_utils import upsert_local_document
from app.db.database import get_db
from app.models import LocalDocument

def load_file(filepath: Path) -> str:
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        if filepath.suffix.lower() == ".pdf":
            reader = PyPDF2.PdfReader(str(filepath))
            text = " ".join(page.extract_text() or "" for page in reader.pages)
        elif filepath.suffix.lower() == ".docx":
            with open(filepath, "rb") as f:
                result = mammoth.extract_raw_text(f)
            text = result.value
        elif filepath.suffix.lower() in [".txt", ".md"]:
            text = filepath.read_text(encoding="utf-8")
        else:
            text = textract.process(str(filepath)).decode("utf-8")
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text: {e}")

def process_and_upsert(filepath: Path, user_id: str, db):
    text = load_file(filepath)
    
    # Upsert dans Qdrant
    upsert_local_document(user_id=user_id, text=text, filename=filepath.name)

    # Sauvegarder en base l'historique
    new_doc = LocalDocument(
        user_id=user_id,
        filename=filepath.name,
    )
    db.add(new_doc)
    db.commit()
