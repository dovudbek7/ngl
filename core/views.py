from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AnonymousMessageForm
from .models import AnonymousMessage

def landing(request):
    form = AnonymousMessageForm()
    if request.method == "POST":
        form = AnonymousMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    return render(request, 'landing.html', {'form': form})

def thank_you(request):
    return render(request, 'success.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('message_list')
        else:
            messages.error(request, 'Login failed. Try again.')
    return render(request, 'login.html')


@login_required
def message_list(request):
    messages = AnonymousMessage.objects.all().order_by('-created_at')
    return render(request, 'message_list.html', {'messages': messages})

@login_required
def message_detail(request, pk):
    msg = get_object_or_404(AnonymousMessage, pk=pk)
    return render(request, 'message_detail.html', {'message': msg})

