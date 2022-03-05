from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from employee.models import employee

def LoginPage(request, page=''):

    if request.user.is_authenticated:
        return redirect('homepage')

    else:
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()
        #     messages.info(request, "cookie supported")
        # else:
        #     messages.info(request, "cookie not supported")
        # request.session.set_test_cookie()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            next_url = request.POST.get("next_url")
            user = authenticate(request,username=username,password=password)


            if user is not None:
                login(request, user)

                if next_url != '' and next_url != "/logout/":
                    response = redirect(next_url)
                else:
                    response = redirect("homepage")
                    

                if request.POST.get('remember_me'):
                    # expires = 'Thu, 28-May-2020 08:53:06 GMT'  # 24小时 格林威治时间
                    # expires = datetime.datetime(2020, 5, 28, 23, 44, 55))
                    expires = 60 * 60 * 24
                    max_age = 60 * 60 * 24
                    response.set_cookie('c_username', username, expires=expires, max_age=max_age)
                    response.set_cookie('c_password', password, expires=expires, max_age=max_age)

                return response

            else:
                messages.warning(request, 'Username or password is incorrect')

        if request.COOKIES.get('c_username'):

            context = {
                'c_username': request.COOKIES['c_username'],
                'c_password': request.COOKIES['c_password'],
                }
        else:
            context = {}

        next_url = request.GET.get("next", '')
        context['next_url'] = next_url
        #return render(request, 'login/login.html', context)
        return render(request, 'template4/login.html', context)



def LogOutPage(request):
    logout(request)
    #return redirect('homepage')
    return redirect('home')


from django.core.mail import send_mail
from django.conf import settings
import uuid
def forgot_password(request):
    global username
    try:
        if request.method == 'POST':
            username = request.POST.get('username') 

            if not employee.objects.filter(gongHao = username):
                messages.success(request, 'Gong hao not in our database')
                return render(request, 'template4/forgot_pass.html')
            elif employee.objects.filter(gongHao = username):
                user_obj = employee.objects.get(user = 1)#dunno why
                token = str(uuid.uuid4())
                user_obj.forgot_password_token = token
                user_obj.save()
                send_email_token(user_obj,token)
                messages.success(request, 'email has been sent') #gak berguna
    except Exception as e:
        print(e)
    return render(request, 'template4/forgot_pass.html')

def send_email_token(person, token):
    subject = "your password link"
    message = str(username) + f"12233 {token}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, ['wiratamawidarto@gmail.com'])

def change_password(request, token):
    try:
        profile_obj = employee.objects.get(forgot_password_token = token)
        context = {'user_id' : profile_obj.gongHao}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')
            if new_password != confirm_password:
                messages.success(request,'both should be same')

        user_obj = employee.objects.get(gongHao = user_id)
        # user_obj.password
    except Exception as e:
        print(e)

    return render(request, 'template4/change_pass.html')
