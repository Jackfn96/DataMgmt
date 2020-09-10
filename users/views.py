from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, Type
from django.contrib.auth.decorators import login_required
from MainViews.models import User

user_details = []


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form2 = Type(request.POST)

        if form.is_valid() and form2.is_valid():

            user_email = form.cleaned_data.get('email')

            # Django Functions
            user = form.save()
            user_type = form2.cleaned_data.get('user_type')
            user.profile.user_type = user_type
            user.profile.save()

            messages.success(request, f'Account successfully created, you are now able to log in')

            return redirect('login')
    else:
        form = UserRegisterForm()
        form2 = Type()
    return render(request, 'users/register.html', {'form': form, 'form2': form2})


def get_details(request):
    user_details.clear()
    current_user = request.user
    user_details.append(current_user.username)
    user_details.append(current_user.email)
    return user_details


@login_required
def profile(request):
    if request.method == 'POST':
        get_details(request)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_email = user_form.cleaned_data.get('email')
            username = user_form.cleaned_data.get('username')

            if user_email != user_details[1] and User.objects.filter(email=user_email).exists():

                messages.error(request, f'Email address already exists.')
                return redirect('profile')

            elif username != user_details[0] and User.objects.filter(username=username).exists():

                messages.error(request, f'Username already exists.')
                return redirect('profile')

            elif username == user_details[0] and \
                    user_email == user_details[1]:

                user_form.save()
                profile_form.save()
                messages.success(request, f'Account successfully updated.')
                return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)
