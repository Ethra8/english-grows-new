from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home/index.html')

def privacy_policy(request):
    return render(request, "home/privacy_policy.html")