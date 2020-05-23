from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.forms import (
    RegistrationForm,
    EditProfileForm,
    RegisterForm,
    LoginForm,
    UserEditForm,
    DateRangeForm
)
from accounts.models import UserProfile, create_request, approve_request, get_all_requests, denied_request, get_my_requests
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password


def user_login(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        print(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        m = User.objects.get(username=username)
        if check_password(password, m.password):
            login(request, m)
            return redirect(reverse('accounts:view_profile'))
        else:
            print("Your username and password didn't match.")

    else:
        form = LoginForm()
        args = {'form': form}
        return render(request, 'accounts/login.html', args)


def user_register(request):
    # if this is a POST request we need to process the form data
    template = 'mymodule/register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Username already exists.'
                })
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {
                    'form': form,
                    'error_message': 'Email already exists.'
                })
            elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
                return render(request, template, {
                    'form': form,
                    'error_message': 'Passwords do not match.'
                })
            else:
                # Create the user:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.phone_number = form.cleaned_data['phone_number']
                user.save()
                # redirect to accounts page:
                return redirect(reverse('accounts:view_profile'))


    # No post data availabe, let's just show the page.
    else:
        form = RegisterForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/reg_form.html', args)




def user_edit(request):
    template = 'mymodule/register.html'

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserEditForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
                # Create the user:
                user = User.objects.get(username=request.user)
                profile = UserProfile.objects.get(user_id=user.id)
                password = form.cleaned_data['password']
                if check_password(password, user.password):
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    profile.phone = form.cleaned_data['phone_number']
                    user.save()
                    profile.save()

                return redirect(reverse('accounts:view_profile'))


    # No post data availabe, let's just show the page.
    else:
        user = User.objects.get(username=request.user)
        profile = UserProfile.objects.get(user_id=user.id)
        form = UserEditForm()
        form.fields["first_name"].initial = user.first_name
        form.fields["last_name"].initial = user.last_name
        form.fields["phone_number"].initial = profile.phone

        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def status_edit(request):
    if request.method == 'POST':
        if request.POST.get("Approve", ''):
            request_id = request.POST["requested_by"]
            approve_request(request_id=request_id, reviewer_id=request.user)
            return redirect(reverse('accounts:all_requests'))
        elif request.POST.get("Reject", ''):
            request_id = request.POST["requested_by"]
            denied_request(request_id=request_id, reviewer_id=request.user)
            return redirect(reverse('accounts:all_requests'))
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html', args)


def my_requests(request):
    if request.method == 'GET':
        requests = get_my_requests(request.user.id)
        args = {'requests': requests}
        return render(request, 'accounts/my_request.html', args)



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            create_request(user, form.cleaned_data['start_date'], form.cleaned_data['end_date'],form.cleaned_data['title'],form.cleaned_data['description'],form.cleaned_data['category'])
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = DateRangeForm()
        args['form'] = form
        return render(request, 'accounts/profile.html', args)


def all_requests(request):
    if request.method == 'POST':
        form = DateRangeForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            create_request(user, form.cleaned_data['start_date'], form.cleaned_data['end_date'],form.cleaned_data['title'],form.cleaned_data['description'],form.cleaned_data['category'])
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
       requests=get_all_requests()
       args = {'requests': requests}
       return render(request, 'accounts/all_request.html', args)