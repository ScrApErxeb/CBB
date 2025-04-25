from api.app.db.models import Email
from api.app.db.session import SessionLocal

def test_email_insertion():
    db = SessionLocal()
    email = Email(id="test_id", snippet="Test snippet", internal_date="2025-04-24")
    db.add(email)
    db.commit()

    # Vérifiez que l'email est dans la base
    result = db.query(Email).filter(Email.id == "test_id").first()
    assert result is not None
    assert result.snippet == "Test snippet"

    # Nettoyage
    db.delete(result)
    db.commit()
    db.close()