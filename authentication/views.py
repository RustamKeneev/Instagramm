from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User

class RegistrationView(View):
    def get(self,request):
        return render(request,'auth/register.html')

    def post(self,request):
        context = {
            'data':request.POST,
            'has_error': False
        }
        data = request.POST
        email = request.POST.get('email')
        username = request.POST.get('username')
        full_name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password)<6:
            messages.add_message(request, messages.ERROR,'Passwords should be at least 6 characters long')
            context['has_error']=True
        if password !=password2:
            messages.add_message(request, messages.ERROR,'Passwords dont match')
            context['has_error'] = True
        if not validate_email(email):
            messages.add_message(request, messages.ERROR,'Please provide a valid email')
            context['has_error'] = True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR,'Email is taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(request, messages.ERROR,'Username is taken')
                context['has_error'] = True
        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request,'auth/register.html', context, status=400)
        user = User.objects.create_user(username=username,email=email)
        user.first_name=full_name
        user.last_name=full_name
        user.set_password(password)
        user.is_active = False
        user.save()
        messages.add_message(request, messages.SUCCESS, 'account created successfully')

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request,'auth/login.html')