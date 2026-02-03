from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(
            self, email, nick_name, password=None,
            commit=True):
        """
        Creates and saves a User with the given email, nickname and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not nick_name:
            raise ValueError(_('Users must have a nick name'))

        user = self.model(
            email=self.normalize_email(email),
            nick_name=nick_name,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user
        
    def create_superuser(self, email, nick_name, password):
        """
        Creates and saves a superuser with the given email, nick name,
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            nick_name=nick_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    nick_name = models.CharField(_('nickname'), max_length=30, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nick_name']

    def get_nick_name(self):
        """
        Return the nick_name.
        """
        return self.nick_name

    def __str__(self):
        return '{} <{}>'.format(self.nick_name, self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True