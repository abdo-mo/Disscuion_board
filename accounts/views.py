from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile


# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    return render(request, 'signup.html', {'form':form})

def validate_username(request):
    username = request.GET.get('username')
    is_taken = User.objects.filter(username__iexact=username).exists()
    data = {'is_taken':is_taken}
    if is_taken:
        data['error_message'] = 'the user is laready taken'
    return JsonResponse(data)

class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'my_acount.html'
    success_url = reverse_lazy('my_acount')

    def get_object(self):
        return self.request.user

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('my_acount')
    else:
        u_form = UserUpdateForm(instance = request.user)
        user = request.user
        Profile.objects.get_or_create(user = user)
        profile = user.profile
        p_form = ProfileUpdateForm(instance = profile)



    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'my_acount.html', context)
