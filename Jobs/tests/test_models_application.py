import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from .factories import JobFactory, UserFactory
from Jobs.models import Application, User

@pytest.mark.django_db
class TestApplicationModel:
    def test_create_application_and_str(self):
        job = JobFactory(title="Data Analyst")
        candidate = UserFactory(role=User.Role.CANDIDATE, email="cand@example.com")
        app = Application.objects.create(
            job=job,
            candidate=candidate,
            cover_letter="I love data",
            cv=SimpleUploadedFile("cv.pdf", b"file", content_type="application/pdf"),
        )
        # Default status should align with choices ('pending' in your choices)
        assert app.status == "pending"
        # __str__ should be human-friendly
        assert str(app) == "cand@example.com -> Data Analyst"

    def test_status_must_be_one_of_choices(self):
        job = JobFactory()
        candidate = UserFactory(role=User.Role.CANDIDATE)
        app = Application(job=job, candidate=candidate, cover_letter="x")
        app.status = "unknown"
        with pytest.raises(Exception):  # ValidationError if full_clean() is used
            app.full_clean()