from django.shortcuts import render, redirect


def home(request):
    return redirect('/pwd/')


def about(request):
    return render(request, 'about.html')


