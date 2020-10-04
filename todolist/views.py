from django.shortcuts import render
import json
import random
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Task, Team, Team_User
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
            return JsonResponse({"ok" : True, "username" : username})
        else:
            return JsonResponse({"ok": False, "message": "Invalid Username or Password"}) 

    else:
        return JsonResponse({"ok" : False, "message": "method must be post"})           

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
            return JsonResponse({"ok" : False, "message": "Passwords must match"})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return JsonResponse({ "ok" :False, "message": "Username already taken."})

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

@csrf_exempt
def edit_task(request, id):
    if request.method == 'PUT':
        task = Task.objects.get(pk = id)    
        data = json.loads(request.body)
        body = data["body"]
        task.body = body
        task.save()
        return JsonResponse({"ok": True, "message" : "Task Updated"})

    else:
        return JsonResponse({"ok": False, "message" : "Method must be put"})    

def get_teams(request):
    teams = request.user.teams.all()
    return JsonResponse({"actual_user" : request.user.username, "teams" : [t.team.serialize() for t in teams]}, safe=False)


@csrf_exempt
def create_team(request):

    if request.method == 'POST':
        code = random.randint(1,1000)
        data = json.loads(request.body)
        name = data['name']
        while len(Team.objects.filter(code = code)) > 0:
            code = random.randint(1,1000)

        team = Team(name = name, owner = request.user, code = code)
        team.save()
        Team_User(user = request.user, team = team).save()

        return JsonResponse(team.serialize())
    else:
        return JsonResponse({"ok": False, "message": "Method must be Post"})
            
def leave_team(request, id):

    team = Team.objects.get(pk = id)
    Team_User.objects.get(user = request.user, team = team ).delete()
    return JsonResponse({"ok" : True, "message": "Leaving team"})            

@csrf_exempt
def join_team(request):
    if request.method ==  "POST":
        code = json.loads(request.body)["code"]
        team = Team.objects.filter(code = code)
        if len(team) > 0:
            if len(Team_User.objects.filter(user = request.user, team = team[0])) > 0 :
                return JsonResponse({ "ok": False, "message" : "You already are in this team"})
            else:     
                Team_User(user = request.user, team= team[0]).save()
                return JsonResponse({"ok" : True, "team" : team[0].serialize()})
        else:
            return JsonResponse({"ok" : False, "message" : "Invalid code" })
    else:
        return JsonResponse({"ok" : False, "message" : "method must be post" })

@csrf_exempt
def add_team_task(request):

    if request.method ==  "POST":
        data = json.loads(request.body)
        body = data['body']
        user = User.objects.get(pk = data['user_id'])
        team = Team.objects.get(pk = data['team_id'])
        task = Task(user = user, body = body, team = team)
        task.save()
        return JsonResponse({"ok" : True, "task" : task.serialize()})

    else:
        return JsonResponse( {"ok" : False, "message": "Method must be post"})    