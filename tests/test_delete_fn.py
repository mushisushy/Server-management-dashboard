from unittest.mock import MagicMock, patch

import pytest

from website.website.models import delete_user


# Test when the user exists
@patch("website.website.models.db.session")
@patch("website.website.models.User")
def test_delete_existing_user(mock_user_class, mock_db_session):
    mock_user = MagicMock()
    mock_user_class.query.get.return_value = mock_user

    delete_user(1)

    mock_user_class.query.get.assert_called_once_with(1)
    mock_db_session.delete.assert_called_once_with(mock_user)
    mock_db_session.commit.assert_called_once()


# Test when the user does not exist
@patch("website.website.models.db.session")
@patch("website.website.models.User")
def test_delete_nonexistent_user(mock_user_class, mock_db_session, capsys):
    mock_user_class.query.get.return_value = None

    delete_user(999)

    mock_user_class.query.get.assert_called_once_with(999)
    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()

    captured = capsys.readouterr()
    assert f"User with ID 999 not found" in captured.out
