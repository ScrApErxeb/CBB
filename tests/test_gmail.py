import pytest
from unittest.mock import patch, MagicMock
from api.app.sources.gmail import fetch_recent_emails

@patch("api.app.sources.gmail.get_gmail_service")
@patch("api.app.sources.gmail.SessionLocal")
def test_fetch_recent_emails(mock_session, mock_gmail_service):
    # Mock Gmail API response
    mock_service = MagicMock()
    mock_gmail_service.return_value = mock_service
    mock_service.users().messages().list().execute.return_value = {
        "messages": [{"id": "123"}, {"id": "456"}]
    }
    mock_service.users().messages().get().execute.side_effect = [
        {"id": "123", "snippet": "Test email 1", "internalDate": "1680000000000"},
        {"id": "456", "snippet": "Test email 2", "internalDate": "1680000000000"},
    ]

    # Mock database session
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    mock_db.query().filter().first.side_effect = [None, None]  # No duplicates

    # Call the function
    emails = fetch_recent_emails()

    # Assertions
    assert len(emails) == 2
    assert "Test email 1" in emails
    assert "Test email 2" in emails
    mock_db.add.assert_called()  # Ensure emails are added to the DB
    mock_db.commit.assert_called_once()