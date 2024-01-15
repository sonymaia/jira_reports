from django import forms


class LoginForms(forms.Form):
    login = forms.CharField(
        label='Login',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@exemplo.com',
            }
        )
    )
    password = forms.CharField(
        label='Password',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )


class RegisterForms(forms.Form):
    name = forms.CharField(
        label='Name',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: MarioSilva',
            }
        )
    )

    email = forms.CharField(
        label='E-mail',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@exemplo.com',
            }
        )
    )

    password = forms.CharField(
        label='Password',
        required=True,
        max_length=500,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a sua senha',
            }
        ),
    )

    jira_url = forms.CharField(
    label='Jira URL',
    required=True,
    max_length=300,
    widget=forms.TextInput(
    attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: https://jira.atlassian.net',
            }
        )
    )

    token = forms.CharField(
        label='Token',
        required=False,
        max_length=1000,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        ),
    )



    


