from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse
from django.contrib.auth import logout

from .pwd import *
from .forms import PwdForm


@login_required()
def open_db(request):
    user = request.user
    if request.method == 'GET':
        try:
            pwd_db = request.session['pwd_db']
            db = open_file(user.id, pwd_db)
            if not db:
                logout(request)
                return redirect('/users/login/')
            data = {'entries': db.entries}
            return render(request, 'app.html', data)
        except KeyError:
            logout(request)
            return redirect('/users/login/')
    else:
        request.session['pwd_db'] = request.POST['password']
        return redirect('/pwd/')


@login_required()
def get_pwd_list(request):
    user_id = request.user.id
    try:
        pwd_db = request.session['pwd_db']
        db = open_file(user_id, pwd_db)
    except KeyError:
        return HttpResponse("Password db not found", status=500)
    except FileNotFoundError:
        return HttpResponse("Db file not found", status=404)
    data = {'entries': db.entries}
    return render(request, "leftbar.html", data)


@login_required()
def pwd_props(request, title):
    pwd_db = request.session['pwd_db']
    user_id = request.user.id
    if title == 'new':
        item = None
        form = PwdForm(title='', username='', password='', url='')
        data = {'item': item, 'form': form}
        return render(request, "pwd_props.html", data)
    else:
        db = open_file(user_id, pwd_db)
        for x in db.entries:
            if x.title == title:
                item = x
                form = PwdForm(title=x.title, username=x.username, password=x.password, url=x.url)
                data = {'item': item, 'form': form}
                return render(request, "pwd_props.html", data)


@login_required()
@csrf_exempt
def del_password(request, name):
    try:
        pwd_db = request.session['pwd_db']
        user_id = request.user.id
        delete_password(pwd_db, user_id, name)
    except KeyError:
        return HttpResponse("Password db not found", status=500)
    except FileNotFoundError:
        return HttpResponse("Db file not found", status=404)
    except AttributeError:
        return HttpResponse("Password don't exists", status=404)
    return HttpResponse()


@login_required()
@csrf_exempt
def generate_password(request):
    pwd_db = request.session['pwd_db']
    post = request.POST
    title = post['title']
    username = post['username']
    pwd = post['password']
    password = check_pwd(pwd)
    user_id = request.user.id
    url = post['url']
    new_title = post['new_title']
    query = check_exists(pwd_db, title, user_id)
    if query:
        password_update(pwd_db, user_id, title, new_title, username, password, url)
        return HttpResponse("Entrada editada", status=202)
    else:
        add_password(pwd_db, user_id, new_title, username, password, url)
        return HttpResponse("Entrada salva", status=201)


@login_required()
def download_db(request):
    user_id = request.user.id
    filename = f"{path}/{user_id}.kdbx"
    response = FileResponse(open(filename, 'rb'))
    return response
