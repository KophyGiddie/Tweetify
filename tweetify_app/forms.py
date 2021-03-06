from models import MyUser
from django import forms
from django.core.exceptions import ValidationError
from models import Tweet
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

class UserCreateForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs=
    {'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs=
        {'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs=
        {'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.widgets.TextInput(attrs=
        {'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.widgets.PasswordInput(attrs=
        {'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.widgets.PasswordInput(attrs=
        {'placeholder': 'Password Confirmation'}))
 
 
    class Meta:
        # TODO: remove password2
        fields = ['email', 'username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = MyUser

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            MyUser._default_manager.get(username=username)
        except MyUser.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            MyUser._default_manager.get(email=email)
        except MyUser.DoesNotExist:
            return email
        raise forms.ValidationError('Duplicate Email')


class AuthenticateForm(forms.Form):
    email = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError('invalid_login')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('inactive')
        return self.cleaned_data

        
class TweetForm(forms.ModelForm):
    tweet_text = forms.CharField(required=True, widget=forms.widgets.Textarea(attrs={'cols':'26', 'class': 'tweet_text'}))

    class Meta:
        model = Tweet
        fields = ['tweet_text']

