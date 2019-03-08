from typing import Any, List, Optional, Sequence
from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)


class CustomUserManager(BaseUserManager):
    '''Custom Manager overriding basic behavior from default UserManager.'''
    def create_user(self, *args: Any, **kwargs: Any) -> Any:
        '''Creates and saves a new User w/ email and password'''
        user: Any = self._set_user(*args, **kwargs)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args: Any, **kwargs: Any) -> Any:
        '''A superuser is a classic user'''
        user: Any = self._set_user(*args, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def _set_user(
        self, email: str, password: str,
        name: Optional[str] = None, firstname: Optional[str] = None
    ) -> Any:
        '''Private method generating a User'''
        required_fields: Sequence[str] = (
            CustomUser.USERNAME_FIELD, *CustomUser.REQUIRED_FIELDS
        )
        for required_field in required_fields:
            if not required_field:
                raise ValueError(f'A {required_field} is required for Users')
        user: CustomUser = self.model(  # type: ignore
            email=self.normalize_email(email),
            name=name,
            firstname=firstname
        )
        user.set_password(password)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    '''Custom User Model'''
    email: models.EmailField = models.EmailField(max_length=255, unique=True)
    name: models.CharField = models.CharField(max_length=255, null=True)
    firstname: models.CharField = models.CharField(max_length=255, null=True)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_admin: models.BooleanField = models.BooleanField(default=False)

    objects: CustomUserManager = CustomUserManager()

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = []

    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self) -> bool:
        return self.is_admin
