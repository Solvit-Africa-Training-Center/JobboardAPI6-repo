import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@exampletest.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = "jobseeker"

    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        pwd = extracted or 'password123'
        self.set_password(pwd)
        if create:
            self.save()

class JobFactory(DjangoModelFactory):
    class Meta:
        model = 'Jobs.job'

    title = factory.Sequence(lambda n: f"Job Title {n}")
    description = factory.Faker('paragraph')
    requirements = factory.Faker('paragraph')
    company_name = factory.Faker('company')
    location = factory.Faker('city')
    salary = Decimal('50000.00')
    category = 'FullTime'
    job_type = 'Technology&IT'
    recruiter = factory.SubFactory(UserFactory, role=User.Role.RECRUITER)
    deadline = factory.LazyFunction(lambda: timezone.now() + timedelta(days=30))


class ApplicationFactory(DjangoModelFactory):
    class Meta:
        model = 'Jobs.application'

    job = factory.SubFactory(JobFactory)
    candidate = factory.SubFactory(UserFactory, role=User.Role.CANDIDATE)
    cover_letter = factory.Faker("paragraph")
    cv = factory.LazyFunction(lambda: SimpleUploadedFile("cv.pdf", b"fake file", content_type="application/pdf"))
    status = "pending"  # matches your STATUS_CHOICES value



class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = 'Jobs.userprofile'

    user = factory.SubFactory(UserFactory)
    resume = factory.LazyFunction(lambda: SimpleUploadedFile("resume.pdf", b"fake file", content_type="application/pdf"))
    bio = factory.Faker("text")



class SavedJobFactory(DjangoModelFactory):
    class Meta:
        model = 'Jobs.savedjob'

    user = factory.SubFactory(UserFactory)
    job = factory.SubFactory(JobFactory)

