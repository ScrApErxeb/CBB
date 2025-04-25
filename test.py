from api.app.db.session import SessionLocal

db = SessionLocal()
try:
    db.execute('SELECT 1')  # test rapide
    print("✅ Connexion PostgreSQL OK")
except Exception as e:
    print("❌ Erreur :", e)
finally:
    db.close()
    print("🔒 Connexion fermée")
