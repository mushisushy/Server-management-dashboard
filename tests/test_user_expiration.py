from unittest.mock import patch, MagicMock
from website.website.models import update_expiration

@patch('website.website.models.db.session')
@patch('website.website.models.User')
def test_update_expiration_success(mock_user_class, mock_db_session):
    mock_user = MagicMock()
    mock_user.expire_date = "2024-01-01"
    mock_user_class.query.get.return_value = mock_user

    update_expiration(1, "2025-01-01")

    mock_user_class.query.get.assert_called_once_with(1)
    assert mock_user.expire_date == "2025-01-01"
    mock_db_session.commit.assert_called_once()

@patch('website.website.models.db.session')
@patch('website.website.models.User')
def test_update_expiration_user_not_found(mock_user_class, mock_db_session, capsys):
    mock_user_class.query.get.return_value = None

    update_expiration(999, "2025-01-01")

    mock_user_class.query.get.assert_called_once_with(999)
    mock_db_session.commit.assert_not_called()

    captured = capsys.readouterr()
    assert "User with ID 999 not found." in captured.out




