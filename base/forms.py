from django import forms

from base.models import IFUser


class RegistrationForm(forms.Form):
    nickname = forms.CharField(label='Přezdívka', max_length=100,
                               error_messages={'required': "Prosím zadejte přezdívku.",
                                               'min_length': 'Příliš krátká přezdívka.'})
    email = forms.EmailField(error_messages={'invalid': 'Prosím zadejte platný email.'})
    password = forms.CharField(label='Heslo', widget=forms.PasswordInput());
    confirm_password = forms.CharField(label='Opakuj heslo', widget=forms.PasswordInput());

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError('Hesla se neshodují.')
        return confirm_password

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if IFUser.objects.filter(username=nickname).exists():
            raise forms.ValidationError('Uživatel s tímto jménem už existuje.')
        return nickname
