from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AnonymousMessageForm
from .models import AnonymousMessage
import requests




def get_location_from_ip(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "country": res.get("country"),
            "city": res.get("city"),
            "lat": res.get("lat"),
            "lon": res.get("lon")
        }
    except:
        return {}
    
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def landing(request):
    form = AnonymousMessageForm()

    if request.method == "POST":
        form = AnonymousMessageForm(request.POST)

        if form.is_valid():

            # commit=False -> DBga yozmay turadi
            msg = form.save(commit=False)

            ip = get_client_ip(request)
            loc = get_location_from_ip(ip)

            # modelga joylaymiz
            msg.ip_address = ip
            msg.country = loc.get("country")
            msg.city = loc.get("city")
            msg.lat = loc.get("lat")
            msg.lon = loc.get("lon")

            msg.save()  # endi DBga yoziladi

            return redirect('thank_you')

    return render(request, 'landing.html', {'form': form})


def thank_you(request):
    return render(request, 'success.html')

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

