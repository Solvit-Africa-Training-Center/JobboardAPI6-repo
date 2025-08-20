import pytest
from decimal import Decimal
from django.utils import timezone
from django.db import IntegrityError
from .factories import JobFactory, UserFactory


@pytest.mark.django_db
class TestJobModel:
    def test_job_creation_and_str(self):
        job = JobFactory(title="Backend Developer")
        assert str(job) == "Backend Developer"
        # recruiter reverse relation
        assert job.recruiter.jobs.count() >= 1

    def test_deadline_is_required_at_db_level(self, django_assert_num_queries):
        recruiter = UserFactory()
        # Creating a job without deadline should fail because null=False
        with pytest.raises(IntegrityError):
            from Jobs.models import Job
            Job.objects.create(
                title="No Deadline",
                description="desc",
                requirements="reqs",
                company_name="Acme",
                location="Kigali",
                salary=Decimal("100.000"),
                category="FullTime",
                job_type="Technology&IT",
                recruiter=recruiter,
                # deadline omitted
            )

    def test_salary_precision(self):
        job = JobFactory(salary=Decimal("12345.678"))
        assert job.salary == Decimal("12345.678")