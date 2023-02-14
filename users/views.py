from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from pathlib import Path

from .forms import UserLoginForm, CustomUserCreationForm, EditUserForm
from password.pwd import create_new_file, change_file_password, path


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'GET':
            login_form = UserLoginForm()
            signup_form = CustomUserCreationForm()
            return render(request, 'login.html', {'login': login_form, 'signup': signup_form})
        else:
            username = request.POST['username']
            password = request.POST['password']
            pwd_db = request.POST['pwd_db']
            request.session['pwd_db'] = pwd_db
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return redirect('/users/login/')


def register_user(request):
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password1']
        pwd_db = request.POST['pwd_db']
        form.save()
        user = authenticate(username=username, password=password)
        db = create_new_file(user.id, pwd_db)
        request.session['pwd_db'] = pwd_db
        if user is not None:
            login(request, user)
            return redirect('/')
    else:
        return redirect('/users/login')


@login_required()
def logout_user(request):
    logout(request)
    return redirect('/users/login')


@login_required()
def edit_user(request):
    if request.method == 'POST':
        form = EditUserForm(user=request.user)
        if form.is_valid(user=request.user, data=request.POST):
            update_user(request)
            return redirect('/pwd/')
        else:
            data = {'form': form}
            return render(request, 'edit.html', data)
    else:
        form = EditUserForm(user=request.user)
        data = {'form': form}
        return render(request, 'edit.html', data)


def update_user(request):
    user = User.objects.get(pk=request.user.id)
    user.username = request.POST['username']
    user.email = request.POST['email']

    pwd = request.POST['password1']
    pwd2 = request.POST['password2']
    if pwd == pwd2 and pwd2 != '' and pwd != '':
        user.set_password(pwd)
        update_session_auth_hash(request, user)

    new_pwd_db = request.POST['pwd_db']
    if new_pwd_db != '':
        pwd_db = request.session['pwd_db']
        change_file_password(user.id, pwd_db, new_pwd_db)
        request.session['pwd_db'] = new_pwd_db
    user.save()

