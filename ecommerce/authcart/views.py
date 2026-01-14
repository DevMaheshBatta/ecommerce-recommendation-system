from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django .contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django .conf import settings
from django.views.generic import View
from django .contrib.auth import authenticate,login,logout
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Initialize token generator
generate_token = PasswordResetTokenGenerator()

def signup(request):
    print("It is signup function")
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        # Check if passwords match
        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return render(request, 'signup.html')

        # Check if email is already taken
        if User.objects.filter(username=email).exists():
            messages.info(request, "Email is already taken")
            return render(request, 'signup.html')

        # Create user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False
        user.save()

        # Email activation link
        email_subject = "Activate Your Account"
        message = render_to_string('activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.content_subtype = "html"  # Set email to HTML format
        email_message.send()

        messages.success(request, "Activate your account by clicking the link sent to your email.")
        return redirect('/auth/login/')

    return render(request,"signup.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  # ✅ Replaced force_text with force_str
            user = User.objects.get(pk=uid)  # ✅ Fixed "objects" typo
        except (User.DoesNotExist, ValueError, TypeError):
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account Activated Successfully")
            return redirect('/auth/login')

        return render(request, 'activationfail.html')  # If activation fails

# Login Handler
def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        userpassword = request.POST['pass1']
        myuser=authenticate(username=username, password=userpassword)

        if myuser is not None:
            login(request,myuser)
            messages.success(request, "Login Successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/auth/login')

    return render(request,"login.html")

# Logout Handler
def handlelogout(request):
    logout(request)  # ✅ Properly logging out the user
    messages.info(request, "Logged Out Successfully")
    return redirect('/auth/login')

