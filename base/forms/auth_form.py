"""Form classes for IFUser entity."""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from base.models.ifuser import IFUser


class IFUserCreationForm(UserCreationForm):
    """Form for creating user."""
    class Meta:
        model = IFUser
        fields = ('username', 'email')


class IFUserChangeForm(UserChangeForm):
    """Form for changing user parameters."""
    class Meta:
        model = IFUser
        fields = ('username', 'email')
