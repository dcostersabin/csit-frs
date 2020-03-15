from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.add_user_form import EmployeeAddingForm
from recognition import data_collection
import os
from django.contrib import messages
from django.shortcuts import redirect
from users.models import Employees, Attendance
from datetime import datetime
from django.http import HttpResponse
from recognition import data_collection
from recognition import train
from recognition import recognize

# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = BASE_DIR + '/static/dataset/'


# indexpage
def index(request):
    return render(request, 'index/index.html')


@login_required
def home(request):
    if request.user.is_authenticated:
        employees = Employees.objects.order_by('-id')[:10]
        today_count = Attendance.objects.filter(entry_date=datetime.now().date()).count()
        today = Attendance.objects.filter(entry_date=datetime.now().date())[:10]
        return render(request, "home/home.html", {'employees': employees, 'today': today, 'todays_count': today_count,
                                                  'employees_count': employees.count()})
    else:
        return render(request, 'index/index.html')


def add_user(request):
    user = EmployeeAddingForm(request.POST)
    if user.is_valid():
        new = user.save()
        file_path = new.name + '__id__' + str(new.id)
        data_collection.create_dir(file_path)
        if os.path.isdir(path + '' + file_path):
            messages.success(request, f'New User Added Now You Can Add Data')
            return redirect('home')
        else:
            messages.info(request, f'Failed To Create User Enter Valid Data')
            return redirect('home')

    else:
        messages.warning(request, f'Failed To Create User Enter Valid Data')
        return redirect('home')


def capture(request):
    if data_collection.capture_image((request.POST['id']), 0):
        messages.success(request, "Data Has Been Collected Successfully")
        return redirect('home')
    else:
        messages.success(request, "Data Creation Failed")
        return redirect('home')


def train_data(request):
    status = train.train()
    if status:
        messages.success(request, "The Machine Was Trained Successfully")
        return redirect('home')
    else:
        messages.warning(request, "The Machine Failed To  Train")
        return redirect('home')


def rec(request):
    name = recognize.recognize()
    temp_id = name.split("__id__", 1)
    user = Employees.objects.filter(id=temp_id[1]).get()
    user_path = user.name + '__id__' + str(user.id)
    if Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id,
                                 exit_date=datetime.now().date()).exists():
        user_current_data = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).get()
        return render(request, 'mis/attend.html',
                      {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check',
                       'attendance': True, 'entry_date': user_current_data.entry_date,
                       'entry_time': user_current_data.entry_time, 'complete': True,
                       'exit_time': user_current_data.exit_time, 'post': user.post, 'department': user.department})
    elif Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).exists():
        user_current_data = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).get()
        return render(request, 'mis/attend.html',
                      {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check',
                       'attendance': True, 'entry_date': user_current_data.entry_date,
                       'entry_time': user_current_data.entry_time, 'complete': False, 'post': user.post,
                       'department': user.department})
    else:
        return render(request, 'mis/attend.html',
                      {'name': user.name, 'employee_id': user.employee_id, 'id': user.id, 'status': 'check',
                       'attendance': False, 'complete': False,
                       'post': user.post, 'department': user.department})


def show_users(request):
    employees = Employees.objects.all().order_by('-id')
    return render(request, 'mis/showusers.html', {'employees': employees})


def add_more_data(request):
    if data_collection.capture_image(request.POST['id'], 1):
        messages.success(request, "New Data Collected Successfully")
        return redirect('home')
    else:
        messages.warning(request, "Failed To Initialized Data")
        return redirect('home')


def admin_test(request):
    name = recognize.recognize()
    temp_id = name.split("__id__", 1)
    user = Employees.objects.filter(id=temp_id[1]).get()
    user_path = user.name + '__id__' + str(user.id)
    no_files = len([name for name in os.listdir(path + '' + user_path) if
                    os.path.isfile(os.path.join(path + '' + user_path, name))])
    return render(request, "mis/individualUser.html", {"data": user, "file": range(1, no_files)})


def view_profile(request):
    user = Employees.objects.filter(id=request.POST['user_id']).get()
    total_attendance = Attendance.objects.filter(user_id=user.id).order_by('-entry_date')
    user_path = user.name + '__id__' + str(user.id)
    no_files = len([name for name in os.listdir(path + '' + user_path) if
                    os.path.isfile(os.path.join(path + '' + user_path, name))])
    return render(request, "mis/individualUser.html",
                  {"data": user, "file": range(1, no_files), 'attendance': total_attendance})


def search(request):
    try:
        user = Employees.objects.filter(employee_id=request.POST['user_id']).get()
        user_path = user.name + '__id__' + str(user.id)
        no_files = len([name for name in os.listdir(path + '' + user_path) if
                        os.path.isfile(os.path.join(path + '' + user_path, name))])
        return render(request, 'mis/individualUser.html', {'data': user, 'file': range(1, no_files)})
    except ObjectDoesNotExist as e:
        messages.warning(request, "Please Enter A Valid Data")
        return redirect('home')


def attend(request):
    # return HttpResponse(datetime.now().date())

    if Employees.objects.filter(id=request.POST['id']).exists():
        user = Employees.objects.filter(id=request.POST['id']).get()
        check = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).exists()
        if not check:
            new = Attendance()
            new.user_id_id = user.id
            new.entry_date = datetime.now().date()
            new.entry_time = datetime.now().time()
            new.save()
            messages.success(request, "Recorded Entry For User " + user.name)
            return redirect('index')

        else:
            update = Attendance.objects.filter(entry_date=datetime.now().date(), user_id=user.id).get()
            update.exit_date = datetime.now().date()
            update.exit_time = datetime.now().time()
            update.save()
            messages.success(request, "Recorded Exit For User " + user.name)
            return redirect('index')

    else:
        messages.warning(request, "The Id Provided Doesnt Match")
        return HttpResponse(render(request, 'index/index.html'))
