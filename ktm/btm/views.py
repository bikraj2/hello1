from django.shortcuts import render
from btm.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls  import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'btm/index.html')
@login_required
def special(request):
    return HttpResponse("you are logged in mofo")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def  register(request):

    registered=False

    if request.method=="POST":
         user_form = UserForm(data=request.POST)
         profile_form = UserProfileInfoForm(data=request.POST)

         if user_form.is_valid() and profile_form.is_valid():
             user=user_form.save()
             user.set_password(user.password)
             user.save()

             profile=profile_form.save(commit=False)

             profile.user =user
             if 'profile_pic' in request.FILES:
                 profile.profile_pic = request.FILES['profile_pic']


             registered=True

         else:
               print(user_form.errors,profile_form.errors)
    else:
          user_form=UserForm()
          profile_form=UserProfileInfoForm()
    dict1= {'user':user_form,'profile':profile_form,'registered':registered }
    return render(request,'btm/registration.html',context=dict1)





def user_login(request):

    if request.method=="POST":
        username =request.POST.get('username')
        password =request.POST.get('password')

        user= authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect("account not active")
        else:
            print("someone tried to login in and failed")
            print("username: {} and password".format(username,password))
            return HttpResponse("invalid login details")
    else:
        return render(request,'btm/login.html')
