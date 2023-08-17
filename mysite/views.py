from django.shortcuts import render,redirect
from django.template.loader import get_template
# Create your views here.
from django.http import HttpResponse
from .models import Scene,Characteristic,Content
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    template = get_template('homepage.html')
    scenes = Scene.objects.all()
    every_page_num = 12

    lists = Paginator(scenes,every_page_num)
    pages = request.GET.get('page',1)
    current_page = lists.get_page(pages).number #當前頁
    page_range = list(range(max(current_page-2,1),current_page))+\
        list(range(current_page,min(current_page+2,lists.num_pages)+1))

    
    lower = every_page_num * (current_page-1) + 1
    upper = every_page_num * current_page
    features = Characteristic.objects.filter(scene_id__gte=lower,scene_id__lte=upper)

    try:
        cons = lists.page(pages)
    except EmptyPage:
        cons = lists.page(lists.num_pages)
    except PageNotAnInteger:
        cons = lists.page(1)
    html = template.render(locals())
    return HttpResponse(html)


def scene_content(request,slug):
    template = get_template('contentpage.html')
    scenes = Scene.objects.get(slug = slug)
    features = Characteristic.objects.all()
    
    html = template.render(locals())
    return HttpResponse(html)

def logins(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            msg = 'UserName 或 Password 不正確 !'
            return render(request,'login.html',locals())

    return render(request, 'login.html')

def regist(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username).exists():          
            msg = 'UserName 已存在'
            return render(request,'regist.html',locals())
        if username == '':
            msg = 'UserName 不能為空'
            return render(request,'regist.html',locals())
        elif password == '' or password2 == '':
            msg = 'Password 不能為空'
            return render(request,'regist.html',locals())
        elif password != password2:
            msg = '兩次輸入密碼不同'
            return render(request,'regist.html',locals())
        
        cuser = User.objects.create_user(username=username,password=password)
        cuser.save()
        return redirect('/login/')
    return render(request, 'regist.html')

def log_out(request):
    logout(request)
    return redirect('/')