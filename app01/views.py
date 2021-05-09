from django.shortcuts import render

# Create your views here.

def index(request):
    username = request.GET.get('username')
    type = request.GET.get('type')
    content = {'username':username,'type':type}
    return render(request,'index.html',context=content)

def login(request):
    return render(request,'login.html')
