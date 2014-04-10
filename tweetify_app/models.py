from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import hashlib
import re
import warnings
from django.utils import timezone
from django.core import validators
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render


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

    def is_following(self, user, obj):
        """ Returns `True` or `False` """
        if isinstance(user, AnonymousUser):
            return False
        return 0 < self.follows(obj).filter(user=user).count()


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
    
    email = models.EmailField('email address', unique=True, )
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        # TODO: reverse function?
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


class Tweet(models.Model):
    tweet_text = models.CharField(blank=False, max_length=140)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now=True)

    def hashtags(self):
        if self.tweet_text.find('@') != -1:
            startPoint = self.tweet_text.find('@')
            endPoint = " "
            newtext = self.tweet_text[startPoint:]
            endIndex = newtext.find(endPoint)
            username = newtext[0:endIndex]
            if username.find('.') != -1:
                username = username[0:len(username)-1]
            username1 = username[1:]
            add_a = "<a href = '/user/%s'> " % username1
            newstring = str(add_a) + str(username)
            newstring2 = newstring + str('</a>')
            self.tweet_text1 = self.tweet_text.replace(username, newstring2)
            return self.tweet_text1

    def __unicode__(self):
        return self.tweet_text

