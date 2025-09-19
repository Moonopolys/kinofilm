from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterationFrom
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data= request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Authenticationdan muvafaqqiyatli otdingiz😊😊😊")
            return redirect("main")
    else:
        form = LoginForm()

    context = {
        'form': form,
        "title": "Login"
    }

    return render(request, 'auth/login.html', context)


def user_register(request):
    if request.method == "POST":
        form = RegisterationFrom(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully")
            return redirect("login")
    else:
        form = RegisterationFrom()
    context = {
            'form': form,
            "title": "Registeration"
        }

    return render(request, 'auth/register.html', context)


from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('main')