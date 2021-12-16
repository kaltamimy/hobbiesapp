from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import  LoginUserForm, CreateUserForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                messages.success(request, 'Account was created for '+user)
                return redirect('login')
        return render(request, 'mainapp/signup.html', {'form': form,})
        
def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == "POST":
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.info(request, 'Username or Password is Incorrect!')

        return render(request, 'mainapp/login.html', {'form': LoginUserForm()})

def logout_view(request):
    logout(request)
    return redirect('login')

def profile_view(request):
	return render(request, "mainapp/profile.html")

def edit_profile_view(request):
    return render(request, 'mainapp/edit_profile.html')

def users_list_view(request):
    return render(request, "mainapp/users_list.html")