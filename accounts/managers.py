from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, username: str, password: str = None):
        """Creates and returns a regular user with the given email and username."""
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')

        # Normalize email to lowercase before saving
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            is_active=True
        )

        if password:
            user.set_password(password)
        else:
            raise ValueError('User must have a password')

        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, username: str, password: str):
        """Creates and returns a superuser with the given email, username, and password."""
        user = self.create_user(email, username, password)

        # Set superuser-specific fields
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user
