from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='usuarios:sinPermiso')
def menuPrincipal(request):
    return render(request, 'core/menuPrincipal.html')
