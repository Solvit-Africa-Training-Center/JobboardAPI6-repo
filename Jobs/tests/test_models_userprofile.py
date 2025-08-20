import pytest
from .factories import UserProfileFactory

@pytest.mark.django_db
def test_userprofile_str_and_fields():
    profile = UserProfileFactory()
    assert str(profile) == f"Profile of {profile.user.email}"
    assert profile.user.profile == profile 
    if profile.resume:
        assert profile.resume.name.startswith("resume/")