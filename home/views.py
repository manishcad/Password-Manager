from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm,UserRegisterForm,UpdatePasswordForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .utils import generate_random_password
from django.http import JsonResponse
from home.models import UserPassword
from home.encrypt_util import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
# Create your views here.


@login_required(login_url="login-page")
def home(request):
    return render(request,"pages/home.html")


def register_page(request):
    form=UserRegisterForm()
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account registered successfully. Please log in to your account.")
            return redirect("login-page")
    context={'form':form}
    return render(request,"pages/register.html",context)


def login_page(request):
    form=LoginForm()
    if request.method=="POST":
        form=LoginForm(request.POST)
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Invalid Username Or Password")
    context={"form":form}
    return render(request,"pages/index.html",context)

@login_required(login_url="login-page")
def add_new_password(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/', "request.path"))
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = encrypt(request.POST['password'])
            application_type = request.POST['application_type']
            if application_type == 'Website':
                website_name = request.POST['website_name']
                website_url = request.POST['website_url']
                UserPassword.objects.create(username=username, password=password, application_type=application_type,
                                            website_name=website_name, website_url=website_url, user=request.user).save()
                messages.success(request, f"New password added for {website_name}")
            elif application_type == 'Desktop application':
                application_name = request.POST['application_name']
                UserPassword.objects.create(username=username, password=password, application_type=application_type,
                                            application_name=application_name, user=request.user).save()
                messages.success(request, f"New password added for {application_name}.")
            elif application_type == 'Game':
                game_name = request.POST['game_name']
                game_developer = request.POST['game_developer']
                UserPassword.objects.create(username=username, password=password, application_type=application_type,
                                            game_name=game_name, game_developer=game_developer, user=request.user).save()
                
            return redirect("manage-passwords")
        except Exception as error:
            print("Error: ", error)

    return render(request, 'pages/add-password.html')


@login_required(login_url="login-page")
def manage_passwords(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/', request.path))
    sort_order = 'asc'
    logged_in_user = request.user
    user_passwords = UserPassword.objects.filter(user=logged_in_user)
    if request.GET.get('sort_order'):
        sort_order = request.GET.get('sort_order', 'desc')
        user_passwords = user_passwords.order_by('-date_created' if sort_order == 'desc' else 'date_created')
    if not user_passwords:
        return render(request, 'pages/manage-passwords.html',
                      {'no_password': "No password available. Please add password."})
    print(str("this is the password ")+user_passwords[0].password)
    return render(request, 'pages/manage-passwords.html', {'all_passwords': user_passwords, 'sort_order': sort_order})

@login_required(login_url="login-page")
def edit_password(request, pk):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/', request.path))
    user_password = UserPassword.objects.get(id=pk)
    user_password.password = decrypt(user_password.password)
    form = UpdatePasswordForm(instance=user_password)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # delete password
            user_password.delete()
            return redirect('/manage-passwords')
        form = UpdatePasswordForm(request.POST, instance=user_password)

        if form.is_valid():
            try:
                user_password.password = encrypt(user_password.password)
                form.save()
                messages.success(request, "Password updated.")
                user_password.password = decrypt(user_password.password)
                return HttpResponseRedirect(request.path)
            except ValidationError as e:
                form.add_error(None, e)

    context = {'form': form}
    return render(request, 'pages/edit-password.html', context)



def logout_page(request):
    logout(request)
    return redirect("login-page")


def generate_password(request):
    password = generate_random_password()
    return JsonResponse({'password': password})