import shutil
import pytest


@pytest.fixture(autouse=True)
def temp_media_root(tmp_path, settings):
    """
    Fixture to set a temporary media root for tests that require file uploads.
    This ensures that tests do not interfere with the actual media files.
    """
    media_dir = tmp_path / 'media'
    media_dir.mkdir()
    settings.MEDIA_ROOT = str(media_dir)
    yield
    shutil.rmtree(str(media_dir), ignore_errors=True)