from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import Group

from .forms import *


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Buscamos el grupo cliente
            group = Group.objects.get(name='Cliente')
            #Asignamos a todos los usuarios por defecto al grupo Cliente
            user.groups.add(group)       
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {
        'form': form
        })

def forbidden(request):
    return render(request, 'registration/forbidden.html')