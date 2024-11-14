from django import forms

class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data