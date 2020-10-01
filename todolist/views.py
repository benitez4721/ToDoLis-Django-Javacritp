from django.shortcuts import render
import json
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Task
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('main'))
    else:    
        return render(request,'todolist/auth.html')

@csrf_exempt
def login_view(request):

    if request.method == "POST":

        data = json.loads(request.body)
        username = data["username"]
        password = data["password"]    
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return JsonResponse({"username" : username})
        else:
            return JsonResponse({"error": "invalid username or password"}) 

    else:
        return JsonResponse({"error": "method must be post"})           

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@csrf_exempt
def register_view(request):

    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        email = data["email"]
        password = data["password"]
        confirmation = data["confirmation"]

        print(f"{username}: {confirmation}")
        if password != confirmation:
            return JsonResponse({"error": "Passwords must match"})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({
                "error": "Username already taken."
            })

        return JsonResponse({"ok": True}) 
    else:
        return JsonResponse({"error": "Method must be post"})           


def main(request):

    tasks = request.user.tasks.all()
    return render(request, 'todolist/main.html', {
        'tasks' : tasks
    })

@csrf_exempt
def add_task(request):

    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        body = data["body"]

        task = Task(user = user,body = body)
        task.save()

        return JsonResponse({'ok': True, 'id': task.id, 'message': 'Task added successsfully'})

    else:
        return JsonResponse({'ok': False, 'message': 'Method must be post'})

@csrf_exempt
def check(request, id):

    if request.method == "PUT":

        task = Task.objects.get(pk = id)
        task.done = not task.done
        task.save()

        return JsonResponse({ "ok" : True, "message": "task updated"})

def delete(request,id):
    
    Task.objects.get(pk = id).delete()

    return JsonResponse({"ok" : True, "message" : "Task deleted"})