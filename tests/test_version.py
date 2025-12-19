import pytest
from unittest.mock import MagicMock, patch
from ide_updater.modules.vscode import VSCodeUpdater
from ide_updater.modules.cursor import CursorUpdater
from ide_updater.modules.kiro import KiroUpdater

@pytest.fixture
def mock_config():
    return {
        "install_dir": "/tmp/test_install",
        "temp_dir": "/tmp/test_temp",
        "ides": {
            "vscode": {"enabled": True},
            "cursor": {"enabled": True},
            "kiro": {"enabled": True}
        }
    }

def test_vscode_version(mock_config):
    updater = VSCodeUpdater(mock_config)
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "1.85.0"}
        assert updater.get_latest_version() == "1.85.0"

def test_kiro_version(mock_config):
    updater = KiroUpdater(mock_config)
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"version": "1.23.0"}
        assert updater.get_latest_version() == "1.23.0"

def test_cursor_updater_name(mock_config):
    updater = CursorUpdater(mock_config)
    assert updater.name == "Cursor"

def test_cursor_version_fallback(mock_config):
    updater = CursorUpdater(mock_config)
    # Mock HEAD failure and GET success
    with patch('requests.head') as mock_head:
        mock_head.return_value.status_code = 404
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            # Mocking the HTML content with a version inside
            mock_get.return_value.text = '<html><li>"1.7.54: Feature"</li></html>'
            assert updater.get_latest_version() == "1.7.54"
