from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User, auth

from fee.models import *
from reports.models import Backup
from .models import *
from django.contrib import messages
import datetime
import json

# Create your views here.


def login(request):
    user = request.user
    if user.is_authenticated:
        print("here")
        return redirect('school:dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            school = School.objects.get(user=user)
            return redirect('school:dashboard')
        else:
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def dashboard(request):
    user = request.user
    school = School.objects.get(user=user)
    try:
        last_fee_submit = FeeSubmit.objects.filter(session=Current.objects.all()[0].session).order_by('-id')[0]
    except:
        last_fee_submit = None
    print(last_fee_submit)
    last_backup = Backup.objects.last()
    return render(request, 'index.html', {'school': school, 'last_fee_submit': last_fee_submit, 'last_backup': last_backup})


def students(request):
    admin = request.user
    school = School.objects.get(user=admin)
    current = Current.objects.all()[0]
    students = Student.objects.filter(school=school, session=current.session).order_by('Class__class_no')
    return render(request, 'students.html', {'students': students})


def studentoutline(request, student_id):
    student = Student.objects.get(id=student_id)
    school = student.school
    total = 0
    clas = student.Class
    current = Current.objects.all()[0]
    c = FeeStruct.objects.filter(clas=clas, session=current.session)
    # print(c)
    for i in c:
        total = total + i.amount
    sub_fee = 0
    fees = FeeSubmit.objects.filter(student=student)
    for f in fees:
        sub_fee = sub_fee + f.amount
    rem_fee = total - sub_fee
    sub = sub_fee
    month_qs = Month.objects.filter(school=school)
    # print(month_qs)

    # fee submit by month
    fee_submit_by_month_obj = FeeSubmitByMonth.objects.get(student=student)
    # print(fee_submit_by_month_obj)
    fee_submitted_month_no = fee_submit_by_month_obj.month_no
    print(fee_submitted_month_no)
    # this is the list of months that have been submitted
    print(month_qs[:fee_submitted_month_no])
    print(month_qs[fee_submitted_month_no:])
    fee_submitted_month_qs = month_qs[:fee_submitted_month_no]
    fee_left_month_qs = month_qs[fee_submitted_month_no:]

    fee_struct_submitted_qs = FeeStructByMonth.objects.filter(
        clas=clas, month__in=fee_submitted_month_qs, session=current.session)
    print(fee_struct_submitted_qs)
    fee_struct_left_qs = FeeStructByMonth.objects.filter(
        clas=clas, month__in=fee_left_month_qs, session=current.session)
    print(fee_struct_left_qs)

    # cheque
    cheque_qs = ChequeDetails.objects.filter(fee_submit__in = fees)
    # print(cheque_qs)
    online_qs = OnlineNeftDetails.objects.filter(fee_submit__in = fees)
    # misc fees
    misc_qs = MiscFee.objects.filter(student=student)

    return render(request, 'studentoutline.html', {'student': student, 'total': total, 'sub_fee': sub_fee, 'rem_fee': rem_fee, 'fees': fees, 'fee_struct_submitted_qs': fee_struct_submitted_qs, 'fee_struct_left_qs': fee_struct_left_qs, 'cheque_qs': cheque_qs, 'online_qs': online_qs, 'misc_qs': misc_qs, "add_no": str(student.add_no)})


def studentAdd(request):
    current = Current.objects.all()[0]
    class_qs = Classes.objects.all().order_by('class_no')
    if request.method == "POST":
        print(request.POST)
        # print(request)
        dob = request.POST['dob']
        if dob == "":
            dob = datetime.date(2022, 1, 1)
        if (request.POST['add_no'] == "") or (request.POST['name'] == "") or (request.POST['class'] == "") or (request.POST['fathername'] == ""):
            raise Exception("Mandatory fields cannot be empty")
        student = Student(
            add_no=request.POST['add_no'],
            fname=request.POST['name'].upper(),
            fathername=request.POST['fathername'].upper(),
            Class=Classes.objects.get(id=request.POST['class']),
            roll_no=request.POST['roll'],
            dob=dob,
            gender=request.POST['gender'],
            religion=request.POST['religion'],
            category=request.POST['category'],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST['address'],
            session=current.session,
        )
        student.save()
        fee_submit_by_month = FeeSubmitByMonth(student=student, session=current.session)
        fee_submit_by_month.save()
    return render(request, 'addstudent.html', {'class_qs': class_qs})


def studentEdit(request, student_id):
    student_obj = Student.objects.get(id=student_id)
    class_qs = Classes.objects.all()
    if request.method == "POST":
        print(request.POST)
        # student_obj.update('fathername', request.POST['fathername'])
        dob = request.POST['dob']
        if dob == "":
            dob = datetime.date(2022, 1, 1)
        # if (request.POST['add_no'] == "") or (request.POST['name'] == "") or (request.POST['class'] == "") or (request.POST['fathername'] == ""):
        #     raise Exception("Mandatory fields cannot be empty")
        Student.objects.filter(id=student_id).update(
            add_no=request.POST['add_no'],
            fname=request.POST['name'].upper(),
            fathername=request.POST['fathername'].upper(),
            roll_no=request.POST['roll'],
            dob=dob,
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST['address'],
        )
    return render(request, 'editstudent.html', {'student': student_obj, 'student_dob': student_obj.dob.strftime("%Y-%m-%d"), 'class_qs': class_qs})


def sessions(request):
    admin = request.user
    school = School.objects.get(user=admin)
    current = Current.objects.all()[0]
    sessions = Session.objects.filter(school=school)
    return render(request, 'sessions.html', {'sessions': sessions, 'current': current})


def updateCurrentSession(request):
    if "session_id" in request.GET:
        session_obj = Session.objects.get(id=request.GET['session_id'])
        current = Current.objects.all()[0]
        current.session = session_obj
        current.save()
        messages.success(request, 'Session updated successfully!')
        return HttpResponse(json.dumps({"success": "session changed successfully"}), content_type="application/json")
    return HttpResponse(json.dumps({"error": "session not changed"}), content_type="application/json")


def addSession(request):
    if "session_name" in request.GET:
        session_name = request.GET['session_name']
        current = Current.objects.all()[0]
        print(current.session)
        # create session
        session_obj = Session(session=session_name,
                              school=current.session.school)
        session_obj.save()

        # copy fee struct by month
        fee_struct_by_month_qs = FeeStructByMonth.objects.filter(session=current.session)
        # print(fee_struct_by_month_qs)
        for fee_struct_by_month_q in fee_struct_by_month_qs:
            fee_struct_by_month_q_values = fee_struct_by_month_q.__dict__
            fee_struct_by_month_q_values.pop('_state')
            fee_struct_by_month_q_values.pop('id')
            fee_struct_by_month_q_values.pop('amount')
            fee_struct_by_month_new_q = FeeStructByMonth(**fee_struct_by_month_q_values)
            fee_struct_by_month_new_q.session = session_obj
            fee_struct_by_month_new_q.save()

        # copy fee structs
        fee_struct_qs = FeeStruct.objects.filter(session=current.session)
        print("fee_struct", fee_struct_qs)
        for fee_struct_q in fee_struct_qs:
            fee_struct_q_values = fee_struct_q.__dict__
            print("here_fee", fee_struct_q_values)
            fee_struct_q_values.pop('_state')
            fee_struct_q_values.pop('id')
            fee_struct_new_q = FeeStruct(**fee_struct_q_values)
            fee_struct_new_q.session = session_obj
            fee_struct_new_q.save()

        # copy students objects from previous session to new session
        student_qs = Student.objects.filter(session=current.session)
        for student_q in student_qs:
            # print(student_q)
            class_obj = student_q.Class
            # class_name = class_obj.clas
            class_no = class_obj.class_no
            try:
                # class_int = int(class_name)
                # class_int = class_int + 1
                # class_str = str(class_int)
                class_no = class_no + 1
                new_class_obj = Classes.objects.get(class_no=class_no)
                student_q_values = student_q.__dict__
                # print(student_q_values)
                student_q_values.pop('_state')
                student_q_values.pop('id')
                # print(student_q_values)
                student_new_q = Student(**student_q_values)
                student_new_q.Class = new_class_obj
                student_new_q.session = session_obj
                # print("here")
                student_new_q.save()

                # FeeSubmitByMonth
                fee_submit_by_month_obj = FeeSubmitByMonth(student=student_new_q, session=session_obj)
                fee_submit_by_month_obj.save()
            except:
                print("class not found pass out student")
                continue
        messages.success(request, "Session added successfully!")
        return HttpResponse(json.dumps({"success": "session added successfully"}), content_type="application/json")
    return HttpResponse(json.dumps({"error": "session cannot added"}), content_type="application/json")


def studentDelete(request):
    if "id" in request.GET:
        student_obj = Student.objects.get(id=request.GET['id'])
        student_obj.delete()
        return HttpResponse(json.dumps({"success": "student deleted successfully"}), content_type="application/json")
    return HttpResponse(json.dumps({"error": "student cannot deleted"}), content_type="application/json")