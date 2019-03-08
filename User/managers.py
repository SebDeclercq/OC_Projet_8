from typing import Any
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migration: bool = True

    def _create_user(
            self, email: str, password: str, **extra_fields: Any
    ) -> 'User':  # type: ignore  # noqa
        if not email or not password:
            raise ValueError(f'Email and Password are required for Users')
        email = self.normalize_email(email)
        user: 'User' = self.model(email=email, **extra_fields)  # type: ignore  # noqa
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, password: str, **extra_fields: Any
    ) -> 'User':  # type: ignore # noqa
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str, password: str, **extra_fields: Any
    ) -> 'User':  # type: ignore  # noqa
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
