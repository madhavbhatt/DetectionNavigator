from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserLoginForm, PasswordChangeForm
from django.views.decorators.cache import never_cache
from django.views.decorators.clickjacking import *


User = get_user_model()


@xframe_options_deny
@never_cache
def login_view(request):
    logout(request)
    form = UserLoginForm(request.POST or None)
    next = request.GET.get('next')
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "user_login.html", {"form": form})


@xframe_options_deny
@never_cache
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

