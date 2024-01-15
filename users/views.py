from django.shortcuts import render, redirect
from django.http import Http404
from users.forms import LoginForms, RegisterForms
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.models import Config
from pathlib import os
from cryptography.fernet import InvalidToken
from reports.main import encrypt_or_decrypt


#from django.contrib.auth.models import User

def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            name = form['login'].value()
            password = form['password'].value()

        userAut = auth.authenticate(
            request,
            username=name,
            password=password
        )
        if userAut is not None:
            auth.login(request, userAut)
            #messages.success(request, f'{nome} logado com sucesso!')
            return redirect('/')
        else:
            messages.error(request, 'Erro ao efetuar login')

    return render(request, 'users/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')

def register(request):
    if request.user.is_authenticated:
        
        # get the user
        user = request.user
       
        # get the settings
        try:
            config = Config.objects.get(fk_user=user)
        except Config.DoesNotExist:
            config = Config(fk_user=user)

                
        if request.method == 'POST': 
            formUser = RegisterForms(request.POST)
        
            if formUser.is_valid():
                if user.password != formUser.cleaned_data['password']:
                    new_password = formUser.cleaned_data['password']
                    try:
                        validate_password(new_password, user=user)  #Validate a new password
                        user.set_password(formUser.cleaned_data['password'])
                    except ValidationError as error:
                        formUser.add_error('password', error)  #Adds the error to the password field
                        messages.error(request, error)

                #If you don't have any problems save the user changes
                if not formUser.has_error('password'):
                    user.username = formUser.cleaned_data['name']
                    user.email = formUser.cleaned_data['email']
                    user.save()
                    
                    #change the settings
                    config.fk_user = user
                    config.token = encrypt_or_decrypt(formUser.cleaned_data['token'])
                    config.jira_url = formUser.cleaned_data['jira_url']
                    config.save()

                    update_session_auth_hash(request, user)
                    messages.success(request, 'Perfil atualizado com sucesso!')
                
                return render(request, 'users/register.html', {'formUser': formUser})

        
        user = request.user


        try:
            token = encrypt_or_decrypt(config.token, False)
        except InvalidToken as error:
            messages.error(request, f"Erro no token: Por favor, atualizar com um novo token! {error}")
            token = ""

        data_form = {
            'name': user.username,
            'email': user.email,
            'password': user.password,
            'jira_url': config.jira_url,
            'token': token,
        }
        formUser = RegisterForms(initial=data_form)
        return render(request, 'users/register.html', {'formUser': formUser})
    else:
        # Redirecione para a página de login
        return redirect('login')
    




