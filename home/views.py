from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.models import task
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login/")
def todo(request):
    if request.method == "POST":
        title = request.POST['task']
        description = request.POST['description']
        task_obj = task.objects.create(
            user=request.user,
            title=title,
            description=description
        )
        task_obj.save()
        messages.info(request, "Task Created Successfully.")
        return redirect("/todo/")
    tasks = task.objects.filter(user=request.user).order_by('-status')
    context = {
        'tasks':tasks
    }
    return render(request, "todo.html", context=context)

@login_required(login_url="/login/")
def done(request,id):
    if not (task.objects.filter(id=id).first()):
        messages.info(request, "Task doesn't exists.")
        return redirect("/todo/")
    if (task.objects.filter(id=id).first()).user != request.user:
        messages.info(request, "The task doesn't belongs to you.")
        return redirect("/todo/")
    if (task.objects.filter(id=id).first()).status == "Pending":
        task_obj = task.objects.filter(id=id).first()
        task_obj.status = 'Done'
        task_obj.save()
        messages.info(request, "Task Marked as Done.")
        return redirect("/todo/")
    else:
        messages.info(request, "Task was already marked as Done.")
        return redirect("/todo/")


@login_required(login_url="/login/")
def delete(request,id):
    if not (task.objects.filter(id=id).first()):
        messages.info(request, "Task doesn't exists.")
        return redirect("/todo/")
    if (task.objects.filter(id=id).first()).user != request.user:
        messages.info(request, "The task doesn't belongs to you.")
        return redirect("/todo/")
    task_obj = task.objects.filter(id=id).first()
    task_obj.delete()
    messages.info(request, "Task Deleted.")
    return redirect("/todo/")


def home(request):
    # return render(request, "index.html")
    return redirect("/login/")


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/todo/")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username):
            messages.info(request, "Invalid Username")
            return render(request, "login.html")
        user = authenticate(username=username, password=password)
        if user == None:
            messages.info(request, "Invalid Password")
            return render(request, "login.html")
        else:
            login(request, user)
            return redirect('/todo/')
        print(username)
    return render(request, "login.html")


def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/login/")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("/todo/")
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username):
            messages.info(request, "Username already taken")
            return render(request, "register.html")
        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            user.set_password(password)
            user.save()
            return redirect('/')
    return render(request, "register.html")