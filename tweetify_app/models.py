from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import hashlib
import re
import warnings
from django.utils import timezone
from django.core import validators
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

class MyUser(AbstractBaseUser):
    """
    Custom user class.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first_name'), max_length=30, 
           help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid firstname.'), 'invalid')
        ])
    last_name = models.CharField(_('last_name'), max_length=30, 
           help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid lastname.'), 'invalid')
        ])    
    
    email = models.EmailField('email address', unique=True)
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s" % hashlib.md5(self.email).hexdigest()

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            DeprecationWarning, stacklevel=2)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache


    # def __unicode__(self):
    #     return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

class Tweet(models.Model):
    tweet_text = models.CharField(max_length=140)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.tweet_text

MyUser.profile = property(lambda u: MyUser.objects.get_or_create(user=u)[0])
