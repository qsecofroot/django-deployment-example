from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse('logged in')

@login_required
def user_logout(request):

    logout(request)
    #return HttpResponseRedirect(reverse("basic_app:index"))
    return HttpResponseRedirect(reverse("basic_app:index"))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username') #括号里对应的这是login.html里的那个username
        password = request.POST.get('password')#同上

        user = authenticate(username=username,password=password)#前面的是authenticate的参数，后面的是刚才声明的变量

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse("basic_app:index"))
            else:
                return HttpResponse('account is not active')
        else:
            print('some tried to login but failed')
            print('username:{} and password:{}'.format(username,password))
            return HttpResponse('invalid login detected')
    else:
        return render(request,'basic_app/login.html')
