from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RegisterForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


def profile(request: HttpRequest, user_id: int) -> HttpResponse:
    user = get_object_or_404(User, id=user_id)
    return render(request, 'account/profile.html', {'user': user})


def get_email(request: HttpRequest) -> HttpResponse:
    user = request.user
    return render(request, 'account/partials/profile/email.html', {'user': user})


def get_email_form(request: HttpRequest) -> HttpResponse:
    user = request.user
    return render(request, 'account/partials/profile/email_form.html', {'user': user})


@login_required
@require_POST
def change_email(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    new_email = request.POST.get('email', '')

    success, message = user.change_email(new_email)

    if success:
        template = 'account/partials/profile/email.html'
    else:
        template = 'account/partials/profile/email_form.html'

    return render(
        request,
        template,
        {
            'user': user,
            'error': message if not success else None,
            'success': message if success else None,
        },
    )


