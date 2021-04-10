from django.shortcuts import render
from django.shortcuts import redirect

def redirect_admin(request):
    return redirect('/admin')

def handler404(request, exception):
    return redirect('/admin')