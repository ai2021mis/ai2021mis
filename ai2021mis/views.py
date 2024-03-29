from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from employee.models import employee

#these imports are for custom email forgot pass
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings

def LoginPage(request, page=''):

    if request.user.is_authenticated:
        return redirect('home')

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
                    response = redirect("home")
                    

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



def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            # data = password_form.cleaned_data.get('email')
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(Q(email = data))
            if user_email.exists():
                for user in user_email:
                    subject = "password request."
                    email_template_name = 'template4/password_reset_subject.txt'
                    parameters = {
                        'email': user.email,
                        'domain' : settings.WEB_HOST,
                        # 'domain' : '127.0.0.1/',
                        'site_name': 'nchu mis',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        # 'protocol': 'https',
                    }
                    email = render_to_string(email_template_name, parameters)
                    try:
                        send_mail(subject, email, '', [user.email], fail_silently = False)
                    except:
                        return HttpResponse('Invalid Header')
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()

    context = {
        'password_form': password_form,
        }
    return render(request, 'template4/forgot_pass.html', context)