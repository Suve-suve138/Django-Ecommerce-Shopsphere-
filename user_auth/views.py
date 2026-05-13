from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_(request):
    if request.method=='POST':
        a = request.POST['uname']
        b = request.POST['password']

        u = authenticate(
            username = a,
            password = b
        )
        # print(u)
        if u:
            login(request,u)
            return redirect('home')
        else:
            return render(request,'login_.html',{'error':'invalid username or password'})
    return render(request,'login_.html')
@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')



def register(request):
    if request.method=='POST':
        a = request.POST['fname']
        b = request.POST['lname']
        c = request.POST['email']
        d = request.POST['uname']
        e = request.POST['password']

        try:
            u = User.objects.get(username = d)
            return render (request,'register.html',{'status':'username already exists !!'})
        except:
            u = User.objects.create(
                first_name = a,
                last_name = b,
                email = c,
                username = d,
            )
            u.set_password(e)
            u.save()
        return redirect('login_')

    return render(request,'register.html')



@login_required(login_url='login_')
def profile(request):
    return render(request,'profile.html')

def forget_pass(request):
    if request.method=='POST':
        u = request.POST['uname']
        try:
            a = User.objects.get(username = u)
            request.session['fp_user'] = a.username
            return redirect('new_pass')
        except:
            return render(request,'forget_pass.html',{'error':True})
    return render(request,'forget_pass.html')



def new_pass(request):
    username = request.session.get('fp_user')
    if username is None:
        return redirect('forget_pass')
    user = User.objects.get(username = username)
    if request.method=='POST':
        p = request.POST['npass']
        if user.check_password(p):
            return render(request,'new_pass.html',{'error':True})
        user.set_password(p)
        user.save()
        del request.session['fp_user']
        return redirect('login_')

    return render(request,'new_pass.html')

@login_required(login_url='login_')
def reset_pass(request):
    if request.method=='POST':
        if 'opass' in request.POST:
            a = request.POST['opass']
            b = request.user.check_password(a)
            # print(b)
            if b :
                return render(request,'reset_pass.html',{'new_pass':True})
            else:
                return render(request,'reset_pass.html',{'wrong':True})
        if 'npass' in request.POST:
            np = request.POST['npass']
            if request.user.check_password(np):
                return render(request,'reset_pass.html',{'same':True})
            else:
                request.user.set_password(np)
                request.user.save()
                return redirect('login_')
    return render(request,'reset_pass.html')