from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Link, Account
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import simplejson
from . import signup as sp
import requests
import re
import json

TAGS = ["TV", "Movie", "Ebook", "Music", "Tutorial", "Game", "Software"]


def get_total_size(l, type=None):
    total_size = 0
    for i in l:
        size_b = re.sub(r"([0-9]+).([0-9]+)", "", i.size).strip()

        try:
            size = float(re.sub(r"([A-Z]|[a-z])+", "", i.size).strip())
        except:
            pass

        if type==None or type=="TB":
            if size_b == "TB":
                total_size = total_size + size

            if size_b == "GB":
                size = size/1024
                total_size = total_size + size

            if size_b == "MB":
                size = size/(1024*1024)
                total_size = total_size + size

        if type=="GB":
            if size_b == "GB":
                total_size = total_size+ size

            if size_b == "TB":
                size = size * 1024
                total_size = total_size + size

            if size_b == "MB":
                size = size / (1024)
                total_size = total_size + size

    return total_size

def isAlive(link):
	link_match = re.search(r'/#!(.*)!(.*)$', link) or re.search(r'/#F!(.*)!(.*)$', link)
	if link_match == None:
		return False
	else:
		mega_data = [{"a":"g", "g":1, "ssl":0, "p":link_match.group(1)}]
		mega_response = requests.post("https://g.api.mega.co.nz/cs", data=json.dumps(mega_data))
		if json.loads(mega_response.text)[0] == -9:
			return False
		else:
			return True

def checkable(link):
    link_match = re.search(r'/#!(.*)!(.*)$', link) or re.search(r'/#F!(.*)!(.*)$', link)
    try:
        return link_match.group(1)
    except:
        return None

def index(request, tagfilter):
    links_list = Link.objects.filter(tag=tagfilter).order_by('-date')
    paginator = Paginator(links_list, 20)

    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        links = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        links = paginator.page(paginator.num_pages)

    context = {
        'links': links,
        'tagfilter': tagfilter,
    }
    return render(request, 'megalinks/new/list.html', context)


@login_required(login_url='/login/')
def detail(request, id):
    if request.user.is_authenticated():
        try:
            link = Link.objects.get(id=id)
            link.checkable = checkable(link.link)
        except Link.DoesNotExist:
            messages.error(request, "Link does not exist.")
            return redirect('activity')
        return render(request, 'megalinks/new/detail.html', {'link': link})
    else:
        return HttpResponse("You have not logged in")


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next = request.GET.get('next', '')
                    if next != '':
                        return redirect(next)

                    return redirect('activity')
                else:
                    return HttpResponse("Sorry but your account is disabled")
            else:
                messages.error(request, 'Wrong username/password.')
                return redirect('login')

        else:
            return render(request, 'megalinks/new/sign_in.html', {})
    else:
        return redirect('activity')

def search(request):
    query = request.GET.get('query', '')
    links_list = Link.objects.filter(Q(title__icontains=query) | Q(tag__icontains=query)).order_by('-date')
    paginator = Paginator(links_list, 20)

    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)

    context = {
        'links': links,
        'tagfilter': "Search Results for: "+query,
        'search': query
    }
    return render(request, 'megalinks/new/list.html', context)





def activity(request):
    links_list = Link.objects.all().order_by('-date')
    paginator = Paginator(links_list, 20)

    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)

    context = {
        'links': links,
    }
    return render(request, 'megalinks/new/list.html', context)

def signup(request):
    if request.user.is_authenticated():
        messages.info(request, "You are already logged in.")
        return redirect('activity')
    else:
        if request.method == "GET":
            return render(request, 'megalinks/new/sign_up.html', {})

        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if username=='' or password=='':
                messages.error(request, "Please enter valid username and password.")
                return redirect('signup')

            group = Group.objects.get(name="Uploaders")
            u = User(username=username, password=password)
            u.set_password(password)
            u.save()
            u.groups.add(group)
            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(request,"Thank you for signing up!")
            return redirect('activity')


@login_required()
def logout_user(request):
    logout(request)
    return redirect('activity')


# def check(request):
#     id = request.GET.get('id', '')
#     if id == '':
#         return HttpResponse("Error");
#
#     l = Link.objects.get(id=int(id))
#     if isAlive(l.link):
#         return HttpResponse("True")
#     else:
#         return HttpResponse("False")

def check(request):
    return render(request, 'megalinks/new/check_link.html', {})

def contribute(request):
    return render(request, 'megalinks/new/contribute.html', {})

@login_required(login_url='/login/')
def add_link(request):
    if request.method == "GET":
        return render(request, 'megalinks/new/add_link.html', {})
    else:
        title = request.POST.get('title','')
        size = request.POST.get('size','')
        size_b = request.POST.get('size_b','')
        tag = request.POST.get('tag','')
        link = request.POST.get('link','')
        description = request.POST.get('description','')
        l = Link(
            title=title,
            size=size+size_b,
            tag=tag,
            link=link,
            description=description
        )
        l.save()

        messages.success(request, "Link has been posted.")
        if request.POST.get('submit', '') == 'Save and Add Another':
            return redirect('add_link')
        else:
            return redirect('activity')


@login_required(login_url='/login/')
def edit_link(request, id):
    try:
        l = Link.objects.get(id=id)
    except:
        messages.error(request, "Link post not found.")
        return redirect('activity')

    if request.method == "GET":
        l.size_b = re.sub(r"([0-9]+).([0-9]+)", "", l.size).strip()
        l.size = float(re.sub(r"([A-Z]|[a-z])+", "", l.size))
        return render(request, 'megalinks/new/edit_link.html', { 'link': l })

    else:
        if request.user == l.user or request.user.is_superuser:
            title = request.POST.get('title', '')
            size = request.POST.get('size', '') + request.POST.get('size_b', '')
            tag = request.POST.get('tag', '')
            link = request.POST.get('link', '')
            description = request.POST.get('description', '')
            l.title = title
            l.size = size
            l.tag = tag
            l.link = link
            l.description = description
            l.save()

            messages.success(request, "Link has been updated.")
            return redirect('activity')
        else:
            messages.error(request, "You do not have permission to edit this post.")
            return redirect('activity')

@login_required(login_url='/login/')
def submissions(request):
    if request.user.is_superuser:
        links_list = Link.objects.all().order_by('-date')
    else:
        links_list = Link.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(links_list, 20)

    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)

    context = {
        'links': links,
        'tagfilter': 'Submissions'
    }
    return render(request, 'megalinks/new/list.html', context)

def statistics(request):
    users = User.objects.all().count()
    posts = Link.objects.all()
    site = {
        'users': users,
        'posts': posts.count(),
        'accounts': Account.objects.all().count()
    }
    data = []
    for i in TAGS:
        tag_posts = Link.objects.filter(tag=i)
        tag_size = "%.2f" % get_total_size(tag_posts, type="GB")

        data.append({'name': i, 'posts': tag_posts.count(), 'size': tag_size })

    data.sort(key=lambda x: x['posts'], reverse=True)
    if request.user.is_authenticated:
        user_posts = Link.objects.filter(user=request.user)
        request.user.posts = user_posts.count()
        request.user.size = "%.4f" % get_total_size(user_posts)
        request.user.accounts = Account.objects.filter(user=request.user).count()

    return render(request, 'megalinks/new/statistics.html', {'site': site, 'data': data})

@login_required(login_url='/login/')
def delete_link(request, id):
    try:
        l = Link.objects.get(id=id)
    except:
        messages.error(request, "Link not found.")
        return redirect('activity')

    if request.user == l.user or request.user.is_superuser:
        l.delete()
        messages.success(request, "Link deleted.")
        return redirect('activity')

    else:
        messages.error(request, "You do not have permission to delete this link.")
        return redirect('activity')

@login_required(login_url='/login/')
def account_new(request):
    if request.method == "GET":
        return render(request, 'megalinks/new/account_new.html', {})
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username != '' and password != '':
            response = sp.signup(username, password)
            if response['success']:
                a = Account(
                    user=request.user,
                    email=response['email'],
                    password=response['password']
                )
                a.save()
                return HttpResponse(simplejson.dumps(response), content_type='application/json')

            else:
                error = {'success': False, 'message': 'There was some error.'}

                return HttpResponse(simplejson.dumps(error), content_type='application/json')
        else:
            error = {'success': False, 'message': 'Enter valid username and password.'}

            return HttpResponse(simplejson.dumps(error), content_type='application/json')


@login_required(login_url='/login/')
def accounts(request):
    if request.user.is_superuser:
        accounts = Account.objects.all().order_by('-date')
    else:
        accounts = Account.objects.filter(user=request.user).order_by('-date')
    paginator = Paginator(accounts, 20)

    page = request.GET.get('page')
    try:
        links = paginator.page(page)
    except PageNotAnInteger:
        links = paginator.page(1)
    except EmptyPage:
        links = paginator.page(paginator.num_pages)

    context = {
        'links': links,
        'tagfilter': 'Generated Accounts'
    }
    return render(request, 'megalinks/new/account_list.html', context)
