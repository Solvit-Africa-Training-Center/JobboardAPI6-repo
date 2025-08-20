import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError


User = get_user_model()

@pytest.mark.django_db
class TestUserModel:

    def test_create_user_success(self):
        user = User.objects.create_user(
            email="test@Example.com",  # input with mixed case
            password="secret123",
            first_name="Grace",
            last_name="Hopper",
            role=User.Role.CANDIDATE,
        )
        # Django normalizes email: domain part is lowercase
        assert user.email == "test@example.com"
        assert user.first_name == "Grace"
        assert user.last_name == "Hopper"
        assert user.role == User.Role.CANDIDATE
        assert user.check_password("secret123") is True

        # assert user.is_staff is False
        # assert user.is_superuser is False



    def test_create_user_without_email_raises(self):
        with pytest.raises(ValueError):
            User.objects.create_user(
                email="",
                password="pass",
                first_name="No",
                last_name="Email",
                role=User.Role.CANDIDATE,
            )

    def test_email_is_unique(self):
        User.objects.create_user(
            email="unique@example.com",
            password="pass",
            first_name="Uni",
            last_name="Que",
            role=User.Role.RECRUITER,
        )
        with pytest.raises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com",
                password="pass2",
                first_name="Dup",
                last_name="Licate",
                role=User.Role.CANDIDATE,
            )

    def test_create_superuser_flags_and_role(self):
        admin = User.objects.create_superuser(
            email="admin@example.com",
            password="super123",
            first_name="Admin",
            last_name="User",
        )
        assert admin.is_staff is True
        assert admin.is_superuser is True
        assert admin.role == User.Role.ADMIN


    def test_str_representation(self):
        user = User.objects.create_user(
            email="str@example.com",
            password="pass",
            first_name="Str",
            last_name="User",
            role=User.Role.RECRUITER,
        )
        assert str(user) == "str@example.com (recruiter)"